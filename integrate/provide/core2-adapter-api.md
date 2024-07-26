# Adapter kontrakt

Når du skal implementere et adapter må det snakke med FINTs Provider. Her forklarer vi hvilke data som må utveksles fra adapteret til FINT.

> Se swagger siden for mer informasjon
> swagger: https://api.felleskomponent.no/provider/swagger/webjars/swagger-ui/index.html#/

## 1. Opprette tilgang

En teknisk kontakten i ditt fylke må opprette et adapter i kundeportalen før du kan begynne med denne veiledningen. Fra kundeportalen kan
man da hente ut oauth2-kredentials som må brukes for å autentisere kommunikasjonen med FINT. 

## 2. Registrere adapteret

Det første adapteret må gjøre, er å registrere seg selv mot endepunktet https://api.felleskomponent.no/provider/register.
Du kan se et eksempel på hvordan den ser ut under.

```json
{
    "adapterId": "44-577524-5753",
    "orgId": "123456789",
    "username": "adapter-brukernavn",
    "heartbeatIntervalInMinutes": 2,
    "capabilities": [
    {
        "domainName": "utdanning",
        "packageName": "vurdering",
        "resourceName": "elevfravær",
        "fullSyncIntervalInDays": 0,
        "deltaSyncInterval": "IMMEDIATE",
        "component": "string"
    }
    ]
}
```

## 3. Sende regelmessige statusbeskjeder

Heartbeat sendes til https://api.felleskomponent.no/provider/heartbet og ser slik ut:

> HeartbeatIntervalInMinutes kan ikke være lengre en 5
> 
> Husk å å bytte ut til riktig miljø. Hvis adapteret foreksempel er registrert i beta miljøet,
> så må heartbeat også sendes der

 ```json
    {
    "adapterId": "44-577524-5753",
    "username": "mitt-adapter",
    "orgId": "123456789",
    "time": 0
    }
   ```


## 4. Overfør data
Inni resource feltet skal du legge inn identifikatorveriden til elementet og reursen.
De sendes som en liste.

```json
{
  "metadata": {
    "adapterId": "44-577524-5753",
    "corrId": "string",
    "orgId": "fintlabs-no",
    "totalSize": 786,
    "page": 1,
    "pageSize": 786,
    "totalPages": 1
  },
  "resources": [
    {
      "identifier": "elevfrafar_1",
      "resource": {
        "elevForhold": elevForhold,
        "fraværsregistrering": fraværsregistrering
      }
    }
  ],
  "syncType": "FULL"
}

```

## Paginering av dataene

Når du skal overføre store mengder data så må du dele det inn i pages
For å page så deler du totale antall elementer og deler det på antall pages du skal overføre

```json
    "page": 1,
    "pageSize": 12500,
    "totalPages": 4
```

```json
    "page": 1,
    "pageSize": 50000,
    "totalPages": 5
```


