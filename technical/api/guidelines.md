# Using FINT APIs

## General guidelines

To get the most value from FINT APIs, some guidelines to follow.

## Information is a Graph

FINT's resources have relatively few attributes, but more relations.  Every resource only has the attributes that are
directly relevant for the resource.  Everything else is represented as relations (links) to other resources. 
As an example, the class `Personalressurs`, representing an employee, does not have the employee's name.  Instead there is
a link to `Person`, representing a private person, where you find the properties of the employee as a private person.

### Refer, not Replicate

Information always changes.  Stale data is often worse than not having any data at all.  The FINT API is based on the principle that information should be fetched from the source when needed, not replicated beforehand.

### References are Stable

Resources in FINT are represented using URIs.  These URIs are constructed by the API based on attributes that can be used to identify the resource, represented by the type `Identifikator`.

As long as the identifiable attribute does not change, neither does the URI representing the resource.

## Everything is a Resource

All classes in the FINT information model is represented in the exact same way, as resources with URIs and references using URIs to other classes it refers to.

The type of the resource is explicit from the URI of the resource.  For instance, from the URI `/administrasjon/personal/personalressurs`, the type of the resource is always `Personalressurs`.
