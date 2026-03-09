## Hvorfor FINT versjon 2

FINT versjon 2, vår oppdaterte API-integrasjonsplattform, bygger videre på det beste fra sin forgjenger og introduserer en rekke forbedringer som gagner både brukere og andre interessenter. Selv om denne oppgraderingen medfører at adaptere må oppdateres og tilpasses, er fordelene så åpenbare at vi mener endringen er nødvendig.

### Årsaker til nyutvikling

- **Ustabilitet med SSE:** Bruken av Server Sent Events har vist seg å være ustabil, noe som fører til at både vi og brukerne tidvis må restarte adapterne.
- **Ineffektiv dataoppdatering:** Det er uhensiktsmessig å hente fullstendige datasett hvert 15. minutt, ettersom oppdateringsbehovet varierer.
- **Samkjøring av alle fylkeskommuner i samme container:** Selv om data er trygt avskilt, er det mer hensiktsmessig å dele opp fylkeskommunene for å oppnå bedre isolasjon og skalerbarhet.
- **Full datahenting ved restart:** Ved en restart må all data hentes på nytt, noe som kan føre til unødvendig belastning og nedetid.

### Fordeler med den nye arkitekturen

- **Forbedret horisontal skalering:** Hver organisasjon kjører nå i separate tjenester, noe som sikrer et stabilt driftsmiljø og isolerer eventuelle problemer til den berørte organisasjonen.
- **Overgang til REST API:** Skiftet fra SSE til REST API gir økt stabilitet og trygghet ved å benytte en mer utbredt teknologisk plattform.
- **Økt fleksibilitet i dataoverføring:** Adapter-leverandører kan oppdatere data etter behov, med mulighet til å sende deltaendringer og slette data, i stedet for å overføre komplette datasett med jevne mellomrom.
- **Eventdrevet arkitektur med Apache Kafka:** Bruken av Kafka i en mikrotjeneste-arkitektur reduserer behovet for full datahenting ved restart, ettersom data kan hentes direkte fra Kafka.
- **Full bakoverkompatibilitet:** Eksisterende løsninger som benytter konsumer-API-et, trenger ikke endres. Dette sikrer kontinuitet og stabilitet for alle integrasjoner.
- **Autorelasjon:** En tjeneste som automatisk oppretter og vedlikeholder spesifikke relasjoner slik at adapteret slipper å utføre større prosessering for å vedlikeholde relasjoner selv.
