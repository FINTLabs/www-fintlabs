# Informasjonsmodellen 3.2.0

> Production
>
> Date: 03.05.2019
>
> Tag: v3.2.0

#### Features

* Felles
    * Added relation `foreldreansvar`..`foreldre` from `Person` to `Person`.

* Administrasjon
    * Added relation from `Fraværstype` to `Lønnsart`
    * Added relation from `Lønnsart` to `Art`
    * Added relation from `Personalressurs` to `Art`

* Utdanning
    * Relation from `Skoleressurs` to `Skole` is now `0..*` for teachers associated with several
      schools.
    * Added relation from `Elevforhold` to `Programområde`.
    * Vigo Kodeverk has been moved to a separate repository.  No changes in naming or packaging otherwise.
    * On `Elev`, `kontaktinformasjon` is now marked as `writable` to account for updates via the API.

#### Deprecated

*Note:* Deprecated classes, attributes and relations might be removed in the next major release.

* Felles
    * The relation `person` on `Kontaktperson` has been deprecated.  `Kontaktperson` now contains
      `navn` and `kontaktinformasjon` that should be used instead.
    * The attribute `foreldreansvar` on `Kontaktperson` has been deprecated.  Parents and children
      should be represented using the new relation `foreldre` and `foreldreansvar` from `Person` to
      `Person`.

#### Bugfixes

NA

### References

[Documentation 3.2.0](https://informasjonsmodell.felleskomponent.no/?v=v3.2.0)