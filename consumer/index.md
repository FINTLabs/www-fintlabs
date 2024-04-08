# Integrer med FINT

Hvis du skal bruke FINT en del, for eksempel til å lage en integrasjon eller et adapter, anbefaler vi at du gjør deg kjent med [våre retningslinjer](consumer/guidelines.md).


## Miljøer

FINT tilbyr tre miljøer:

* <https://play-with-fint.felleskomponent.no> (sandbox)
* <https://beta.felleskomponent.no> (beta)
* <https://api.felleskomponent.no> (produksjon)


## Få tilgang
Miljøet "play-with-fint" kan brukes uten noen form for autentisering, så hvis du bare ønsker å utforske, kan du starte her. Hvis du ønsker å få tilgang til BETA- eller API-miljøet, kan du be om autentiseringsinformasjon fra en organisasjon du samarbeider med. Dette kan gjøres ved å opprette en ny klient i Kundeportalen, som gir deg nok informasjon til å generere en OAuth2-token. Les mer om [tilgang til FINT](consumer/access.md).


## REST API

REST API-endepunktene er bygget i henhold til informasjonsmodellen. For å vite hva du skal spørre etter, bør du gjøre deg kjent med hvordan [informasjonsmodellen er strukturert]().

Se [Forstå APIet](consumer/api-endpoints.md) for å forstå endepunktstrukturen for ulike funksjonaliteter som å hente ved ID, paginering og last-updated. [Oppdatering](consumer/updating.md) angående hvordan du utfører UPDATE- og POST-forespørsler.


Many users prefer to test queries against the REST API using applications like Postman or Insomnia. If you'd rather not install a separate client, you can utilize our web-based [Testklient](consumer/testklient.md) for convenient and direct access to our API endpoints.

Mange brukere foretrekker å teste spørringer mot REST APIet ved hjelp av applikasjoner som Postman eller Insomnia. Om du vil teste spørringer uten å installere en separat klient, kan du benytte vår nettbaserte [Testklient](consumer/testklient.md) for direkte tilgang til våre API-endepunkter.


## GraphQL

[Dokumentasjon](consumer/graphql.md) for vår eldre GraphQL-tjeneste.