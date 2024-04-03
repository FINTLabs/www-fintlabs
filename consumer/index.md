# Integrate with FINT

## Environments

FINT offers three environments:

* <https://play-with-fint.felleskomponent.no> (sandbox)
* <https://beta.felleskomponent.no> (beta)
* <https://api.felleskomponent.no> (production)


## REST API

For all of these environments the URIs follow the same pattern, so to find employee #33445, append the following path to the URI: `/administrasjon/personal/personalressurs/ansattnummer/33445`.

Many users prefer to test queries against the REST API using applications like Postman or Insomnia. If you'd rather not install a separate client, you can utilize our web-based [Testklient](consumer/testklient.md) for convenient and direct access to our API endpoints.


Our REST API is built upon key principles that ensure a robust and scalable architecture for distributed systems. Here's a brief overview of the foundational concepts:

- **REST (Representational State Transfer):** This is the architectural style that guides our API design, emphasizing scalable interaction with web-based services. To deepen your understanding of REST principles, visit [Wikipedia: Representational state transfer](https://en.wikipedia.org/wiki/Representational_state_transfer).
- **HATEOAS (Hypermedia as the Engine of Application State):** This constraint of RESTful design ensures that our clients remain decoupled from server-side logic, promoting long-term flexibility and evolvability of the API. You can read more about HATEOAS on [Wikipedia: HATEOAS](https://en.wikipedia.org/wiki/HATEOAS).
- **HAL (Hypertext Application Language):** We employ HAL to standardize the way resources link to one another within our API, making it straightforward to navigate and consume. More information on HAL is available at [Wikipedia: Hypertext Application Language](https://en.wikipedia.org/wiki/Hypertext_Application_Language).


## GraphQL


## Consepts




