# Developing a FINT 2 adapter

## Before you start
If you'd like to observe the complete integration in action, you can refer to the example adapter available at the following [GitHub repository](https://github.com/FINTLabs/fint-core-adapter-skeleton)

## Publisher-subscriber pattern
To achieve the publisher-subscriber pattern in FINT 2, we will be using Reactive WebClient for making asynchronous API calls and Kafka as the message broker for handling event-based communication between components and services.

## Application properties

Before setting up the adapter, you first need to configure application properties in the application.yaml file. This allows you to set the necessary configuration properties for the adapter, such as ID, username, password, and so on.

This will be sent to the provider at registration.

In the standard code example provided, a single AdapterProperties is configured as follows:

example of application.yaml if we are posting elevfravar to utdanning vurdering in alpha enviornment.
```yaml
fint:
  adapter:
    id: https://example.com/org-no/utdanning/vurdering
    password: ***
    username: ***
    base-url: https://alpha.felleskomponent.no
    registration-id: fint
    org-id: fintlabs.no
    heartbeat-interval: 1
    page-size: 100
    capabilities:
      elevfravar:
        domain-name: utdanning
        package-name: vurdering
        resource-name: elevfravar
        fullSyncIntervalInDays: 7
        deltaSyncInterval: IMMEDIATE
```

* `id` Specifies the unique identifier for the adapter.
* `username/password` Specify the credentials required for authentication.
* `base-url` Specifies the URL of the external provider that the adapter will be communicating with.
* `registration-id` Specifies the registration ID to be used.
* `org-id` Specifies the organization ID for the adapter.
* `heartbeat-interval` Specifies the interval in minutes between the adapter's heartbeats. The recommended value is between 1-3 minutes.
* `capabilities` This property specifies the list of capabilities the adapter will provide. For each capability, the domain-name, package-name, resource-name, fullSyncIntervalInDays, and deltaSyncInterval should be specified.
* `page-size` Specifies the amount of resources one page can contain. The default value is 100, but this can be ignored if you're not planning to use our adapter-common library.
  The `deltaSyncInterval` parameter determines the frequency at which the adapter sends updates. You can choose from the following options:

- **IMMEDIATE**: This option indicates that the adapter will send updates as soon as they are available in the application.

- **LEGACY**: This option indicates that the adapter will send updates every `<=15` minutes. 

It is essential to configure these properties correctly before proceeding with setting up the adapter.

## Dependencies

The first step in setting up an adapter for FINT 2 is to ensure that you have all the required dependencies. There are only two critical dependencies required if you're follwing our method.

build.gradle
```groovy
dependencies {
    implementation 'no.fintlabs:fint-core-adapter-common:0.1.0'
    implementation 'no.fintlabs:fint-core-infra-models:1.1.1'
}
```

pom.xml
```xml
<dependencies>
    <dependency>
        <groupId>no.fintlabs</groupId>
        <artifactId>fint-core-adapter-common</artifactId>
        <version>0.1.0</version>
        
        <groupId>no.fintlabs</groupId>
        <artifactId>fint-core-infra-models</artifactId>
        <version>1.1.1</version>
    </dependency>
</dependencies>
```

Depending on what resources the adapter will handle, you may need additional dependencies. Ensure that all dependencies are added to the build.gradle file in the project.

## Resource Repository

After setting up dependencies, the next step is to create a repository that implements WriteableResourceRepository<ResourceName> of the resource. This repository will handle the communication between the adapter and the external system.

Example of a Repository that contains ElevFravar resource.
```java
@Repository
public class ElevfravarRepository implements WriteableResourceRepository<Elevfravar> {
    
}
```

## Resource Publisher

Once the resource repository is set up, the next step is to create a publisher that extends ResourcePublisher<ResourceName, ResourceRepository<ResourceName>>. The resource publisher is responsible for publishing the resources to the FINT 2 provider. Override the full and delta sync methods in the publisher to ensure that the resources are synced correctly.

```java
@Service
public class ElevfravarPublisher extends ResourcePublisher<ElevfravarResource, ResourceRepository<ElevfravarResource>> {

    public ElevfravarPublisher(ElevfravarRepository repository, AdapterProperties adapterProperties) {
        super(repository, adapterProperties);
    }

    @Override
    @Scheduled(initialDelayString = "10000", fixedRateString = "10800000")
    public void doFullSync() {
        submit(SyncData.ofPostData(repository.getResources()));
    }

    @Override
    @Scheduled(initialDelayString = "120000", fixedRateString = "5400000")
    public void doDeltaSync() {
        submit(SyncData.ofPatchData(repository.getUpdatedResources()));
    }

    @Override
    protected AdapterCapability getCapability() {
        return adapterProperties.getCapabilityByResource("elevfravar");
    }
}
```

## Resource Subscriber

To set up the subscriber, create a new class that extends ResourceSubscriber<ResourceName, CreatedPublisher> and super Webclient, AdapterProperties, CreatedPublisher, and ValidatorService. This class should also override the getCapability method and return the AdapterProperties getCapabilities method.

```java
@Service
public class ElevfravarSubscriber extends ResourceSubscriber<ElevfravarResource, ElevfravarPublisher> {

    protected ElevfravarSubscriber(WebClient webClient, AdapterProperties props, ElevfravarPublisher publisher, ValidatorService validatorService) {
        super(webClient, props, publisher, validatorService);
    }

    @Override
    protected AdapterCapability getCapability() {

        return adapterProperties.getCapabilities().get("elevfravar");
    }
}
```


The final step is to override the last method, createSyncPageEntry of SyncPageEntry<ResourceName>. There are multiple ways of creating a SyncPageEntry, here are three examples with different use cases.

SyncPageEntry of Identifier and Resource:
```java
    @Override
    protected SyncPageEntry<ElevfravarResource> createSyncPageEntry(ElevfravarResource resource) {
    String identificationValue = resource.getSystemId().getIdentifikatorverdi();
    return SyncPageEntry.of(identificationValue, resource);
    }
```

If SystemId is provided as selflink you can use exclude the identifier and only provide the resource as such:
```java
@Override
    protected SyncPageEntry<ElevfravarResource> createSyncPageEntry(ElevfravarResource resource) {
    return SyncPageEntry.ofSystemId(resource);
    }
```

Finally you can provide the identifierName and resource:
```java
    @Override
    protected SyncPageEntry<ElevfravarResource> createSyncPageEntry(ElevfravarResource resource) {
    return SyncPageEntry.ofIdentifierName("identifierName", resource);
    }
```
