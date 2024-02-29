# Tools

## FINT Test Client

FINT has a web-based test client for accessing and inspecting data available through FINT.

This test client is available under the URL `/test-client/` for each environment, i.e.:

- https://play-with-fint.felleskomponent.no/test-client/
- https://beta.felleskomponent.no/test-client/
- https://api.felleskomponent.no/test-client/

For Play-with-FINT the test client immediately presents you with the welcome page where you can
enter the URI for a resource to access.  The other two requires authentication, so you'll need to provide
valid authorization details for a client from FINT's customer portal.

On the welcome page, enter the URI for a resource, i.e. `/administrasjon/organisasjon/organisasjonselement`
and hit the button.  Results are presented as JSON, and all the URLs can be clicked to follow links to
other resources from within the test client.

## `fint-curl`

This script can be used to fetch a protected FINT resource, fetching a bearer token when needed.

To use it, copy the client authorization details from https://kunde.felleskomponent.no to a file called `client.json` in the current directory.  The name and location of this file can be overridden using the environment variable `CLIENT`.

```sh
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

## `jsonvalidate`

This Python 2.7 script performs JSON schema validation on a collection of resources.  The schema to use is provided as an URI on the command line.  It reads the resources from standard input, so it can be piped with `fint-curl` above to retrieve the data, i.e.

```sh
fint-curl https://beta.felleskomponent.no/administrasjon/personal/personalressurs | \
jsonvalidate https://fintlabs.no/schema/administrasjon/personalressurs.json
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
