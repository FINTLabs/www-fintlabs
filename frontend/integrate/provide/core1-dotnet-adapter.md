## .NET SSE-adapter

Denne veiledningen vil lede deg gjennom prosessen med å sette opp og adapter for å kommunisere med Play-With-FINT-Adapter-tjenesten.

### Oppsett av miljøet

#### Klon malen

```bash
$ git clone https://github.com/fintlabs/Fint.Sse.Adapter.Skeleton.git my-adapter
$ cd my-adapter
$ rm -rf .git
```

#### Åpne prosjektet i din favoritt-IDE

Dette er et `netcoreapp2.0`\\`netstandard2.0`-prosjekt. Du må importere avhengighetene. Du kan enten gjøre det i IDE-en eller i kommandolinjen. Dette eksempelet bruker `dotnet` CLI:

```bash
$ dotnet restore
```

Dette `repo` består av tre prosjekter:

- **FINT.Sse.Adapter** - Dette er hovedkoden for `adapteret`.
- **FINT.Sse.Adapter.Console** - Dette er en wrapper rundt `FINT.Sse.Adapter` for å få den til å kjøre ved bruk av `netcoreapp2.0`. Du kan lage en annen wrapper for din favorittversjon/-rammeverk.
- **FINT.Sse.Adapter.Tests** - Dette er prosjektet for `enhetstester`.

### Få en OrgId

* Gå til <https://play-with-fint-adapter.felleskomponent.no/demo/organization/generateOrgId> for å generere en `OrgId`.

!> Denne `OrgId` er gyldig til midnatt samme dag.

* Erstatt `pwfa.no` med din `OrgId` i `appsettings.json`-filen i `Fint.Sse.Adapter.Console`-prosjektet:

```json
{
  "Logging": {
    "IncludeScopes": false,
    "LogLevel": {
      "Default": "Debug",
      "System": "Information",
      "Microsoft": "Information"
    }
  },
  "Configuration": {
    "ConsoleTitle": "FINT Console Boilerplate",
    "SseEndpoint": "https://play-with-fint-adapter.felleskomponent.no/provider/sse",
    "StatusEndpoint": "https://play-with-fint-adapter.felleskomponent.no/provider/status",
    "ResponseEndpoint": "https://play-with-fint-adapter.felleskomponent.no/provider/response",
    "Organizations": "pwfa.no", <-- HERE
    "LogLocation": "logs"
  }
}
```

```csharp
                public void HandleEvent(Event<object> serverSideEvent)
                {
Breakpoint -->      if (serverSideEvent.IsHealthCheck())
                    {
                    ...
                }
```

* Start adapteren i debug-mode.
* Åpne en nettleser og gå til <https://play-with-fint-adapter.felleskomponent.no/swagger-ui.html>
* Fra `Admin`-kontrolleren, konfigurer `/admin/health` ved å sette følgende overskrifter:
  * `x-org-id` bruk den genererte OrgId
  * `x-client` til `test`
* Send health-hendelsen fra `/admin/health`-endepunktet.
* Gå gjennom koden steg for steg for å se hva som skjer.
* Du kan også bruke `dog` og `owner`-kontrollerne for å se hvordan `FintResources` og `Relations` er bygget. Se <https://github.com/FINTmodels/Fint.Relation.Model> for mer informasjon.

### Sikkerhet

`adapteren` bruker `OAuth2` som standard for å autentisere til `provider`-endepunktet. Denne veiledningen er satt opp med en veiledningsbruker. I produksjon vil man få en *ekte* bruker. Dette er `OAuth2`-konfigurasjonen:

```json
"OAuthTokenService": {
    "AccessTokenUri": "https://idp.felleskomponent.no/nidp/oauth/nam/token",
    "ClientId": "2d0ed372-53fb-4d0a-9e7f-d546c5cf2d71",
    "ClientSecret": "kgaiww60LjjNh0iyfv0KSjMZMbv04L6YZfYq5iYpu6IhIyxo6UFdslQMw_BBmZeVOuUCl75f3dE6FaDTVxgYjg",
    "Username": "pwfatut",
    "Password": "pwfatut",
    "Scope": "fint-client",
    "OAuthEnabled": "true"
}
```

### Lenker

* <https://github.com/fintlabs/Fint.Sse.Adapter.Skeleton> - FINT SSE adapter skjelett
* <https://github.com/FINTlibs/Fint.Sse> - FINT SSE klientbibliotek
* <https://github.com/FINTmodels/Fint.Relation.Model> - FINT Relationsmodell

### Bidra

Hvis du finner feil eller har forslag til forbedringer, vennligst gi oss tilbakemelding!
