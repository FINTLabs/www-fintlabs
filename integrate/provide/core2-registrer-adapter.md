# Adapter kontrakt

>Den tekniske kontakten i ditt fylke må opprette et adapter i kundeportalen før du kan begynne med denne veiledningen.

Når du har registrert adapteret så må du sende en kontrakt til provider-registrer.
Den kan sendes til https://api.felleskomponent.no/provider/register. Du kan se et eksempel på hvordan den ser ut under.

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
    "component": "string",
    }
],
}
```

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


## Overfør data til FINT
Inni resource feltet skal du legge inn identifikatorveriden til elementet og reursen.
De sendes som en liste.

```json
{
  "metadata": {
    "adapterId": "44-577524-5753",
    "corrId": "string",
    "orgId": "123456789",
    "totalSize": 100000,
    "page": 4,
    "pageSize": 20000,
    "totalPages": 0,
    "uriRef": "string",
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

## Paging i FINT

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


> Se swagger siden for mer informasjon
> swagger: https://api.felleskomponent.no/provider/swagger/webjars/swagger-ui/index.html#/