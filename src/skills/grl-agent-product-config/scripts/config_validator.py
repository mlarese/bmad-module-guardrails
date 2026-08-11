#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Validazione deterministica di un catalogo di prodotto e di una configurazione.

Lo script decide validità e completezza; non interpreta il documento del cliente,
non inferisce regole assenti e non calcola prezzi. Una combinazione che il catalogo
non dichiara resta non dichiarata: qui non diventa mai compatibile per omissione.

Formati: YAML se `pyyaml` è disponibile (sempre, con `uv run`), altrimenti solo JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:  # pyyaml è dichiarato in PEP 723; l'assenza conta solo con python3 nudo
    import yaml
except ImportError:  # pragma: no cover - dipende dall'ambiente di esecuzione
    yaml = None

OPTION_TYPES = {"enum", "number", "boolean", "text"}
RULE_KINDS = {"requires", "excludes", "required_if"}
IMPACTS = {"blocking", "pricing", "cosmetic"}
ORIGINS = {"written", "imposed", "assumed"}


class DocumentError(Exception):
    """Il file non è leggibile come catalogo o configurazione."""


# --- caricamento --------------------------------------------------------------


def load_document(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DocumentError(f"file non trovato: {path}")
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise DocumentError(
                f"{path}: serve pyyaml per leggere YAML. "
                "Esegui con `uv run`, oppure converti il file in JSON."
            )
        data = yaml.safe_load(text)
    elif suffix == ".json":
        data = json.loads(text)
    else:
        raise DocumentError(f"{path}: estensione non gestita ({suffix or 'nessuna'})")
    if not isinstance(data, dict):
        raise DocumentError(f"{path}: il contenuto non è una mappa")
    return data


def finding(code: str, message: str, where: str = "") -> dict[str, str]:
    entry = {"code": code, "message": message}
    if where:
        entry["where"] = where
    return entry


# --- catalogo -----------------------------------------------------------------


def index_options(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    options = catalog.get("options") or []
    return {opt.get("code"): opt for opt in options if isinstance(opt, dict) and opt.get("code")}


def allowed_values(option: dict[str, Any]) -> set[Any]:
    values = option.get("values") or []
    return {v.get("code") for v in values if isinstance(v, dict) and "code" in v}


def validate_catalog(catalog: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    line = catalog.get("line") or {}
    if not line.get("code"):
        errors.append(finding("line-code-missing", "manca line.code"))
    if not line.get("reviewed_by"):
        errors.append(
            finding(
                "catalog-not-reviewed",
                "manca line.reviewed_by: un catalogo non revisionato da una persona non si usa",
            )
        )
    if not line.get("reviewed_on"):
        warnings.append(finding("review-date-missing", "manca line.reviewed_on"))
    if not line.get("source"):
        warnings.append(finding("source-missing", "manca line.source: da dove vengono queste regole"))

    raw_options = catalog.get("options") or []
    if not raw_options:
        errors.append(finding("no-options", "il catalogo non dichiara nessuna opzione"))

    seen_codes: set[str] = set()
    for index, option in enumerate(raw_options):
        where = f"options[{index}]"
        if not isinstance(option, dict):
            errors.append(finding("option-malformed", "l'opzione non è una mappa", where))
            continue
        code = option.get("code")
        if not code:
            errors.append(finding("option-code-missing", "opzione senza code", where))
            continue
        where = f"options.{code}"
        if code in seen_codes:
            errors.append(finding("option-duplicated", f"codice opzione duplicato: {code}", where))
        seen_codes.add(code)

        opt_type = option.get("type")
        if opt_type not in OPTION_TYPES:
            errors.append(
                finding("option-type-invalid", f"type non ammesso: {opt_type!r}", where)
            )
        if opt_type == "enum":
            values = option.get("values") or []
            if not values:
                errors.append(finding("enum-without-values", "enum senza values", where))
            value_codes: set[Any] = set()
            for value in values:
                if not isinstance(value, dict) or "code" not in value:
                    errors.append(finding("value-malformed", "valore senza code", where))
                    continue
                if value["code"] in value_codes:
                    errors.append(
                        finding("value-duplicated", f"valore duplicato: {value['code']}", where)
                    )
                value_codes.add(value["code"])
        if opt_type == "number":
            low, high = option.get("min"), option.get("max")
            if low is not None and high is not None and low > high:
                errors.append(finding("range-inverted", f"min {low} maggiore di max {high}", where))
            if option.get("unit") is None:
                warnings.append(finding("unit-missing", "opzione numerica senza unit", where))

        impact = option.get("impact")
        if impact is not None and impact not in IMPACTS:
            errors.append(finding("impact-invalid", f"impact non ammesso: {impact!r}", where))
        if impact is None and not option.get("required"):
            warnings.append(
                finding("impact-unset", "opzione facoltativa senza impact: le domande non si ordinano", where)
            )

    options = index_options(catalog)
    rules = catalog.get("rules") or []
    pairs: dict[tuple[str, str], set[str]] = {}
    requires_edges: list[tuple[tuple[Any, Any], tuple[Any, Any]]] = []
    excludes_rules: list[tuple[dict[str, Any], dict[str, Any], str]] = []

    for index, rule in enumerate(rules):
        where = f"rules[{index}]"
        if not isinstance(rule, dict):
            errors.append(finding("rule-malformed", "la regola non è una mappa", where))
            continue
        kind = rule.get("kind")
        if kind not in RULE_KINDS:
            errors.append(finding("rule-kind-invalid", f"kind non ammesso: {kind!r}", where))
            continue
        if not rule.get("because"):
            errors.append(
                finding(
                    "rule-without-reason",
                    "regola senza because: non si può spiegare al cliente né verificare quando il prodotto cambia",
                    where,
                )
            )

        when = rule.get("when") or {}
        then = rule.get("then") or {}
        errors.extend(check_rule_side(when, options, where, "when", value_required=True))
        errors.extend(
            check_rule_side(then, options, where, "then", value_required=kind != "required_if")
        )

        if kind in {"requires", "excludes"} and when.get("option") and then.get("option"):
            key = (
                f"{when.get('option')}={when.get('value')}",
                f"{then.get('option')}={then.get('value')}",
            )
            pairs.setdefault(key, set()).add(kind)
        if kind == "requires" and when.get("option") and then.get("option"):
            requires_edges.append(
                ((when["option"], when.get("value")), (then["option"], then.get("value")))
            )
        if kind == "excludes":
            excludes_rules.append((when, then, where))

    errors.extend(required_made_impossible(excludes_rules, options))

    for (left, right), kinds in pairs.items():
        if {"requires", "excludes"} <= kinds:
            errors.append(
                finding(
                    "rule-contradiction",
                    f"la stessa coppia è insieme requires ed excludes: {left} → {right}",
                )
            )

    for cycle in find_cycles(requires_edges):
        warnings.append(
            finding("rule-cycle", "catena di requires che si chiude su sé stessa: " + " → ".join(cycle))
        )

    status = "invalid" if errors else "valid"
    return {
        "kind": "catalog",
        "status": status,
        "line": line.get("code"),
        "options": len(options),
        "rules": len(rules),
        "errors": errors,
        "warnings": warnings,
    }


def required_made_impossible(
    excludes_rules: list[tuple[dict[str, Any], dict[str, Any], str]],
    options: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    """Un'opzione obbligatoria che un `excludes` rende inselezionabile.

    Il caso: l'opzione è `required: true`, ha un solo valore ammesso, e una regola
    `excludes` vieta proprio quel valore. Nessuna configurazione può essere valida,
    e il catalogo lo dichiara soltanto quando qualcuno prova a configurare.
    """
    errori: list[dict[str, str]] = []
    for when, then, where in excludes_rules:
        for lato, altro in ((then, when), (when, then)):
            codice = lato.get("option")
            option = options.get(codice) if codice else None
            if not option or not option.get("required"):
                continue
            ammessi = allowed_values(option)
            vietato = lato.get("value")
            if not ammessi or vietato is None:
                continue
            if ammessi == {vietato}:
                errori.append(
                    finding(
                        "required-impossible",
                        f"l'opzione obbligatoria {codice!r} ha come solo valore {vietato!r}, "
                        f"che un excludes vieta insieme a {altro.get('option')!r}: "
                        "nessuna configurazione può essere valida",
                        where,
                    )
                )
    return errori


def check_rule_side(
    side: dict[str, Any],
    options: dict[str, dict[str, Any]],
    where: str,
    label: str,
    value_required: bool,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    code = side.get("option")
    if not code:
        errors.append(finding("rule-side-incomplete", f"{label} senza option", where))
        return errors
    option = options.get(code)
    if option is None:
        errors.append(finding("rule-unknown-option", f"{label} cita un'opzione inesistente: {code}", where))
        return errors
    if "value" not in side:
        if value_required:
            errors.append(finding("rule-side-incomplete", f"{label} senza value", where))
        return errors
    errors.extend(
        finding(code_, message, where)
        for code_, message in value_problems(option, side["value"], code)
    )
    return errors


def value_problems(option: dict[str, Any], value: Any, code: str) -> list[tuple[str, str]]:
    opt_type = option.get("type")
    if opt_type == "enum":
        if value not in allowed_values(option):
            return [("value-not-allowed", f"{code}: valore non ammesso dal catalogo: {value!r}")]
    elif opt_type == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return [("value-not-numeric", f"{code}: atteso un numero, trovato {value!r}")]
        low, high = option.get("min"), option.get("max")
        if low is not None and value < low:
            return [("value-below-min", f"{code}: {value} sotto il minimo {low}")]
        if high is not None and value > high:
            return [("value-above-max", f"{code}: {value} sopra il massimo {high}")]
    elif opt_type == "boolean":
        if not isinstance(value, bool):
            return [("value-not-boolean", f"{code}: atteso true o false, trovato {value!r}")]
    elif opt_type == "text":
        if not isinstance(value, str):
            return [("value-not-text", f"{code}: atteso testo, trovato {value!r}")]
    return []


def find_cycles(edges: list[tuple[tuple[Any, Any], tuple[Any, Any]]]) -> list[list[str]]:
    graph: dict[tuple[Any, Any], list[tuple[Any, Any]]] = {}
    for source, target in edges:
        graph.setdefault(source, []).append(target)

    cycles: list[list[str]] = []
    seen_cycles: set[frozenset[tuple[Any, Any]]] = set()

    def walk(node: tuple[Any, Any], path: list[tuple[Any, Any]]) -> None:
        if node in path:
            cycle = path[path.index(node) :] + [node]
            marker = frozenset(cycle)
            if marker not in seen_cycles:
                seen_cycles.add(marker)
                cycles.append([f"{opt}={val}" for opt, val in cycle])
            return
        for target in graph.get(node, []):
            walk(target, path + [node])

    for start in list(graph):
        walk(start, [])
    return cycles


# --- configurazione -----------------------------------------------------------


def condition_holds(side: dict[str, Any], selections: dict[str, Any]) -> bool:
    code = side.get("option")
    if code not in selections:
        return False
    if "value" not in side:
        return True
    return selections[code] == side["value"]


def validate_config(config: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    missing: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []

    line = catalog.get("line") or {}
    if not line.get("reviewed_by"):
        errors.append(
            finding(
                "catalog-not-reviewed",
                "il catalogo non è passato per revisione umana: nessuna configurazione è validabile su di esso",
            )
        )
    declared_line = config.get("line")
    if declared_line and line.get("code") and declared_line != line.get("code"):
        errors.append(
            finding(
                "line-mismatch",
                f"la configurazione dichiara la linea {declared_line}, il catalogo è {line.get('code')}",
            )
        )

    options = index_options(catalog)
    selections = config.get("selections") or {}
    evidence = config.get("evidence") or {}

    for code, value in selections.items():
        option = options.get(code)
        if option is None:
            errors.append(finding("unknown-option", f"opzione non presente nel catalogo: {code}"))
            continue
        errors.extend(
            finding(problem_code, message, f"selections.{code}")
            for problem_code, message in value_problems(option, value, code)
        )
        entry = evidence.get(code)
        if not isinstance(entry, dict) or not entry.get("origin"):
            errors.append(
                finding(
                    "evidence-missing",
                    f"{code}: scelta senza origine dichiarata (written, imposed o assumed)",
                    f"evidence.{code}",
                )
            )
        elif entry["origin"] not in ORIGINS:
            errors.append(
                finding("evidence-origin-invalid", f"{code}: origin non ammesso: {entry['origin']!r}")
            )
        elif entry["origin"] == "written" and not entry.get("quote"):
            warnings.append(finding("quote-missing", f"{code}: origine written senza citazione"))
        elif entry["origin"] == "imposed" and not entry.get("rule"):
            warnings.append(finding("rule-reference-missing", f"{code}: origine imposed senza la regola"))

    for code in evidence:
        if code not in selections:
            warnings.append(finding("evidence-orphan", f"evidence per un'opzione non selezionata: {code}"))

    for code, option in options.items():
        if option.get("required") and code not in selections:
            missing.append(
                {
                    "option": code,
                    "impact": option.get("impact", "blocking"),
                    "reason": "opzione obbligatoria del catalogo",
                }
            )

    for rule in catalog.get("rules") or []:
        if not isinstance(rule, dict):
            continue
        kind, when, then = rule.get("kind"), rule.get("when") or {}, rule.get("then") or {}
        because = rule.get("because", "")
        if not condition_holds(when, selections):
            continue
        target = then.get("option")
        if kind == "required_if":
            if target not in selections:
                missing.append(
                    {
                        "option": target,
                        "impact": (options.get(target) or {}).get("impact", "blocking"),
                        "reason": f"richiesta da {when.get('option')}={when.get('value')} — {because}",
                    }
                )
        elif kind == "requires":
            if target not in selections:
                missing.append(
                    {
                        "option": target,
                        "impact": (options.get(target) or {}).get("impact", "blocking"),
                        "reason": f"imposta da {when.get('option')}={when.get('value')} — {because}",
                        "expected": then.get("value"),
                    }
                )
            elif selections[target] != then.get("value"):
                errors.append(
                    finding(
                        "requires-violated",
                        f"{when.get('option')}={when.get('value')} impone {target}={then.get('value')!r}, "
                        f"trovato {selections[target]!r} — {because}",
                    )
                )
        elif kind == "excludes" and condition_holds(then, selections):
            errors.append(
                finding(
                    "excludes-violated",
                    f"{when.get('option')}={when.get('value')} esclude "
                    f"{target}={then.get('value')!r} — {because}",
                )
            )

    # Un'opzione che esiste solo sotto condizione non è una scelta aperta: finché la
    # condizione non scatta non riguarda nessuno, e quando scatta è già in `missing`.
    conditional = {
        (rule.get("then") or {}).get("option")
        for rule in catalog.get("rules") or []
        if isinstance(rule, dict) and rule.get("kind") == "required_if"
    }
    blocked = {item["option"] for item in missing}
    open_choices = [
        {"option": code, "impact": option.get("impact", "cosmetic")}
        for code, option in options.items()
        if not option.get("required")
        and code not in selections
        and code not in blocked
        and code not in conditional
    ]

    if errors:
        status = "invalid"
    elif missing:
        status = "incomplete"
    else:
        status = "valid"

    order = {"blocking": 0, "pricing": 1, "cosmetic": 2}
    missing.sort(key=lambda item: order.get(item.get("impact"), 3))
    open_choices.sort(key=lambda item: order.get(item.get("impact"), 3))

    return {
        "kind": "config",
        "status": status,
        "line": line.get("code"),
        "selections": len(selections),
        "errors": errors,
        "missing": missing,
        "open_choices": open_choices,
        "warnings": warnings,
    }


# --- CLI ----------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="config_validator.py",
        description=(
            "Verifica un catalogo di prodotto o una configurazione. "
            "Esiti: valid (ordinabile), incomplete (manca qualcosa che blocca), invalid (almeno un conflitto). "
            "`missing` è ciò che blocca — opzioni obbligatorie e opzioni imposte da una regola — e porta a incomplete. "
            "`open_choices` sono le opzioni facoltative non ancora decise: restano visibili ma non cambiano l'esito. "
            "Exit code 0 se valid, 1 se incomplete o invalid, 2 se il file non è leggibile."
        ),
    )
    parser.add_argument("-o", "--output", type=Path, help="scrive il JSON su file invece che su stdout")
    parser.add_argument("--verbose", action="store_true", help="diagnostica su stderr")
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog_cmd = subparsers.add_parser("catalog", help="coerenza interna di un catalogo")
    catalog_cmd.add_argument("path", type=Path, help="percorso del catalogo (.yaml o .json)")

    config_cmd = subparsers.add_parser("config", help="validità di una configurazione sul suo catalogo")
    config_cmd.add_argument("path", type=Path, help="percorso della configurazione (.yaml o .json)")
    config_cmd.add_argument(
        "--catalog",
        type=Path,
        help="catalogo da usare; se assente si legge il campo `catalog` della configurazione",
    )
    return parser


def resolve_catalog_path(config: dict[str, Any], config_path: Path, override: Path | None) -> Path:
    if override is not None:
        return override
    declared = config.get("catalog")
    if not declared:
        raise DocumentError(
            f"{config_path}: la configurazione non dichiara il campo `catalog` e --catalog non è stato passato"
        )
    candidate = Path(str(declared))
    return candidate if candidate.is_absolute() else (config_path.parent / candidate)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "catalog":
            report = validate_catalog(load_document(args.path))
        else:
            config = load_document(args.path)
            catalog_path = resolve_catalog_path(config, args.path, args.catalog)
            if args.verbose:
                print(f"catalogo: {catalog_path}", file=sys.stderr)
            report = validate_config(config, load_document(catalog_path))
    except DocumentError as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False), file=sys.stdout)
        print(str(error), file=sys.stderr)
        return 2

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if report["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
