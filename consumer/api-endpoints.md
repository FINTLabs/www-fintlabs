# Understanding the API

These operations are available for all classes in the FINT information model.

## Get all objects of a given class

`/domain/package/class`, i.e. `/administrasjon/personal/personalressurs`

This operation fetches all objects of a given class from the FINT cache. The response looks
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

## Pagination

`/domain/package/class?size=X&offset=Y`, i.e. `/administrasjon/personal/personalressurs?size=10000&offset=20000`

The complete list of resources could be very long, and the FINT API supports pagination in order to enable clients to
consume parts of the data.

Pagination is enabled by providing a `size` request parameter.  The response then looks like this:

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
        "href": ".../?offset=20000&size=10000"
      }
    ],
    "prev": [
      {
        "href": ".../?offset=10000&size=10000"
      }
    ],
    "next": [
      {
        "href": ".../?offset=30000&size=10000"
      }
    ]
  },
  "total_items": 1800000,
  "offset": 20000,
  "size": 10000
}
```

The `prev` and `next` links will only appear if there are additional pages before or after this page, respectively.

In addition, the `total_items` attribute indicates the total size of the dataset, and the `offset` and `size` parameters
correspond to the ones in the `self` link.

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

The general algorithm for continuously retrieving updates are this:

1. Maintain a `timestamp` variable, initially set to `0`.
2. Fetch the `.../last-updated` value, and store this in a _new_ variable.
3. Fetch resources, using the request parameter `sinceTimeStamp=<timestamp>`
4. Update the `timestamp` variable with the value retrieved from step 2.
5. Repeat as often as you find necessary.

__NOTE:__ This algorithm can be combined with pagination.  In this case, step 3 becomes a loop where resources
are fetched until the response no longer contains a `next` link.

## Health Check

`/domain/package/admin/health`, i.e. `/administrasjon/personal/admin/health`

Triggers a health check towards the adapter providing data.  The response indicates whether the adapter is connected and responding.


