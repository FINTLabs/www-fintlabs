# Accessing FINT

All FINT APIs are protected, and require Bearer token authorization.

## OAuth 2.0 Resource Owner Credentials Flow

To access FINT resources, a valid Bearer token must be obtained from the FINT IDP.  Authorization details are available from the FINT customer portal, https://kunde.felleskomponent.no

### Example projects for accessing FINT data

- Java, using Spring Boot: https://github.com/FINTLabs/client-example-spring
- Java, using Google HTTP and OAuth libraries: https://github.com/FINTLabs/client-example-plain-java
- Node.JS: https://github.com/FINTLabs/client-example-node
- Kotlin, using Spring Boot: https://github.com/FINTLabs/client-example-kotlin-spring
- Elm: https://github.com/FINTLabs/fint-api-client-demo
- BizTalk: https://github.com/FINTLabs/Fint.BizTalk.Example
- C#: https://github.com/FINTLabs/Fint.DotNet.Example

### Libraries for accessing OAuth protected resources

- Spring Boot OAuthRestTemplate: https://github.com/FINTLabs/fint-oauth-token-service

### Obtaining a valid Bearer token using `curl`

```sh
curl -s ${IDP_URL} \
-u "${OAUTH_ID}:${OAUTH_SECRET}" \
-d grant_type=password \
-d username="${OAUTH_USER}" \
-d password="${OAUTH_PWD}" \
-d scope="${SCOPE}" | \
jq -r '.access_token'
```

After obtaining the valid token, add it to the request header:

```sh
curl -H "Authorization: Bearer ${TOKEN}" https://.....
```

## FINT environments

FINT offers three environments, Play-with-FINT, Beta and Production:

- https://play-with-fint.felleskomponent.no
- https://beta.felleskomponent.no
- https://api.felleskomponent.no

For all of these environments the URIs follow the same pattern, so to find employee #33445, append the following path to the URI: `/administrasjon/personal/personalressurs/ansattnummer/33445`.

