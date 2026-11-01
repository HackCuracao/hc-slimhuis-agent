# Wat dit agentje wel en niet doet

**Wel:** elke 5 minuten één POST naar HackCuraçao met alleen getallen: versie van Home Assistant en van de add-on,
uptime, leeftijd van de laatste back-up, aantal beschikbare updates, aantal sensoren met lage batterij,
aantal apparaten offline, totaal aantal apparaten en schijfgebruik in procenten.

**Niet:** entiteitsnamen, waarden, automatiseringen, camerabeelden, locaties of IP-adressen worden niet verstuurd.
De server weigert elke melding met extra velden (strikt schema).

- Geen open poorten op de box; alleen uitgaand HTTPS.
- Het token is per woning, wordt bij ons alleen als hash bewaard en kan direct worden ingetrokken.
- Verwijder de add-on en de meldingen stoppen.
- De broncode is één leesbaar bestand (`hc_slimhuis/agent.py`).
