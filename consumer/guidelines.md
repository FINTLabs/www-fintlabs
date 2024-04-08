# Konsepter

## REST API

Vårt REST API er bygget med nøkkelprinsipper som skal sikre en robust og skalerbar arkitektur for distribuerte systemer. Her er en kort oversikt over de grunnleggende konseptene vi benytter:

- **REST (Representational State Transfer):** Dette er den arkitektoniske stilen som leder designet av vårt API, med mål om å kunne skape skalerbar interaksjon med web-baserte tjenester. For å fordype deg i REST-prinsippene, besøk [Wikipedia: Representational state transfer](https://en.wikipedia.org/wiki/Representational_state_transfer).
- **HATEOAS (Hypermedia as the Engine of Application State):** Denne begrensningen av RESTful-design sikrer at våre klienter forblir koblet fra server-sidelogikk, og fremmer langsiktig fleksibilitet og utvikling av API-et. Du kan lese mer om HATEOAS på [Wikipedia: HATEOAS](https://en.wikipedia.org/wiki/HATEOAS).
- **HAL (Hypertext Application Language):** Vi bruker HAL for å standardisere måten ressurser lenker til hverandre innen vårt API, noe som gjør det enkelt å navigere og konsumere. Mer informasjon om HAL er tilgjengelig på [Wikipedia: Hypertext Application Language](https://en.wikipedia.org/wiki/Hypertext_Application_Language).


## Generelle retningslinjer

For å få mest mulig verdi fra FINT APIer, er noen retningslinjer å følge.

### Informasjon som en Graf

FINT-ressurser har relativt få attributter, men flere relasjoner. Hver ressurs har bare de attributtene som er
direkte relevant for ressursen. Alt annet representeres som relasjoner (lenker) til andre ressurser.
Som et eksempel, klassen `Personalressurs`, som representerer en ansatt, har ikke den ansattes navn. I stedet er det
en lenke til `Person`, som representerer en privatperson, hvor du finner egenskapene til den ansatte som en privatperson.

### Referer, ikke repliker

Informasjon endres alltid. Foreldet data er ofte verre enn å ikke ha noen data i det hele tatt. FINT APIet er basert på prinsippet om at informasjon bør hentes fra kilden når det er nødvendig, ikke replikeres på forhånd.

### Stabile referanser

Ressurser i FINT representeres ved hjelp av URIer. Disse URIene er konstruert av APIet basert på attributter som kan brukes til å identifisere ressursen, representert ved typen `Identifikator`. 

Så lenge det identifiserbare attributtet ikke endres, endres heller ikke URIen som representerer ressursen.

### Alt er en ressurs

Alle klasser i FINTs informasjonsmodell representeres på nøyaktig samme måte, som ressurser med URIer og referanser ved hjelp av URIer til andre klasser den refererer til.

Typen av ressursen er eksplisitt fra URIen til ressursen. For eksempel, fra URIen `/administrasjon/personal/personalressurs`, er typen av ressursen alltid `Personalressurs`.
