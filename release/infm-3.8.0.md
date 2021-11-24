# Informasjonsmodellen 3.8.0

> Production
>
> Date: 24.03.2021
>
> Tag: v3.8.0

#### Features
* Administrasjon

    * Added relation `aktivitet`,`anlegg`,`ansvar`,`art`,`diverse`,`funksjon`,`kontrakt`,`løpenummer`,`objekt`,`prosjekt` and `ramme`,`organisasjonselement` to `Fullmakt`.
    * Added relation `aktivitet`,`anlegg`,`diverse`,`kontrakt`,`løpenummer`,`object`,`prosjekt` and `ramme` to `Arbeidsforhold`.

* Arkiv
    * Added class `Format` as `Kodeverk`.
    * Added relation `format` to `Dokumentobject`.


#### Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Administrasjon
    * The relation `myndighet` on `Fullmakt` is deprecated.
    * The relation `fullmakt` on `Kontodimensjon` is deprecated.
* Arkiv
    * The attribute `format` on `Dokumentobjekt` is deprecated.
    
  
#### Bugfixes

* Arkiv
    * Changed multiplicity for attribute `klasse` on `Registrering`, from 1 to 0..1.
* Utdanning
    * Changed multiplicity for relation `utdanningsprogram` on `Programområde`, from 1 to 1..*.
  

### References

[Documentation 3.8.0](https://informasjonsmodell.felleskomponent.no/?v=v3.8.0)

