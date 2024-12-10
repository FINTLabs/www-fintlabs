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

Det første adapteret må gjøre, er å registrere seg selv ved å sende en POST-forespørsel til URL-en [https://api.felleskomponent.no/provider/register](https://api.felleskomponent.no/provider/register).
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
        "resourceName": "elevfravar",
        "fullSyncIntervalInDays": 7,
        "deltaSyncInterval": "IMMEDIATE"
      }
    ]
}
```

| Kontraksfelter                                          | Beskrivelse                                                                                                                                                          |
|:--------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| adapterID                                               | En **persistent unik ID** for adapteret. Den bør være i følgende format: https:\/\/firma-domene\/kunde-domene\/FINT-domene\/FINT-pakke (valgfritt)\/UUID (valgfritt) |
| orgId                                                   | OrgId for kunden denne kontrakten representerer.                                                                                                                     |
| username                                                | Brukernavn brukt for autentisering mot FINT.                                                                                                                         |
| heartbeatIntervalInMinutes                              | Intervall i minutter adapteret skal sende heartbeats til FINT.                                                                                                       |
| capabilities                                            | Liste (array) over kapabiliteter for adapteret.                                                                                                                      |

> AdapterID skal være en unik ID. Om adapteret testkjører på en utvikler-pc skal denne ha en unik ID.

| Kapabilitetsfelter     | Beskrivelse                                                     |
|:-----------------------|:----------------------------------------------------------------|
| domainName             | Navn på FINT-domenet. For eksempel: `utdanning`.                |
| packageName            | Navn på FINT-pakken. For eksempel: `vurdering`.                 |
| resourceName           | Navn på FINT-klassen/enheten. For eksempel: `fravar`.           |
| fullSyncIntervalInDays | Antall dager mellom hver fullstendige synkronisering (maks 7).  |
| deltaSyncInterval      | Delta sync strategi: NONE, LEGACY (hvert 15. minutt), IMMEDIATE |

## 3. Sende regelmessige statusbeskjeder

Heartbeat sendes med en POST-forespørsel til [https://api.felleskomponent.no/provider/heartbeat](https://api.felleskomponent.no/provider/heartbeat) 
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

## 4. Dataoverføring

Det kan utføres tre ulike typer dataoverføring:

| Forespørselstype | Parameteren `syncType` | Beskrivelse                                          |
|:-----------------|:-----------------------|------------------------------------------------------|
| POST             | FULL                   | All data sendes                                      |
| PATCH            | DELTA                  | Kun endret data sendes                               |
| DELETE           | DELETE                 | Kun identifikatorer for data som skal fjernes sendes |

URLen bygges opp etter hvilken ressurs som skal overføres: /provider/\[Domene\]/\[Komponent\]/\[Ressurs\]
For eksempel: (https://api.felleskomponent.no/provider/utdanning/vurdering/elevfravar)[https://api.felleskomponent.no/provider/utdanning/vurdering/elevfravar]

Inni resource feltet skal du legge inn identifikatorveriden til elementet og reursen.
De sendes som en liste.

```json
{
  "metadata": {
    "adapterId": "https://novari.no/rogfk.no/udanning/vurdering",
    "corrId": "95db7353-6cf6-4757-84c5-2a7782d3e504",
    "orgId": "rogfk.no",
    "totalSize": 786,
    "page": 1,
    "pageSize": 786,
    "totalPages": 1
  },
  "resources": [
    {
      "identifier": "10001",
      "resource": {
        "json-data"
      }
    }
  ],
  "syncType": "FULL"
}
```

| Felter     | Beskrivelse                                                                                                                                                                                      |
|:-----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| adapterId  | Samme Id som brukt ved registrering av adapteret.                                                                                                                                                |
| corrId     | En universell unik identifisering for denne batchen.                                                                                                                                             |
| orgId      | OrgId for mottakerorganisasjon.                                                                                                                                                                  |
| totalSize  | Det totale antallet ressurser som skal synkroniseres over alle sider. Dette tallet representerer det fullstendige antallet elementer som blir overført i løpet av hele synkroniseringsprosessen. |
| page       | Den nåværende siden i synkroniseringen. Dette tallet angir hvilken side av de paginerte dataene som blir sendt akkurat nå, hvor første side starter på 1.                                        |
| pageSize   | Størrelsen på den nåværende siden, det vil si hvor mange ressurser som er inkludert på denne spesifikke siden i synkroniseringen.                                                                |
| totalPages | Det totale antallet sider i synkroniseringen. Dette tallet angir hvor mange sider dataene er delt opp i for denne synkroniseringsprosessen.                                                      |
| resources  | Et array med ressurser. Hver resurs har en unik identifikator og en resource med selve dataene for ressursen.                                                                                    |
| syncType   | Type overføring. Se tidligere beskrivelse.                                                                                                                                                       |

### Paginering av dataene

Når du skal overføre store mengder data, er det nødvendig å dele dataene opp i mindre deler, kjent som "pages" eller sider. Dette gjøres for å sikre at overføringen er håndterbar og effektiv, spesielt når mengden data er stor.

For å implementere paginering, må du beregne hvor mange sider som trengs ved å dele det totale antallet elementer (totalSize) på ønsket antall elementer per side (pageSize). Resultatet vil gi deg totalPages, som representerer det totale antallet sider i synkroniseringen. Det trenger ikke være likt antall elementer pr side.

Hver side overføres deretter som en separat forespørsel, hvor metadataene spesifiserer hvilken side av dataene som overføres (ved hjelp av page-feltet).

#### Eksempel på paginering

Hvis du har 50,000 elementer som skal synkroniseres, og ønsker å dele dette opp i sider med 12,500 elementer per side, vil metadataene se slik ut:

```json
    "totalSize" : 50000
    "page": 1,
    "pageSize": 12500,
    "totalPages": 4
```

Dette betyr at det totalt vil være 4 sider, hver med 12,500 elementer. Første side (side 1) overføres med denne informasjonen, etterfulgt av side 2, 3, og 4.

I tilfeller hvor det totale antallet elementer er 250,000, og du velger å bruke 50,000 elementer per side, vil pagineringsdataene se slik ut:

```json
    "totalSize" : 250000
    "page": 1,
    "pageSize": 50000,
    "totalPages": 5
```

Dette betyr at det vil være 5 sider totalt, hver med 50,000 elementer.

Gjennom å bruke paginering sikrer du at store mengder data kan overføres på en strukturert og effektiv måte, som reduserer belastningen både på klienten og serveren.

## Hendelser

Enkelte ressurser er merket som skrivbare i modellen. I disse tilfellene kan klienter sende oppdateringer til FINT ved hjelp av en 
POST- eller PUT-forespørsel for å opprette eller endre en ressurs. Hendelsene er asynkrone, noe som betyr at dersom forespørselen blir godtatt, 
vil klienten motta en `Location`-header som gjør det mulig å følge opp statusen til hendelsen.
I tillegg kan en klient be om validering av en ressurs og i noen tilfeller sende en DELETE-forespørsel.


| Klient forespørsel | Hendelsestype til adapter (Operation type) |
|:-------------------|:-------------------------------------------|
| POST               | CREATE                                     |
| PUT                | UPDATE                                     |
| POST?validate=true | VALIDATE                                   | 
| DELETE             | DELETE                                     |


### Hente hendelser

Adapteret henter innsendte hendelser ved å sende en GET-forespørsel til `/event`-endepunktet. Adapteret kan filtrere relevante 
hendelser ved å spesifisere en sti som `/event/[domene]/[pakke]/[ressurs]`. For eksempel kan `/event/administrasjon/personal/fravar` 
brukes for å hente hendelser relatert til fravær. Som svar returneres en liste over hendelsesforespørsler, hvor en enkelt forespørsel kan se slik ut:

```
{
  corrId: "244fec3c-5044-4d77-b908-2c3330e3110c"
  orgId: "vestfoldfylke.no"
  domainName: "administrasjon"
  packageName: "personal"
  resourceName: "fravar"
  operationType: "CREATE"
  created: 1733821906
  timeToLive: 1733825506
  value: "{<JSON for ressursen>}"
}
```

### Gi svar på hendelser

Når adapteret er ferdig med å behandle en hendelse, sender det en respons tilbake til FINT ved hjelp av en POST-forespørsel 
til `/event`-endepunktet. Svaret må følge kontrakten definert i [ResponseFintEvent](https://github.com/FINTLabs/fint-core-infra-models/blob/main/src/main/java/no/fintlabs/adapter/models/ResponseFintEvent.java) 
og kan se slik ut:

```
{
  corrId: "244fec3c-5044-4d77-b908-2c3330e3110c"
  orgId: "vestfoldfylke.no"
  adapterId: "https://yourdomain.com/vestfoldfylke.no/administrasjon/personal"
  handledAt: 1733820206
  value: {
    identifier: "107849"
    resource: { <JSON for ressursen> }
  }
  operationType: "CREATE"
  failed: false
  errorMessage: null
  rejected: false
  rejectReason: null
  conflicted: false
  conflictReason: null
}
```

Default-verdier er valgfrie. Ved `VALIDATE` trenger ikke `resource` settes, med mindre det er en konflikt.

> DELETE-hendelser er for tiden under utvikling og ikke ferdig dokumentert.
