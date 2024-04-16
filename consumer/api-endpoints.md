# Forstå API-et

Disse operasjonene er tilgjengelige for alle klasser i FINT informasjonsmodellen.

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

`/domain/package/class?size=X&offset=Y`, for eksempel `/administrasjon/personal/personalressurs?size=10000&offset=20000`

Den komplette listen over ressurser kan være svært lang, og FINT API støtter paginering for å muliggjøre at klienter kan konsumere deler av dataene.

Paginering er aktivert ved å oppgi en `size` forespørselsparameter. Responsen ser da slik ut:

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

Returnerer en samling av alle objekter som har blitt oppdatert (lagt til eller endret) etter det oppgitte tidsstemplet. Responsen ser slik ut:

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

__NOTE:__ Denne algoritmen kan kombineres med paginering. I dette tilfellet blir trinn 3 en løkke der ressurser
hentes til responsen ikke lenger inneholder en `next`-lenke.

## Helsesjekk

`/domain/package/admin/health`, for eksempel `/administrasjon/personal/admin/health`

Utløser en helsesjekk mot adapteren som leverer data. Responsen indikerer om adapteren er tilkoblet og svarer.


