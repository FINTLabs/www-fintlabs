# Autorelasjon

Autorelasjon er en innebygd funksjon i FINT som automatisk oppretter og vedlikeholder relasjoner mellom ressurser. Du som adapterleverandør trenger bare å sende inn ressursen med en referanse - FINT bygger den andre siden av relasjonen for deg.

## Støttede relasjonstyper

| Type | Beskrivelse | Støttet |
|---|---|---|
| En-til-mange (One → Many) | Én ressurs peker på én annen, som får en liste tilbake | Ja |
| Mange-til-mange (Many ↔ Many) | Begge sider kan ha flere referanser til hverandre | Ja |
| En-til-en | Én ressurs peker på nøyaktig én annen | Nei |

> **Viktig for mange-til-mange:** Relasjonen blir kun bygget når data sendes fra **kilderessursen**. Bare én av sidene er definert som kilde. For å finne ut hvilken ressurs som er kilden, sjekk [relasjonsreglene](https://github.com/FINTLabs/fint-core-consumer/blob/main/RELATION_RULES.md) — kilden er ressursen som er listet som overskrift, og målressursen er den som oppdateres.

## Hvordan fungerer det?

1. Adapteret sender inn en ressurs med en relasjon til en annen ressurs.
2. FINT leser relasjonen og finner målressursen.
3. FINT legger automatisk inn en tilbake-relasjon på målressursen.
4. Adapteret trenger aldri selv å oppdatere eller bygge denne listen.

**Kort sagt: Adapteret sender én vei - autorelasjon bygger resten.**

## Eksempel: En-til-mange

`Fraværsregistrering` har en en-til-mange-relasjon til `Elevfravær`. Når adapteret sender inn en `Fraværsregistrering` med en referanse til et `Elevfravær`, legger autorelasjon automatisk til en tilbake-relasjon fra `Elevfravær` til `Fraværsregistrering`.

### Før adapteret sender data

`Elevfravær` i FINT-cache har ingen relasjon til `Fraværsregistrering`:

```json
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
```

### Adapteret sender inn Fraværsregistrering

Fraværsregistreringen refererer til `Elevfravær` via relasjonen `elevfravar`:

```json
{
  "systemId": {
    "identifikatorverdi": "888"
  },
  "_links": {
    "elevfravar": [
      {
        "href": "systemid/12345"
      }
    ]
  }
}
```

### Etter autorelasjon

`Elevfravær` har nå automatisk fått en relasjon tilbake til `Fraværsregistrering`:

```json
{
  "systemId": {
    "identifikatorverdi": "12345"
  },
  "_links": {
    "fravarsregistrering": [
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
```

## Komplett liste over relasjonsregler

En fullstendig og oppdatert oversikt over alle ressurser og relasjoner som støttes av autorelasjon finner du her:

[Relasjonsregler (RELATION_RULES.md)](https://github.com/FINTLabs/fint-core-consumer/blob/main/RELATION_RULES.md)
