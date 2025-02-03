## Hvorfor FINT versjon 2

FINT versjon 2, vår oppdaterte API-integrasjonsplattform, bygger videre på det beste fra sin forgjenger og innfører forbedringer for både brukere og utviklere basert på tidligere erfaringer. Selv om denne oppgraderingen medfører at adaptere må oppdateres og tilpasses, er fordelene så åpenbare at vi mener endringen er nødvendig.

### Årsaker til nyutvikling

- **Ustabilitet med SSE:** Bruken av Server Sent Events har vist seg å være ustabil og mindre pålitelig enn ønskelig. 
- **Ineffektiv dataoppdatering:** Det er uhensiktsmessig å hente alle data på nytt hvert 15. minutt, siden behovet for oppdatering varierer.
- **Samkjøring av alle fylker i samme container:** Selv om data er trygt avskilt, er det mer hensiktsmessig å kunne splitte fylkene for bedre isolasjon og skalerbarhet.
- **Full datahenting ved restart:** Ved en restart må all data hentes på nytt, noe som kan føre til unødvendig belastning og nedetid.

### Fordeler med den nye arkitekturen

- **Forbedret horisontal skalering:** Hver organisasjon kjører nå i separate tjenester, noe som sikrer et stabilt driftsmiljø og isolerer eventuelle problemer til den aktuelle organisasjonen.
- **Skifte til REST API:** Overgangen fra SSE til REST API gir økt stabilitet og trygghet ved å benytte en mer utbredt teknologisk plattform.
- **Økt fleksibilitet i dataoverføring:** Adapter-leverandører kan oppdatere data når det er hensiktsmessig, med mulighet til å sende deltaendringer og slette data, i stedet for å overføre fullstendige datasett med jevne mellomrom.
- **Eventdrevet system med Apache Kafka:** Bruken av Kafka i en mikrotjeneste-arkitektur reduserer behovet for full datahenting ved restart, siden data kan leses direkte fra Kafka.
- **Full bakoverkompatibilitet:** Eksisterende løsninger som er bygget mot konsumer-API-et trenger ikke endres, noe som sikrer kontinuitet og stabilitet for alle integrasjoner.