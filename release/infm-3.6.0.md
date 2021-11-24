# Informasjonsmodellen 3.6.0

> Production
>
> Date: 08.10.2020
>
> Tag: v3.6.0

#### Features

* Arkiv

    * Archive represents a new domain in the information model. The domain includes Noark, Kulturminnevern, Personal and Kodeverk. Needs that are covered are joint integration with archive systems in accordance with the Noark 5 version 5.0 standard, and specific case types of personnel files and grants for cultural heritage.

* Økonomi

    * Economy represents a new domain in the information model. The domain includes Faktura and Kodeverk. Needs that are covered are joint integration with economy systems, limited to invoices and product registers, and especially invoicing of pupils in upper secondary education.

* Personvern
    * Privacy represents a new domain in the information model. The domain includes Samtykke and Kodeverk. Needs that are covered are collection and exchange of consents, at the individual level, which expresses which personal data can be processed by which services and for what purpose.

* Utdanning
    * Added relation from Skoleressurs to Person. The relation should be a link to a person object in the administrative domain, as the authoritative source for information on employees. The relation must be hardcoded in the adapter, if not it will automatically create a link to a person object in the education domain.

* Felles
    * Added Matrikkelnummer as complex datatype.

* Administrasjon
    * Added jobbtittel to Personalressurs.

#### Deprecated

Note: Deprecated classes, attributes and relations might be removed in the next major release.

* Utdanning
    * The attribute periode on Gruppe is deprecated. Timeframes for relevant group types should be represented using relations to Termin and/or Skoleår.

#### Bugfixes

NA

### References

[Documentation 3.6.0](https://informasjonsmodell.felleskomponent.no/?v=v3.6.0)


