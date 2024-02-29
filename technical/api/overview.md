# Overview of FINT's APIs

## Information Model at the Center

In FINT APIs, the information model defines how the APIs are structured and how they function.

### Types of classes

The FINT information model has four types of classes:

1. Main classes (`hovedklasse`)
1. Abstract classes
1. Complex datatypes
1. References

Only main classes are directly accessible from FINT APIs, and every main class in the model has an API endpoint.

All other types are used to construct the main classes, either by abstraction of common fields, or to represent fields in the classes.

### Identity

Main classes have identity, and can be referred to using an identifier value.  This is represented by attributes of the type `Identifikator`.  All main classes have at least one attribute of this type, but it's perfectly legal to have more than one identifying attribute.

If the class has multiple identifying attributes, any of the identifying attributes can be used to reference it, and the FINT API exposes endpoints to refer to the class by all of the identifying attributes.

For instance, `Personalressurs` can be identified by both `ansattnummer`, `brukernavn` and `systemId`. 

### Relations

Relations can be added to main classes, either directly or in an abstract base class.  In addition, attributes of the class can be comples datatypes, which also can have relations.

The name of the relation represents the relationship from the source to the target, and is often the name as the class of the target.

Relations can be optional or mandatory, single-valued or multi-value.  In any case, they are always represented in the same form. 

All relations are in the `_links` attribute on the class it links from.  Remember, this can be an inner complex datatype.  

The `_links` attribute is an object where the name of the relation is used as the property name.  The property is an array of objects with a `href` attribute containing the URI to the target resource.

All relations to other resources in the information model *always* refer to a main class using one of the identifiable fields.

The FINT model also includes references to resources outside the model.  These are represented by a special type of relation called `Referanse`.  They are also represented as URIs.

### Attributes

Attributes in the resources can either be complex datatypes or any of the primitive types:

- string
- integer
- float
- dateTime

Attributes can be optional or mandatory, single-valued or multi-value.  Multi-value attributes are always represented as an array, even if there is only a single value.

Dates are represented in ISO 8601 form with UTC time zone: `2019-06-05T09:48:23Z`.

## Naming convention

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



## Common operations

These operations are available for all classes in the FINT information model.

### Get all objects of a given class

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
    "total_items": 111,
    "size": 111,
    "offset": 0
}
```

### Pagination of result (`size` and `offset`)

For areas where there are a large number of resources, the API supports pagination.  This is controlled
by two query parameters:

| parameter | description |
|-----------|-------------|
| `size`    | Number of items to return.  Limits the response to contain maximum `size` elements. |
| `offset`  | Position in list to start returning items from.  Skips `offset` items. |

The response contains `prev` or `next` entries within `_links` if there are more items either before
or after (or both) compared to the current page.

The `total_items` attribute in the response can also be used to determine number of requests required.


**Example: 25,000**

Fetch first page: `/administrasjon/personal/person?size=25000&offset=0`

First 25,000 elements are returned.  The response contains the following:

```json
{
    "_links": {
        "self": [
            {
                "href": "/administrasjon/personal/person?size=25000&offset=0"
            }
        ],
        "next": [
            {
                "href": "/administrasjon/personal/person?size=25000&offset=25000"
            }
        ]
    },
    "total_items": 123456,
    "size": 25000,
    "offset": 0
}
```

Keep following the `next` link as long as it's present, for a total of five requests.

Each response will indicate 123,456 total items.  The first four responses will have a `size` of 25,000,
but the last response will have a size of 23,456 and no `next` link:

```json
{
    "_links": {
        "self": [
            {
                "href": "/administrasjon/personal/person?size=25000&offset=100000"
            }
        ],
        "prev": [
            {
                "href": "/administrasjon/personal/person?size=25000&offset=75000"
            }
        ]
    },
    "total_items": 123456,
    "size": 23456,
    "offset": 100000
}
```

### Fetch individual item by identifier

`/domain/package/class/field/value`, i.e. `/administrasjon/personal/personalressurs/ansattnummer/123456`

Given an identifier field name (any field of type `Identifikator`) and the identifier value, try
fetching the individual item.

### Size of cache for a given class

`/domain/package/class/cache/size`, i.e. `/administrasjon/personal/personalressurs/cache/size`

Return the size of the cache for a given class.  The response looks like this:

```json
{
  "size": 10632
}
```

### Timestamp for when cache was last updated

`/domain/package/class/last-updated`, i.e. `/administrasjon/personal/personalressurs/last-updated`

Return a timestamp indicating when the cache was last updated.  The response looks like this:

```json
{
  "lastUpdated": "1559551091034"
}
```

### Get objects updated since timestamp

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
    "total_items": 24324,
    "size": 2,
    "offset": 0
}
```

If `size` is `0`, this indicates that there are no new updates since the given timestamp.

This request can also be combined with pagination using `size` and `offset` in case a large number of items
have been updated.

**Note:** When FINT API restarts, all items are regarded new.  This means a `sinceTimeStamp` parameter
from before the restart will return all items.  It is therefore recommended to use pagination as well if the
result is large.

### Health Check

`/domain/package/admin/health`, i.e. `/administrasjon/personal/admin/health`

Triggers a health check towards the adapter providing data.  The response indicates whether the adapter is connected and responding.
