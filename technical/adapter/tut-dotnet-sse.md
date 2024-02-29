# Tutorial: .Net SSE adapter

## Introduction
This tutorial will lead you through the process of setting up and adapter to communicate with the Play-With-FINT-Adapter service.


## Setting up the enviornment

### Clone the skeleton

```shell
$ git clone https://github.com/FINTprosjektet/Fint.Sse.Adapter.Skeleton.git my-adapter
$ cd my-adapter
$ rm -rf .git
```

### Open the project in our favorite IDE
This is a `netcoreapp2.0`\\`netstandard2.0` project. You need to import the dependencies. You can either do it in the IDE or in the commandline. This example uses the `dotnet` CLI:

```shell
$ dotnet restore
```

This `repo` consists of three projects:

- **FINT.Sse.Adapter** - This is the main `adapter` code.
- **FINT.Sse.Adapter.Console** - This is a wrapper around `FINT.Sse.Adaper` to make it run using `netcoreapp2.0`. You can create another wrapper for your favorit version/framework.
- **FINT.Sse.Adapter.Tests** - This is the `unit test` project.

## Get an OrgId
* Go <a href="https://play-with-fint-adapter.felleskomponent.no/demo/organization/generateOrgId" target="_blank">here</a> to generate an `OrgId`. 

> This `OrgId` is vaild until midnight the same day.

* Replace `pwfa.no` with your `OrgId` in the `appsettings.json` file in the `Fint.Sse.Adapter.Console` project:

```json
{
  "Logging": {
    "IncludeScopes": false,
    "LogLevel": {
      "Default": "Debug",
      "System": "Information",
      "Microsoft": "Information"
    }
  },
  "Configuration": {
    "ConsoleTitle": "FINT Console Boilerplate",
    "SseEndpoint": "https://play-with-fint-adapter.felleskomponent.no/provider/sse",
    "StatusEndpoint": "https://play-with-fint-adapter.felleskomponent.no/provider/status",
    "ResponseEndpoint": "https://play-with-fint-adapter.felleskomponent.no/provider/response",
    "Organizations": "pwfa.no", <-- HERE
    "LogLocation": "logs"
  }
}
```

```csharp
                public void HandleEvent(Event<object> serverSideEvent)
                {
Breakpoint -->      if (serverSideEvent.IsHealthCheck())
                    {
                    ...
                }
```
* Start the adapter in debug mode
* Open a browser and hit [https://play-with-fint-adapter.felleskomponent.no/swagger-ui.html](https://play-with-fint-adapter.felleskomponent.no/swagger-ui.html)
* From the `Admin` controller, configure the `/admin/health` with setting the following headers:
  * `x-org-id` use the generated OrgId
  * `x-client` to `test`
* Send the health event from the `/admin/health` endpoint.
* Step through the code to see what happens.
* You can also hit the `dog` and `owner` controllers to see how `FintResources` and `Relations` are build. See [https://github.com/FINTmodels/Fint.Relation.Model](https://github.com/FINTmodels/Fint.Relation.Model) for more information.

## Security
The `adapter` uses `OAuth2` by default to authenticated to the `provider` endpoint. This tutorial is set up with at tutorial user. In production one will get a *real* user. This is the `OAuth2` config:

```json
"OAuthTokenService": {
    "AccessTokenUri": "https://idp.felleskomponent.no/nidp/oauth/nam/token",
    "ClientId": "2d0ed372-53fb-4d0a-9e7f-d546c5cf2d71",
    "ClientSecret": "kgaiww60LjjNh0iyfv0KSjMZMbv04L6YZfYq5iYpu6IhIyxo6UFdslQMw_BBmZeVOuUCl75f3dE6FaDTVxgYjg",
    "Username": "pwfatut",
    "Password": "pwfatut",
    "Scope": "fint-client",
    "OAuthEnabled": "true"
}
```

## Links
* [Javadocs](https://docs.felleskomponent.no/fint-sse-adapter-skeleton) for the Java SSE Adapter Skeleton
* [Github project](https://github.com/FINTprosjektet/Fint.Sse.Adapter.Skeleton) for the CSharp/.Net SSE Adapter Skeleton
* [Fint.Sse](https://github.com/FINTlibs/Fint.Sse)
* [Fint.Relation.Model](https://github.com/FINTmodels/Fint.Relation.Model])
* [Overview](/adapter/overview/) of the adapter and FINT architecture

## Contribute
If you find bugs or have suggestions for improvement please feel free to submit an [issue](https://github.com/FINTprosjektet/Fint.Sse.Adapter.Skeleton/issues).



