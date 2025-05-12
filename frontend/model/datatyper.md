# Datatyper i Informasjonsmodellen.

## Dato og tid

Til dato og tid brukes to datatypet, date og datetime.
For begge brukes ISO 8601 format YYYY-MM-DDThh:mm:ssZ .

Referanse: ISO 8601 : https://en.wikipedia.org/wiki/ISO_8601

### Date

Timedelen er egentlig unødvendig der bare dato har verdi. 
Det anbefales at en da setter den til klokken 12 på dagen (zulu). 
Derved kan dato leses direkte uten å gjøre om til lokaltid ( i Norge).


#### Eksempler
 * 29.mars 1990 -> 1990-03-29T12:00:00Z
 * 29.juni 1990 -> 1990-06-29T12:00:00Z

### Datetime

Brukes der hvor både dato og klokkeslett har verdi.

#### Eksempler

* 29.mars 1990 klokken 13:30 (UTC +1) -> 1990-03-29T12:30:00Z
* 29.juni 1990 klokken 13:30 (UTC +2 sommertid) -> 1990-06-29T11:30:00Z

#### Merk

I noen klasser er det satt datetime på attributter hvor bare dato er av verdi.
Dette vil fremgå av beskrivelsen av attributten.

## Identifikator

En kombinasjon av tegn eller og/eller bokstaver som unikt identifiserer et objekt blant andre objekter av samme type uten arv.

Identifikatorer må være stabile over tid, og henvise til samme objekt.

Dersom identifikatorer konstrueres av sammensatte verdier må særskilt hensyn tas for å sikre at identifikatorverdien ikke endres over tid.

Eksempel
Kan for eksempel brukes til å identifisere en person ut fra fødselsnummer eller ansattnummer.

* For en person kan det være fødselsnummer
* For er personresurs kan det være ansattnummer eller signatur
* For er elev kan det være elevnummer.
* For organisasjonselement kan det være organisasjonsnummer fra Enhetsregistret.
* systemId kan være objektID eller rowID i underliggende database, dersom denne er stabil over tid.

## Beløp
Beløp (pengebeløp) er alltid av typen `long`.

Beløpet skal alltid oppgis i hundredeler av hovedvalutaen.

### Eksempel

 * Beløpet 123,45 NOK overføres som verdien 12345 .
 * Beløpet 100 NOK overføres som verdien 10000 .

