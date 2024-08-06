# Adapter API

Hvis du planlegger å implementere et adapter uten å benytte vårt JAVA-rammeverk, eller ønsker en bedre forståelse av 
hvordan adaptere kommuniserer med FINT, må adapteret kommunisere med FINTs Provider. Denne seksjonen forklarer hvilke 
data som må utveksles mellom adapteret og FINT.

> For mer informasjon, se [Swagger for provider](https://api.felleskomponent.no/provider/swagger/webjars/swagger-ui/index.html#/)

## 1. Opprette tilgang

Før du kan begynne med denne veiledningen, må en teknisk kontakt i ditt fylke opprette et adapter i kundeportalen. 
Når adapteret er opprettet, kan du hente ut OAuth2-legitimasjon fra kundeportalen. Disse legitimasjonene er nødvendige 
for å autentisere kommunikasjonen med FINT.

## 2. Registrere adapteret

Det første adapteret må gjøre, er å registrere seg selv mot endepunktet [https://api.felleskomponent.no/provider/register](https://api.felleskomponent.no/provider/register).
Under finner du et eksempel på hvordan registreringsforespørselen kan se ut:

```json
{
    "adapterId": "https://novari.no/rogfk.no/udanning/vurdering/429365f2-6853-40d8-8526-f2a020f15412",
    "orgId": "rogfk.no",
    "username": "vis@adapter.rogfk.no",
    "heartbeatIntervalInMinutes": 2,
    "capabilities": [
      {
        "domainName": "utdanning",
        "packageName": "vurdering",
        "resourceName": "elevfravær",
        "fullSyncIntervalInDays": 0,
        "deltaSyncInterval": "IMMEDIATE"
      }
    ]
}
```

| Kontraksfelter                                          | Beskrivelse                                                                                                                                                              |
|:--------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| adapterID                                               | En **persistent unik ID** for adapteret. Den bør være i følgende format: https://<firma domene>/<kunde domene>/<FINT domene>/<FINT pakke (valgfritt)>/<UUID (valgfritt)> |
| orgId                                                   | OrgId for kunden denne kontrakten representerer.                                                                                                                         |
| username                                                | Brukernavn brukt for autentisering mot FINT.                                                                                                                             |
| heartbeatIntervalInMinutes                              | Intervall i minutter adapteret skal sende heartbeats til FINT.                                                                                                           |
| capabilities                                            | Liste (array) over kapabiliteter for adapteret.                                                                                                                          |

> AdapterID skal være en unik ID. Om adapteret testkjører på en utvikler-pc skal denne ha en unik ID.

| Kapabilitetsfelter     | Beskrivelse                                                     |
|:-----------------------|:----------------------------------------------------------------|
| domainName             | Navn på FINT-domenet. For eksempel: `utdanning`.                |
| packageName            | Navn på FINT-pakken. For eksempel: `vurdering`.                 |
| resourceName           | Navn på FINT-klassen/enheten. For eksempel: `fravar`.           |
| fullSyncIntervalInDays | Antall dager mellom hver fullstendige synkronisering.           |
| deltaSyncInterval      | Delta sync strategi: NONE, LEGACY (hvert 15. minutt), IMMEDIATE |


## 3. Sende regelmessige statusbeskjeder

Heartbeat sendes til [https://api.felleskomponent.no/provider/heartbeat](https://api.felleskomponent.no/provider/heartbeat) 
og fungerer som en beskjed om at adapteret kjører og fungerer som normalt. Heartbeats skal sendes med intervaller mellom 
1 og 5 minutter. Det må altså ikke gå mer enn 5 minutter mellom hvert heartbeat.


```json
{
  "adapterId": "https://novari.no/rogfk.no/udanning/vurdering/429365f2-6853-40d8-8526-f2a020f15412",
  "username": "vis@adapter.rogfk.no",
  "orgId": "rogfk.no",
  "time": 1722932941
}
```
Heartbeat-tiden for adapteret angitt som Unix-tidsstempel. De andre feltene skal tilsvare verdiene fra adapterregistreringen.

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


