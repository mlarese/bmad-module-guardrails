---
name: test-e-debug
description: Porta un firmware da «sembra funzionare» a evidenza riproducibile su host, simulatore e target.
code: TD
added: 2026-08-10
type: prompt
---

# Test, debug e diagnosi

## Esito

Una matrice di prova dice quale rischio viene verificato, su quale ambiente, con quale input,
quale misura e quale criterio pass/fail. Il firmware engineer consegna inoltre il minimo set di
artefatti per ripetere la diagnosi: sorgenti e configurazione, ELF con simboli, map file, image
hash, versione del compiler e log del target.

## Piramide di prova

Testa su host le funzioni pure, i parser, i calcoli, le macchine a stati e i casi limite senza
periferiche; usa simulatori o emulazione per boot e integrazioni che lo consentono; usa hardware
per clock, pin, interrupt, DMA, elettrica, power mode, watchdog, reset e timing che il modello non
può dimostrare. Un test host non è evidenza di comportamento elettrico e un test manuale su board
non sostituisce la regressione ripetibile.

Per ogni caso importante includi startup/reset, timeout, brownout o perdita di alimentazione,
periferica che non risponde, buffer pieno, dati corrotti, interrupt duplicato, aggiornamento
interrotto e recovery. Fault injection è utile solo se il fault è osservabile e l'uscita attesa
è definita.

## Debug

Usa map file, simboli, registri di fault, stack frame, backtrace, contatori e trace con una
configurazione riproducibile. GDB/JTAG/SWD e il protocollo del probe devono lavorare sull'ELF
esatto che gira sul target; un mismatch fra binary e simboli produce diagnosi ingannevoli. Se il
problema è timing, misura il pin o il trace: non dedurlo dal tempo stampato in log.

Quando proponi un log o una strumentazione, specifica costo in flash/RAM, latenza, frequenza,
privacy del payload e come rimuoverla. La causa di un fault va separata dal sintomo e l'ipotesi
va chiusa con una prova che potrebbe anche smentirla.

## Build e qualità

Tratta warning, static analysis, coding rule e coverage come evidenze diverse. MISRA può rendere
esplicite regole e deviazioni, ma non dimostra da sola assenza di bug, portabilità o robustezza.
Il criterio di accettazione collega ogni requisito critico a test, misura, log o review; ciò che
non può essere provato resta `EVIDENZA_INSUFFICIENTE`, non «pass».
