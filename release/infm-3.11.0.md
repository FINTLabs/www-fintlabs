# Informasjonsmodellen 3.11.0

> Under development

### Description

### Content

#### Features

* Utdanning

  * Added class `Eksamensform`.
  * Added class `Karakterhistorie`.
  * Added class `Karakterstatus`.
  * Added class `Elevfravær`.
  * Added class `Faggruppemedlemskap`.
  * Added class `Faggruppe`.
  * Added class `Sensor`.
  
  * Added complex datatype `Fraværsregistrering`.
  
  * Added attribute `tospråkligFagopplæring` on `Elevforhold`.
  * Changed attribute `karakter ` on `Fagvurdering`.

  * Added relation `fraværsregistreringer` on `Elevforhold`.
  * Added relation `faggruppemedlemskap` on `Elevforhold`.
  * Added relation `skoleår` on `Elevforhold`.
  * Added relation `faggruppe` on `Fag`.
  * Added relation `nus` on `Eksamensgruppemedlemskap`.
  * Added relation `sensor` on `Eksamensgruppe`.
  * Added relation `eksamensform` on `Eksamensgruppe`.
  * Added relation `sensor` on `Skoleressurs`.
  * Added relation `karakterhistorie` on `Sluttfagvurdering`.

  
* Administrasjon
  * Added class `Formål`.

  * Added relation `formål` on `Kontostreng`.
  * Added relation `formål` on `Arbeidsforhold`.
  * Added relation `formål` on `Fullmakt`.

* Arkiv
  * Added class `Saksmappetype`

  * Added attribute `skjerming` on `Korrespondansepart`.

  * Added relation `saksmappetype` on `Saksmappe`.

#### Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
  * The relation fravær on Elevforhold is deprecated.

#### Bugfixes

* Administrasjon
  * The deprecated relation myndighet in Fullmakt changed multiplisity from 1..* to 0..*

### Schedule

NA

### References

[Documentation 3.11.0](https://informasjonsmodell.felleskomponent.no/docs?v=feature_3_11_0)



