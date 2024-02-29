# Adapter Events

## FINT Adapter Events

The general flow between FINT and adapters are:

1. Adapter subscribes to events using the SSE endpoint
1. FINT delivers events on the SSE stream
1. Adapter accepts the event by `POST`ing to the status endpoint.  There is a 2-minute timeout on accepting events. If you use the adapter skeleton this is already handled.
1. Adapter responds to the event by `POST`ing to the response endpoint.  There is a 15-minute timeout on responding to events.

### Causes for events

FINT components produce events for three reasons:
- Health status requests
- Periodic cache update events every 15 minutes, triggering `GET_ALL_*` events.
- Incoming POST / PUT requests from clients.  Every request produces exactly one event.

FINT expects exactly one status and one response to every event delivered.  Additional responses will be rejected with `410 GONE`.

### Event kinds

FINT Adapters must be able to handle three different kinds of events:

  1. Request for system health status
  1. Requests to get all instances of a class from the FINT Consumer Cache Service
  1. Requests to get a single element of a class from the FINT Consumer API.
  1. Requests to update (create, modify or delete) a single element of a class from the FINT Consumer API.

The FINT Consumer will be issuing the events to the FINT Provider for the relevant `assetID`, and the FINT Provider will dispatch the event to all adapters connected and registered for this `assetID`.

This enables scenarios with distributed or redundant adapters where several adapters share the workload of handling events.  The adapter run-time instances must coordinate between themselves which instance responds to an event, since the provider will only accept a single set of responses for any given event.

Workloads can be distributed using two different strategies, which also could be combined:

  1. Divide and conquer: Different adapters handle different actions for a given component.  For instance, for `/administrasjon/personal`, one adapter could handle `Personalressurs` and `Arbeidsforhold`, and a different adapter could handle `Fastlonn`, `Variabellonn`, etc.
  1. Active and passive:  Several adapters are configured to respond to the same event, but coordinate internally to determine which of the instances should respond.

Any adapter instance registered with the asset ID can handle events in three ways:

  1. Accept the event and respond with data.  The consumer handles the data from the response.  Other adapters attempting to respond will receive a `410` status from the Provider.
  1. Reject the event.  The consumer ignores any data from the response.  Other adapters attempting to respond will receive a `410` status from the Provider.
  1. Ignore the event, assuming another instance is handling it.  If no other adapter is handling the events, the provider will expire the event after 120 seconds.

### System health status (`HEALTH`)

Every FINT Consumer has a health endpoint (`/admin/health`) that clients could `GET` from to
request health status.

Adapters have 30 seconds to respond to this health event.  The request payload contains an array
of health status structures, and the response should contain the same, with one additional element
for the status of the adapter and connection to the back-end systems.

The health status structure looks like this:

    {
      "component": "adapter",
      "status": "APPLICATION_HEALTHY",
      "timestamp": 1571327388028,
      "time": "2019-10-17T15:49:48.028Z"
    }

`timestamp` is in milliseconds since Unix epoch, `time` in ISO 8601.

`status` should be `APPLICATION_HEALTHY` or `APPLICATION_UNHEALTHY` depending on the state of the back-end application.

### Get all instances of a class (`GET_ALL_`_type_)

The FINT Consumer Cache Service issues these events every 15 minutes to update the consumer in-memory cache with all elements of the type.

Adapters are expected to retrieve all active elements from the back-end system and insert the data in the response event.

### Get a single instance of a class by ID (`GET_`_type_)

FINT Consumer APIs issue these events in cases where clients want the most recent version of a given element, and waits for the adapter to respond before returning data to the client.

The event's `query` attribute contains the `Identifikator` field name and field value to identify the element in the form _`field/value`_, exactly as the URI of the element in the Consumer API.

For instance, for `Personalressurs` with an `ansattnummer` ID of `12345`, the URI would be `/administrasjon/personal/personalressurs/ansattnummer/12345`, and the `query` attribute would then be `ansattnummer/12345`.

Adapters are expected to extract the `query` attribute, search the back-end system for the most recent version of the requested element.

For error situations, the adapter can control the HTTP response returned to the client using the following:

| `responseStatus` | `statusCode`   | HTTP result |
|------------------|----------------|-------------|
| `ERROR`          | (any)          | `500`       |
| `REJECTED`       | `"GONE"`       | `410`       |
| `REJECTED`       | `"NOT_FOUND"`  | `404`       |
| `REJECTED`       | (other values) | `400`       |

### Create a new element, or update an existing element by ID (`UPDATE_`_type_)

FINT Consumer APIs issue these events for `POST`, `PUT`, and `DELETE` requests for a given type, according to the following:

| REST Operation                     | `operation`| `query`       |
|------------------------------------|------------|---------------|
| `POST /path/to/type`               | `CREATE`   | (empty)       |
| `POST /path/to/type?validate=true` | `VALIDATE` | (empty)       |
| `PUT /path/to/type/field/value`    | `UPDATE`   | `field/value` |
| `DELETE /path/to/type/field/value` | `DELETE`   | `field/value` |

The adapters are expected to handle the various operations according to the following:

  - `VALIDATE`: The payload must be subjected to a semantic validation according to business rules, but not stored in the back-end system.  The response must either be `ACCEPTED` or `REJECTED` to indicate whether the payload is valid or not, or `ERROR` if the validation cannot be performed and should be retried.
  - `CREATE`: The payload must be subjected to a semantic validation according to business rules, supplied with a `systemId` `Indentifikator` (if relevant), and stored in the back-end system.  The response payload must be updated to correspond to the final version stored in the back-end system.  The response status must be `ACCEPTED`, `REJECTED`, or `CONFLICT` to indicate if the payload was valid or not, or if the creation conflicts with any other data in the system.  The `ERROR` response indicates a transient error, and that the creation can be retried.
  - `UPDATE`: The existing element, identified by the `query` field, should be updated with the payload according to business rules and which fields are `writable` in the FINT information model.  The response payload must include the final version stored in the back-end system.  Response status as above.
  - `DELETE`: The existing element, identified by the `query` field, should be removed from the back-end system if this is valid according to the business rules.  No response payload is expected, response status as above.

Events *must* be responded with a `responseStatus` setting indicating the result of the operation:

| `responseStatus` | HTTP status | Description of result
|------------------|-------------|------------------------
| `ACCEPTED`       | `303`       | The operation was accepted and completed successfully.  Based on event payload, the FINT API produces a `Location` header referring to the newly created resource.
| `REJECTED`       | `400`       | The operation was rejected.  The `message`, `statusCoude` and `problems` fields contain explanations as to why.
| `ERROR`          | `500`       | An error occurred during processing of the event.  The client may retry the same operation later.
| `CONFLICT`       | `409`       | The operation is in conflict with other activity.  The response contains an updated version of the resource so the client can update its own state.

If write operations are not supported or permitted, the event must be rejected by posting `ADAPTER_REJECTED` at the `/status` phase.

The response payload is handled according to the following, depending on ResponseStatus:

- `ACCEPTED`: The payload is added to the cache
- `REJECTED`: The payload is ignored.
- `ERROR`: The payload is ignored.
- `CONFLICT`: The payload is added to the cache.

Note the last clause.  For CONFLICT the adapter is supposed to deliver the most recent version of the information, so clients and the FINT cache can be updated.
