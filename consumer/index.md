# Integrate with FINT

If you're considering using FINT extensively, such as for creating an integration or an adapter, we recommend familiarizing yourself with [our guidelines](consumer/guidelines.md).

## Environments

FINT offers three environments:

* <https://play-with-fint.felleskomponent.no> (sandbox)
* <https://beta.felleskomponent.no> (beta)
* <https://api.felleskomponent.no> (production)

## Getting access
The "play-with-fint" environment can be used without any authentication, so if you just want to explore, you can start here. If you wish to access the BETA or API environment, you can request access information from an organization you are collaborating with. This can be issued by creating a new client in Kundeportalen, where you will receive login information to generate an OAuth2 token. Contact us if your organization does not have a specific collaboration partner but desires extensive access by having us create a separate organization for you. Read more about [accessing FINT](consumer/access.md). 

## REST API

The REST API endpoints are built in accordance with the information model. To know what to query for, you should familiarize yourself with how [the information model is structured]().

Refer to [Understanding the API](consumer/api-endpoints.md) to grasp the endpoint structure for various functionalities like fetching by ID, pagination, and last-updated. [Updateing](consumer/updating.md) regarding how to perform UPDATE and POST requests. 

Many users prefer to test queries against the REST API using applications like Postman or Insomnia. If you'd rather not install a separate client, you can utilize our web-based [Testklient](consumer/testklient.md) for convenient and direct access to our API endpoints.

## GraphQL

[Documentation](consumer/graphql.md) for our legacy GraphQL service.
