# Informasjonsmodellen 3.11.0

> Under development

### Description

### Content

#### Features

* Utdanning
          
  * Added class `Eksamensform`.
  * Added class `KarakterHistorie`.
  * Added class `Karakterstatus`.
  * Added class `Elevfravær`.
  * Added class `Fagmedlemskap`.
  
  * Added complex datatype `Fraværsregistrering`.
  
  * Added attribute `tospråkligFagopplæring` on `Elevforhold`.

  * Added relation `elevfravær` on `Elevforhold`.
  * Added relation `fagmedlemskap` on `Elevforhold`.
  * Added relation `fagmedlemskap` on `Fag`.
  * Added relation `fag` on `Fagmedlemskap`.
  * Added relation `elevforhold` on `Fagmedlemskap`.

#### Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
  * The relation fravær on Elevforhold is deprecated.

#### Bugfixes

### Schedule

NA

### References

[Documentation 3.11.0](https://informasjonsmodell.felleskomponent.no/docs?v=feature_3_11_0)



