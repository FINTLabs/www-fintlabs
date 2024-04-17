## FINT 2

FINT 2, vår oppdaterte API-integrasjonsplattform, bygger videre på det beste fra sin forgjenger og innfører forbedringer for både brukere og utviklere basert på tidligere erfaringer.

### Hovedelementene i den nye arkitekturen inkluderer:

1. **Forbedret horisontal skalering:** I FINT 2 kjører hver organisasjon i separate tjenester, noe som sikrer et stabilt driftsmiljø. For eksempel vil en restart av en komponent for en organisasjon ikke forstyrre andre organisasjoner.

2. **Skifte til REST API:** Vi har erstattet Server Sent Events (SSE) med REST API for kommunikasjon mellom FINT og adapterne. Dette bygger på en mer utbredt teknologisk plattform som gir økt stabilitet og trygghet.

3. **Økt fleksibilitet i dataoverføring:** Leverandører har nå friheten til å velge hvor ofte de vil overføre data, med overføringsfrekvenser justerbare fra hver 15. minutt til ukentlig. Overføringer kan suppleres med endringer, og det er mulighet for å fjerne elementer.

4. **Eventdrevet system med Apache Kafka:** Dette bidrar til en mer robust mikrotjeneste-arkitektur. Med data bevart i Kafka, hvis en konsumer restartes, trenger systemet ikke å hente data på nytt, men kan i stedet lese det fra Kafka.

5. **Full bakoverkompatibilitet:** Løsninger som allerede er bygget mot konsumer-API-et (klienter) trenger ikke å gjøre noen endringer. Dette gir kontinuitet og stabilitet for eksisterende integrasjoner.

![ill3](_media/core2-flow.svg)