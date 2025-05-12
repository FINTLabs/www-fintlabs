# Testklient

FINT tilbyr en webbasert testklient for å få tilgang til og inspisere data som er tilgjengelige gjennom FINT.

Denne testklienten er tilgjengelig under URLen `/test-client/` for hvert miljø:

- <https://play-with-fint.felleskomponent.no/test-client/>
- <https://beta.felleskomponent.no/test-client/>
- <https://api.felleskomponent.no/test-client/>

For Play-with-FINT presenterer testklienten umiddelbart velkomstsiden hvor du kan
taste inn URIen for en ressurs for å få tilgang. De to andre krever autentisering, så du må oppgi
gyldige autorisasjonsdetaljer for en klient fra FINTs kundeportal.

På velkomstsiden, skriv inn URIen for en ressurs, for eksempel `/administrasjon/organisasjon/organisasjonselement`
og trykk på knappen. Resultatene presenteres som JSON, og alle URLene kan klikkes for å følge lenker til
andre ressurser fra innsiden av testklienten.
