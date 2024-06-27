
# Informasjonsmodellen

Informasjonsmodellen kan sees i sin helhet på:
[https://informasjonsmodell.felleskomponent.no](https://informasjonsmodell.felleskomponent.no) . 
Du vil alltid komme på siste versjon, men kan velge hvilken versjon du vil se på. 

På denne siden kan du se pågående arbeider og høringsutkast: [https://fintlabs.atlassian.net/wiki/spaces/informasjonsmodellen/overview](https://fintlabs.atlassian.net/wiki/spaces/informasjonsmodellen/overview).


Versjonshistorikken er tilgjengelig på GitHub: [https://github.com/FINTLabs/fint-informasjonsmodell/releases](https://github.com/FINTLabs/fint-informasjonsmodell/releases)

## Versjonering

FINT bruker [semantisk versjonering](http://semver.org/) på Informasjonsmodellen:

* `MAJOR` versjon har **bakover inkompatible endringer**
* `MINOR` *(Funksjonsutgivelse)* versjoner legger til funksjonalitet på en **bakoverkompatibel måte**, og
* `PATCH` *(feilretting)* versjoner legger til **bakoverkompatible feilrettinger**.


Ytterligere etiketter for pre-release og build-metadata er tilgjengelige som utvidelser til `MAJOR.MINOR.PATCH` formatet.

* `PATCH` tall utgis i trinn på 10: 0, 10, 20, ...

>Versjonsforholdet mellom FINT Informationmodellen og de tekniske implementeringene er at de starter med de samme `MAJOR.MINOR.PATCH`-versjonene.
>Ytterligere utgivelser av tekniske implementeringer basert på den **samme** FINT Informasjonsmodellen vil øke `PATCH`-nummeret med `1`.

## Utvikling

Informasjonsmodellen er designet og dokumentert i `Enterprise Architect (EA)`. Du finner `EA`-prosjektet på <https://github.com/fintlabs/fint-informasjonsmodell>

## Presentasjon

For en mer brukervennlig visning av Informasjonsmodellen utviklet vi en frontend til `XMI 2.1`-eksporten fra `EA`.
For mer informasjon om FINT Informasjonsmodellen og en beskrivelse av alle klassene, attributtene og relasjonene, gå til <https://informasjonsmodell.felleskomponent.no>.

Prosjektet for frontend finner du her <https://github.com/fintlabs/fint-informasjonsmodell-documentation>.

Den tekniske implementasjonen av Informasjonsmodellen finner du på <https://github.com/FINTmodels>.

### Bidra

Hvis du finner feil eller har forslag til forbedringer, send gjerne inn et henvendelse på <https://github.com/fintlabs/fint-informasjonsmodell/issues>.

### Siste versjoner

| **Komponent**      | **GitHub Utgivelse**                                                                                                                                                   |                                                                                                                                                                                         |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Informasjonsmodell | [![GitHub release](https://img.shields.io/github/release/fintlabs/fint-informasjonsmodell.svg)](https://github.com/fintlabs/fint-informasjonsmodell)                   | [![Documentation](https://img.shields.io/badge/read-documentation-brightgreen.svg)](https://informasjonsmodell.felleskomponent.no/)                                                     |
| **Java**           | **GitHub Release**                                                                                                                                                     | **Package Version**                                                                                                                                                                     |
| Hendelsesmodel     | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-event-model.svg)](https://github.com/FINTmodels/fint-event-model)                             | [![repo.fintlabs.no](https://img.shields.io/badge/fint--event--model-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-event-model/latest)                              |
| Relasjonsmodel     | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-relation-model.svg)](https://github.com/FINTmodels/fint-relation-model)                       | [![repo.fintlabs.no](https://img.shields.io/badge/fint--relation--model-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-relation-model/latest)                        |
| Felles             | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-felles-model-java.svg)](https://github.com/FINTmodels/fint-felles-model-java)                 | [![repo.fintlabs.no](https://img.shields.io/badge/fint--felles--model--java-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-felles-model-java/latest)                 |
| Administrasjon     | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-administrasjon-model-java.svg)](https://github.com/FINTmodels/fint-administrasjon-model-java) | [![repo.fintlabs.no](https://img.shields.io/badge/fint--administrasjon--model--java-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-administrasjon-model-java/latest) |
| Utdanning          | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-utdanning-model-java.svg)](https://github.com/FINTmodels/fint-utdanning-model-java)           | [![repo.fintlabs.no](https://img.shields.io/badge/fint--utdanning--model--java-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-utdanning-model-java/latest)           |
| Vigo Kodelister    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-vigokv-model.svg)](https://github.com/FINTmodels/fint-vigokv-model)                           | [![repo.fintlabs.no](https://img.shields.io/badge/fint--vigokv--model-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-vigokv-model/latest  )                          |
| **.NET**           | **GitHub Release**                                                                                                                                                     | **Package Version**                                                                                                                                                                     |
| Hendelsesmodel     | [![GitHub release](https://img.shields.io/github/release/FINTmodels/Fint.Event.Model.svg)](https://github.com/FINTmodels/Fint.Event.Model)                             | [![NuGet](https://img.shields.io/nuget/v/FINT.Event.Model)](https://www.nuget.org/packages/FINT.Event.Model/latest)                                                                     |
| Relasjonsmodel     | [![GitHub release](https://img.shields.io/github/release/FINTmodels/Fint.Relation.Model.svg)](https://github.com/FINTmodels/Fint.Relation.Model)                       | [![NuGet](https://img.shields.io/nuget/v/FINT.Relation.Model)](https://www.nuget.org/packages/FINT.Relation.Model/latest)                                                               |
| Felles             | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Felles.svg)](https://github.com/FINTmodels/FINT.Model.Felles)                           | [![NuGet](https://img.shields.io/nuget/v/FINT.Model.Felles)](https://www.nuget.org/packages/FINT.Model.Felles/latest)                                                                   |
| Administrasjon     | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Administrasjon.svg)](https://github.com/FINTmodels/FINT.Model.Administrasjon)           | [![NuGet](https://img.shields.io/nuget/v/FINT.Model.Administrasjon)](https://www.nuget.org/packages/FINT.Model.Administrasjon/latest)                                                   |
| Utdanning          | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Utdanning.svg)](https://github.com/FINTmodels/FINT.Model.Utdanning)                     | [![NuGet](https://img.shields.io/nuget/v/FINT.Model.Utdanning)](https://www.nuget.org/packages/FINT.Model.Utdanning/latest)                                                             |
