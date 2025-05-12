# OAuth 2.0

Alle FINT API-er er beskyttet og krever autorisasjon med Bearer-token.

## OAuth 2.0 Resource Owner Credentials Flow

For å få tilgang til FINT-ressurser, må et gyldig Bearer-token innhentes fra FINT IdP. Autorisasjonsdetaljer er tilgjengelige fra FINTs kundeportal, <https://kunde.felleskomponent.no>.

## Eksempelprosjekter for å få tilgang til FINT-data

- Java, ved bruk av Spring Boot: <https://github.com/FINTLabs/client-example-spring>
- Java, ved bruk av Google HTTP- og OAuth-biblioteker: <https://github.com/FINTLabs/client-example-plain-java>
- Node.JS: <https://github.com/FINTLabs/client-example-node>
- Kotlin, ved bruk av Spring Boot: <https://github.com/FINTLabs/client-example-kotlin-spring>
- Elm: <https://github.com/FINTLabs/fint-api-client-demo>
- BizTalk: <https://github.com/FINTLabs/Fint.BizTalk.Example>
- C#: <https://github.com/FINTLabs/Fint.DotNet.Example>

## Biblioteker for å få tilgang til OAuth-beskyttede ressurser

- Spring Boot OAuthRestTemplate: <https://github.com/FINTLabs/fint-oauth-token-service>

## Skaffe et gyldig Bearer-token ved bruk av `curl`

```bash
curl -s ${IDP_URL} \
-u "${OAUTH_ID}:${OAUTH_SECRET}" \
-d grant_type=password \
-d username="${OAUTH_USER}" \
-d password="${OAUTH_PWD}" \
-d scope="${SCOPE}" | \
jq -r '.access_token'
```

Etter å ha skaffet det gyldige tokenet, legg det til i forespørselens header:

```bash
curl -H "Authorization: Bearer ${TOKEN}" https://.....
```

## Skaffe et gyldig Bearer-token ved bruk av webbasert verktøy

FINT tilbyr et webbasert verktøy for å skaffe et token som du kan bruke i for eksempel `ModHeader`-tillegget for `Chrome`.

<https://token.fintlabs.no/>
