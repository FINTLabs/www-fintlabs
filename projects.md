# Oversikt
Her finner du en oversikt over de tjenestene som FINT har i dag.

FINTs tjenester er delt inn i to hovedkategorier. FINT Felleskomponenter som er API'er på fagsystemene og FINT Tjenester som er løsninger som støtter arbeidsprosessene til fylkeskommunene. Disse tjenestene bruker FINTs API'er.

![ill1](_media/fint-leveranse-oversikt.svg)

## FINT Felleskomponenter

### Informasjonsmodell i sentrum

FINTs felleskomponenter springer ut fra FINTs informasjonsmodell, og følger denne direkte.  
Se [informasjonsmodellen](https://informasjonsmodell.felleskomponent.no/docs/package_administrasjon) for mer detaljer.

Informasjonsmodellen bygger på grunnblokkene tatt frem i SKATE, og er med å muliggjøre kommunesektorens orden i eget hus.
Den er også et viktig ledd for at kommunesektoren skal kunne virkeliggjøre "kun en gang" prinsippet.

Felleskomponentene har fokus omkring (fylkes)kommunenes interne behov for informasjonsutveksling, hvor informasjon fra
ett fagsystem benyttes i et annet, eller informasjon fra flere fagsystem sammenstilles i en enhetlig prosess.

Eksempelvis er ansattinformasjon fra HRM-systemet sentralt for brukeradministrasjon, samt for planlegging av aktiviteter
i fagsystemer innenfor skoleadministrasjon, helse, samferdsel m.v.

* Kravspesifikkasjon ved anskaffelse av systemet som trenger f.eks. ansatt- og organisasjonsinformasjon.
* Til digitalisering av prosesser mot innbyggere. F.eks. løsninger rettet mot elever.
* Til digitalisering og effektivisering av interne prosesser som identitetsforvaltning og vedlikehold av arkiv.
   
### Administrasjon

<div class="row">
  <div class="column">
  Innenfor Administrasjon har vi integrert mot HRM-systemer, arkivsystemer og økonomisystemer.  Her er informasjon om 
  ansatte, organisasjon, felles elementer fra NOARK tilgjengelig og faktura.

  **Integrasjonene er tilgengelige for HRM-systemer fra:**
  
  * Visma Enterprise HRM
  * Visma Bluegarden
  * Evry Unit4
  
  
  **Integrasjonene er tilgengelige for økonomisystemer:**

  * Visma Enterprise Fakturering
  * Xlegder (under utvikling)
  
  
  **Integrasjoner er tilgjengelige for arkivsystemer:**

  * Sikri - Elements og ePhorte
  * TietoEvry (P360)
  * Documaster
  * ACOS - Websak (under utvikling)


  Informasjon fra dette domenet benyttes i tjenester for kulturminneforvaltning, arkivadministrasjon og IAM.
  </div>
  <div class="column">

![adm1](_media/fint-leveranse-administrasjon.svg ':size=300')

  </div>
</div>


### Utdanning

<div class="row">
  <div class="column">
  Innenfor Utdanning har vi integrert mot skoleadministrative systemer.  Her er elev- og 
  gruppeinformasjon, utdanningsprogrammer, timeplaner og vurderingsresultater tilgjengelige.

  **Integrasjoner er tilgjengelige for skoleadministrative systemer:**

   * IST SATS
   * IST Extens
   * Visma InSchool


  Informasjonen fra dette domenet brukes videre til tjenester innenfor digitale læringsplattformer, betaling, 
  Kulturtanken, elevbevis, skoleskyss.
  </div>
  <div class="column">

![utd1](_media/fint-leveranse-utdanning.svg ':size=300')

  </div>
</div>

### Kultur

<div class="row">
  <div class="column">
  Arkivsystemene har integrasjoner som inneholder støtte for tilskudds- og dispensasjonsordninger innen
  kulturminneforvaltningen, og integrerer mot Riksantikvarens Digisak-system.

  **Integrasjoner er tilgjengelige for arkivsystemer:**

  * Sikri - Elements og ePhorte
  * TietoEvry (P360)
  * Documaster
  * ACOS - Websak (under utvikling)
  * KS SvarUT


  </div>
  <div class="column">

![adm1](_media/fint-leveranse-kulturminne.svg ':size=300')

  </div>
</div>


## FINT Tjenester

### Personalmapper
Personalmapper er en tjeneste for automatisk opprettelse og oppdatering av personalmappe (provisjonering). Tjenesten tilbyr:
- Opprettelse av personalmapper for alle ansatte. Man velger selv hvilke personalkategorier som skal ha personalmappe.
- Ved endring av navn, arbeidssted og leder oppdaterer tjenesten:
  -  den administrative enheten den ansatte hører til
  -  lederen som saksbehandler
  -  navnet i tittelen og i klassifikasjonen
-  Når den ansatte slutter blir personalmappen satt til "ferdigstilt"
-  Hvis en ansatt kommer tilbake settes mappen til "under behandling" hvis den ikke er lukket. Da opprettes en ny personalmappe.

Alle kodeverk og standardinnstillinger for en personalmappe er konfigurerbare for hver organisasjon.

Her er et flytdiagram som beskriver den overordnede flyten i det automatiske vedlikeholdet av personalmapper.

![peronalmapper](_media/personalmappe-flyt-overordnet.svg)

### Den Kulturelle Skolesekken

Den kulturelle skolesekken (DKS) er en nasjonal ordning som sørger for at alle skoleelever i Norge får oppleve profesjonell kunst og kultur hvert år.
Gjennom ordningen får elevene mulighet til å oppleve, gjøre seg kjent med og utvikle forståelse for profesjonelle kunst- og kulturuttrykk.
DKS er et samarbeidsprosjekt mellom kultur- og opplæringssektoren på nasjonalt, regionalt og lokalt nivå, og omfatter alle skolene i Norge. Fylkeskommunen er ansvarlig for regional koordinering og programmering, men kommunene har også mulighet for å utvikle egne program lokalt. 
Informasjonen er hentet fra [denkulturelleskolesekken.no](https://www.denkulturelleskolesekken.no/forside/om-dks/)
#### API for håndtering av skoler, trinn, basis- og undervisningsgrupper.
Den Kulturelle Skolesekken og FINT utvikler et API som skal bidra til å effektivisere dagens manuelle håndtering av informasjon om skoler, elevtall, trinn, klasser m.m. i DKS portal og fagsystem. For at API-et skal fungere etter hensikten er det behov for tilgang til skoledata hos hvert enkelt fylke. I påvente av Visma InSchool må tilgang til skoledata løses ved hjelp av uttrekk fra det nåværende skoleadministrative systemet til fylkene.

#### Sett opp PIFU-uttrekk mot FINT.
FINT trenger tilgang til PIFU-IMS eksport av fylkets skoledata. Dette for å kunne sette opp adapter som datakilde for API-et mot DKS. 
Et PIFU-IMS adapter prosesserer uttrekk og tilgjengeliggjør data gjennom FINT sine felleskomponenter.	Fylkeskommunene styrer selv hvem som får tilgang til felleskomponentene og til hvilken informasjon.
De fylker som er koblet opp mot Visma InSchool (VIS) leverer allerede oppdaterte skoledata til FINT og trenger ikke aktivere og sette opp noe mer.
Fylkene som ikke er koblet på VIS må sende FINT tilgang til PIFU-eksporten fra deres skoleadministrative system, og opprette adapter, klient og ressurs i FINTs kundeportal.
#### Opprette adapter, klient og ressurs.
En teknisk kontakt fra fylkeskommunen oppretter et adapter, en klient og en ressurs via FINTs [kundeportal](https://kunde.felleskomponent.no).
En veiledning for opprettelse av adapter og klient finner du [her](https://www.fintlabs.no/#/tutorials). Felleskomponentene som skal aktiveres, på adapteret og klienten, er utdanningsprogram, elev og timeplan.
Når adapteret og klienten er laget, må en ressurs opprettes for å unngå at dataen blandes med eksisterende FINT-data. Som ressursnavn bruker du navnet på din fylkeskommune og bindestrek "dks". 
Eksempel: "viken-fylkeskommune-dks". Adapteret og klienten som er opprettet skal kobles til ressursen. Det gjør du ved å redigere ressursen og legge til adapter under "ADAPTERS" og klienten under "KLIENTER".
Ta kontakt med FINT når adapter og klient er opprettet slik at FINT kan få tilsendt autentiseringsinformasjonen på en sikker måte.

### Betaling

*Målgruppe:*  Administrativt ansatte ved videregående skoler.

FINT Betaling gjør det mulig for videregående skoler å sende ut betalingforespørsler til enkeltelever, basisgrupper og undervisningsgrupper. Brukeren logger inn i løsningen, via Feide, velger en skole, og løsningen henter elev- og gruppeinformasjon basert på den valgte skole fra FINT. De velger hvem som skal faktureres og får presentert et vareregister som er hentet fra økonomisystemet til fylkeskommunen. 

Når mottaker(e) og produkt(er) er valgt, og brukeren bekrefter forespørselen sendes den videre til fylkeskommunens økonomisystem. I FINT Betaling er det mulig å følge betalingshistorikk, dvs om den er sendt, betalt, ubetalt eller kreditert. 

Målet med løsningen på sikt er at all betalingsoppfølging skal kunne gjøres i samme grensesnitt, og at elevene får mulighet
til å velge hvordan oppdragene skal betales, for eksempel med Vipps eller kort i tillegg til giro. 

### Kundeportal

*Målgruppe:* Alle som bruker FINT

Gjennom FINT Kundeportal er (fylkes)kommunene i stand til selv å administrere integrasjonene gjennom FINT.  Ansatte 
i (fylkes)kommunen registreres som kontaktpersoner for sin organisasjon, og kan deretter med pålogging via IDporten
få tilgang til kundeportalen på vegne av sin arbeidsgiver.  Her administreres teknisk tilgangsinformasjon for integrasjoner
som bruker eller leverer data gjennom FINT, og integrasjonene kan kvalitetstestes og feilsøkes.  

Her finnes også muligheten for å kontakte FINT dersom det er hendelser eller spørsmål, og overvåke hendelseslogger.

### IMS OneRoster

*Under utvikling*

IMS OneRoster er en internasjonal standard for utveksling av skoleadministrative data via API (og CSV). FINT har implementert 
støtte for standarden og vil, etter en test- og piloteringsfase, tilby dette som en felles tjeneste. Standarden er i utstrakt 
bruk internasjonalt, men det primære bruksområdet er gjerne automatisert synkronisering av skoledata til Office 365 Education porteføljen via 
Microsoft School Data Sync.

## Tilkoblede løsninger
### Riksantikvaren Digisak

*Målgruppe:*  Kulturminneforvaltning hos fylkeskommunene.

Digisak er Riksantikvarens nye fagsystem for saksbehandling av tilskudds- og dispensasjonssøknader innenfor 
kulturminneforvaltningen.  Oppgaver innenfor kulturminneforvaltningen blir overført fra Riksantikvaren til fylkeskommunen,
og fagsystemet skal understøtte søknadsbehandlingen fra søknad til vedtak og utbetalinger.

*Integrerer:*

* Arkivering av søknader med tilhørende dokumentasjon
* Dokumentasjon av saksbehandlingen
* Utbetaling av tilskudd

### Visma InSchool

*Målgruppe:* Elever og lærer i videregående skole.

*Integrerer:*

* Ansatt- og organisasjonsinformasjon
* Faste- og variable lønnstransaskjoner
* Kontoplaner
* Fullmaktsregister
* Ansattfravær

### PocketID
*Dette er under utvikling*

*Målgruppe:* Elever og lærlinger i videregående skole.

Se [http://www.pocketid.no](http://www.pocketid.no).

### Vigo BAS

*Målgruppe:* IT-avdelinger hos (fylkes)kommunene.

Vigo BAS er en Identity Management løsning utviklet i et samarbeid mellom flere fylkeskommuner.  Den henter informasjon om ansatte og elever fra
FINT, oppretter påloggingsinformasjon i f.eks. Active Directory og FEIDE, og oppdaterer kontaktinformasjon og
påloggingsdetaljer i kildestystemet.

*Integrerer:*

* Ansatt- og elevinformasjon
* Påloggingsinformasjon
* Tilganger

### NetIQ

*Målgruppe:* IT-avdelinger hos (fylkes)kommunene.

NetIQ er en Identity Management løsning utviklet i et samarbeid mellom flere fylkeskommuner.  Den henter informasjon om ansatte og elever fra
FINT, oppretter påloggingsinformasjon i f.eks. Active Directory og FEIDE, og oppdaterer kontaktinformasjon og
påloggingsdetaljer i kildestystemet.

*Integrerer:*

* Ansatt- og elevinformasjon
* Påloggingsinformasjon
* Tilganger

## Prosjekter

### Asker kommune sak- og arkivsystem

Asker kommune har valgt en løsning hvor saksbehandling og arkiv håndteres av to ulike systemer.  FINT utvikler en 
overføringstjeneste som skal overføre saker fra sakssystemet til arkivet fortløpende etter gitte kriterier.
