## Information Model at the Center

In FINT, the information model defines how the APIs are structured and how they function.

### Types of classes

The FINT information model has four types of classes:

1. Main classes (`hovedklasse`)
1. Abstract classes
1. Complex datatypes
1. References

Only main classes are directly accessible from FINT APIs, and every main class in the model has an API endpoint.

?>A main class is equivalent to a resource in REST

All other types are used to construct the main classes, either by abstraction of common fields, or to represent fields in the classes.

### Identity

Main classes have identity, and can be referred to using an identifier value. This is represented by attributes of the type `Identifikator`. All main classes have at least one attribute of this type, but it's perfectly legal to have more than one identifying attribute.

If the class has multiple identifying attributes, any of the identifying attributes can be used to reference it, and the FINT API exposes endpoints to refer to the class by all of the identifying attributes.

For instance, `Personalressurs` can be identified by both `ansattnummer`, `brukernavn` and `systemId`.

### Relations

Relations can be added to main classes, either directly or in an abstract base class.  In addition, attributes of the class can be complex datatypes, which also can have relations.

The name of the relation represents the relationship from the source to the target, and has often the same name as the class of the target.

Relations can be optional or mandatory, single-value or multi-value.  In any case, they are always represented in the same form.

All relations are in the `_links` attribute on the class it links from.  Remember, this can be an inner complex datatype.

The `_links` attribute is an object where the name of the relation is used as the property name.  The property is an array of objects with a `href` attribute containing the URI to the target resource.

All relations to other resources in the information model *always* refer to a main class using one of the identifiable fields.

The FINT model also includes references to resources outside the model.  These are represented by a special type of relation called `Referanse`.  They are also represented as URIs.

### Attributes

Attributes in the resources can either be complex datatypes or any of the primitive types:

- string
- integer
- float
- dateTime

Attributes can be optional or mandatory, single-value or multi-value.  Multi-value attributes are always represented as an array, even if there is only a single value.

#### Date

Dates are represented in ISO 8601 form with UTC +0 (Z) time zone.

Example: `2019-06-05T09:48:23Z`.

The adapter is responsible for all date data to UTC +0. The consumer is responsible for changing date data to a usefull timesone for the application.

Example:

Here you can se what a Date of birth can look like:

- In a HRM system: '2000-02-14T00:00:00+1'
- In FINT: '2000-02-13T23:00:00Z'
- In Consumer application: '2000-02-14T00:00:00+1'
