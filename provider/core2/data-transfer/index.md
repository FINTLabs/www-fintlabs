# Dataoverføring til FINT

Du trenger et fint-adapter for å overføre data, se artikkel om hvordan opprette adapter [her](/provider/core2/registrer-a-core-2-adapter/index.md)

Når du har registrert adapteret kan du sende data. En dataoverføring ser slik ut:
```json
{
  "metadata": {
    "adapterId": "string",
    "corrId": "string",
    "orgId": "string",
    "totalSize": 0,
    "page": 0,
    "pageSize": 0,
    "totalPages": 0,
    "uriRef": "string"
  },
  "resources": [
    {
      "identifier": "string",
      "resource": {}
    }
  ],
  "syncType": "FULL"
}
```


Feltene:
```
 adapterId: id´en til adapteret
 corrid: corrilasjons id for overførelsen
 orgId: OrganisasjonsIden til de som eier adapteret
 totalSize: antall ellementer i overførelsen
 uriRef: referansen til resursen eks /utdanning/elev/elev
  "resources": [
    {
      "identifier": "string",: identifikatoren til objektet
      "resource": { Dette kan eks være en elev
      "brukernavn": "testen"
      "elevnummer": 202928485,
      }
     syncType: type sync som skal gjøres
```

## Pageing:
paging er å dele elementene inn i bolker, slik at man ikke sender alt på en page.

totalSize / pageSize = totalPages

Feltene betyr:

1. totalSize: total antall elementer i overføringen,
2. page: første siden
3. pageSize: antall elementer på hver side 
4. totalPages: antall sider

Det kan foreksempel deles slik:

```
   "totalSize": 50000,
    "page": 1,
    "pageSize": 10000,
    "totalPages": 5,
```

Eller
```
   "totalSize": 100000,
    "page": 1,
    "pageSize": 10000,
    "totalPages": 10,
```

## Synctypene

Adapteret kan gjøre fullsync, deltasync og delete sync

FULL er for å opprette et nytt element (POST)

```json
  "resources": [
{
"identifier": "string",
"resource": {
        "Nytt element"
}
}
],
"syncType": "FULL"
```

DELTA er for å oppdatere (PATCH)

```json
  "resources": [
{
"identifier": "string",
"resource": {
        "oppdatert element"
}
}
],
"syncType": "DELTA"
```

For å slette et element i FINT trenger man bare å sende id´en til elementet, man trenger ikke å sende med alle feltene
(DELETE)

```json
  "resources": [
{
"identifier": "15541545121",
"resource": {}
}
],
"syncType": "DELETE"
```