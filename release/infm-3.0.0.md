# Informasjonsmodellen 3.0.0

> Production
>
> Date: 07.06.2018
>
> Tag: v3.0.0

#### Breaking changes

* Administrasjon
    * `Fastlønn` and `Variabellønn` have been revised.
        * Instead of collections containing multiple transactions they have been remodeled to represent individual transactions.
        * `Beskjeftigelse` is incorporated into `Fastlønn`
        * `Variabelttillegg` is incorporated into `Variabellønn`
        * The class `Fasttillegg` has been introduced to represent the `fasttillegg` attribute previously found on `Fastlønn`
* Utdanning
    * `Vurdering` has been moved to the package `Vurdering` and is now `hovedklasse` with `systemId`.
    * `Elev` now has an optional `elevnummer` and mandatory `systemId`.

#### Features

* Administrasjon
    * `systemId` is now optional on `Fastlønn`, `Variabellønn` and `Fravær`, as these classes are used to create new information in the back end system.
* Ressurser
    * Added `Identitet` and `Rettighet` under `Tilgangsstyring` for identity and access management.

#### Deprecated

NA

#### Bugfixes

* Administrasjon
    * Fixed multiplicity for `ansiennitet`.  The field is now optional.
    * Fixed documentation for `Fravær`.

### References

[Documentation 3.0.0](https://informasjonsmodell.felleskomponent.no/?v=v3.0.0)