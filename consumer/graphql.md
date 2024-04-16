# GraphQL API

FINT tilbyr også et eksperimentelt [GraphQL](https://graphql.org/) API for å få tilgang til data som et graf.

GraphQL-endepunktet er på `/graphql/graphql`. Det krever det samme Bearer-tokenet som resten av FINT APIene.

Vår anbefalte klient for å teste GraphQL er https://insomnia.rest - ved bruk av denne kan OAuth-legitimasjonen fra kundeportalen brukes direkte som et miljø.

Opprett en `POST`-forespørsel til GraphQL-endepunktet, konfigurer OAuth 2, og Insomnia henter GraphQL-skjemaet slik at du kan validere forespørselen og se resultatene.

## FINT GraphQL-skjema

GraphQL-skjemaet for FINT følger informasjonsmodellen nøyaktig. Rot-skjemaet definerer spørre-endepunkter for alle ressurser ved en identifikator. Det er ikke mulig å få alle ressurser for en klasse av ytelseshensyn.

## Eksempel på spørringer

Her er noen eksempler for å komme i gang.

## Informasjon om ansatte

Gitt et ansattnummer, finn personens navn og fødselsnummer, alle stillinger med størrelse og arbeidssted:


```graphql
query ($ansattnummer: String) {
  personalressurs(ansattnummer: $ansattnummer) {
    person {
      fodselsnummer {
        identifikatorverdi
      }
      navn {
        fornavn
        etternavn
      }
    }
    arbeidsforhold {
      ansettelsesprosent
      arbeidssted {
        organisasjonsKode {
          identifikatorverdi
        }
        organisasjonsnavn
      }
    }
  }
}
```

## Informasjon om studenter

Gitt en students FEIDE-navn, finn studentens kontaktinformasjon, skole og hjemmeadresse.

```graphql
query ($feidenavn: String) {
  elev(feidenavn: $feidenavn) {
    kontaktinformasjon {
      epostadresse
      mobiltelefonnummer
    }
    elevforhold {
      skole {
        navn
        organisasjon {
          organisasjonsnavn
        }
      }
    }
    person {
      navn {
        fornavn
        etternavn
      }
      bostedsadresse {
        adresselinje
        postnummer
        poststed
      }
    }
  }
}
```

## Klassemedlemskap

Gitt et systemId for en undervisningsgruppe, finn navn og kontaktinformasjon for alle studenter i den gruppen:

```graphql
query ($systemId: String) {
  undervisningsgruppe(systemId: $systemId) {
    navn
    beskrivelse
    elevforhold {
      elev {
        kontaktinformasjon { 
          mobiltelefonnummer
        }
        person {
          navn {
            fornavn
            etternavn
          }
        }
      }
    }
  }
}
```

