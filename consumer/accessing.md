# Tilgang til FINT

Alle FINT API-er er beskyttet og krever godkjenning med Bearer-token.

## OAuth 2.0 Resource Owner Credentials Flow

For å få tilgang til FINT-ressurser, må et gyldig Bearer-token innhentes fra FINT IDP. Autorisasjonsdetaljer er tilgjengelige fra FINTs kundeportal, https://kunde.felleskomponent.no


### Eksempelprosjekter for tilgang til FINT-data

- Java, ved bruk av Spring Boot: https://github.com/FINTLabs/client-example-spring
- Java, ved bruk av Google HTTP og OAuth-biblioteker: https://github.com/FINTLabs/client-example-plain-java
- Node.JS: https://github.com/FINTLabs/client-example-node
- Kotlin, ved bruk av Spring Boot: https://github.com/FINTLabs/client-example-kotlin-spring
- Elm: https://github.com/FINTLabs/fint-api-client-demo
- BizTalk: https://github.com/FINTLabs/Fint.BizTalk.Example
- C#: https://github.com/FINTLabs/Fint.DotNet.Example

### Biblioteker for tilgang til OAuth-beskyttede ressurser

- Spring Boot OAuthRestTemplate: https://github.com/FINTLabs/fint-oauth-token-service

### Innhenting av et gyldig Bearer-token ved bruk av `curl`

```sh
curl -s ${IDP_URL} \
-u "${OAUTH_ID}:${OAUTH_SECRET}" \
-d grant_type=password \
-d username="${OAUTH_USER}" \
-d password="${OAUTH_PWD}" \
-d scope="${SCOPE}" | \
jq -r '.access_token'
```

Etter å ha fått det gyldige tokenet, legg det til i forespørselens header:

```sh
curl -H "Authorization: Bearer ${TOKEN}" https://.....
```

## FINT-miljøer

FINT tilbyr tre miljøer, play-with-fint, Beta og Produksjon:

- https://play-with-fint.felleskomponent.no
- https://beta.felleskomponent.no
- https://api.felleskomponent.no

For alle disse miljøene følger URIene samme mønster, så for å finne ansatt #33445, legg til følgende bane i URIen: `/administrasjon/personal/personalressurs/ansattnummer/33445`.

