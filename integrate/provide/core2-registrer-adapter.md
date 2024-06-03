# Adapter kontrakt

>Før du begynner med denne må du registrere et adapter 
> på [kundeportalen](../portal/adapter.md).


Når du har registrert adapteret så må du sende en kontrakt til provider-registrer.
Den kan sendes til https://api.felleskomponent.no/provider/register. Du kan se et eksempel på hvordan den ser ut under.

```json
{
"adapterId": "Adapter-id fra kundeportalen",
"orgId": "organisasjons id",
"username": "adapter-brukernavn",
"heartbeatIntervalInMinutes": 2,
"capabilities": [
    {
    "domainName": "utdanning",
    "packageName": "vurdering",
    "resourceName": "elevfravær",
    "fullSyncIntervalInDays": 0,
    "deltaSyncInterval": "IMMEDIATE",
    "component": "string",
    "entityUri": "string"
    }
],
"time": 0
}
```

Heartbeat sendes til https://api.felleskomponent.no/provider/heartbet og ser slik ut:

> HeartbeatIntervalInMinutes kan ikke være lengre en 5
> 
> Husk å å bytte ut til riktig miljø. Hvis adapteret foreksempel er registrert i beta miljøet,
> så må heartbeat også sendes der

 ```json
    {
    "adapterId": "string",
    "username": "string",
    "orgId": "string",
    "time": 0
    }
   ```


## Overfør data til FINT
Inni resource feltet skal du legge inn identifikatorveriden til elementet og reursen. 
De sendes som en liste.

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
    "uriRef": "string",
    "time": 0
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

## Paging i FINT

Når du skal overføre store mengder data så må du dele det inn i pages
For å page så deler du totale antall elementer og deler det på antall pages du skal overføre

```json
    "page": 1,
    "pageSize": 12500,
    "totalPages": 4
```

> Se swagger siden for mer informasjon
> swagger: https://api.felleskomponent.no/provider/swagger/webjars/swagger-ui/index.html#/