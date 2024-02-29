# A Technical Overview Of Adapters

## Introduction
A Common API is a API on a business application. The Common API gets and sends information to/from a business application through an adapter. This document aims to describe how an adapter should be implemented.

## Architectural overview - Common API

<img src="/images/architec-overview-kopi.png" alt="Overview" class="img-responsive" />

### Information Models
The Common API consist of standardized information models that will presented as resources in the Consumer API. Each Common API can consist of one or more information models. The models are documented here https://informasjonsmodell.felleskomponent.no

### Consumer API
Consumer API is where clients (applications, processes etc) access the data from the Business Application. 
Provider API
Provider API is where the adapter feeds the Common API with data.

### Adapter
The adapter is the “link” between the Common API and the Business Application. The main tasks for the adapter is:
Getting data from the Business Application
Mapping the data from the business application model to the Common API model
Sending the mapped data to the Common API

## Common API internals
The Common API has two main services:

* Cache service
* Event service

### Cache Service

The cache service has the following responsibility:
Store data from the business applications for all the organisations using the Common API
Populate the cache
Keeps track of which data has changed since the last time the cache was populated

### Event service

The internals in the Common API is event based. An event is created by:

* Cache Service
* Client

When a client hits a endpoint in the Consumer API the Common API is generating an event and sends it to the Cache Service. An event from the client will never go all the way down to the adapter.

When the Cache Service need to update the cache it sends an event down to the adapter.

All events are logged at all stages.

<img src="/images/fint-event-flow.png" alt="Event Flow" class="img-responsive" style="background:#fff" />

***Event flow***

## Provider API
The provider API is where the adapter communicates with the Common API. The adapter connects to get events from the Common API and sends back the response with the information from the business application.

The provider API makes use of SSE (Server-Sent-Events) (https://en.wikipedia.org/wiki/Server-sent_events) to send events to the adapter.

## Endpoints

<img src="/images/adapter-flow.png" alt="Adapter Flow" class="img-responsive" />

| Endpoint           | Method | Flow## | Description                                                                                                                               |
|--------------------|--------|-------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /provider/sse/:id  | GET    | 1     | The adapter registers on this endpoint. Id should be an UUID. If the adapter supports several orgId’s each orgId must have it’s own UUID. |
| /provider/status   | POST   | 3     | When the adapter receives an event it should post back a status to tell the provider if the event can be handled.  Adapters must accept or reject events with `/status` within 120 seconds. |
| /provider/response | POST   | 4     | This is where the adapter sends back the response.  Adapters must respond to events within 20 minutes. |

## Authentication

The provider API is secured with OAuth2 using the Resource Owner Password Credentials Grant flow.

<img src="/images/authentication.png" alt="Authentication" class="img-responsive" />

The ***Adapter is both Resource Owner and Client***. See https://github.com/FINTprosjektet/fint-oauth-consumer-client-sample for an example implementation.

## Error handling

The adapter must handle the following error scenarios:
The event sent from the provider is not understood
There is something wrong with the received event
Could not communicate with the source system

All of the error situations should result in an event sent from the adapter to the provider with the status `PROVIDER_REJECTED`. If the adapter has information about the error this can be added to the message field in the event-object.

## Adapter skeleton

There is a skeleton as a starting point and guideline for develop a adapter. This skeleton has code for communicating with the provider api. See the readme for more information.

| Language | Link                                                               |
|----------|--------------------------------------------------------------------|
| Java     | https://github.com/FINTprosjektet/fint-sse-adapter-skeleton        |
| C##       | https://github.com/FINTprosjektet/fint-sse-adapter-skeleton-csharp |

## Information Models
The main purpose of the adapter is to map the internal business application model to the FINT information model. This includes relations between objects. 

The FINT information model consist of two key elements:

Main classes which represent the resources. This can be a person, student, employee, employment, code and so on.
Relations between main classes. 

For more information about the FINT information model and a description of all the classes, attributes and relations one can go to https://informasjonsmodell.felleskomponent.no.

The technical implementations of the models can be found at https://github.com/FINTmodels.

## Vocabulary

| Norwegian term  | English term         |
|-----------------|----------------------|
| Felleskomponent | Common API           |
| Fagapplikasjon  | Business application |