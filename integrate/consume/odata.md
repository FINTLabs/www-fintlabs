## General info
This java library is used to filter streams of objects based on grammars and parse trees built with ANTLR. At present the library has support for most of OData 4.01 Logical Operators (5.1.1.1) and Lambda Operators (5.1.1.13) as specified in http://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html.

## ODataFilter examples

### Logical Operators
#### equals
```
GET ~/persons?$filter=familyName eq 'Family name'
```
#### not equals
```
GET ~/persons?$filter=familyName ne 'Family name'
```
#### greater than
```
GET ~/persons?$filter=opprettet gt '2020-11-25T10:30:30Z'
```
#### greater than or equal
```
GET ~/persons?$filter=opprettet ge '2021-6-13T11:35:20Z'
```
#### less than
```
GET ~/persons?$filter=opprettet lt '2021-6-13T11:35:20Z'
```
#### less than or equal
```
GET ~/persons?$filter=opprettet le '2021-6-13T11:35:20Z'
```
#### and
```
GET ~/identifikatorverdi?$filter=systemid contains '50' and systemid contains 'id'
```
#### or
```
GET ~/identifikatorverdi?$filter=systemid contains '4' or systemid contains '2'
```
#### not
```
GET ~/identifikatorverdi?$filter=not systemid contains '4'
GET ~/identifikatorverdi?$filter=systemid contains '4' and not systemid contains '2'
```

### String and Collection Functions
#### starts with
```
GET ~/persons?$filter=lastName startswith 'Kn'
```
#### ends with
```
GET ~/persons?$filter=lastName endswith 'en'
```
#### contains
```
GET ~/persons?$filter=firstName contains 'ri'
```

### Lambda operators
#### any
```
GET ~/persons?$filter=any(p:p/href ne '${felles.person}/fodselsnummer/01010111111')
```
#### all
```
GET ~/persons?$filter=all(p:p/href eq '${felles.person}/fodselsnummer/04821648912')
```