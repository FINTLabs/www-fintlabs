# Adapter API

Hvis du planlegger å implementere et adapter uten å benytte vårt JAVA-rammeverk, eller ønsker en bedre forståelse av 
hvordan adaptere kommuniserer med FINT, må adapteret kommunisere med FINTs Provider. Denne seksjonen forklarer hvilke 
data som må utveksles mellom adapteret og FINT.

> For mer informasjon, se [Swagger for provider](https://api.felleskomponent.no/provider/swagger/webjars/swagger-ui/index.html#/)

Alle svar fra Core 2 har headeren `x-core-version: 2.1`. Den viser at adapteret snakker med den nye plattformen.

## 1. Opprette tilgang

Før du kan begynne med denne veiledningen, må en teknisk kontakt i ditt fylke opprette et adapter i kundeportalen. 
Når adapteret er opprettet, kan du hente ut OAuth2-legitimasjon fra kundeportalen. Disse legitimasjonene er nødvendige 
for å autentisere kommunikasjonen med FINT.

Adapteret sender tokenet som en `Authorization: Bearer`-header i alle forespørsler. Tokenet må være utstedt med scope 
`fint-adapter`, og det bestemmer hvilke organisasjoner og komponenter adapteret har tilgang til.

Skal adapteret levere data for flere organisasjoner, for eksempel underorganisasjoner, må de være lagt til på adapteret i 
kundeportalen. Adapteret må da registrere en kontrakt for hver organisasjon (se neste steg).

## 2. Registrere adapteret

Det første adapteret må gjøre, er å registrere en kontrakt ved å sende en POST-forespørsel til URL-en [https://api.felleskomponent.no/provider/register](https://api.felleskomponent.no/provider/register).
Kontrakten forteller FINT hvilke ressurser adapteret leverer data for, og hvilke hendelser det kan svare på.
Under finner du et eksempel på hvordan registreringsforespørselen kan se ut:

```json
{
    "adapterId": "https://novari.no/rogfk.no/utdanning/vurdering/429365f2-6853-40d8-8526-f2a020f15412",
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
    ],
    "eventCapabilities": [
      {
        "domainName": "utdanning",
        "packageName": "vurdering",
        "resourceName": "elevfravar",
        "operations": ["CREATE", "UPDATE", "VALIDATE"]
      }
    ]
}
```

| Kontraktsfelter            | Beskrivelse                                                                                                                                                          |
|:---------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| adapterId                  | En **persistent unik ID** for adapteret. Den bør være i følgende format: https:\/\/firma-domene\/kunde-domene\/FINT-domene\/FINT-pakke (valgfritt)\/UUID (valgfritt). Mangler den, bruker FINT `username` i stedet. |
| orgId                      | Organisasjonen kontrakten gjelder for. Må være en av organisasjonene adapteret har tilgang til i kundeportalen.                                                       |
| username                   | Brukernavnet adapteret autentiserer seg med. Må være det samme som i tokenet.                                                                                        |
| heartbeatIntervalInMinutes | Intervall i minutter adapteret skal sende heartbeats til FINT. Bør være mellom 1 og 5.                                                                               |
| capabilities               | Liste over ressursene adapteret leverer data for. Kan være tom hvis adapteret bare svarer på hendelser.                                                              |
| eventCapabilities          | Liste over ressursene og operasjonene adapteret svarer på hendelser for. Valgfri. Se [Hendelser](integrate/provide/core2-adapter-api.md?id=hendelser).                                                        |

> AdapterID skal være en unik ID. Om adapteret testkjører på en utvikler-pc skal denne ha en unik ID.

> Feltet `time` i kontrakten er utgått, og FINT leser det ikke. Ikke send det.

| Kapabilitetsfelter     | Beskrivelse                                                                  |
|:-----------------------|:-----------------------------------------------------------------------------|
| domainName             | Navn på FINT-domenet. For eksempel: `utdanning`.                             |
| packageName            | Navn på FINT-pakken. For eksempel: `vurdering`.                              |
| resourceName           | Navn på FINT-klassen/enheten. For eksempel: `elevfravar`.                    |
| fullSyncIntervalInDays | Antall dager mellom hver fullstendige synkronisering. Mellom 1 og 7.         |
| deltaSyncInterval      | Valgfri. Delta sync strategi: `NONE`, `LEGACY` (hvert 15. minutt), `IMMEDIATE` |

| Hendelseskapabilitetsfelter | Beskrivelse                                                                                    |
|:----------------------------|:-----------------------------------------------------------------------------------------------|
| domainName                  | Navn på FINT-domenet.                                                                          |
| packageName                 | Navn på FINT-pakken.                                                                           |
| resourceName                | Navn på FINT-klassen/enheten.                                                                  |
| operations                  | Operasjonene adapteret svarer på: `CREATE`, `UPDATE`, `VALIDATE`, `DELETE` og/eller `READ`. Minst én. |

FINT svarer `200 OK` når kontrakten er lagret. Ellers gjelder disse reglene:

- Hver ressurs må finnes i informasjonsmodellen. Er noe feil, svarer FINT `400 Bad Request` med en liste over feltene 
  som er feil (se [Feilmeldinger](integrate/provide/core2-adapter-api.md?id=feilmeldinger)), og ingenting blir lagret.
- Står samme ressurs flere ganger i `capabilities`, beholder FINT bare én av dem, den med kortest `fullSyncIntervalInDays`. 
  Store og små bokstaver i navnene spiller ingen rolle.
- I `eventCapabilities` kan hver ressurs bare stå én gang. Står den flere ganger, svarer FINT `400 Bad Request`.
- En kontrakt gjelder for én kombinasjon av `username` og `orgId`. Registreres den på nytt, erstattes hele kontrakten, 
  så ressurser som ikke lenger er med, blir fjernet.
- Dataoverføring krever en registrert kontrakt for organisasjonen. Registrer kontrakten når adapteret starter, og på nytt 
  når den endres. Hendelser kan hentes og besvares uten kontrakt, se [Hendelser](integrate/provide/core2-adapter-api.md?id=hendelser).

## 3. Sende regelmessige statusbeskjeder

Heartbeat sendes med en POST-forespørsel til [https://api.felleskomponent.no/provider/heartbeat](https://api.felleskomponent.no/provider/heartbeat) 
og fungerer som en beskjed om at adapteret kjører og fungerer som normalt. Heartbeats skal sendes med intervallet fra 
kontrakten (`heartbeatIntervalInMinutes`). Det bør ikke gå mer enn 5 minutter mellom hvert heartbeat.


```json
{
  "adapterId": "https://novari.no/rogfk.no/utdanning/vurdering/429365f2-6853-40d8-8526-f2a020f15412",
  "username": "vis@adapter.rogfk.no",
  "orgId": "rogfk.no"
}
```
Feltene skal tilsvare verdiene fra kontrakten. FINT bruker tidspunktet heartbeatet kommer inn, så feltet `time` trenger ikke sendes.

## 4. Dataoverføring

Det kan utføres tre ulike typer dataoverføring:

| Forespørselstype | Parameteren `syncType` | Beskrivelse                                          | Svar ved suksess |
|:-----------------|:-----------------------|:-----------------------------------------------------|:-----------------|
| POST             | FULL                   | All data sendes                                      | `201 Created`    |
| PATCH            | DELTA                  | Kun endret data sendes                               | `201 Created`    |
| DELETE           | DELETE                 | Kun identifikatorer for data som skal fjernes sendes | `200 OK`         |

URLen bygges opp etter hvilken ressurs som skal overføres: /provider/\[domene\]/\[pakke\]/\[ressurs\].
For eksempel: [https://api.felleskomponent.no/provider/utdanning/vurdering/elevfravar](https://api.felleskomponent.no/provider/utdanning/vurdering/elevfravar)

Ressursen må være med i `capabilities` i kontrakten til organisasjonen i `metadata.orgId`. Hvis ikke, svarer FINT `403 Forbidden`.

Et vellykket svar betyr at FINT har tatt imot siden, ikke at ressursene er lagret. Ressursene lagres asynkront kort tid etter. 
Felter som ikke finnes i informasjonsmodellen, blir ignorert.

Inni resource feltet skal du legge inn identifikatorverdien til elementet og ressursen.
De sendes som en liste.

```json
{
  "metadata": {
    "adapterId": "https://novari.no/rogfk.no/utdanning/vurdering",
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
      "resource": { <JSON for ressursen> }
    }
  ],
  "syncType": "FULL"
}
```

| Felter     | Beskrivelse                                                                                                                                                                                      |
|:-----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| adapterId  | Samme Id som brukt ved registrering av adapteret.                                                                                                                                                |
| corrId     | En universell unik identifisering for denne synkroniseringen. **Alle sidene i samme synkronisering må ha samme `corrId`.**                                                                      |
| orgId      | OrgId for mottakerorganisasjon. Organisasjonen må ha en registrert kontrakt.                                                                                                                     |
| totalSize  | Det totale antallet ressurser som skal synkroniseres over alle sider. Ved fullstendig synkronisering må tallet være **nøyaktig**, se [Fullstendig synkronisering](integrate/provide/core2-adapter-api.md?id=fullstendig-synkronisering). |
| page       | Den nåværende siden i synkroniseringen. Dette tallet angir hvilken side av de paginerte dataene som blir sendt akkurat nå, hvor første side starter på 1.                                        |
| pageSize   | Størrelsen på den nåværende siden, det vil si hvor mange ressurser som er inkludert på denne spesifikke siden i synkroniseringen.                                                                |
| totalPages | Det totale antallet sider i synkroniseringen. Dette tallet angir hvor mange sider dataene er delt opp i for denne synkroniseringsprosessen.                                                      |
| resources  | Et array med ressurser. Hver ressurs har en `identifier` og en `resource` med selve dataene for ressursen.                                                                                       |
| syncType   | Type overføring. Se tidligere beskrivelse.                                                                                                                                                       |

`identifier` er nøkkelen FINT lagrer ressursen under. Den må være en av ressursens identifikatorverdier, for eksempel 
verdien i `systemId.identifikatorverdi`.

- Samme ressurs må alltid sendes med samme `identifier`, også i svar på hendelser. Får den en annen, lagres den to ganger, 
  og klienter ser begge til neste fullstendige synkronisering er ferdig.
- Er `identifier` ikke en av ressursens identifikatorverdier, får ressursen ingen [autorelasjon](integrate/provide/core2-autorelation.md).
- Klienter slår opp ressurser på identifikatorfeltene i selve ressursen, ikke på `identifier`.

Ved DELETE brukes bare `identifier`. `resource` kan utelates.

### Fullstendig synkronisering

En fullstendig synkronisering (FULL) er alltid en komplett oversikt over ressurstypen. Når FINT har mottatt like mange 
ressurser som `totalSize` for en `corrId`, slettes alle ressurser av typen som ikke ble levert i denne synkroniseringen.

- Er `totalSize` for høy, blir synkroniseringen aldri ferdig, og gamle data blir ikke slettet.
- Er `totalSize` for lav, blir synkroniseringen ferdig for tidlig, og ressurser fra de siste sidene kan bli slettet før de kommer inn igjen.
- Endringer som kommer via delta-synkronisering eller hendelser mens den fullstendige synkroniseringen pågår, blir ikke slettet.
- En fullstendig synkronisering med `totalSize: 0` tømmer ressurstypen.
- Delta- og delete-synkronisering sletter aldri annet enn det de sender.

Har en ressurstype ikke hatt en fullført fullstendig synkronisering på 21 dager, sletter FINT alle ressursene av typen. 
Ressurser som bare oppdateres med delta-synkronisering eller hendelser, forsvinner derfor etter 21 dager. Send derfor en 
fullstendig synkronisering minst så ofte som `fullSyncIntervalInDays` i kontrakten.

### Uendrede ressurser

FINT sammenligner hver ressurs med den som allerede er lagret. Er innholdet likt, regnes ressursen som levert, men ikke 
endret. Klienter som henter endringer med `sinceTimeStamp`, får derfor bare ressurser med faktisk endret innhold. 
Rekkefølgen på lenkene i `_links` regnes ikke som en endring.

### Relasjoner i `_links`

Relasjoner til andre ressurser sendes i `_links`. Hver relasjon er en liste med lenker:

```json
"_links": {
  "elevforhold": [
    { "href": "systemid/9595833" }
  ]
}
```

- FINT leser de to siste delene av lenken som identifikatorfelt og identifikatorverdi, for eksempel `systemid/9595833`. 
  Resten av lenken blir ignorert, så relative og absolutte lenker fungerer likt. FINT bygger lenkene på nytt med riktig 
  adresse når klienter henter data.
- Identifikatorfeltet må være et identifikatorfelt på ressursen det lenkes til. Store og små bokstaver spiller ingen rolle.
- Inneholder identifikatorverdien `/` eller andre spesialtegn, må den URL-kodes, for eksempel `%2F`.
- En lenke kan også sendes som en ren tekststreng i stedet for et objekt med `href`.
- Lenker FINT ikke kan tolke, blir lagret og vist som de er, men gir ikke autorelasjon.
- `self`-lenker trenger ikke sendes. FINT lager dem selv ut fra identifikatorfeltene.

### Paginering av dataene

Når du skal overføre store mengder data, er det nødvendig å dele dataene opp i mindre deler, kjent som "pages" eller sider. Dette gjøres for å sikre at overføringen er håndterbar og effektiv, spesielt når mengden data er stor.

For å implementere paginering, må du beregne hvor mange sider som trengs ved å dele det totale antallet elementer (totalSize) på ønsket antall elementer per side (pageSize). Resultatet vil gi deg totalPages, som representerer det totale antallet sider i synkroniseringen. Det trenger ikke være likt antall elementer pr side.

Hver side overføres deretter som en separat forespørsel med samme `corrId` og `totalSize`, hvor metadataene spesifiserer hvilken side av dataene som overføres (ved hjelp av page-feltet).

#### Eksempel på paginering

Hvis du har 50,000 elementer som skal synkroniseres, og ønsker å dele dette opp i sider med 12,500 elementer per side, vil metadataene se slik ut:

```json
    "totalSize": 50000,
    "page": 1,
    "pageSize": 12500,
    "totalPages": 4
```

Dette betyr at det totalt vil være 4 sider, hver med 12,500 elementer. Første side (side 1) overføres med denne informasjonen, etterfulgt av side 2, 3, og 4.

I tilfeller hvor det totale antallet elementer er 250,000, og du velger å bruke 50,000 elementer per side, vil pagineringsdataene se slik ut:

```json
    "totalSize": 250000,
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
I tillegg kan en klient be om validering av en ressurs, eller be om å lese data direkte fra kildesystemet (se [Live-lesing](integrate/provide/core2-adapter-api.md?id=live-lesing-read)).


| Klient forespørsel             | Hendelsestype til adapter (Operation type) |
|:-------------------------------|:-------------------------------------------|
| POST                           | CREATE                                     |
| PUT                            | UPDATE                                     |
| POST?validate=true             | VALIDATE                                   | 
| GET med `Prefer: respond-async` | READ                                       |

> DELETE-hendelser er under utvikling. Klienter kan foreløpig ikke slette ressurser, så adapteret får ikke DELETE-hendelser.

### Hvilke hendelser adapteret får

Adapteret får ventende hendelser for alle organisasjonene det har tilgang til, avgrenset av stien det henter fra. Det 
trenger verken tilgang til komponenten eller en kontrakt for å hente og svare på hendelser. Hent derfor fra en sti som 
bare dekker ressursene adapteret svarer på.

`eventCapabilities` i kontrakten for organisasjonen styrer hvilke operasjoner adapteret får:

- En ressurs som er listet, får nøyaktig de operasjonene som er listet.
- En ressurs som ikke er listet, får alle operasjoner unntatt `READ`. Det samme gjelder alle ressurser for en organisasjon uten kontrakt.
- `READ` må alltid listes eksplisitt. Lister du en ressurs med bare `READ`, får adapteret ikke lenger skrivehendelser for den.

### Hente hendelser

Adapteret henter innsendte hendelser ved å sende en GET-forespørsel til `/provider/event/[domene]`, `/provider/event/[domene]/[pakke]` 
eller `/provider/event/[domene]/[pakke]/[ressurs]`. Domenet må alltid være med. For eksempel kan `/provider/event/administrasjon/personal/fravar` 
brukes for å hente hendelser relatert til fravær. Parameteren `size` begrenser antallet hendelser i svaret. Uten den får adapteret alle.

Som svar returneres en liste over ventende hendelser, eldste først. En enkelt hendelse kan se slik ut:

```json
{
  "corrId": "244fec3c-5044-4d77-b908-2c3330e3110c",
  "orgId": "vestfoldfylke.no",
  "domainName": "administrasjon",
  "packageName": "personal",
  "resourceName": "fravar",
  "operationType": "CREATE",
  "created": 1733821906000,
  "timeToLive": 1733822806000,
  "value": "{<JSON for ressursen>}"
}
```

| Felter        | Beskrivelse                                                                                                  |
|:--------------|:-------------------------------------------------------------------------------------------------------------|
| corrId        | Hendelsens unike ID. Brukes i svaret.                                                                        |
| orgId         | Organisasjonen hendelsen gjelder. Henter adapteret flere pakker eller organisasjoner samtidig, kan dette variere. |
| operationType | `CREATE`, `UPDATE`, `VALIDATE` eller `READ`.                                                                 |
| created       | Når hendelsen ble opprettet, som Unix-tidsstempel i millisekunder.                                           |
| timeToLive    | Fristen for å svare, som Unix-tidsstempel i millisekunder. Fristen er 15 minutter etter `created`.           |
| value         | Ressursen klienten sendte, som en JSON-streng som adapteret må lese som JSON. Bare for skrivehendelser.      |
| filter        | Klientens OData-filter. Bare for `READ`.                                                                     |
| id            | Identifikatoren klienten ba om, som `{"idField": "systemid", "idValue": "123"}`. Bare for `READ`, og aldri sammen med `filter`. |

### Gi svar på hendelser

Når adapteret er ferdig med å behandle en hendelse, sender det en respons tilbake til FINT ved hjelp av en POST-forespørsel 
til `/provider/event`. Svaret må følge kontrakten definert i [ResponseFintEvent](https://github.com/FINTLabs/fint-core-infra-models/blob/main/src/main/java/no/fintlabs/adapter/models/event/ResponseFintEvent.java) 
og kan se slik ut:

```json
{
  "corrId": "244fec3c-5044-4d77-b908-2c3330e3110c",
  "orgId": "vestfoldfylke.no",
  "adapterId": "https://yourdomain.com/vestfoldfylke.no/administrasjon/personal",
  "value": {
    "identifier": "107849",
    "resource": { <JSON for ressursen> }
  },
  "operationType": "CREATE",
  "failed": false,
  "errorMessage": null,
  "rejected": false,
  "rejectReason": null,
  "conflicted": false,
  "conflictReason": null
}
```

- `corrId`, `orgId` og `operationType` må være med og ha verdiene fra hendelsen. Mangler ett av dem, svarer FINT `400 Bad Request`. 
  Er `operationType` en annen enn i hendelsen, er det hendelsens som gjelder.
- Tilhører hendelsen en annen av adapterets organisasjoner enn den i `orgId`, svarer FINT `403 Forbidden`.
- `value` må være med ved vellykket `CREATE` og `UPDATE`, og når `conflicted` er `true`. Den må ha en `identifier` og en 
  `resource` som passer informasjonsmodellen. Hvis ikke, svarer FINT `400 Bad Request`, og hendelsen står fortsatt åpen, 
  så adapteret kan svare på nytt innen fristen. I andre svar blir `value` ignorert.
- `value.resource` sendes som et JSON-objekt, ikke som en streng slik `value` i hendelsen er.
- `value.identifier` virker som `identifier` i dataoverføringen: FINT lagrer ressursen under den. Bruk samme verdi som ressursen har når den synkroniseres.
- Lister kontrakten ressursen uten operasjonen i hendelsen, svarer FINT `403 Forbidden`.
- `handledAt` settes av FINT.
- Felter med standardverdi kan utelates eller sendes som `null`.

Ved en vellykket `CREATE` eller `UPDATE` lagrer FINT ressursen i `value` med én gang, så den er tilgjengelig for klienter uten å 
vente på neste synkronisering. Ved en `UPDATE` med `conflicted: true` lagres også ressursen, siden den viser hva kildesystemet har. 
`VALIDATE` lagrer aldri noe.

Svaret avgjør hva klienten får når den sjekker statusen:

| Svar fra adapteret                    | Klienten får                                |
|:--------------------------------------|:--------------------------------------------|
| Vellykket `CREATE` eller `UPDATE`     | `201 Created` med ressursen                 |
| Vellykket `VALIDATE`                  | `200 OK`                                    |
| `rejected: true`                      | `400 Bad Request`                           |
| `conflicted: true`                    | `409 Conflict` med ressursen i `value`      |
| `failed: true`                        | `500 Internal Server Error`                 |
| Ikke svart innen fristen              | `500 Internal Server Error` ("Event expired.") |

Adapteret har 15 minutter på å svare. Et svar som kommer etter fristen, et svar på en hendelse som allerede er besvart, 
og et svar med ukjent `corrId` får `404 Not Found`, og ingenting blir lagret.

### Live-lesing (READ)

Med live-lesing kan en klient lese data direkte fra kildesystemet i stedet for fra FINTs cache. Klienten sender en vanlig 
GET-forespørsel med headeren `Prefer: respond-async`, og FINT lager en `READ`-hendelse til adapteret. For å støtte dette må adapteret:

1. **Liste ressursen med `READ` i `eventCapabilities`.** Svarer adapteret også på skrivehendelser for ressursen, må de operasjonene listes i tillegg, 
   for eksempel `["READ", "CREATE", "UPDATE", "VALIDATE"]`.
2. **Hente hendelser som vanlig.** En `READ`-hendelse har ingen `value`, men enten `filter` (klientens OData-filter, for eksempel 
   `systemId/identifikatorverdi eq '12345'`) eller `id` (`{"idField": "systemid", "idValue": "12345"}`).
3. **Svare med resultatet i `values`**, ikke i `value`. `values` er en liste på samme form som `resources` i dataoverføringen:

```json
{
  "corrId": "244fec3c-5044-4d77-b908-2c3330e3110c",
  "orgId": "vestfoldfylke.no",
  "operationType": "READ",
  "values": [
    {
      "identifier": "12345",
      "resource": { <JSON for ressursen> }
    }
  ]
}
```

- En tom `values`-liste betyr at ingenting ble funnet.
- Ved lesing på `id` kan `values` inneholde høyst én ressurs.
- Kan adapteret ikke oversette filteret, svarer det med `rejected: true` og `rejectReason`. Er kildesystemet nede, svarer det med `failed: true` og `errorMessage`.
- `conflicted` kan ikke brukes for `READ`.
- Svaret kan være på høyst 8 MB. Et større svar får `413 Payload Too Large`, og klienten får beskjed om å bruke et smalere filter.

Resultatet fra en live-lesing blir ikke lagret i FINTs cache.

## Feilmeldinger

| Status             | Når                                                                                                         |
|:-------------------|:------------------------------------------------------------------------------------------------------------|
| `400 Bad Request`  | Forespørselen kan ikke leses, kontrakten bryter en regel, eller svaret på en hendelse er ugyldig.            |
| `401 Unauthorized` | Tokenet mangler eller er ugyldig.                                                                           |
| `403 Forbidden`    | Adapteret har ikke tilgang. `detail` i svaret forklarer hvorfor, se under.                                  |
| `404 Not Found`    | Svar på en hendelse som er ukjent, allerede besvart eller utløpt.                                           |
| `413 Payload Too Large` | Svaret på en `READ`-hendelse er større enn 8 MB.                                                       |

`401` og `403` sendes som `application/problem+json`. Ved `403` sier `type` og `detail` hva som er galt, for eksempel:

```json
{
  "type": "https://fintlabs.no/problem/no-contract",
  "title": "Forbidden",
  "status": 403,
  "detail": "The adapter has no contract for the organization. Register a contract for it with POST /provider/register before syncing.",
  "instance": "/provider/utdanning/vurdering/elevfravar"
}
```

Vanlige årsaker er at tokenet tilhører en klient og ikke et adapter, at tokenet mangler scope `fint-adapter`, at adapteret 
mangler tilgang til komponenten eller organisasjonen i kundeportalen, at `username` i kontrakten ikke er brukernavnet i tokenet, 
at kontrakten mangler eller ikke dekker ressursen eller operasjonen, eller at et svar på en hendelse har feil `orgId`.

Er kontrakten ugyldig, svarer FINT `400 Bad Request` med en liste over feltene som er feil:

```json
{
  "title": "Bad Request",
  "status": 400,
  "detail": "The request body is not valid",
  "errors": [
    { "field": "capabilities", "message": "must not be null" }
  ]
}
```
