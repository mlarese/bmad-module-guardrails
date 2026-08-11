#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Registro locale delle issue GitHub: letture, merge, stati, sessioni.

Tutto quello che in questa skill ha una sola risposta giusta sta qui, e non nel
prompt: la fusione incrementale del registro, la scala di precedenza degli stati,
il diff di fine sessione, i conteggi e l'età del dato. A parità di registro e di
risposta di `gh`, il risultato è sempre lo stesso.

Il modello resta responsabile di quello che è giudizio: leggere un commento in
prosa e capire se qualcuno ha chiesto di aspettare, decidere se una issue è
chiara, scrivere il motivo di una decisione. Lo script marca quei casi come
`da_decidere` invece di indovinarli.

Sottocomandi:

    registry.py sync     --path P --repo owner/name [--limit N] [--input file]
    registry.py derive   --path P [--hold-labels a,b] [--rejected-labels c,d]
    registry.py set      --path P --issue N [--status S] [--verdict V] ...
    registry.py stats    --path P [--max-age-days 30]
    registry.py session  --path P --start --scope 1,2,3 --file S
    registry.py session  --path P --close --file S

Ogni scrittura è atomica: file temporaneo più rinomina. Un `registry.json`
illeggibile non viene sovrascritto, viene messo da parte — dentro ci sono gli
stati dichiarati a mano, che nessuna rilettura di GitHub può ricostruire.

Uscita sempre su stdout in JSON: il prompt legge un riassunto compatto, non
cinquecento record grezzi.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = "grl-issues/registry@3"

STATI = [
    "DA_VALUTARE",
    "DA_CHIARIRE",
    "DA_FARE",
    "IN_SVILUPPO",
    "IN_VERIFICA",
    "IN_ATTESA",
    "NON_APPROVATA",
    "CHIUSA",
]

# Uno stato dichiarato a mano cede solo a un fatto letto da GitHub.
STATI_FORTI = {"IN_SVILUPPO", "IN_VERIFICA", "NON_APPROVATA", "CHIUSA"}

CAMPI_GH = "number,title,state,labels,milestone,assignees,updatedAt,url,body"
CAMPI_GH_ALL = CAMPI_GH + ",closedAt"

# Campi che vivono solo nel registro: nessuna rilettura di GitHub li ricostruisce.
CAMPI_LOCALI = ("readiness", "hold", "status", "status_source", "status_note", "links", "closed_in_session")


def adesso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def leggi_registro(path: Path) -> dict:
    """Il registro, oppure uno vuoto. Un file illeggibile viene messo da parte."""
    if not path.is_file():
        return {"schema": SCHEMA, "repo": None, "account": None, "as_of": None, "sync": {}, "issues": []}
    try:
        dati = json.loads(path.read_text(encoding="utf-8"))
        conosciuto = dati.get("schema") in (SCHEMA, "grl-issues/registry@2", "grl-issues/registry@1")
        if not conosciuto:
            raise SystemExit(
                json.dumps(
                    {"status": "blocked", "reason": f"schema non riconosciuto: {dati.get('schema')}"},
                    ensure_ascii=False,
                )
            )
        return dati
    except json.JSONDecodeError:
        guasto = path.with_suffix(".corrotto.json")
        path.rename(guasto)
        return {
            "schema": SCHEMA,
            "repo": None,
            "account": None,
            "as_of": None,
            "sync": {},
            "issues": [],
            "_recuperato_da": str(guasto),
        }


def scrivi_registro(path: Path, dati: dict) -> None:
    """Scrittura atomica: un'interruzione a metà non lascia un registro troncato."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(dati, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def gh_issue_list(repo: str, limite: int, stato: str, dal: str | None) -> list[dict]:
    campi = CAMPI_GH_ALL if stato == "all" else CAMPI_GH
    cmd = ["gh", "issue", "list", "--repo", repo, "--state", stato, "--limit", str(limite), "--json", campi]
    if dal:
        cmd += ["--search", f"updated:>={dal}"]
    esito = subprocess.run(cmd, capture_output=True, text=True)
    if esito.returncode != 0:
        raise SystemExit(json.dumps({"status": "blocked", "reason": esito.stderr.strip()[:400]}, ensure_ascii=False))
    return json.loads(esito.stdout or "[]")


# Dati che non devono finire nel registro: la sintesi è una vetrina, non un archivio.
REDAZIONI = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email omessa]"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "[ip omesso]"),
    (re.compile(r"\b(?:gh[pousr]_|sk-|xox[baprs]-)[A-Za-z0-9_-]{8,}"), "[segreto omesso]"),
    (re.compile(r"\+?\d[\d ().-]{8,}\d"), "[numero omesso]"),
]


def sintesi(corpo: str | None, limite: int = 220) -> str:
    """Una riga che dice di cosa parla la issue: il titolo da solo non basta.

    Non è un riassunto e non è il corpo: sono le prime frasi utili, ripulite dal
    markup e dai dati che non devono stare nel registro. Chi vuole il testo
    intero lo legge su GitHub — qui serve solo a capire a cosa si riferisce una
    riga dell'elenco.
    """
    if not corpo:
        return ""
    righe = []
    dentro_codice = False
    for riga in corpo.splitlines():
        riga = riga.strip()
        if riga.startswith("```"):
            dentro_codice = not dentro_codice
            continue
        # via il codice, le intestazioni, le citazioni, le immagini e le tabelle
        if dentro_codice or not riga or riga.startswith(("#", ">", "![", "|", "---")):
            continue
        riga = re.sub(r"[*_`]+", "", riga)
        riga = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", riga)
        righe.append(riga)
        if sum(len(r) for r in righe) >= limite:
            break
    testo = " ".join(righe).strip()
    for pattern, sostituto in REDAZIONI:
        testo = pattern.sub(sostituto, testo)
    if len(testo) > limite:
        testo = testo[:limite].rsplit(" ", 1)[0] + "…"
    return testo


def normalizza(grezza: dict) -> dict:
    return {
        "number": grezza["number"],
        "title": grezza.get("title", ""),
        "summary": sintesi(grezza.get("body")),
        "state": (grezza.get("state") or "OPEN").lower(),
        "labels": [l["name"] if isinstance(l, dict) else l for l in grezza.get("labels") or []],
        "milestone": (grezza.get("milestone") or {}).get("title") if isinstance(grezza.get("milestone"), dict) else grezza.get("milestone"),
        "assignees": [a["login"] if isinstance(a, dict) else a for a in grezza.get("assignees") or []],
        "updated_at": grezza.get("updatedAt"),
        "closed_at": grezza.get("closedAt"),
        "url": grezza.get("url"),
    }


def fondi(esistente: dict | None, nuova: dict, quando: str) -> dict:
    """I campi di GitHub si aggiornano, quelli locali si conservano."""
    voce = dict(esistente or {})
    if not nuova.get("summary") and esistente and esistente.get("summary"):
        nuova = {k: v for k, v in nuova.items() if k != "summary"}
    voce.update(nuova)
    voce["checked_at"] = quando
    for campo in CAMPI_LOCALI:
        if esistente and campo in esistente and campo not in nuova:
            voce[campo] = esistente[campo]
    voce.setdefault("readiness", {"verdict": None, "checked_at": None, "missing": [], "criteria": []})
    voce.setdefault("hold", {"active": False, "source": None, "who": None, "since": None, "clears_when": None})
    voce.setdefault("links", {"blocked_by": [], "duplicate_of": None, "pr": [], "code": []})
    voce.setdefault("status", "DA_VALUTARE")
    voce.setdefault("status_source", "derivato")
    voce.setdefault("status_note", None)
    voce.setdefault("closed_in_session", None)
    return voce


def deriva_stato(voce: dict, hold_labels: set[str], rejected_labels: set[str]) -> tuple[str, str | None]:
    """La scala di precedenza. Restituisce lo stato e l'eventuale contraddizione."""
    etichette = {l.lower() for l in voce.get("labels", [])}
    dichiarato = voce.get("status") if voce.get("status_source") == "dichiarato" else None

    if voce.get("state") == "closed":
        derivato = "CHIUSA"
    elif etichette & rejected_labels:
        derivato = "NON_APPROVATA"
    elif voce.get("hold", {}).get("active") or (etichette & hold_labels):
        derivato = "IN_ATTESA"
    elif voce.get("assignees"):
        derivato = "IN_SVILUPPO"
    elif voce.get("readiness", {}).get("verdict") == "NON_PRONTA":
        derivato = "DA_CHIARIRE"
    elif voce.get("readiness", {}).get("verdict") in ("PRONTA", "PRONTA_CON_RISERVA"):
        derivato = "DA_FARE"
    else:
        derivato = "DA_VALUTARE"

    if not dichiarato:
        return derivato, None
    # Un fatto letto da GitHub vince sulla dichiarazione, e la divergenza si dichiara.
    if derivato in ("CHIUSA", "NON_APPROVATA") and derivato != dichiarato:
        return derivato, f"#{voce['number']}: dichiarato {dichiarato}, GitHub dice {derivato}"
    if dichiarato in STATI_FORTI:
        return dichiarato, None
    return derivato, None


def comando_sync(args: argparse.Namespace) -> dict:
    path = Path(args.path)
    registro = leggi_registro(path)
    quando = adesso()
    incrementale = bool(registro.get("as_of")) and not args.completo

    if args.input:
        grezze = json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:
        dal = registro["as_of"][:10] if incrementale else None
        grezze = gh_issue_list(args.repo, args.limit, "all" if incrementale else "open", dal)

    indice = {v["number"]: v for v in registro.get("issues", [])}
    nuove, aggiornate = 0, 0
    for grezza in grezze:
        normale = normalizza(grezza)
        numero = normale["number"]
        if numero in indice:
            aggiornate += 1
        else:
            nuove += 1
        indice[numero] = fondi(indice.get(numero), normale, quando)

    troncato = len(grezze) >= args.limit
    registro.update(
        {
            "schema": SCHEMA,
            "repo": args.repo,
            "account": args.account,
            "as_of": quando,
            "sync": {
                "mode": "incremental" if incrementale else "full",
                "state": "all" if incrementale else "open",
                "limit": args.limit,
                "truncated": troncato,
            },
            "issues": sorted(indice.values(), key=lambda v: v["number"]),
        }
    )
    contraddizioni = applica_stati(registro, args.hold_labels, args.rejected_labels)
    scrivi_registro(path, registro)
    return {
        "action": "sync",
        "mode": registro["sync"]["mode"],
        "letti": len(grezze),
        "nuove": nuove,
        "aggiornate": aggiornate,
        "truncated": troncato,
        "contraddizioni": contraddizioni,
        "recuperato_da": registro.get("_recuperato_da"),
        **conteggi(registro, args.max_age_days),
    }


def applica_stati(registro: dict, hold: str, rejected: str) -> list[str]:
    insieme_hold = {s.strip().lower() for s in (hold or "").split(",") if s.strip()}
    insieme_rej = {s.strip().lower() for s in (rejected or "").split(",") if s.strip()}
    contraddizioni = []
    for voce in registro.get("issues", []):
        stato, nota = deriva_stato(voce, insieme_hold, insieme_rej)
        if nota:
            contraddizioni.append(nota)
            voce["status_source"] = "derivato"
        voce["status"] = stato
        if voce.get("hold", {}).get("active") is False and (
            {l.lower() for l in voce.get("labels", [])} & insieme_hold
        ):
            voce["hold"] = {
                "active": True,
                "source": "label",
                "who": None,
                "since": voce.get("updated_at"),
                "clears_when": None,
            }
    return contraddizioni


def conteggi(registro: dict, max_age_days: int) -> dict:
    per_stato = {s: 0 for s in STATI}
    for voce in registro.get("issues", []):
        per_stato[voce.get("status", "DA_VALUTARE")] = per_stato.get(voce.get("status", "DA_VALUTARE"), 0) + 1
    aperte = sum(1 for v in registro.get("issues", []) if v.get("state") == "open")
    eta = None
    obsoleto = False
    if registro.get("as_of"):
        try:
            quando = datetime.fromisoformat(registro["as_of"])
            eta = (datetime.now(timezone.utc) - quando).days
            obsoleto = eta > max_age_days
        except ValueError:
            obsoleto = True
    return {
        "as_of": registro.get("as_of"),
        "age_days": eta,
        "stale": obsoleto,
        "open": aperte,
        "by_status": per_stato,
        "hold_without_exit": [
            v["number"]
            for v in registro.get("issues", [])
            if v.get("hold", {}).get("active") and not v.get("hold", {}).get("clears_when")
        ],
    }


def comando_derive(args: argparse.Namespace) -> dict:
    path = Path(args.path)
    registro = leggi_registro(path)
    contraddizioni = applica_stati(registro, args.hold_labels, args.rejected_labels)
    scrivi_registro(path, registro)
    return {"action": "derive", "contraddizioni": contraddizioni, **conteggi(registro, args.max_age_days)}


def comando_set(args: argparse.Namespace) -> dict:
    """Scrittura di una singola voce: la usano anche readiness e verify."""
    path = Path(args.path)
    registro = leggi_registro(path)
    voce = next((v for v in registro.get("issues", []) if v["number"] == args.issue), None)
    if voce is None:
        return {"action": "set", "status": "blocked", "reason": f"#{args.issue} non è nel registro: serve un sync"}

    if args.verdict:
        voce["readiness"] = {
            "verdict": args.verdict,
            "checked_at": adesso(),
            "missing": [s for s in (args.missing or "").split(",") if s],
            "criteria": json.loads(args.criteria) if args.criteria else voce.get("readiness", {}).get("criteria", []),
        }
    if args.hold_who or args.hold_clears:
        voce["hold"] = {
            "active": True,
            "source": args.hold_source or "comment",
            "who": args.hold_who,
            "since": adesso(),
            "clears_when": args.hold_clears,
        }
    if args.code:
        voce.setdefault("links", {}).setdefault("code", [])
        for percorso in [c.strip() for c in args.code.split(",") if c.strip()]:
            if percorso not in voce["links"]["code"]:
                voce["links"]["code"].append(percorso)

    if args.clear_hold:
        voce["hold"] = {"active": False, "source": None, "who": None, "since": None, "clears_when": None}

    precedente = voce.get("status")
    if args.status:
        if args.status not in STATI:
            return {"action": "set", "status": "blocked", "reason": f"stato non ammesso: {args.status}"}
        voce["status"] = args.status
        voce["status_source"] = "dichiarato"
        voce["status_note"] = args.note
    else:
        stato, _ = deriva_stato(voce, set(), set())
        if precedente in STATI_FORTI and stato not in ("CHIUSA", "NON_APPROVATA"):
            stato = precedente
        voce["status"] = stato

    voce["checked_at"] = adesso()
    scrivi_registro(path, registro)
    return {"action": "set", "issue": args.issue, "status": voce["status"], "was": precedente}


def comando_stats(args: argparse.Namespace) -> dict:
    registro = leggi_registro(Path(args.path))
    per_stato: dict[str, list[int]] = {}
    for voce in registro.get("issues", []):
        per_stato.setdefault(voce.get("status", "DA_VALUTARE"), []).append(voce["number"])
    return {
        "action": "stats",
        "repo": registro.get("repo"),
        "account": registro.get("account"),
        "truncated": registro.get("sync", {}).get("truncated", False),
        "issues_by_status": per_stato,
        **conteggi(registro, args.max_age_days),
    }


def comando_session(args: argparse.Namespace) -> dict:
    path = Path(args.path)
    registro = leggi_registro(path)
    sessione_file = Path(args.file)
    indice = {v["number"]: v for v in registro.get("issues", [])}

    if args.start:
        ambito = [int(n) for n in args.scope.split(",") if n.strip()]
        baseline = [
            {
                "number": n,
                "state": indice.get(n, {}).get("state"),
                "status": indice.get(n, {}).get("status"),
                "updated_at": indice.get(n, {}).get("updated_at"),
            }
            for n in ambito
        ]
        sessione = {"started_at": adesso(), "ended_at": None, "scope": ambito, "baseline": baseline, "taken": []}
        sessione_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = sessione_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(sessione, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(sessione_file)
        mancanti = [n for n in ambito if n not in indice]
        return {"action": "session-start", "session": str(sessione_file), "scope": len(ambito), "non_nel_registro": mancanti}

    sessione = json.loads(sessione_file.read_text(encoding="utf-8"))
    prima = {v["number"]: v for v in sessione["baseline"]}
    chiuse, aperte, cambiate, non_verificate = [], [], [], []
    for numero, vecchia in prima.items():
        attuale = indice.get(numero)
        if attuale is None:
            non_verificate.append(numero)
        elif attuale.get("state") == "closed" and vecchia.get("state") != "closed":
            chiuse.append(numero)
        elif attuale.get("updated_at") != vecchia.get("updated_at"):
            cambiate.append(numero)
        else:
            aperte.append(numero)
    nuove = [n for n in indice if n not in prima and indice[n].get("state") == "open"]
    in_sviluppo = [n for n in prima if indice.get(n, {}).get("status") in ("IN_SVILUPPO", "IN_VERIFICA")]

    sessione["ended_at"] = adesso()
    sessione["esito"] = {"chiuse": chiuse, "aperte": aperte, "cambiate": cambiate, "nuove": nuove}
    tmp = sessione_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(sessione, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(sessione_file)
    for numero in chiuse:
        indice[numero]["closed_in_session"] = sessione_file.name
    scrivi_registro(path, registro)
    return {
        "action": "session-close",
        "session": str(sessione_file),
        "chiuse": chiuse,
        "ancora_aperte": aperte,
        "cambiate_da_altri": cambiate,
        "nuove_in_ambito": nuove,
        "non_verificate": non_verificate,
        "ancora_in_carico": in_sviluppo,
    }


def costruisci_parser() -> argparse.ArgumentParser:
    genitore = argparse.ArgumentParser(add_help=False)
    genitore.add_argument("--path", required=True, help="percorso di registry.json")
    genitore.add_argument("--max-age-days", type=int, default=30)
    genitore.add_argument("--hold-labels", default="")
    genitore.add_argument("--rejected-labels", default="")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="comando", required=True)

    p_sync = sub.add_parser("sync", parents=[genitore])
    p_sync.add_argument("--repo", required=True)
    p_sync.add_argument("--account", default=None)
    p_sync.add_argument("--limit", type=int, default=500)
    p_sync.add_argument("--completo", action="store_true", help="ignora as_of e rilegge tutto")
    p_sync.add_argument("--input", help="file JSON con l'output di gh, invece di eseguirlo")

    sub.add_parser("derive", parents=[genitore])
    sub.add_parser("stats", parents=[genitore])

    p_set = sub.add_parser("set", parents=[genitore])
    p_set.add_argument("--issue", type=int, required=True)
    p_set.add_argument("--status", choices=STATI)
    p_set.add_argument("--note")
    p_set.add_argument("--verdict", choices=["PRONTA", "PRONTA_CON_RISERVA", "NON_PRONTA", "SOSPESA"])
    p_set.add_argument("--missing", help="criteri mancanti, separati da virgola")
    p_set.add_argument("--criteria", help="JSON con esito e citazione per criterio")
    p_set.add_argument("--hold-source", choices=["label", "comment", "dependency", "milestone"])
    p_set.add_argument("--hold-who")
    p_set.add_argument("--hold-clears")
    p_set.add_argument("--clear-hold", action="store_true")
    p_set.add_argument("--code", help="file toccati dalla issue, separati da virgola: li trova la ricognizione")

    p_sess = sub.add_parser("session", parents=[genitore])
    p_sess.add_argument("--file", required=True)
    gruppo = p_sess.add_mutually_exclusive_group(required=True)
    gruppo.add_argument("--start", action="store_true")
    gruppo.add_argument("--close", action="store_true")
    p_sess.add_argument("--scope", default="")

    return parser


def main() -> int:
    args = costruisci_parser().parse_args()
    esiti = {
        "sync": comando_sync,
        "derive": comando_derive,
        "set": comando_set,
        "stats": comando_stats,
        "session": comando_session,
    }
    print(json.dumps(esiti[args.comando](args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
