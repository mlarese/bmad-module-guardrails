#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6.0"]
# ///
"""Pubblica nei repository GitHub i moduli tematici generati in `dist/`.

Va eseguito dopo `tools/build_modules.py`. Per ogni modulo: inizializza il clone
se manca, allinea il remote, committa quello che è cambiato e fa push. Un modulo
senza modifiche viene saltato senza commit vuoti.

L'About del repository su GitHub vive fuori dai file versionati: viene riallineata
qui al campo inglese `about` della topologia, nella stessa lingua del README generato,
così non resta indietro da sola.

  python3 tools/publish_modules.py -m "sync: nuova regola su X"
  python3 tools/publish_modules.py --module grw --dry-run

Codici di uscita: 0 = successo, 1 = errore di pubblicazione, 2 = errore d'ambiente.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Serve PyYAML: pip install PyYAML", file=sys.stderr)
    raise SystemExit(2)


OWNER = "mlarese"
BRANCH = "main"
# Limite dell'API GitHub sulla descrizione del repository: oltre, HTTP 422.
DESCRIPTION_LIMIT = 350


def run(command: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"{' '.join(command)}\n{result.stderr.strip()}")
    return result


def repo_exists(repo: str) -> bool:
    return run(["gh", "repo", "view", f"{OWNER}/{repo}"], check=False).returncode == 0


def ensure_repo(repo: str, description: str, dry_run: bool) -> bool:
    """Crea il repository se non esiste. Ritorna True se è stato creato ora."""
    if repo_exists(repo):
        return False
    if dry_run:
        print(f"  [dry-run] creerei {OWNER}/{repo}")
        return True
    run(["gh", "repo", "create", f"{OWNER}/{repo}", "--public", "--description", description])
    return True


def sync_description(repo: str, description: str, dry_run: bool) -> None:
    if len(description) > DESCRIPTION_LIMIT:
        description = description[: DESCRIPTION_LIMIT - 1].rsplit(" ", 1)[0] + "…"
    current = run(
        ["gh", "repo", "view", f"{OWNER}/{repo}", "--json", "description", "--jq", ".description"],
        check=False,
    )
    if current.returncode == 0 and current.stdout.strip() == description:
        return
    if dry_run:
        print("  [dry-run] aggiornerei l'About")
        return
    run(["gh", "repo", "edit", f"{OWNER}/{repo}", "--description", description])


def module_about(module: dict) -> str:
    """Restituisce l'About pubblico, obbligatoriamente distinto dalla descrizione interna."""
    about = module.get("about")
    if not about:
        raise RuntimeError(f"topologia: manca `about` per il modulo {module.get('code', '?')}")
    if len(about) > DESCRIPTION_LIMIT:
        raise RuntimeError(
            f"topologia: `about` oltre {DESCRIPTION_LIMIT} caratteri per il modulo {module['code']}"
        )
    return about


def tag_release(path: Path, repo: str, version: str, dry_run: bool) -> str | None:
    """Marca la versione anche sul derivato, se non è già marcata.

    Il numero sta già dentro `marketplace.json`, ma da lì non si trova senza
    aprire il pacchetto: chi installa da un derivato non vede la fonte, e un
    repository senza tag non dice a quale release corrisponde il codice che ha
    davanti. Il tag è la versione detta dove si guarda per prima.
    """
    nome = f"v{version}"
    esistente = run(["git", "tag", "-l", nome], cwd=path, check=False).stdout.strip()
    if esistente:
        return None
    if dry_run:
        return f"[dry-run] marcherei {nome}"
    run(["git", "tag", "-a", nome, "-m", f"{repo} {version}"], cwd=path)
    run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            "credential.helper=!gh auth git-credential",
            "push",
            "origin",
            nome,
        ],
        cwd=path,
    )
    return nome


def publish(path: Path, repo: str, message: str, dry_run: bool) -> str:
    """Committa e pusha il contenuto generato. Ritorna cosa è successo."""
    if not (path / ".git").exists():
        if dry_run:
            return "clone da inizializzare"
        run(["git", "init", "-b", BRANCH], cwd=path)
        run(["git", "remote", "add", "origin", f"https://github.com/{OWNER}/{repo}.git"], cwd=path)

    if not dry_run:
        remote = run(["git", "remote", "get-url", "origin"], cwd=path, check=False)
        expected = f"https://github.com/{OWNER}/{repo}.git"
        if remote.returncode != 0:
            run(["git", "remote", "add", "origin", expected], cwd=path)
        elif remote.stdout.strip() != expected:
            run(["git", "remote", "set-url", "origin", expected], cwd=path)

    run(["git", "add", "-A"], cwd=path)
    staged = run(["git", "diff", "--cached", "--stat"], cwd=path, check=False).stdout.strip()
    if not staged:
        return "nessuna modifica"
    if dry_run:
        return f"{len(staged.splitlines()) - 1} file da pubblicare"

    run(["git", "commit", "-m", message], cwd=path)
    # L'helper esplicito evita che osxkeychain risponda con l'account sbagliato.
    run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            "credential.helper=!gh auth git-credential",
            "push",
            "-u",
            "origin",
            BRANCH,
        ],
        cwd=path,
    )
    return f"{len(staged.splitlines()) - 1} file pubblicati"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source-root", default=".", help="radice del repository fonte")
    parser.add_argument("--out", default="dist", help="cartella dei moduli generati")
    parser.add_argument("--module", action="append", help="pubblica solo questo codice (ripetibile)")
    parser.add_argument(
        "-m",
        "--message",
        default="chore: rigenerato dal repository fonte bmad-module-guardrails",
        help="messaggio di commit",
    )
    parser.add_argument("--dry-run", action="store_true", help="mostra cosa farebbe, senza toccare nulla")
    args = parser.parse_args(argv)

    source_root = Path(args.source_root).resolve()
    out_root = Path(args.out)
    if not out_root.is_absolute():
        out_root = source_root / out_root

    topology = yaml.safe_load((source_root / "src" / "module-topology.yaml").read_text(encoding="utf-8"))
    version = yaml.safe_load((source_root / "src" / "module.yaml").read_text(encoding="utf-8"))["module_version"]
    wanted = set(args.module) if args.module else None
    modules = [m for m in topology["modules"] if wanted is None or m["code"] in wanted]

    failures = 0
    for module in modules:
        path = out_root / module["repo"]
        print(f"{module['code']:>4}  {module['repo']}")
        if not path.exists():
            print("      manca in dist/: esegui prima tools/build_modules.py")
            failures += 1
            continue
        try:
            about = module_about(module)
            created = ensure_repo(module["repo"], about, args.dry_run)
            if created:
                print("      repository creato")
            sync_description(module["repo"], about, args.dry_run)
            print(f"      {publish(path, module['repo'], args.message, args.dry_run)}")
            marcato = tag_release(path, module["repo"], str(version), args.dry_run)
            if marcato:
                print(f"      {marcato}")
        except RuntimeError as error:
            print(f"      errore: {error}")
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
