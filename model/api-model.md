## Informasjonsmodellen i sentrum

I FINT, Informasjonsmodellen definerer hvordan API'et er strukturert og hvordan det fungerer.

### Type av klasser
FINT Informasjonsmodell har fire typer klasser:

1. Hovedklasser (`hovedklasse`)
1. Abstrakte klasser
1. Komplekse datatyper
1. Referanser

Bare hovedklasser er direkte tilgjengelige fra FINT APIer, og hver hovedklasse i modellen har et API-endepunkt.

?>En hovedklasse tilsvarer en ressurs i REST

Alle andre typer brukes til å konstruere hovedklassene, enten ved abstraksjon av vanlige felt, eller for å representere felt i klassene.

### Identitet

Hovedklasser har identitet, og kan refereres til ved hjelp av en identifikatorverdi. 
Dette er representert av attributter av typen `Identifikator`. 
Alle hovedklasser har minst ett attributt av denne typen, 
men det er helt lovlig å ha mer enn ett identifiserende attributt.

Hvis klassen har flere identifiserende attributter, kan alle de identifiserende attributtene brukes til å referere til den, og FINT API eksponerer endepunkter for å referere til klassen med alle de identifiserende attributtene.

For eksempel kan `Personalressurs` bli referet til av følgende attributter:
* `ansattnummer`
* `brukernavn`
* `systemId`

### Relasjoner

Relasjoner kan legges til i hovedklasser, enten direkte eller i en abstrakt basisklasse. 
I tillegg kan attributter til klassen være komplekse datatyper, som også kan ha relasjoner.

Navnet på relasjonen representerer forholdet fra kilden til målet, og har ofte samme navn som klassen til målet.

Relasjoner kan være valgfrie eller obligatoriske, enkeltverdier eller flerverdier.
I alle fall er de alltid representert i samme form.

Alle relasjoner er i `_links`-attributtet på klassen den kobler fra. Husk at dette kan være en indre kompleks datatype.

«_links»-attributtet er et objekt der navnet på relasjonen brukes som egenskapsnavnet. Egenskapen er en rekke objekter med et «href»-attributt som inneholder URIen til målressursen.

Alle relasjoner til andre ressurser i informasjonsmodellen refererer *alltid* til en hovedklasse, og bruker et av de identifiserbare feltene.

FINT-modellen inkluderer også referanser til ressurser utenfor modellen. 
Disse er representert av en spesiell type relasjoner kalt Referanse. 
De er også representert som URIer.

### Attributes

Attributter i ressursene kan enten være komplekse datatyper eller en av de primitive typene:

- string
- integer
- float
- boolean
- dateTime/date

Attributter kan være valgfrie eller obligatoriske, enkeltverdier eller flerverdier. 
Multiverdiattributter er alltid representert som en liste, selv om det bare er en enkelt verdi.

<!--
#### Dato

Dates are represented in ISO 8601 form with UTC +0 (Z) time zone.

Example: `2019-06-05T09:48:23Z`.

The adapter is responsible for all date data to UTC +0. The consumer is responsible for changing date data to a usefull timesone for the application.

Example:

Here you can se what a Date of birth can look like:

- In a HRM system: '2000-02-14T00:00:00+1'
- In FINT: '2000-02-13T23:00:00Z'
- In Consumer application: '2000-02-14T00:00:00+1'
-->