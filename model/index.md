
# Informasjonsmodellen

Informasjonsmodellen kan sees i sin helhet på: [https://informasjonsmodell.felleskomponent.no](https://informasjonsmodell.felleskomponent.no) Du vil alltid komme på siste versjon, men kan velge hvilken versjon du vil se på. 

På denne siden kan du se pågående arbeider og høringsutkast: [https://fintlabs.atlassian.net/wiki/spaces/informasjonsmodellen/overview](https://fintlabs.atlassian.net/wiki/spaces/informasjonsmodellen/overview).


Versjonshistorikken er tilgjengelig på GitHub: [https://github.com/FINTLabs/fint-informasjonsmodell/releases](https://github.com/FINTLabs/fint-informasjonsmodell/releases)

# The Information Model

## Versioning

FINT is using [semantic versioning](http://semver.org/) for the information model:

* `MAJOR` version have **backwards incompatible changes**
* `MINOR` *(feature release)* versions add functionality in a **backwards-compatible manner**, and
* `PATCH` *(bug fixes)* versions add **backwards-compatible bug fixes**.

Additional labels for pre-release and build metadata are available as extensions to the `MAJOR.MINOR.PATCH` format.

* `PATCH` numbers are released in increments of 10: 0, 10, 20, ...

>The version relation between the FINT Information model, and the technical implementations is that they start with the same `MAJOR.MINOR.PATCH` versions.  Additional releases of technical implementations based on the **same** FINT Information model will increment the `PATCH` number by `1`.

## Development

The models are designed and documented in `Enterprise Architect (EA)`. You can find the `EA` project at <https://github.com/fintlabs/fint-informasjonsmodell>.

## Presentation

For a more user-friendly view of the models we developed a frontend to the `XMI 2.1` export from `EA`. For more information about the FINT information model and a description of all the classes, attributes and relations go to <https://informasjonsmodell.felleskomponent.no>.

The project for the frontend is found here <https://github.com/fintlabs/fint-informasjonsmodell-documentation>.

The technical implementations of the models can be found at <https://github.com/FINTmodels>.

### Contribute

If you find bugs or have suggestions for improvement please feel free to submit an issue at <https://github.com/fintlabs/fint-informasjonsmodell/issues>.

### Latest versions

| **Component**     | **GitHub Release**                                                                                                                                                     |                                                                                                                                                                            |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Information Model | [![GitHub release](https://img.shields.io/github/release/fintlabs/fint-informasjonsmodell.svg)](https://github.com/fintlabs/fint-informasjonsmodell)                   | [![Documentation](https://img.shields.io/badge/read-documentation-brightgreen.svg)](https://informasjonsmodell.felleskomponent.no/)                                        |
| **Java**          | **GitHub Release**                                                                                                                                                     | **Package Version**                                                                                                                                                        |
| Event Model       | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-event-model.svg)](https://github.com/FINTmodels/fint-event-model)                             | [![repo.fintlabs.no](https://img.shields.io/badge/fint--event--model-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-event-model/latest)                             |
| Relation Model    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-relation-model.svg)](https://github.com/FINTmodels/fint-relation-model)                       | [![repo.fintlabs.no](https://img.shields.io/badge/fint--relation--model-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-relation-model/latest)                       |
| Common            | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-felles-model-java.svg)](https://github.com/FINTmodels/fint-felles-model-java)                 | [![repo.fintlabs.no](https://img.shields.io/badge/fint--felles--model--java-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-felles-model-java/latest)                 |
| Administration    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-administrasjon-model-java.svg)](https://github.com/FINTmodels/fint-administrasjon-model-java) | [![repo.fintlabs.no](https://img.shields.io/badge/fint--administrasjon--model--java-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-administrasjon-model-java/latest) |
| Education         | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-utdanning-model-java.svg)](https://github.com/FINTmodels/fint-utdanning-model-java)           | [![repo.fintlabs.no](https://img.shields.io/badge/fint--utdanning--model--java-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-utdanning-model-java/latest)           |
| Vigo Code Lists   | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-vigokv-model.svg)](https://github.com/FINTmodels/fint-vigokv-model)                           | [![repo.fintlabs.no](https://img.shields.io/badge/fint--vigokv--model-latest-green.svg)](https://repo.fintlabs.no/releases/no/fint/fint-vigokv-model/latest  )                           |
| **.NET**          | **GitHub Release**                                                                                                                                                     | **Package Version**                                                                                                                                                        |
| Event Model       | [![GitHub release](https://img.shields.io/github/release/FINTmodels/Fint.Event.Model.svg)](https://github.com/FINTmodels/Fint.Event.Model)                             | [![NuGet](https://img.shields.io/nuget/v/FINT.Event.Model)](https://www.nuget.org/packages/FINT.Event.Model/latest)                             |
| Relation Model    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/Fint.Relation.Model.svg)](https://github.com/FINTmodels/Fint.Relation.Model)                       | [![NuGet](https://img.shields.io/nuget/v/FINT.Relation.Model)](https://www.nuget.org/packages/FINT.Relation.Model/latest)                       |
| Common            | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Felles.svg)](https://github.com/FINTmodels/FINT.Model.Felles)                           | [![NuGet](https://img.shields.io/nuget/v/FINT.Model.Felles)](https://www.nuget.org/packages/FINT.Model.Felles/latest)                           |
| Administration    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Administrasjon.svg)](https://github.com/FINTmodels/FINT.Model.Administrasjon)           | [![NuGet](https://img.shields.io/nuget/v/FINT.Model.Administrasjon)](https://www.nuget.org/packages/FINT.Model.Administrasjon/latest)           |
| Education         | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Utdanning.svg)](https://github.com/FINTmodels/FINT.Model.Utdanning)                     | [![NuGet](https://img.shields.io/nuget/v/FINT.Model.Utdanning)](https://www.nuget.org/packages/FINT.Model.Utdanning/latest)                     |
