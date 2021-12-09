# Informasjonsmodellen 3.10.0

> Production
>
> Date: 09.12.2021
>
> Tag: v3.10.0
### Description

Utdanning has been the main focus of this release. Only smaller changes have been done on other domains.

### Content

#### Features
* Utdanning (replace `Vurdering`)
  
    * Added abstract class `Fagvurdering`.
    * Added abstract class `Ordensvurdering`.
    * Added class `Underveisfagvurdering`. 
    * Added class `Halvårsfagvurdering`.
    * Added class `Sluttfagvurdering`.
    * Added class `Underveisordensvurdering`.
    * Added class `Halvårsordensvurdering`.
    * Added class `Sluttordensvurdering`.

    * Added relation `sluttordensvurdering` on `Elevforhold`.
    * Added relation `underveisfagvurdering` on `Elevforhold`.
    * Added relation `halvårsfagvurdering` on `Elevforhold`.
    * Added relation `sluttfagvurdering` on `Elevforhold`.
    * Added relation `halvårsordensvurdering` on `Elevforhold`.
    * Added relation `underveisordensvurdering` on `Elevforhold`.
    

* Utdanning
    * Added class `Anmerkninger`.
    * Added class `Elevtilrettelegging`.
    * Added class `Fraværsoversikt`.
      
    * Added complex datatype `Fagvurdering`.
    * Added complex datatype `Fraværsprosent`.
    * Added complex datatype `Ordensvurdering`.
      
    * Added attribute `gjest` on `Elev`.
    * Added attribute `hybeladresse` on `Elev`.
    * Added relation `tilrettelegging` on `Fag`.
    * Added relation `elevfravær` on `Fag`.
    * Added relation `kommune` on `Person`.
    * Added relation `registrertav` on `Fravær`.
    * Added attribute `anmerkninger` on `Elevforhold`.
    * Added attribute `avbruddsdato` on `Elevforhold`.
    * Added relation `sidemål` on `Elevforhold`.
    * Added relation `kroppsøving` on `Elevforhold`.
    * Added relation `avbruddsårsak` on `Elevforhold`.
    * Added relation `elevfravær` on `Elevforhold`.
    * Added relation `tilrettelegging` on `Elevforhold`.
    
* Utdanning Kodeverk
    * Added class `Avbruddsårsak`.
    * Added class `Fagmerknad`.
    * Added class `Tilrettelegging`.
    
* Felles
    * Added relation `kommune` on `Person`.


#### Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
    * The class Vurdering is deprecated.
    * The attribute dokumentert on Fravær is deprecated.
    * The relation vurdering on Elevforhold is deprecated.
    * The relation eksamensgruppe on Fravær is deprecated.
    

#### Bugfixes

* Utdanning
    * Added description for attribute `persongruppemedlemskap` on `Elevforhold`.
    * Clarified description for reference `Grepreferanse`. 
* Felles
    * Clarified description for attribute `foreldreansvar` on `Person`.
    * Clarified description for attribute `foreldre` on `Person`.
    
  

### References

[Documentation 3.10.0](https://informasjonsmodell.felleskomponent.no/docs?v=v3.10.0)




