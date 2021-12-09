# Informasjonsmodellen 3.1.0

> Production
>
> Date: 24.09.2018
>
> Tag: v3.1.0

#### Features

* Utdanning
    * Relations are expressed between concrete classes instead of abstract classes.  This makes relations more explicit,
      and simplifies the way these relations are consumed.
    * Added relation from `Skole` to groups.
    * Added relation between `Fag` and `Programområde`.
    * Added bidirectional relation between `Elevforhold` and `Vurdering` and `Fravær`.
        * A new attribute `endelig` on `Vurdering` indicates final assessments.
    * Relations from `Vurdering` and `Fravær` to `Undervisningsgruppe` and `Eksamensgruppe` are used to indicate
      absence and assessments in context of these groups.

#### Deprecated

*Note:* Deprecated classes, attributes and relations will be removed in the next major release.

* Utdanning
    * The class `Medlemskap` has been deprecated.  
      Group membership is instead represented as relations between `Elevforhold` or `Undervisningsforhold` and the
      various groups.

#### Bugfixes

* Utdanning
    * Fixed multiplicity on relation to `Elevkategori` from `Elevforhold`.
    * Documentation updates.

### References

[Documentation 3.1.0](https://informasjonsmodell.felleskomponent.no/?v=v3.1.0)