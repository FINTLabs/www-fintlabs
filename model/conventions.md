## Navnekonvensjoner

FINT informasjonsobjekter er navngitt basert på pakkestrukturen i Informasjonsmodellen:

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

For hver pakke er klasser av typen `hovedklasse` tilgjengelig gjennom FINT API.

Som et eksempel har pakken *Personal* i domenet *Administrasjon* følgende klasser som er `hovedklasser`:

- Arbeidsforhold `/arbeidsforhold`
- Fastlønn `/fastlonn`
- Fasttillegg `/fasttillegg`
- Fravær `/fravar`
- Personalressurs `/personalressurs`
- Variabellønn `/variabellonn`

Særnorske bokstaver er erstattet som følger:

| Original | Erstatning |
| -------- |------------|
| æ        | a          |
| ø        | o          |
| å        | a          |