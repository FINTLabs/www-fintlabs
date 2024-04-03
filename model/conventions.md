## Naming convention

FINT information objects are named based on the packaging structure in the information model:

- Administrasjon `/administrasjon`
    - Fullmakt `/administrasjon/fullmakt`
    - Kodeverk `/administrasjon/kodeverk`
    - Organisasjon `/administrasjon/organisasjon`
    - Personal `/administrasjon/personal`
- Utdanning `/utdanning`
    - Elev `/utdanning/elev`
    - Kodeverk `/utdanning/kodeverk`
    - Timeplan `/utdanning/timeplan`
    - Utdanningsprogram `/utdanning/utdanningsprogram`
    - Vurdering `/utdanning/vurdering`

For every package, classes of the stereotype `hovedklasse` are accessible through the FINT API.
As an example, for the package *Personal* within the domain *Administrasjon*, the following classes
are currently `hovedklasse`:

- Personalressurs `/personalressurs`
- Arbeidsforhold `/arbeidsforhold`
- Fravær `/fravar`
- Fastlønn `/fastlonn`
- Fasttillegg `/fasttillegg`
- Variabellønn `/variabellonn`

Norwegian characters are translated according to the following scheme:

| Original | Replacement |
| -------- | ----------- |
| æ        | a           |
| ø        | o           |
| å        | a           |