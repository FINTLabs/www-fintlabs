# Verktøy

## OAuth 2.0

All FINT APIs are protected, and require Bearer token authorization.

### OAuth 2.0 Resource Owner Credentials Flow

To access FINT resources, a valid Bearer token must be obtained from the FINT IdP.  Authorization details are available from the FINT customer portal, <https://kunde.felleskomponent.no>.

### Example projects for accessing FINT data

- Java, using Spring Boot: <https://github.com/FINTLabs/client-example-spring>
- Java, using Google HTTP and OAuth libraries: <https://github.com/FINTLabs/client-example-plain-java>
- Node.JS: <https://github.com/FINTLabs/client-example-node>
- Kotlin, using Spring Boot: <https://github.com/FINTLabs/client-example-kotlin-spring>
- Elm: <https://github.com/FINTLabs/fint-api-client-demo>
- BizTalk: <https://github.com/FINTLabs/Fint.BizTalk.Example>
- C#: <https://github.com/FINTLabs/Fint.DotNet.Example>

### Libraries for accessing OAuth protected resources

- Spring Boot OAuthRestTemplate: <https://github.com/FINTLabs/fint-oauth-token-service>

### Obtaining a valid Bearer token using `curl`

```bash
curl -s ${IDP_URL} \
-u "${OAUTH_ID}:${OAUTH_SECRET}" \
-d grant_type=password \
-d username="${OAUTH_USER}" \
-d password="${OAUTH_PWD}" \
-d scope="${SCOPE}" | \
jq -r '.access_token'
```

After obtaining the valid token, add it to the request header:

```bash
curl -H "Authorization: Bearer ${TOKEN}" https://.....
```

### Obtaining a valid Bearer token using web-based tool

FINT has a web-based tool to get a token that you can use to insert a token using i.e. `ModHeader` plugin for `Chrome`.

<https://token.fintlabs.no/>

## JSON

FINT offer [draft-07](https://json-schema.org/specification.html) JSON Schema for all classes in the FINT information model.  These are available under <https://schema.fintlabs.no/>.

To find a particular schema, the domain of the resource class and the name of the resource is added to the URI in the form `<domain>/<class>.json`

For instance, the schema for `Personalressurs` is available at <https://schema.fintlabs.no/administrasjon/personalressurs.json>.

### jsonvalidate

This Python 2.7 script performs JSON schema validation on a collection of resources.  The schema to use is provided as an URI on the command line.  It reads the resources from standard input, so it can be piped with [`fint-curl`](tools.mdd=fint-curl) to retrieve the data, i.e.

```bash
fint-curl https://beta.felleskomponent.no/administrasjon/personal/personalressurs | \
jsonvalidate https://schema.fintlabs.no/administrasjon/personalressurs.json
```

Make sure the libraries are the most recent ones from PyPI, the versions supplied with Debian / Ubuntu are too old.

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

## GraphQL

FINT also offers an experimental [GraphQL](https://graphql.org/) API for accessing data as a graph.

The GraphQL endpoint is at `/graphql/graphql`.  It requires the same Bearer token as the rest of the FINT APIs.

Our recommended client to test GraphQL is <https://insomnia.rest> - using this the OAuth credentials from the customer portal can be used directly as an Environment.

Create a `POST` request to the GraphQL endpoint, configure OAuth 2, and Insomnia fetches the GraphQL schema so you can validate the query and see the results.

### FINT GraphQL Schema

The GraphQL schema for FINT follow the information model exactly.  The root schema defines query endpoints for all resources by an identifier.  It is not possible to get all resources for a class for performance reasons.

### Example queries

Here are some examples to get you started.

#### Employee information

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

#### Student information

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

#### Class membership

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

## Test Client

FINT has a web-based test client for accessing and inspecting data available through FINT.

This test client is available under the URL `/test-client/` for each environment, i.e.:

- <https://play-with-fint.felleskomponent.no/test-client/>
- <https://beta.felleskomponent.no/test-client/>
- <https://api.felleskomponent.no/test-client/>

For Play-with-FINT the test client immediately presents you with the welcome page where you can
enter the URI for a resource to access.  The other two requires authentication, so you'll need to provide
valid authorization details for a client from FINT's customer portal.

On the welcome page, enter the URI for a resource, i.e. `/administrasjon/organisasjon/organisasjonselement`
and hit the button.  Results are presented as JSON, and all the URLs can be clicked to follow links to
other resources from within the test client.

### fint-curl

This script can be used to fetch a protected FINT resource, fetching a bearer token when needed.

To use it, copy the client authorization details from <https://kunde.felleskomponent.no> to a file called `client.json` in the current directory. The name and location of this file can be overridden using the environment variable `CLIENT`.

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
