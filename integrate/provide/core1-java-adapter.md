## Java SSE-adapter

### Introduksjon

Denne veiledningen vil lede deg gjennom prosessen med å sette opp og adapter for å kommunisere med Play-With-FINT-Adapter-tjenesten.

### Oppsett av miljøet

#### Klon malen

```bash
$ git clone https://github.com/FINTLabs/fint-sse-adapter-skeleton.git my-adapter
$ cd my-adapter
$ rm -rf .git
```

#### Åpne prosjektet i din favoritt-IDE

Dette er et Gradle-prosjekt, så sørg for å importere Gradle-avhengighetene. Du kan enten gjøre det i IDE-en eller i kommandolinjen:

```bash
$ ./gradlew --refresh-dependencies build
```

!> *Merk at dette prosjektet bruker `Lombok`, så du må aktivere `annotation processing` hvis du bruker `IntelliJ`. Det finnes også en `Lombok`-plugin for `IntelliJ`.*

### Få en OrgId

* Gå til <https://play-with-fint-adapter.felleskomponent.no/demo/organization/generateOrgId> for å generere en `OrgId`.

!> Denne `OrgId` er gyldig til midnatt samme dag.

* Erstatt `pwfa.no` med din `OrgId` i `application.yml`-filen:

```yaml
fint:
 adapter:
  organizations: OrgId
```

### Den første testen

* Sett et breakpoint ved starten av handleEvent-metoden i klassen `EventHandlerService`.


```java
                public void handleEvent(Event event) {
Breakpoint -->      if (event.isHealthCheck()) {
                    ...
                }
```

* Start adapteren i debug mode
* Åpne en nettleser og gå til <https://play-with-fint-adapter.felleskomponent.no/swagger-ui.html>
* Fra `Admin`-kontrolleren, konfigurer `/admin/health` ved å sette følgende overskrifter:
  * `x-org-id` bruk den genererte OrgId
  * `x-client` til `test`
* Send health-hendelsen fra `/admin/health`-endepunktet.
* Gå gjennom koden steg for steg for å se hva som skjer.
* Du kan også bruke `dog` og `owner`-kontrollerne for å se hvordan `FintResources` og `Relations` er bygget. Se <https://github.com/FINTmodels/fint-relation-model> for mer informasjon.

### Sikkerhet

`adapteren` bruker `OAuth2` som standard for å autentisere til `provider`-endepunktet. Denne veiledningen er satt opp med en veiledningsbruker. I produksjon vil man få en *ekte* bruker. Dette er `OAuth2`-konfigurasjonen:

```yaml
fint:
 oauth:
  enabled: true
  username: pwfatut
  password: pwfatut
  client-id: 2d0ed372-53fb-4d0a-9e7f-d546c5cf2d71
  client-secret: kgaiww60LjjNh0iyfv0KSjMZMbv04L6YZfYq5iYpu6IhIyxo6UFdslQMw_BBmZeVOuUCl75f3dE6FaDTVxgYjg
  access-token-uri: https://idp.felleskomponent.no/nidp/oauth/nam/token
  scope: fint-client
```

### Lenker

* <https://github.com/fintlabs/fint-sse-adapter-skeleton> - FINT SSE adapter mal
* <https://github.com/FINTlibs/fint-sse> - FINT SSE klientbibliotek
* <https://github.com/FINTmodels/fint-relation-model> - FINT Relationsmodell

### Bidra

Hvis du finner feil eller har forslag til forbedringer, vennligst gi oss tilbakemelding!