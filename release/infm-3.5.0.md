# Informasjonsmodellen 3.5.0

> Production
>
> Date: 04.05.2020
>
> Tag: v3.5.0

#### Features

* Administrasjon 
    * Added arbeidsforholdsperiode to Arbeidsforhold

* Utdanning
    * Added abstract class `Gruppemedlemskap` as well as specific classes for `Undervisningsgruppemedlemskap`, `Basisgruppemedlemskap`, `Kontaktlærergruppemedlemskap`, `Eksamensgruppemedlemskap`, and `Programområdemedlemskap`. These classes represent memberships for `Elevforhold` with added information on `gyldighetsperiode`.
    * Added `Skoleår` and `Termin`. These are code lists for school years and school terms. Added relations to these from all relevant group types.
    * Added `gyldighetsperiode` and `hovedskole` to `Elevforhold`.

#### Deprecated

NA

#### Bugfixes

* Felles
    * Fixed documentation for `Kjønn` and `Periode`.
* Administrasjon
    * Fixed multiplicity on `overordnet` reference for `Organisasjonselement`.
* Utdanning
    * Fixed documentation for `Gruppe`, `Grepreferanse` and `Vigoreferanse`.

### References

[Documentation 3.5.0](https://informasjonsmodell.felleskomponent.no/?v=v3.5.0)

