# Autorelasjon

Autorelasjon er en innebygd funksjon i FINT som automatisk oppretter og vedlikeholder relasjoner mellom ressurser. Du som adapterleverandør trenger bare å sende inn ressursen med en referanse - FINT bygger den andre siden av relasjonen for deg.

## Støttede relasjonstyper

En relasjon får autorelasjon når alt dette gjelder:

- Informasjonsmodellen definerer en motsatt relasjon for den.
- Den motsatte siden er en liste (0..n eller 1..n).
- Er relasjonen selv også en liste (mange-til-mange), må ressursen være kilden, altså den eiende siden.
- Målressursen ligger i samme domene som kilderessursen. Felles ressurser som `person` regnes som en del av domenet de brukes i.

| Type | Beskrivelse | Støttet |
|---|---|---|
| En-til-mange (One → Many) | Kilden peker på én annen ressurs, som får en liste tilbake | Ja |
| Mange-til-mange (Many ↔ Many) | Begge sider kan ha flere referanser til hverandre | Ja, fra kildesiden |
| En-til-en og mange-til-en | Den motsatte siden er ikke en liste | Nei |
| På tvers av domener | Målressursen ligger i et annet domene | Nei |

Relasjoner som ikke får autorelasjon, må adapteret selv sende på begge sider.

> **Viktig for mange-til-mange:** Relasjonen blir kun bygget når data sendes fra **kilderessursen**. Bare én av sidene er definert som kilde. For å finne ut hvilken ressurs som er kilden, sjekk [relasjonsreglene](https://github.com/FINTLabs/fint-core/blob/main/RELATION_RULES.md) — kilden er ressursen som er listet som overskrift, og målressursen er den som får tilbake-relasjonen.

## Komplett liste over relasjonsregler

En fullstendig og oppdatert oversikt over alle ressurser og relasjoner som støttes av autorelasjon finner du her:

[Relasjonsregler (RELATION_RULES.md)](https://github.com/FINTLabs/fint-core/blob/main/RELATION_RULES.md)

Filen lages automatisk fra koden i [fint-core](https://github.com/FINTLabs/fint-core), så den er alltid i takt med reglene FINT bruker. Hver seksjon er en kilderessurs, og hver rad sier:

- **Source relation**: relasjonen adapteret sender på kilderessursen.
- **Target resource**: ressursen relasjonen peker på.
- **Back-relation**: relasjonen FINT fyller ut på målressursen.

## Hvordan fungerer det?

1. Adapteret sender inn kilderessursen med en relasjon til målressursen.
2. FINT lagrer koblingen mellom de to ressursene.
3. Når en klient henter målressursen, legger FINT tilbake-relasjonen inn i `_links`. Selve målressursen blir ikke endret.
4. Fjerner adapteret relasjonen fra kilderessursen, eller slettes kilderessursen, forsvinner tilbake-relasjonen.

**Kort sagt: Adapteret sender én vei - autorelasjon bygger resten.**

### Krav til det adapteret sender

- Lenken må peke på målressursen med et av målressursens identifikatorfelt, for eksempel `systemid/12345`. Se [Relasjoner i `_links`](integrate/provide/core2-adapter-api.md?id=relasjoner-i-_links). Lenker FINT ikke kan tolke, gir ikke autorelasjon.
- `identifier` i dataoverføringen, og `value.identifier` i svar på hendelser, må være en av kilderessursens identifikatorverdier. 
  FINT bruker den til å bygge lenken tilbake til kilden. Passer den ikke med noen av dem, får ressursen ingen autorelasjon.
- Adapteret kan gjerne sende listesiden selv også. FINT legger ikke til en tilbake-relasjon som allerede finnes med samme identifikator. Bruker adapteret et annet identifikatorfelt enn FINT, vil begge lenkene vises.

### Endringer i tilbake-relasjoner og `sinceTimeStamp`

Siden målressursen ikke endres, oppdateres heller ikke endringstidspunktet dens når en tilbake-relasjon kommer til eller forsvinner. Klienter som henter endringer med `sinceTimeStamp`, får derfor ikke målressursen på grunn av en ny eller fjernet tilbake-relasjon.

## Eksempel: En-til-mange

Hver `Fraværsregistrering` peker på ett `Elevfravær` gjennom relasjonen `elevfravar`, mens et `Elevfravær` kan ha mange fraværsregistreringer. Når adapteret sender inn en `Fraværsregistrering` med en referanse til et `Elevfravær`, legger autorelasjon automatisk til en tilbake-relasjon fra `Elevfravær` til `Fraværsregistrering`.

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
