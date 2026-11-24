# Forstå API-et

Disse operasjonene er tilgjengelige for alle klasser i FINT informasjonsmodellen.

API-et følger [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS). Hver ressurs har en `_links`-del med lenker til seg selv 
(`self`) og til ressursene den er relatert til, så klienter kan følge lenkene i stedet for å bygge adresser selv. Se også 
[Retningslinjer](integrate/consume/guidelines.md).

## Hent alle objekter av en gitt klasse

`/domain/package/class`, for eksempel `/administrasjon/personal/personalressurs`

Denne operasjonen henter alle objekter av en gitt klasse fra FINTs cache. Responsen ser slik ut:


```json
{
  "_embedded": {
    "_entries": [
      {

      },
      {

      }
    ]
  },
  "_links": {
    "self": [
      {
          "href": "..."
      }
    ]
  },
  "total_items": 111
}
```

## Paginering

Den komplette listen over ressurser kan være svært lang, og FINT API støtter paginering for å muliggjøre at klienter kan konsumere deler av dataene.

Paginering er aktivert ved å oppgi en `size` forespørselsparameter. Core 2 og Core 1 paginerer på hver sin måte. Se 
[Hva ligger hvor](integrate/consume/platforms.md) for hvilken plattform et domene kommer fra.

### Paginering i Core 2

`/domain/package/class?size=X`, for eksempel `/administrasjon/personal/personalressurs?size=250`

I Core 2 følger klienten `next`-lenken fra side til side:

1. Hent den første siden med `size`.
2. Hent neste side med `next`-lenken i responsen. Bruk lenken slik den står.
3. Gjenta til responsen ikke har en `next`-lenke. Da har klienten alle objektene.

Responsen ser slik ut:

```json
{
  "_embedded": {
    "_entries": [
      {

      },
      {

      }
    ]
  },
  "_links": {
    "self": [
      {
        "href": ".../?offset=250&size=250&cursor=..."
      }
    ],
    "prev": [
      {
        "href": ".../?offset=0&size=250&cursor=..."
      }
    ],
    "next": [
      {
        "href": ".../?offset=500&size=250&cursor=..."
      }
    ]
  },
  "total_items": 10632,
  "offset": 250,
  "size": 250
}
```

`next`-lenken har en `cursor` som forteller hvor neste side starter. Klienten skal ikke lage eller endre `cursor`, og 
skal ikke regne ut `offset` selv.

`prev`- og `next`-lenkene vises bare når det finnes en side før eller etter denne siden. `total_items` er den totale 
størrelsen på datasettet, og `size` er antall objekter i denne responsen.

#### Største sidestørrelse

Hver ressurs har en største sidestørrelse. Ingen ressurs har en større side enn 1000 objekter, og noen ressurser har en 
lavere grense. Se [Grenser for paginering](integrate/consume/core2.md?id=grenser-for-paginering) for grensen til hver ressurs.

Ber klienten om en `size` over grensen, inneholder responsen en side med grensens størrelse. `size` i responsen og i 
lenkene viser størrelsen på siden klienten fikk. En klient som følger `next`-lenken, får alle objektene uansett grense.

En forespørsel uten `size` henter fortsatt alle objektene i én respons.

### Paginering i Core 1

`/domain/package/class?size=X&offset=Y`, for eksempel `/administrasjon/personal/personalressurs?size=10000&offset=20000`

I Core 1 velger klienten selv hvor siden starter, med `offset`. `size` har ingen grense. Responsen ser slik ut:

```json
{
  "_embedded": {
    "_entries": [
      {

      },
      {

      }
    ]
  },
  "_links": {
    "self": [
      {
        "href": ".../?offset=20000&size=10000"
      }
    ],
    "prev": [
      {
        "href": ".../?offset=10000&size=10000"
      }
    ],
    "next": [
      {
        "href": ".../?offset=30000&size=10000"
      }
    ]
  },
  "total_items": 1800000,
  "offset": 20000,
  "size": 10000
}
```

`prev` og `next` lenkene vil kun vises hvis det er ytterligere sider før eller etter denne siden, henholdsvis.

I tillegg indikerer `total_items` attributtet den totale størrelsen på datasettet, og `offset` og `size` parametrene svarer til de i `self`-lenken.


## Hent individuelt element ved identifikator

`/domain/package/class/field/value`, for eksempel `/administrasjon/personal/personalressurs/ansattnummer/123456`

Gitt et identifikatorfeltnavn (ethvert felt av type `Identifikator`) og identifikatorverdien, forsøk å hente det individuelle elementet.

## Størrelse på cache for en gitt klasse

`/domain/package/class/cache/size`, for eksempel `/administrasjon/personal/personalressurs/cache/size`

Returner størrelsen på cachen for en gitt klasse. Responsen ser slik ut:

```json
{
  "size": 10632
}
```

## Tidsstempel for når cachen sist ble oppdatert

`/domain/package/class/last-updated`, for eksempel `/administrasjon/personal/personalressurs/last-updated`

Returner et tidsstempel som angir når cachen sist ble oppdatert. Responsen ser slik ut:

```json
{
  "lastUpdated": "1559551091034"
}
```

## Hent objekter oppdatert siden tidsstempel

`/domain/package/class?sinceTimeStamp=<time>`, for eksempel `/administrasjon/personal/personalressurs?sinceTimeStamp=1559551091034`

Returnerer en samling av alle objekter som har blitt oppdatert (lagt til eller endret) **ved eller etter** det oppgitte tidsstemplet.
Filteret er inkluderende (`>=`), så objekter som ble endret nøyaktig på tidsstemplet, kommer med.

> **Core 1:** Filteret er ekskluderende (`>`), så bare objekter endret etter tidsstemplet kommer med. Se [Core 2](integrate/consume/core2.md).

Responsen ser slik ut:

```json
{
  "_embedded": {
    "_entries": [
      {

      },
      {

      }
    ]
  },
  "_links": {
    "self": [
      {
          "href": "..."
      }
    ]
  },
  "total_items": 2
}
```

Hvis `total_items` er `0`, indikerer dette at det ikke er noen nye oppdateringer siden det gitte tidsstemplet.

Den generelle algoritmen for kontinuerlig å hente oppdateringer er denne:

1. Opprett en `timestamp`-variabel, opprinnelig satt til `0`.
2. Hent verdien fra `.../last-updated`, og lagre denne i en _ny_ variabel.
3. Hent ressurser, ved å bruke forespørselsparameteren `sinceTimeStamp=<timestamp>`
4. Oppdater `timestamp`-variabelen med verdien hentet fra trinn 2.
5. Gjenta så ofte som du finner nødvendig.

Siden filteret er inkluderende, kan objekter fra forrige runde komme med på nytt. Oppdater derfor objektene du allerede har
basert på identifikatoren (upsert), slik at et objekt som kommer to ganger, ikke gir duplikater.

__NOTE:__ Denne algoritmen kan kombineres med paginering. I dette tilfellet blir trinn 3 en løkke der ressurser
hentes til responsen ikke lenger inneholder en `next`-lenke.

## Helsesjekk

`/domain/package/admin/health`, for eksempel `/administrasjon/personal/admin/health`

Utløser en helsesjekk mot adapteret som leverer data. Responsen indikerer om adapteret er tilkoblet og svarer.

> **Bare Core 1:** Endepunktet finnes ikke i Core 2, og trengs ikke der. I Core 2 sender adapterne selv jevnlige heartbeats til FINT.


