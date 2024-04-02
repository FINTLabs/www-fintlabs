## FINT innvendig (in english)

The Common API has two main services:

* Cache service
* Event service

### Cache Service

The cache service has the following responsibility:

* Store data from the business applications for all the organisations using the Common API
* Populate the cache
* Keeps track of which data has changed since the last time the cache was populated

### Event service

The internals in the Common API is event based. An event is created by:

* Cache Service
* Client

When a client hits a endpoint in the Consumer API the Common API is generating an event and sends it to the Cache Service. An event from the client will never go all the way down to the adapter.

When the Cache Service need to update the cache it sends an event down to the adapter through the Provider.

All events are logged at all stages.

![ill2](_media/event-flow.svg)

### Vocabulary

| English term         | Norwegian term       |
|----------------------|----------------------|
| Common API           | Felleskomponent      |
| Business application | Fagsystem            |

