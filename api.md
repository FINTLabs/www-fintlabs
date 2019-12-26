# 
# What is REST?

>The basis for almost all modern web-based APIs.

## REST? HATEOAS? HAL?
### Representational state transfer

https://en.wikipedia.org/wiki/Representational_state_transfer

### Hypermedia As The Engine Of Application State

https://en.wikipedia.org/wiki/HATEOAS

### Hypertext Application Language

https://en.wikipedia.org/wiki/Hypertext_Application_Language


# Information Model at the Center

In FINT APIs, the information model defines how the APIs are structured and how they function.

## Types of classes

The FINT information model has four types of classes:

1. Main classes (`hovedklasse`)
1. Abstract classes
1. Complex datatypes
1. References

Only main classes are directly accessible from FINT APIs, and every main class in the model has an API endpoint.

?>A main class is equivalent to a resource in REST

All other types are used to construct the main classes, either by abstraction of common fields, or to represent fields in the classes.

## Identity

Main classes have identity, and can be referred to using an identifier value.  This is represented by attributes of the type `Identifikator`.  All main classes have at least one attribute of this type, but it's perfectly legal to have more than one identifying attribute.

If the class has multiple identifying attributes, any of the identifying attributes can be used to reference it, and the FINT API exposes endpoints to refer to the class by all of the identifying attributes.

For instance, `Personalressurs` can be identified by both `ansattnummer`, `brukernavn` and `systemId`. 

## Relations

Relations can be added to main classes, either directly or in an abstract base class.  In addition, attributes of the class can be comples datatypes, which also can have relations.

The name of the relation represents the relationship from the source to the target, and is often the name as the class of the target.

Relations can be optional or mandatory, single-valued or multi-value.  In any case, they are always represented in the same form. 

All relations are in the `_links` attribute on the class it links from.  Remember, this can be an inner complex datatype.  

The `_links` attribute is an object where the name of the relation is used as the property name.  The property is an array of objects with a `href` attribute containing the URI to the target resource.

All relations to other resources in the information model *always* refer to a main class using one of the identifiable fields.

The FINT model also includes references to resources outside the model.  These are represented by a special type of relation called `Referanse`.  They are also represented as URIs.

## Attributes

Attributes in the resources can either be complex datatypes or any of the primitive types:

- string
- integer
- float
- dateTime

Attributes can be optional or mandatory, single-valued or multi-value.  Multi-value attributes are always represented as an array, even if there is only a single value.

Dates are represented in ISO 8601 form with UTC time zone: `2019-06-05T09:48:23Z`.

# Naming convention

FINT information objects are named based on the packaging structure in the information model:

- Administrasjon `/administrasjon`
  - Fullmakt `/administrasjon/fullmakt`
  - Kodeverk `/administrasjon/kodeverk`
  - Organisasjon `/administrasjon/organisasjon`
  - Personal `/administrasjon/personal`
- Utdanning `/utdanning`
  - Elev `/utdanning/elev`
  - Kodeverk `/utdanning/kodeverk`
  - Timeplan `/utdanning/timeplan`
  - Utdanningsprogram `/utdanning/utdanningsprogram`
  - Vurdering `/utdanning/vurdering`

For every package, classes of the stereotype `hovedklasse` are accessible through the FINT API.
As an example, for the package *Personal* within the domain *Administrasjon*, the following classes
are currently `hovedklasse`:

- Personalressurs `/personalressurs`
- Arbeidsforhold `/arbeidsforhold`
- Fravær `/fravar`
- Fastlønn `/fastlonn`
- Fasttillegg `/fasttillegg`
- Variabellønn `/variabellonn`

Norwegian characters are translated according to the following scheme:

| Original | Replacement |
|---|---|
| æ | a |
| ø | o |
| å | a |



# Common operations

These operations are available for all classes in the FINT information model.

## Get all objects of a given class

`/domain/package/class`, i.e. `/administrasjon/personal/personalressurs`

This operation fetches all objects of a given class from the FINT cache.  The response looks
like this:

```json
{
    "_embedded": {
        "_entries": [
            {
                
            },
            {
                
            }
        ]
    },
    "_links": {
        "self": [
            {
                "href": "..."
            }
        ]
    },
    "total_items": 111
}
```

## Fetch individual item by identifier

`/domain/package/class/field/value`, i.e. `/administrasjon/personal/personalressurs/ansattnummer/123456`

Given an identifier field name (any field of type `Identifikator`) and the identifier value, try
fetching the individual item.

## Size of cache for a given class

`/domain/package/class/cache/size`, i.e. `/administrasjon/personal/personalressurs/cache/size`

Return the size of the cache for a given class.  The response looks like this:

```json
{
  "size": 10632
}
```

## Timestamp for when cache was last updated

`/domain/package/class/last-updated`, i.e. `/administrasjon/personal/personalressurs/last-updated`

Return a timestamp indicating when the cache was last updated.  The response looks like this:

```json
{
  "lastUpdated": "1559551091034"
}
```

## Get objects updated since timestamp

`/domain/package/class?sinceTimeStamp=<time>`, i.e. `/administrasjon/personal/personalressurs?sinceTimeStamp=1559551091034`

Returns a collection of all objects that have been updated (added or modified) later than the
provided timestamp.  The response looks like this:

```json
{
    "_embedded": {
        "_entries": [
            {
                
            },
            {
                
            }
        ]
    },
    "_links": {
        "self": [
            {
                "href": "..."
            }
        ]
    },
    "total_items": 2
}
```

If `total_items` is `0`, this indicates that there are no new updates since the given timestamp.

## Health Check

`/domain/package/admin/health`, i.e. `/administrasjon/personal/admin/health`

Triggers a health check towards the adapter providing data.  The response indicates whether the adapter is connected and responding.

# General guidelines

To get the most value from FINT APIs, some guidelines to follow.

## Information is a Graph

FINT's resources have relatively few attributes, but more relations.  Every resource only has the attributes that are
directly relevant for the resource.  Everything else is represented as relations (links) to other resources. 
As an example, the class `Personalressurs`, representing an employee, does not have the employee's name.  Instead there is
a link to `Person`, representing a private person, where you find the properties of the employee as a private person.

### Refer, not Replicate

Information always changes.  Stale data is often worse than not having any data at all.  The FINT API is based on the principle that information should be fetched from the source when needed, not replicated beforehand.

### References are Stable

Resources in FINT are represented using URIs.  These URIs are constructed by the API based on attributes that can be used to identify the resource, represented by the type `Identifikator`.

As long as the identifiable attribute does not change, neither does the URI representing the resource.

## Everything is a Resource

All classes in the FINT information model is represented in the exact same way, as resources with URIs and references using URIs to other classes it refers to.

The type of the resource is explicit from the URI of the resource.  For instance, from the URI `/administrasjon/personal/personalressurs`, the type of the resource is always `Personalressurs`.


# Updating information using FINT

Updates use HTTP operations to create, modify and delete information.  It builds upon the "everything
is a resource" principle, so when updating information the resource URI is central.

## Asynchronous operations

Since the updates must propagate via the FINT component and an adapter before being processed by the
back end system, updates might take some time to complete.  For this, FINT APIs use asynchronous
operations as described in http://restcookbook.com/Resources/asynchroneous-operations/.

The process is as follows:

1. The client initiates an update operation.
1. The FINT API validates the syntax of the operation and responds with status code `202` and a `Location` 
   header referring to a `/status/<uuid>` resource
1. The client fetches the *Status* resource.
   - If the operation is still pending, the FINT API keeps responding with status code `202`.
1. If the operation has completed, the FINT API responds with the final status of the update:
   - If successful, status `303` with a `Location` referring to the resource that has been
     created or updated.
   - _Note:_ If the operation is a deletion, the status code is `410` instead.
   - If rejected by the back-end system, status `400` with a response body indicating the error.
   - If the update is in conflict with other updates or data in the back-end system, the status
     is `409` and the response body contains the original information the update conflicts with.
   - If there was a temporary failure processing the request, status `500` with the
     error message.
      In this case the client can re-try the request.

The *Status* resource is valid for 30 minutes after initiating the original request.

## Creating new objects

`POST /domain/package/class`, i.e. 
`POST /administrasjon/personal/fravar`

The body must be a complete resource to be created, including `_links` to other resources it refers to.

Internal identifiers controlled by the back-end system can be omitted.

## Modifying existing objects

`PUT /domain/package/class/field/value`, i.e. `PUT /administrasjon/personal/personalressurs/ansattnummer/123456`

The resource to be modified is identified by the identifiable field and value.
Any field of type `Identifikator` can be used to identify the resource.

The body must be the complete resource after modification.
Attributes that can be modified are indicated in the information model.

## Deleting objects

`DELETE /domain/package/class/field/value`, i.e. `DELETE /administrasjon/personal/fravar/systemid/abcdef1234`

Not all information classes support deletion.
If deletion is not supported, the operation is rejected with status `400`.


# Accessing
All FINT APIs are protected, and require Bearer token authorization.

## OAuth 2.0 Resource Owner Credentials Flow

To access FINT resources, a valid Bearer token must be obtained from the FINT IDP.  Authorization details are available from the FINT customer portal, https://kunde.felleskomponent.no

## Example projects for accessing FINT data

- Java, using Spring Boot: https://github.com/FINTLabs/client-example-spring
- Java, using Google HTTP and OAuth libraries: https://github.com/FINTLabs/client-example-plain-java
- Node.JS: https://github.com/FINTLabs/client-example-node
- Kotlin, using Spring Boot: https://github.com/FINTLabs/client-example-kotlin-spring
- Elm: https://github.com/FINTLabs/fint-api-client-demo
- BizTalk: https://github.com/FINTLabs/Fint.BizTalk.Example
- C#: https://github.com/FINTLabs/Fint.DotNet.Example

## Libraries for accessing OAuth protected resources

- Spring Boot OAuthRestTemplate: https://github.com/FINTLabs/fint-oauth-token-service

## Obtaining a valid Bearer token using `curl`

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

# FINT environments

FINT offers three environments, Play-with-FINT, Beta and Production:

- https://play-with-fint.felleskomponent.no
- https://beta.felleskomponent.no
- https://api.felleskomponent.no

For all of these environments the URIs follow the same pattern, so to find employee #33445, append the following path to the URI: `/administrasjon/personal/personalressurs/ansattnummer/33445`.

# JSON Schema

FINT offer [draft-07](https://json-schema.org/specification.html) JSON Schema for all classes in the FINT information model.  These are available under https://fintlabs.no/schema/

To find a particular schema, the domain of the resource class and the name of the resource is added to the URI in the form `<domain>/<class>.json`

For insance, the schema for `Personalressurs` is available at https://fintlabs.no/schema/administrasjon/personalressurs.json

# GraphQL API

FINT also offers an experimental [GraphQL](https://graphql.org/) API for accessing data as a graph.

The GraphQL endpoint is at `/graphql/graphql`.  It requires the same Bearer token as the rest of the FINT APIs.

Our recommended client to test GrapqQL is https://insomnia.rest - using this the OAuth credentials from the customer portal can be used directly as an Environment.

Create a `POST` request to the GraphQL endpoint, configure OAuth 2, and Insomnia fetches the GraphQL schema so you can validate the query and see the results.

## FINT GraphQL Schema

The GraphQL schema for FINT follow the information model exactly.  The root schema defines query endpoints for all resources by an identifier.  It is not possible to get all resources for a class for performance reasons.

## Example queries

Here are some examples to get you started.

### Employee information

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

### Student information

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

### Class membership

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

## Get FINT Token Web
FINT has a web-based tool to get a token that you can use to insert a token using i.e. `ModHeader` plugin for `Chrome`.

https://token.fintlabs.no/

## `fint-curl`

This script can be used to fetch a protected FINT resource, fetching a bearer token when needed.

To use it, copy the client authorization details from https://kunde.felleskomponent.no to a file called `client.json` in the current directory.  The name and location of this file can be overridden using the environment variable `CLIENT`.

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

## `jsonvalidate`

This Python 2.7 script performs JSON schema validation on a collection of resources.  The schema to use is provided as an URI on the command line.  It reads the resources from standard input, so it can be piped with `fint-curl` above to retrieve the data, i.e.

```bash
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



