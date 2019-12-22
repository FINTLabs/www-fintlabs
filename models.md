# Informationmodels
## Models and Common API
*FINT Information models* are models used in the *Common API*. The models contains information resoures the county council use in their day to day tasks. *FINT* aims to develop this model to contain vital information in all the areas the county council operates in. This means that every new version will contain more information and an new areas.

>Go to [Information Model at the Center](api?id=information-model-at-the-center) for more details.

### Versioning

FINT is using [semantic versioning](http://semver.org/) for its models:

- `MAJOR` version have **backwards incompatible changes**
- `MINOR` *(feature release)* versions add functionality in a **backwards-compatible manner**, and
- `PATCH` *(bug fixes)* versions add **backwards-compatible bug fixes**. 

Additional labels for pre-release and build metadata are available as extensions to the `MAJOR.MINOR.PATCH` format. 

- `MINOR` versions are generally even numbers: 0, 2, 4, ...
- `PATCH` numbers are released in increments of 10: 0, 10, 20, ...

>The version relation between the *FINT Information model* and the *technical implementations* is that they start with the same `MAJOR.MINOR.PATCH` versions.  Additional releases of *technical implementations* based on the **same** *FINT Information model* will increment the `PATCH` number by `1`. 

## FINT information models
The models are designed and documented in `Enterprise Architect (EA)`. You can find the `EA` project at [https://github.com/FINTprosjektet/fint-informasjonsmodell](https://github.com/FINTprosjektet/fint-informasjonsmodell). 

### Documentation portal
For a more userfriendly view of the models we developet a frontend to the `XMI 2.1` export from `EA`. You can find the documentation portal at [https://informasjonsmodell.felleskomponent.no](https://informasjonsmodell.felleskomponent.no).

The project for the frontend is found [here](https://github.com/FINTprosjektet/fint-informasjonsmodell-documentation).

### Contribute
If you find bugs or have suggestions for improvement please feel free to submit an [issue](https://github.com/FINTprosjektet/fint-informasjonsmodell/issues).

### Latest versions

| **Component**     | **GitHub Release**                                                                                                                                                     |                                                                                                                                                                            |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Information Model | [![GitHub release](https://img.shields.io/github/release/FINTprosjektet/fint-informasjonsmodell.svg)](https://github.com/FINTprosjektet/fint-informasjonsmodell)       | [![Documentation](https://img.shields.io/badge/read-documentation-brightgreen.svg)](https://informasjonsmodell.felleskomponent.no/)                                        |
| **Java**          | **GitHub Release**                                                                                                                                                     | **Package Version**                                                                                                                                                        |
| Event Model       | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-event-model.svg)](https://github.com/FINTmodels/fint-event-model)                             | [![Bintray](https://img.shields.io/bintray/v/fint/maven/fint-event-model.svg)](https://bintray.com/fint/maven/fint-event-model/_latestVersion)                             |
| Relation Model    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-relation-model.svg)](https://github.com/FINTmodels/fint-relation-model)                       | [![Bintray](https://img.shields.io/bintray/v/fint/maven/fint-relation-model.svg)](https://bintray.com/fint/maven/fint-relation-model/_latestVersion)                       |
| Common            | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-felles-model-java.svg)](https://github.com/FINTmodels/fint-felles-model-java)                 | [![Bintray](https://img.shields.io/bintray/v/fint/maven/fint-felles-model-java.svg)](https://bintray.com/fint/maven/fint-felles-model-java/_latestVersion)                 |
| Administration    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-administrasjon-model-java.svg)](https://github.com/FINTmodels/fint-administrasjon-model-java) | [![Bintray](https://img.shields.io/bintray/v/fint/maven/fint-administrasjon-model-java.svg)](https://bintray.com/fint/maven/fint-administrasjon-model-java/_latestVersion) |
| Education         | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-utdanning-model-java.svg)](https://github.com/FINTmodels/fint-utdanning-model-java)           | [![Bintray](https://img.shields.io/bintray/v/fint/maven/fint-utdanning-model-java.svg)](https://bintray.com/fint/maven/fint-utdanning-model-java/_latestVersion)           |
| Vigo Code Lists   | [![GitHub release](https://img.shields.io/github/release/FINTmodels/fint-vigokv-model.svg)](https://github.com/FINTmodels/fint-vigokv-model)                           | [![Bintray](https://img.shields.io/bintray/v/fint/maven/fint-vigokv-model.svg)](https://bintray.com/fint/maven/fint-vigokv-model/_latestVersion)                           |
| **.NET**          | **GitHub Release**                                                                                                                                                     | **Package Version**                                                                                                                                                        |
| Event Model       | [![GitHub release](https://img.shields.io/github/release/FINTmodels/Fint.Event.Model.svg)](https://github.com/FINTmodels/Fint.Event.Model)                             | [![Bintray](https://img.shields.io/bintray/v/fint/nuget/FINT.Event.Model.svg)](https://bintray.com/fint/nuget/FINT.Event.Model/_latestVersion)                             |
| Relation Model    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/Fint.Relation.Model.svg)](https://github.com/FINTmodels/Fint.Relation.Model)                       | [![Bintray](https://img.shields.io/bintray/v/fint/nuget/FINT.Relation.Model.svg)](https://bintray.com/fint/nuget/FINT.Relation.Model/_latestVersion)                       |
| Common            | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Felles.svg)](https://github.com/FINTmodels/FINT.Model.Felles)                           | [![Bintray](https://img.shields.io/bintray/v/fint/nuget/FINT.Model.Felles.svg)](https://bintray.com/fint/nuget/FINT.Model.Felles/_latestVersion)                           |
| Administration    | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Administrasjon.svg)](https://github.com/FINTmodels/FINT.Model.Administrasjon)           | [![Bintray](https://img.shields.io/bintray/v/fint/nuget/FINT.Model.Administrasjon.svg)](https://bintray.com/fint/nuget/FINT.Model.Administrasjon/_latestVersion)           |
| Education         | [![GitHub release](https://img.shields.io/github/release/FINTmodels/FINT.Model.Utdanning.svg)](https://github.com/FINTmodels/FINT.Model.Utdanning)                     | [![Bintray](https://img.shields.io/bintray/v/fint/nuget/FINT.Model.Utdanning.svg)](https://bintray.com/fint/nuget/FINT.Model.Utdanning/_latestVersion)                                    |
