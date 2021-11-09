# Informasjonsmodellen 3.9.0

> Production
> 
> Date: 10.06.2021
> 
> Tag: v3.9.0
### Description

Utdanning has been the main focus of this release. Only smaller changes have been done on other domains.

### Content

#### Features
* Utdanning

    * Added class `Persongruppe`.
    * Added class `Persongruppemedlemskap`.
    * Added attribute `eksamensdato` on `Eksamensgruppe`.

* Arkiv
    * Added complex datatype `Avskriving`.
    

#### Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
    * The relation `basisgruppe` on `Elevforhold` is deprecated.
    * The relation `undervisningsgruppe` on `Elevforhold` is deprecated.
    * The relation `kontaktlærergruppe` on `Elevforhold` is deprecated.
    * The relation `eksamensgruppe` on `Elevforhold` is deprecated.
    * The relation `programområde` on `Elevforhold` is deprecated.


#### Bugfixes

* Arkiv
    * Changed name of relation `fartoyNavn` on `TilskuddFartøy` from `fartoyNavn` to `fartøyNavn`.

### Schedule

In production

### References

[Documentation 3.9.0](https://informasjonsmodell.felleskomponent.no/?v=v3.9.0)




