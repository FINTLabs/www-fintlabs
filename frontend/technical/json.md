# JSON

FINT tilbyr JSON-skjema [draft-07](https://json-schema.org/specification.html) for alle klasser i FINTs informasjonsmodell. Disse er tilgjengelige under <https://schema.fintlabs.no/>.

For å finne et bestemt skjema, legges domenet for ressursklassen og navnet på ressursen til URIen i formen `<domain>/<class>.json`

For eksempel er skjemaet for `Personalressurs` tilgjengelig på <https://schema.fintlabs.no/administrasjon/personalressurs.json>.

## jsonvalidate

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
