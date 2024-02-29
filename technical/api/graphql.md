# GraphQL API

FINT also offers an experimental [GraphQL](https://graphql.org/) API for accessing data as a graph.

The GraphQL endpoint is at `/graphql/graphql`.  It requires the same Bearer token as the rest of the FINT APIs.

Our recommended client to test GrapqQL is https://insomnia.rest - using this the OAuth credentials from the customer portal can be used directly as an Environment.

Create a `POST` request to the GraphQL endpoint, configure OAuth 2, and Insomnia fetches the GraphQL schema so you can validate the query and see the results.

## FINT GraphQL Schema

The GraphQL schema for FINT follow the information model exactly.  The root schema defines query endpoints for all resources by an identifier.  It is not possible to get all resources for a class for performance reasons.

## Example queries

Here are some examples to get you started.

## Employee information

Given an employee ID, find person's name and National Identity Number, all positions with size and place of employment:

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

## Student information

Given a student's FEIDE name, find student's contact information, school and home address. 

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

## Class membership

Given a teaching group's systemId, find names and contact information for all students in that group:

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

