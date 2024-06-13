## Oppdatere informasjon ved bruk av FINT

Oppdateringer bruker HTTP-operasjoner for å opprette, endre og slette informasjon. Det bygger på prinsippet om at "alt er en ressurs", så når man oppdaterer informasjon, er ressursens URI sentral.

### Asynkrone operasjoner

Siden oppdateringene må formidles via FINT-komponenten og et adapter før de behandles av
baksystemet, kan oppdateringer ta noe tid å fullføre. For dette bruker FINT APIer asynkrone
operasjoner som beskrevet i <http://restcookbook.com/Resources/asynchroneous-operations/>.


Prosessen er som følger:

1. Klienten initierer en oppdateringsoperasjon.
2. FINT API validerer syntaksen til operasjonen og responderer med statuskode [`202`](https://http.cat/202) og en `Location` header som henviser til en `/status/<uuid>`-ressurs.
3. Klienten henter *Status*-ressursen.
   - Hvis operasjonen fortsatt pågår, fortsetter FINT API å svare med statuskode `202`.
1. Hvis operasjonen er fullført, svarer FINT API med den endelige statusen for oppdateringen:
   - Hvis vellykket, status [`201`](https://http.cat/201) med en `Location` som henviser til ressursen som har blitt
     opprettet eller oppdatert, og en payload med den oppdaterte ressursen.
   - _Merk:_ Hvis operasjonen er en sletting, er statuskoden [`204`](https://http.cat/204) i stedet.
   - Hvis avvist av baksystemet, status [`400`](https://http.cat/400) med en respons-body som indikerer feilen.
   - Hvis oppdateringen er i konflikt med andre oppdateringer eller data i baksystemet, er status
     [`409`](https://http.cat/409) og responslegemet inneholder den opprinnelige informasjonen oppdateringen er i konflikt med.
   - Hvis det var en midlertidig feil under behandlingen av forespørselen, status [`500`](https://http.cat/500) med
     feilmeldingen. I dette tilfellet kan klienten forsøke forespørselen på nytt.

*Status*-ressursen er gyldig i 30 minutter etter at den opprinnelige forespørselen ble initiert.

### Opprette nye objekter

`POST /domain/package/class`, for eksempel
`POST /administrasjon/personal/fravar`

HTTP-forespørselens innhold må være en komplett ressurs som skal opprettes, inkludert `_links` til andre ressurser den refererer til.

Interne identifikatorer kontrollert av baksystemet kan utelates.

### Endre eksisterende objekter

`PUT /domain/package/class/field/value`, for eksempel `PUT /administrasjon/personal/personalressurs/ansattnummer/123456`

Ressursen som skal endres identifiseres ved det identifiserbare feltet og verdien.
Ethvert felt av typen `Identifikator` kan brukes for å identifisere ressursen.

HTTP-forespørselens innhold må være den komplette ressursen etter endring.
Attributter som kan endres er angitt i informasjonsmodellen.


### Slette objekter

`DELETE /domain/package/class/field/value`, for eksempel `DELETE /administrasjon/personal/fravar/systemid/abcdef1234`

Ikke alle informasjonsklasser støtter sletting.
Hvis sletting ikke støttes, blir operasjonen avvist med status `400`.

