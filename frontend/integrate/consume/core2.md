# Core 2

Core 2 er den nye plattformen bak FINT. Endringen er først og fremst i infrastrukturen, og i hvordan leverandørene leverer 
data til FINT (se [Levere data](integrate/provide/index.md) og [Hvorfor Core 2](integrate/provide/core2-why.md)). For klienter 
er API-et det samme som i Core 1, med noen få unntak som står under. Se [Hva ligger hvor](integrate/consume/platforms.md) 
for hvilke domener som kommer fra Core 1 og Core 2.

Svar fra Core 2 har headeren `x-core-version`, og verdien begynner på `2`.

## Versjon 3 og 4 av informasjonsmodellen

Versjon 4 av [informasjonsmodellen](model/index.md) for domenet `utdanning` leveres fra Core 2. I produksjon kan 
fylkeskommunene fortsatt bruke versjon 3 av `utdanning` til de er klare for versjon 4, og versjon 3 leveres da fra Core 1. 
I beta finnes bare versjon 4 av `utdanning`, fra Core 2.

Hvilken versjon en klient bruker, velges for klienten i [Kundeportalen](portal/klient.md). FINT setter headeren 
`x-fint-model-version` (`V3` eller `V4`) på hver forespørsel ut fra det valget, og headeren bestemmer hvor forespørselen går. 
Klienten trenger ikke sende den selv, og en verdi klienten sender, blir overskrevet.

En enkelt forespørsel kan be om den andre versjonen med headeren `x-fint-model-version-override: V3` eller `V4`.

## Forskjeller for klienter

|                                                                                         | Core 1                                                    | Core 2                                                                  |
|:----------------------------------------------------------------------------------------|:----------------------------------------------------------|:------------------------------------------------------------------------|
| [`sinceTimeStamp`](integrate/consume/api.md?id=hent-objekter-oppdatert-siden-tidsstempel) | Ekskluderende: objekter endret etter tidsstemplet (`>`)   | Inkluderende: objekter endret ved eller etter tidsstemplet (`>=`)       |
| [`admin/health`](integrate/consume/api.md?id=helsesjekk)                                | Finnes                                                    | Finnes ikke, og trengs ikke. Adapterne sender heartbeats til FINT.      |
| [Sletting med `DELETE`](integrate/consume/updates.md?id=slette-objekter)                | Bare `arkivressurs` i `arkiv/noark`                       | Støttes ikke                                                            |

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
4. **Fjern kall til `admin/health`.**
5. **Test i beta.** `utdanning` kjører på Core 2 i beta, så klienten kan testes der før den tas i bruk i produksjon.
