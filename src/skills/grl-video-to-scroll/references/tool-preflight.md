# Preflight degli strumenti

Il workflow non presume che il computer sia pronto. Prima di chiedere il customer journey o cercare sorgenti esegue `scripts/check_tools.py` e conserva il JSON in `tool-preflight.json`.

## Capability obbligatorie

- `uv`: esegue gli script isolati del workflow;
- `ffmpeg`: estrae i frame;
- `ffprobe`: legge durata e dimensioni del video;
- `{project-root}/_bmad/scripts/resolve_config.py`, `resolve_customization.py` e `memlog.py`: runtime BMad necessario per configurazione, personalizzazione e memoria.

Se una voce manca, lo stato è `missing`. Il workflow mostra il comando adatto al sistema operativo e chiede conferma prima di installare. Un comando suggerito non è un'autorizzazione: non eseguire `brew`, `apt`, `winget`, `pip` o installer remoti senza il sì esplicito dell'utente. Dopo l'installazione ripeti il controllo; il passaggio è sbloccato solo da `status: pass`.

## Comandi suggeriti

- macOS con Homebrew: `brew install uv ffmpeg`
- Debian/Ubuntu: `sudo apt-get install ffmpeg` e installazione di `uv` dal package manager o dalla documentazione ufficiale del sistema;
- Windows con winget: `winget install --id=astral-sh.uv -e` e `winget install --id=Gyan.FFmpeg.Shared -e`.

Se il sistema non corrisponde a questi casi, chiedi quale package manager usare e non improvvisare un installer. Se `uv` non è ancora disponibile, il check può essere lanciato con `python3 scripts/check_tools.py {project-root}` per produrre comunque il report; gli altri script restano bloccati finché il preflight non passa.
