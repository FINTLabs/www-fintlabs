# Utvikling av en FINT 2-adapter

## Før du starter
Hvis du ønsker å observere den komplette integrasjonen i aksjon, kan du henvise til eksempeladapteret som er tilgjengelig på følgende [GitHub repository](https://github.com/FINTLabs/fint-core-adapter-skeleton)

## Utgiver-abonnent mønster
For å oppnå utgiver-abonnent mønsteret i FINT 2, vil vi bruke Reactive WebClient for å utføre asynkrone API-kall og Kafka som meldingsmegler for å håndtere hendelsesbasert kommunikasjon mellom komponenter og tjenester.

## Applikasjons konfigurasjon

Før du setter opp adapteret, må du først konfigurere applikasjonsen i application.yaml-filen. Dette lar deg sette nødvendige konfigurasjonsegenskaper for adapteret, som ID, brukernavn, passord og så videre.

Dette vil bli sendt til leverandøren ved registrering.

I det standard kodeeksempelet som er gitt, er en enkelt AdapterProperties konfigurert som følger:

eksempel på application.yaml hvis vi poster elevfravær til utdanning vurdering i alpha-miljøet.
```yaml
fint:
  adapter:
    id: https://example.com/org-no/utdanning/vurdering
    password: ***
    username: ***
    base-url: https://alpha.felleskomponent.no
    registration-id: fint
    org-id: fintlabs.no
    heartbeat-interval: 1
    page-size: 100
    capabilities:
      elevfravar:
        domain-name: utdanning
        package-name: vurdering
        resource-name: elevfravar
        fullSyncIntervalInDays: 7
        deltaSyncInterval: IMMEDIATE
```

* `id` Spesifiserer den unike identifikatoren for adapteret..
* `username/password` Spesifiser brukernavn og passord for FINT adapteret.
* `base-url` Spesifiser hvilket miljø dataen skal leveres til.
* `registration-id` Spesifiserer registrerings-IDen som skal brukes.
* `org-id` Spesifiserer organisasjons-IDen for adapteret.
* `heartbeat-interval` Spesifiserer intervall i minutter mellom adapterets hjerteslag. Den anbefalte verdien er mellom 1-3 minutter..
* `capabilities` Denne egenskapen spesifiserer listen over evner adapteret vil tilby. For hver evne, skal domene-navn, pakke-navn, ressurs-navn, fullSyncIntervalInDays og deltaSyncInterval spesifiseres.
* `page-size` Spesifiserer hvor mange ressurser en side kan inneholde. Standardverdien er 100, men dette kan ignoreres hvis du ikke planlegger å bruke vårt adapter-fellesbibliotek.
  The `deltaSyncInterval` bestemmer frekvensen som adapteret sender oppdateringer. Du kan velge blant følgende alternativer:

- **IMMEDIATE**: Dette alternativet indikerer at adapteret vil sende oppdateringer så snart de er tilgjengelige i applikasjonen.

- **LEGACY**: Dette alternativet indikerer at adapteret vil sende oppdateringer hver 15 minutter.

Det er essensielt å konfigurere disse egenskapene korrekt før du fortsetter med å sette opp adapteret.

## Avhengiheter

Det første steget i å sette opp et adapter for FINT 2 er å sikre at du har alle nødvendige avhengigheter. Det er bare to kritiske avhengigheter som kreves hvis du følger vår metode.

build.gradle
```groovy
dependencies {
    implementation 'no.fintlabs:fint-core-adapter-common:0.1.0'
    implementation 'no.fintlabs:fint-core-infra-models:1.1.1'
}
```

pom.xml
```xml
<dependencies>
    <dependency>
        <groupId>no.fintlabs</groupId>
        <artifactId>fint-core-adapter-common</artifactId>
        <version>0.1.0</version>
        
        <groupId>no.fintlabs</groupId>
        <artifactId>fint-core-infra-models</artifactId>
        <version>1.1.1</version>
    </dependency>
</dependencies>
```

Avhengig av hvilke ressurser adapteret vil håndtere, kan det være nødvendig med tilleggsavhengigheter. Sørg for at alle avhengigheter er lagt til i build.gradle-filen i prosjektet.

## Ressursarkiv

Etter å ha satt opp avhengigheter, er neste steg å opprette et arkiv som implementerer WriteableResourceRepository for ressursen. Dette arkivet vil håndtere kommunikasjonen mellom adapteret og det eksterne systemet.

Eksempel på et arkiv som inneholder ElevFravær-ressursen.
```java
@Repository
public class ElevfravarRepository implements WriteableResourceRepository<Elevfravar> {
    
}
```

## Ressursutgiver

Når ressursarkivet er satt opp, er neste steg å opprette en utgiver som utvider ResourcePublisher<ResourceName, ResourceRepository>. Ressursutgiveren er ansvarlig for å publisere ressursene til FINT 2 provideren. Overstyr de fulle og delta-synkroniseringsmetodene i utgiveren for å sikre at ressursene er synkronisert korrekt.

```java
@Service
public class ElevfravarPublisher extends ResourcePublisher<ElevfravarResource, ResourceRepository<ElevfravarResource>> {

    public ElevfravarPublisher(ElevfravarRepository repository, AdapterProperties adapterProperties) {
        super(repository, adapterProperties);
    }

    @Override
    @Scheduled(initialDelayString = "10000", fixedRateString = "10800000")
    public void doFullSync() {
        submit(SyncData.ofPostData(repository.getResources()));
    }

    @Override
    @Scheduled(initialDelayString = "120000", fixedRateString = "5400000")
    public void doDeltaSync() {
        submit(SyncData.ofPatchData(repository.getUpdatedResources()));
    }

    @Override
    protected AdapterCapability getCapability() {
        return adapterProperties.getCapabilityByResource("elevfravar");
    }
}
```

## Ressursabonnent

For å sette opp abonnenten, opprett en ny klasse som utvider ResourceSubscriber<ResourceName, CreatedPublisher> og over Webclient, AdapterProperties, CreatedPublisher, og ValidatorService. Denne klassen bør også overstyre getCapability-metoden og returnere AdapterProperties getCapabilities-metoden.

```java
@Service
public class ElevfravarSubscriber extends ResourceSubscriber<ElevfravarResource, ElevfravarPublisher> {

    protected ElevfravarSubscriber(WebClient webClient, AdapterProperties props, ElevfravarPublisher publisher, ValidatorService validatorService) {
        super(webClient, props, publisher, validatorService);
    }

    @Override
    protected AdapterCapability getCapability() {

        return adapterProperties.getCapabilities().get("elevfravar");
    }
}
```


Det siste trinnet er å overstyre den siste metoden, createSyncPageEntry of SyncPageEntry. Det er flere måter å opprette en SyncPageEntry på, her er tre eksempler med ulike bruksområder.

SyncPageEntry av Identifikator og Ressurs:
```java
    @Override
    protected SyncPageEntry<ElevfravarResource> createSyncPageEntry(ElevfravarResource resource) {
    String identificationValue = resource.getSystemId().getIdentifikatorverdi();
    return SyncPageEntry.of(identificationValue, resource);
    }
```

Hvis SystemId gis som selflink kan du utelate identifikatoren og bare gi ressursen som slik:
```java
@Override
    protected SyncPageEntry<ElevfravarResource> createSyncPageEntry(ElevfravarResource resource) {
    return SyncPageEntry.ofSystemId(resource);
    }
```

Til slutt kan du gi identifikatornavnet og ressursen:
```java
    @Override
    protected SyncPageEntry<ElevfravarResource> createSyncPageEntry(ElevfravarResource resource) {
    return SyncPageEntry.ofIdentifierName("identifierName", resource);
    }
```
