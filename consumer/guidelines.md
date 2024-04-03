# Consepts

## REST API

Our REST API is built upon key principles that ensure a robust and scalable architecture for distributed systems. Here's a brief overview of the foundational concepts:

- **REST (Representational State Transfer):** This is the architectural style that guides our API design, emphasizing scalable interaction with web-based services. To deepen your understanding of REST principles, visit [Wikipedia: Representational state transfer](https://en.wikipedia.org/wiki/Representational_state_transfer).
- **HATEOAS (Hypermedia as the Engine of Application State):** This constraint of RESTful design ensures that our clients remain decoupled from server-side logic, promoting long-term flexibility and evolvability of the API. You can read more about HATEOAS on [Wikipedia: HATEOAS](https://en.wikipedia.org/wiki/HATEOAS).
- **HAL (Hypertext Application Language):** We employ HAL to standardize the way resources link to one another within our API, making it straightforward to navigate and consume. More information on HAL is available at [Wikipedia: Hypertext Application Language](https://en.wikipedia.org/wiki/Hypertext_Application_Language).

## General guidelines

To get the most value from FINT APIs, some guidelines to follow.

### Information is a Graph

FINT resources have relatively few attributes, but more relations.  Every resource only has the attributes that are
directly relevant for the resource.  Everything else is represented as relations (links) to other resources.
As an example, the class `Personalressurs`, representing an employee, does not have the employee's name.  Instead there is
a link to `Person`, representing a private person, where you find the properties of the employee as a private person.

### Refer, not Replicate

Information always changes.  Stale data is often worse than not having any data at all.  The FINT API is based on the principle that information should be fetched from the source when needed, not replicated beforehand.

### References are Stable

Resources in FINT are represented using URIs.  These URIs are constructed by the API based on attributes that can be used to identify the resource, represented by the type `Identifikator`.

As long as the identifiable attribute does not change, neither does the URI representing the resource.

### Everything is a Resource

All classes in the FINT information model is represented in the exact same way, as resources with URIs and references using URIs to other classes it refers to.

The type of the resource is explicit from the URI of the resource.  For instance, from the URI `/administrasjon/personal/personalressurs`, the type of the resource is always `Personalressurs`.

