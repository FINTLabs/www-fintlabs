# Core 2

Core 2 er den nye plattformen bak FINT. Endringen er først og fremst i infrastrukturen, og i hvordan leverandørene leverer 
data til FINT (se [Levere data](integrate/provide/index.md) og [Hvorfor Core 2](integrate/provide/core2-why.md)). For klienter 
er API-et det samme som i Core 1, med noen få unntak som står under. Se [Hva ligger hvor](integrate/consume/platforms.md) 
for hvilke domener som kommer fra Core 1 og Core 2.

Svar fra Core 2 har headeren `x-core-version` med en verdi på formen `2.x`, for eksempel `2.1`. Slik kan du se hvilken 
plattform som svarer (se [Tilgang](integrate/consume/access.md) for hvordan du får et token):

```sh
curl -i -H "Authorization: Bearer ${TOKEN}" https://api.felleskomponent.no/utdanning/elev/elev/last-updated
```

```
HTTP/2 200
x-core-version: 2.1
...
```

Mangler headeren, kom svaret fra Core 1.

## Versjon 3 og 4 av informasjonsmodellen

Versjon 4 av [informasjonsmodellen](model/index.md) for domenet `utdanning` leveres fra Core 2. I produksjon kan 
fylkeskommunene fortsatt bruke versjon 3 av `utdanning` til de er klare for versjon 4, og versjon 3 leveres da fra Core 1. 
I beta finnes bare versjon 4 av `utdanning`, fra Core 2.

Hvilken versjon en klient bruker, velges for klienten i [Kundeportalen](portal/klient.md). FINT setter headeren 
`x-fint-model-version` (`V3` eller `V4`) på hver forespørsel ut fra det valget, og headeren bestemmer hvor forespørselen går. 
Klienten trenger ikke sende den selv, og en verdi klienten sender, blir overskrevet.

En enkelt forespørsel kan be om den andre versjonen med headeren `x-fint-model-version-override: V3` eller `V4`:

```sh
curl -H "Authorization: Bearer ${TOKEN}" -H "x-fint-model-version-override: V4" \
  https://api.felleskomponent.no/utdanning/elev/elev
```

## Forskjeller for klienter

|                                                                                         | Core 1                                                    | Core 2                                                                  |
|:----------------------------------------------------------------------------------------|:----------------------------------------------------------|:------------------------------------------------------------------------|
| [`sinceTimeStamp`](integrate/consume/api.md?id=hent-objekter-oppdatert-siden-tidsstempel) | Ekskluderende: objekter endret etter tidsstemplet (`>`)   | Inkluderende: objekter endret ved eller etter tidsstemplet (`>=`)       |
| [`admin/health`](integrate/consume/api.md?id=helsesjekk)                                | Finnes                                                    | Finnes ikke, og trengs ikke. Adapterne sender heartbeats til FINT.      |
| [Sletting med `DELETE`](integrate/consume/updates.md?id=slette-objekter)                | Bare `arkivressurs` i `arkiv/noark`                       | Støttes ikke                                                            |
| [Paginering](integrate/consume/api.md?id=paginering)                                    | `size` og `offset`, ingen grense for `size`               | `size` og `next`-lenken, som har en `cursor`. Hver ressurs har en største sidestørrelse, høyst 1000 objekter |

## Grenser for paginering

Core 2 begrenser hvor mange objekter en side kan ha når klienten bruker [paginering](integrate/consume/api.md?id=paginering-i-core-2). 
Grensene skal holde en side på omtrent 0,5 MB eller mindre. Ber klienten om en `size` over grensen, får den en side med 
grensens størrelse. En forespørsel uten `size` har ingen grense.

Ressursene i tabellen har en grense under 1000 objekter. Alle andre ressurser har grensen 1000.

| Ressurs                                               | Største `size` |
|:------------------------------------------------------|---------------:|
| `administrasjon/fullmakt/fullmakt`                    |            500 |
| `administrasjon/fullmakt/rolle`                       |              1 |
| `administrasjon/organisasjon/arbeidslokasjon`         |              5 |
| `administrasjon/organisasjon/organisasjonselement`    |             50 |
| `administrasjon/personal/arbeidsforhold`              |            250 |
| `administrasjon/personal/fastlonn`                    |            250 |
| `administrasjon/personal/fasttillegg`                 |            250 |
| `administrasjon/personal/fravar`                      |            500 |
| `administrasjon/personal/person`                      |            500 |
| `administrasjon/personal/personalressurs`             |            250 |
| `administrasjon/personal/variabellonn`                |            250 |
| `personvern/kodeverk/behandlingsgrunnlag`             |            500 |
| `personvern/kodeverk/personopplysning`                |            500 |
| `personvern/samtykke/behandling`                      |              1 |
| `personvern/samtykke/samtykke`                        |            500 |
| `personvern/samtykke/tjeneste`                        |            500 |
| `ressurs/datautstyr/digitalenhet`                     |            500 |
| `ressurs/datautstyr/enhetsgruppe`                     |            250 |
| `utdanning/elev/elev`                                 |            500 |
| `utdanning/elev/elevforhold`                          |            100 |
| `utdanning/elev/klasse`                               |            100 |
| `utdanning/elev/kontaktlarergruppe`                   |            100 |
| `utdanning/elev/person`                               |            500 |
| `utdanning/elev/skoleressurs`                         |            500 |
| `utdanning/elev/undervisningsforhold`                 |            500 |
| `utdanning/kodeverk/karakterskala`                    |            100 |
| `utdanning/larling/larling`                           |            500 |
| `utdanning/larling/virksomhet`                        |             10 |
| `utdanning/timeplan/fag`                              |             50 |
| `utdanning/timeplan/faggruppe`                        |            100 |
| `utdanning/timeplan/undervisningsgruppe`              |            100 |
| `utdanning/utdanningsprogram/arstrinn`                |             10 |
| `utdanning/utdanningsprogram/programomrade`           |            500 |
| `utdanning/utdanningsprogram/programomrademedlemskap` |            500 |
| `utdanning/utdanningsprogram/skole`                   |              1 |
| `utdanning/utdanningsprogram/utdanningsprogram`       |             10 |
| `utdanning/vurdering/eksamensgruppe`                  |            250 |
| `utdanning/vurdering/elevfravar`                      |            100 |
| `utdanning/vurdering/elevvurdering`                   |            500 |
| `utdanning/vurdering/fravarsregistrering`             |            500 |
| `utdanning/vurdering/halvarsfagvurdering`             |            500 |
| `utdanning/vurdering/sluttfagvurdering`               |            500 |
| `utdanning/vurdering/underveisfagvurdering`           |            500 |

Grensene kan bli endret. Ikke legg dem inn i klienten. Følg `next`-lenken i responsen, så får klienten alle objektene 
uansett grense.

## Flytte en klient til Core 2

1. **Bruk versjon 4 av informasjonsmodellen.** Bruker klienten versjon 3 av `utdanning`, velg V4 for klienten i Kundeportalen, 
   og tilpass klienten til endringene i modellen.
2. **Hent alt på nytt når klienten flyttes.** Hent hele samlingen uten `sinceTimeStamp`, og nullstill tidsstempler klienten 
   har lagret fra Core 1. Et tidsstempel fra Core 1 kan ikke brukes mot Core 2.
3. **Tål at et objekt kommer to ganger med `sinceTimeStamp`.** Siden filteret er inkluderende, kommer objektene fra den 
   siste leveransen med på nytt i neste runde. Oppdater objektene du allerede har basert på identifikatoren (upsert), i 
   stedet for å legge dem til på nytt. Gjør klienten noe mer når et objekt kommer, for eksempel skriver til et annet system, 
   bør den først sjekke om innholdet faktisk er endret. Med upsert kan klienten også trekke noen sekunder fra tidsstemplet 
   for å være sikker på å få med alt, siden data lagres kort tid etter at de er levert.
4. **Følg `next`-lenken når klienten paginerer.** Hent den første siden med `size`, og følg `next`-lenken til responsen 
   ikke har en. Ikke regn ut `offset` selv. Core 2 har en største sidestørrelse for hver ressurs, så en klient som regner 
   ut `offset` selv, kan hoppe over objekter. Se [Paginering i Core 2](integrate/consume/api.md?id=paginering-i-core-2).
5. **Fjern kall til `admin/health`.**
6. **Test i beta.** `utdanning` kjører på Core 2 i beta, så klienten kan testes der før den tas i bruk i produksjon.
