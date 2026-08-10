---
name: ricerca-live
description: Verifica documentazione, versioni, limiti e procedure firmware correnti con una gerarchia di fonti primaria.
code: RL
added: 2026-08-10
type: prompt
---

# Ricerca tecnica live

## Esito

Una decisione firmware con fonte, URL, versione o revisione, data `as_of`, copertura e limite
dichiarati. La fonte deve dimostrare la proprietà che si sta usando: un blog o un esempio non
prova il comportamento di una revisione MCU, di un driver o di un servizio OTA.

## Gerarchia

- datasheet, reference manual, errata, SDK/BSP e release notes del produttore del chip o della
  board;
- documentazione ufficiale di ARM/CMSIS, RTOS, bootloader, toolchain e debugger;
- standard e linee guida ufficiali applicabili al prodotto, con versione e scope;
- issue tracker o forum ufficiale solo per un limite non ancora formalizzato, marcandolo come
  evidenza secondaria;
- articoli, tutorial e benchmark indipendenti solo come contesto o ipotesi riproducibile, mai come
  autorità per un registro, una garanzia o una feature corrente.

## Punti di partenza ufficiali

- CMSIS startup e vector table: `https://arm-software.github.io/CMSIS_5/Core/html/startup_c_pg.html`
- CMSIS NVIC e interrupt: `https://arm-software.github.io/CMSIS_5/5.7.0/Core/html/group__NVIC__gr.html`
- FreeRTOS scheduling: `https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling`
- GCC freestanding environments: `https://gcc.gnu.org/onlinedocs/gcc/Freestanding-Environments.html`
- GDB remote debugging: `https://sourceware.org/gdb/current/onlinedocs/gdb.html/Remote-Debugging.html`
- Zephyr Twister e test su device: `https://docs.zephyrproject.org/latest/develop/test/twister.html`
- NIST SP 800-193, resilienza del firmware: `https://csrc.nist.gov/pubs/sp/800/193/final`
- MISRA: `https://misra.org.uk/`

Quando una fonte primaria è accessibile ma non chiude la domanda, non colmare il vuoto con una
fonte più rumorosa: restringi la pretesa, chiedi la revisione esatta o marca la decisione
`EVIDENZA_INSUFFICIENTE`.
