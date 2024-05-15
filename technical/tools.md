# Verktøy

## OAuth 2.0

Alle FINT API-er er beskyttet og krever autorisasjon med Bearer-token.

### OAuth 2.0 Resource Owner Credentials Flow

For å få tilgang til FINT-ressurser, må et gyldig Bearer-token innhentes fra FINT IdP. Autorisasjonsdetaljer er tilgjengelige fra FINTs kundeportal, <https://kunde.felleskomponent.no>.

### Eksempelprosjekter for å få tilgang til FINT-data

- Java, ved bruk av Spring Boot: <https://github.com/FINTLabs/client-example-spring>
- Java, ved bruk av Google HTTP- og OAuth-biblioteker: <https://github.com/FINTLabs/client-example-plain-java>
- Node.JS: <https://github.com/FINTLabs/client-example-node>
- Kotlin, ved bruk av Spring Boot: <https://github.com/FINTLabs/client-example-kotlin-spring>
- Elm: <https://github.com/FINTLabs/fint-api-client-demo>
- BizTalk: <https://github.com/FINTLabs/Fint.BizTalk.Example>
- C#: <https://github.com/FINTLabs/Fint.DotNet.Example>

### Biblioteker for å få tilgang til OAuth-beskyttede ressurser

- Spring Boot OAuthRestTemplate: <https://github.com/FINTLabs/fint-oauth-token-service>

### Skaffe et gyldig Bearer-token ved bruk av `curl`

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

### Skaffe et gyldig Bearer-token ved bruk av webbasert verktøy

FINT tilbyr et webbasert verktøy for å skaffe et token som du kan bruke i for eksempel `ModHeader`-tillegget for `Chrome`.

<https://token.fintlabs.no/>

## JSON

FINT tilbyr JSON-skjema [draft-07](https://json-schema.org/specification.html) for alle klasser i FINTs informasjonsmodell. Disse er tilgjengelige under <https://schema.fintlabs.no/>.

For å finne et bestemt skjema, legges domenet for ressursklassen og navnet på ressursen til URIen i formen `<domain>/<class>.json`

For eksempel er skjemaet for `Personalressurs` tilgjengelig på <https://schema.fintlabs.no/administrasjon/personalressurs.json>.

### jsonvalidate

Dette Python 2.7-scriptet utfører JSON-skjemavalidering på en samling ressurser. Skjemaet som skal brukes, angis som en URI på kommandolinjen. Det leser ressursene fra standard input, så det kan kobles sammen med [`fint-curl`](tools.mdd=fint-curl) for å hente data, for eksempel:

```bash
fint-curl https://beta.felleskomponent.no/administrasjon/personal/personalressurs | \
jsonvalidate https://schema.fintlabs.no/administrasjon/personalressurs.json
```

Sørg for at bibliotekene er de nyeste fra PyPI, versjonene som følger med Debian / Ubuntu er for gamle.

```python
#!/usr/bin/python

import jsonschema
import requests
import sys
import json
from tqdm import tqdm

r = requests.get(sys.argv[1])

schema = r.json()

data = json.load(sys.stdin)

validator = jsonschema.Draft7Validator(schema)

print "Validating", data["total_items"], "items..."

errors = 0

with open("errors.log", "a") as logfile:
 for item in tqdm(data["_embedded"]["_entries"]):
  try:
   validator.validate(item)
  except Exception as e:
   errors += 1
   print >> logfile, item
   print >> logfile, e

print "Validation completed with", errors, "errors."

```

## Testklient

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

### fint-curl

Dette skriptet kan brukes til å hente en beskyttet FINT-ressurs, og skaffe et Bearer-token når det trengs.

For å bruke det, kopier klientautorisasjonsdetaljene fra <https://kunde.felleskomponent.no> til en fil kalt `client.json` i gjeldende katalog. Navnet og plasseringen av denne filen kan overstyres ved å bruke miljøvariabelen `CLIENT`.

```bash
#!/bin/bash

#set -x

if ! ( curl --version > /dev/null && jq --version > /dev/null)
then
	echo "Required tools curl and jq not installed"
	exit 1
fi

case $(uname -s) in
	Linux)
		STATSZ="stat -c %s"
		STATMT="stat -c %Y"
		;;

	Darwin)
		STATSZ="stat -f %z"
		STATMT="stat -f %m"
		;;

	*)
		echo "Unknown OS $(uname -s)"
		exit 1
		;;
esac

CLIENT=${CLIENT:-client.json}
TOKEN=${CLIENT}.token

if [[ ! -e $CLIENT ]]
then
    echo "Client settings missing"
    exit 1
fi

eval $(cat $CLIENT | jq -r  "\"OAUTH_ID=\"+.clientId, \"OAUTH_SECRET=\"+.openIdSecret, \"OAUTH_USER=\"+.username, \"OAUTH_PWD=\"+.password, \"SCOPE=\"+.scope, \"IDP_URL=\"+.idpUri, \"ASSET_ID=\"+.assetId")

if [[ ! ( -e $TOKEN ) || $($STATSZ $TOKEN) -lt 10 || ( $(( $(date +%s) - $($STATMT $TOKEN) )) -gt 3500 ) ]]
then
    curl -f -s ${IDP_URL:-https://idp.felleskomponent.no/nidp/oauth/nam/token} -u "${OAUTH_ID}:${OAUTH_SECRET}" -d grant_type=password -d username="${OAUTH_USER}" -d password="${OAUTH_PWD}" -d scope="${SCOPE:-fint-client}" | jq -r '.access_token' > $TOKEN
fi

if [[ $($STATSZ $TOKEN) -lt 10 ]]
then
	echo "Authorization failure"
	exit 1
fi

curl -H "Authorization: Bearer $(cat $TOKEN)" -H  "accept: application/json;charset=UTF-8" -H "Content-Type: application/json" -H  "x-org-id: ${ASSET_ID:-fintlabs.no}" -H  "x-client: ${OAUTH_USER}" $*

```
