# Autorelasjon

Autorelasjon i FINT versjon 2 håndterer spesifikke relasjoner der:

- Én ressurs **alltid** peker på én annen ressurs (1 → 1)
- Den andre ressursen **alltid** kan ha 0..n eller 1..n tilbake (altså en flersidig relasjon)

Dette mønsteret er et krav for at autorelasjon skal fungere.

Autorelasjon sørger for at flersidige relasjoner bygges og vedlikeholdes automatisk basert på entydige referanser fra adapteret.

## Hvordan fungerer det?

Når adapteret sender inn en hovedressurs (f.eks. `Elevfravær`), inneholder den en referanse til en annen ressurs (f.eks. `Fraværsregistrering`).

Autorelasjonstjenesten gjør da følgende:

1. Mottar `Elevfravær`.
2. Leser `fravarsregistrering relasjonen` for å se hvilken `Fraværsregistrering` den tilhører.
3. Legger automatisk `Elevfravær` inn i relasjonslisten på `Fraværsregistrering`.
5. Adapteret trenger aldri selv å oppdatere eller bygge denne listen.

Poenget: **Adapteret sender én vei – autorelasjon bygger resten.**

## Eksempel: Elevfravær ↔ Fraværsregistrering

Relasjonstype:

- `Fraværsregistrering` → 0..n eller 1..n `Elevfravær`
- `Elevfravær` → 1 `Fraværsregistrering`

### Fint Cache - Elevfravær - før sending:
```json
{
  "_embedded": {
    "_entries": [
      {
        "systemId": {
          "identifikatorverdi": "12345"
        },
        "_links": {
          "elevforhold": [
            {
              "href": "https://api.felleskomponent.no/utdanning/elev/elevforhold/systemid/9595833"
            }
          ],
          "self": [
            {
              "href": "https://api.felleskomponent.no/utdanning/vurdering/elevfravar/systemid/12345"
            }
          ]
        }
      }
    ]
  },
  "_links": {
    "self": [
      {
        "href": "https://api.felleskomponent.no/utdanning/vurdering/elevfravar"
      }
    ]
  },
  "total_items": 1,
  "offset": 0,
  "size": 1
}
```

### Adapteret sender:

Elevfravær:

```json
{
  "føresPåVitnemål": true,
  "periode": {
    "start": "2025-03-29T11:00:00Z"
  },
  "systemId": {
    "identifikatorverdi": "888"
  },
  "_links": {
    "elevfravar": [
      {
        "href": "systemid/12345" (referer til eksisterende elevfravær)
      }
    ]
  }
}
```

### Fint Cache - Elevfravær - etter sending:
```json
{
  "_embedded": {
    "_entries": [
      {
        "systemId": {
          "identifikatorverdi": "12345"
        },
        "_links": {
          "fraværsregistrering": [ (oppdatert relasjon)
            {
              "href": "https://api.felleskomponent.no/utdanning/vurdering/fravarsregistrering/systemid/888"
            }
          ],
          "elevforhold": [
            {
              "href": "https://api.felleskomponent.no/utdanning/elev/elevforhold/systemid/9595833"
            }
          ],
          "self": [
            {
              "href": "https://api.felleskomponent.no/utdanning/vurdering/elevfravar/systemid/12345"
            }
          ]
        }
      }
    ]
  },
  "_links": {
    "self": [
      {
        "href": "https://api.felleskomponent.no/utdanning/vurdering/elevfravar"
      }
    ]
  },
  "total_items": 1,
  "offset": 0,
  "size": 1
}
```