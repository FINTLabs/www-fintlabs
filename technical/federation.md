# Veiledninger

## Oppsett av Azure AD Federering - VIGO-IDP

### Virkemåte
![ill1](_media/vigo-idp/vigoidp1.png)

- I vigoBAS hentes studentnumber og employeeId fra Fint.

- VigoBAS eksporter studentnumber og employeeId til valgte extensionAttribute i onprem AD (valgfritt hvilke av attributtene 1-15 som benyttes).

- extensionAttributtene overføres til Azure AD via Azure AD connect

- I Azure AD benytter Enterprise appen VIGO-IDP extensionattributtene samt egendefinerte roller for å sette opp claims som benyttes mot de ulike Fint komponenetene.

### Forberedelser

- Studentnumber og emplyeeId fra Fint må eksporteres via vigoBAS til onprem AD (i dette eksempelet er Extension attributt 8 og 9 valgt) slik at disse synces opp til Azure AD.

- Opprettet grupper i onprem AD (som synces til Azure AD) eller Azure AD for kobling til roller/tilgang til Azure IDP'n. 

### Legge til en "Enterprise app"

Hver fylkeskommune må sette opp en Enterprise applications i sin egen Azure tenant. 

- Logg inn på egen Azure tenant https://portal.azure.com

- Søk etter “Azure Active Directory” og velg denne

- Klikk på “Enterprise applications” i venstre menyen

- Klikk på “New application”

- Gi den ett navn (VIGO-IDP)

![ill2](_media/vigo-idp/vigoidp2.png)

- Appen lages og når den popper opp - > klikk på “ 2. Set up single sign on”

![ill3](_media/vigo-idp/vigoidp3.png)

- Klikk på [Create]
- Klikk på "SAML"

![ill4](_media/vigo-idp/vigoidp4.png)

- Klikk på “Edit” under punkt 1 “Basic SAML Configuration”

![ill5](_media/vigo-idp/vigoidp5.png)

- Fyll inn “Identifier (Entity ID):

https://idp.felleskomponent.no/nidp/saml2/metadata

- Fyll inn “Replay URL (Assertion Consumer Service URL”

https://idp.felleskomponent.no/nidp/saml2/spassertion_consumer@

![ill6](_media/vigo-idp/vigoidp6.png)

- Klikk "Save"

### Legge til app roller

- Gå tilbake til Azure Active Directory og klikk på “App registrations”:

![ill7](_media/vigo-idp/vigoidp7.png)

- Klikk på “All applications”. Da kommer alle apper i tennanten opp. Hvis du ikke ser “VIGO-IDP” så søk den opp. Klikk på “VIGO-IDP” appen.

![ill8](_media/vigo-idp/vigoidp8.png)

- Klikk på “App roles|Preview”:

![ill9](_media/vigo-idp/vigoidp9.png)

- Klikk på “ + Create app role”:

![ill10](_media/vigo-idp/vigoidp10.png)

Fyll inn:

- Display name : Valgfritt navn
- Allowed member types : Users/Group
- Value : Predefionert fra Vigo som samsvarer med tjenesten som det skal authentiseres mot
- Description : Valgfri beskrivende tekst

Klikk på [Apply]

![ill11](_media/vigo-idp/create-app-role.png)


For å opprette flere roller: gjenta prosessen ved å trykke på “ +Create app role” og fyll inn som ovenfor. 

Figuren under viser 4 roller som er satt opp: 
- https://role-catalog.vigoiks.no/vigo/drosjeloyve/admin
- https://role-catalog.vigoiks.no/vigo/samtykke/user
- https://role-catalog.vigoiks.no/vigo/elevfakturering/user
- https://role-catalog.vigoiks.no/vigo/isyroad/user

Alle rollene, med beskrivelse, finnes i Rollekatalogen: https://role-catalog.vigoiks.no

![ill12](_media/vigo-idp/app-roles.png)


### Koble gruppe i Azure med rolle

- Gå tilbake til Azure AD og klikk på “Enterprise applications”:

![ill13](_media/vigo-idp/vigoidp13.png)

- Hvis du ikke ser “VIGO-IDP”: Søk den opp i søkefeltet. Klikk på VIGO-IDP:

![ill14](_media/vigo-idp/vigoidp14.png)

- Klikk på “Users and groups”

![ill15](_media/vigo-idp/vigoidp15.png)

- Klikk på “Add user/group”:

![ill16](_media/vigo-idp/vigoidp16.png)

- Klikk på “None selected” under “Users and groups”:

![ill17](_media/vigo-idp/vigoidp17.png)

- Søk opp gruppen:

![ill18](_media/vigo-idp/vigoidp18.png)

- Velg gruppen som skal ha tilgang (som skal ha rollen) og velg [Select]:

![ill19](_media/vigo-idp/vigoidp19.png)

- Klikk på “None selected” under “Select a role”:

![ill20](_media/vigo-idp/vigoidp20.png)

- Har du mange roller så søk opp rollen du opprettet tidligere. Klikk på rollen og velg [Select]:

![ill21](_media/vigo-idp/vigoidp21.png)

- Klikk på [Assign]:

I dette tilfellet vil medlemmer av gruppen “TILGANG-VIGO-SAMTYKKE” få rollen “vigo-samtykke-enduser”

![ill22](_media/vigo-idp/vigoidp22.png)

I bildet under “Users and groups” vil det vises de som har tilgang til appen og de tilknyttede rollene:

![ill23](_media/vigo-idp/vigoidp23.png)


### Legge til claims for SAML autentisering

- I ventre menyen: klikk på “Single sign-on”. Klikk så på “Edit” på punkt 2 under “User Attributes & claims”:

![ill24](_media/vigo-idp/vigoidp24.png)

- Klikk på “ + Add new claim”:

![ill25](_media/vigo-idp/vigoidp25.png)

Fyll inn:

- Name: studentnumber
- Namespace:  http://schemas.xmlsoap.org/ws/2005/05/identity/claims
- Source: Attribute
- Source attribute: Det attributtet i azure ad som innholder studentnumber
  - Verdien hentes fra /utdanning/elev/elev/systemid i Fint og synces via VigoBAS → onprem Ad → Azure AD

![ill26](_media/vigo-idp/vigoidp26.png)

Klikk på “ + Add new claim” og fyll inn:
- Name: employeeId
- Namespace: http://schemas.xmlsoap.org/ws/2005/05/identity/claims
- Source: Attribute
- Source attribute: Det attributtet i azure ad som inneholder employeeId 
  - Verdien hentes fra /administrasjon/personal/personalressurs/ansattnummer/ i Fint og synces via VigoBAS → onprem Ad → Azure AD

![ill27](_media/vigo-idp/vigoidp27.png)

Klikk på “ + Add new claim” og fyll inn:
- Name: roles
- Namespace: http://schemas.xmlsoap.org/ws/2005/05/identity/claims
- Source: Attribute
- Source attribute: user.assignroles

![ill28](_media/vigo-idp/vigoidp28.png)

Klikk på “ + Add new claim” og fyll inn:
- Name: organizationnumber
- Namespace:  http://schemas.xmlsoap.org/ws/2005/05/identity/claims
- Source: Attribute
- Source attribute: “organisasjonsnummer til fylkeskommunen”

![ill29](_media/vigo-idp/vigoidp29.png)

Klikk på “ + Add new claim” og fyll inn:
- Name: organizationid
- Namespace:   http://schemas.xmlsoap.org/ws/2005/05/identity/claims
- Source: Attribute
- Source attribute: “dns navn til fylkeskommunen”

![ill30](_media/vigo-idp/vigoidp30.png)

I oversikten over User attributes and claims skal det se slik ut:

![ill31](_media/vigo-idp/vigoidp31.png)

- Påse at claim under “Required claim” (Name ID) har disse egenskapene:

![ill32](_media/vigo-idp/vigoidp32.png)

![ill33](_media/vigo-idp/vigoidp33.png)


### Last ned og send sertifikat og metadata til FINT

I punkt “3 SAML Signing Certificate” : last ned følgende:
- “Certificate (Base64)”
- “Federation Metadata XML”

![ill34](_media/vigo-idp/vigoidp34.png)

Disse sendes til kontaktpersonen i fintlabs.


### Teste løsningen

Dette kan gjøres etter at Fint har mottat metadata og sertifikat samt konfigurert tilgangen.

- Gå til: https://idp.felleskomponent.no/nidp/
- I vaffelmenyen, klikk på din fylkeskommune.

![ill35](_media/vigo-idp/vigoidp35.png)

For å se selve SAML tokenet så kan man benytte Firefox med SAML-tracer tilleget. 

Attributeliste for egendefinerte claims vil da se slik ut:

```
<AttributeStatement>

...

<Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/employeeId">

<AttributeValue>S5544332211</AttributeValue>

</Attribute>

<Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/roles">

<AttributeValue>vigo-samtykke-enduser</AttributeValue>

</Attribute>

<Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/studentnumber">

<AttributeValue>E1122334455</AttributeValue>

</Attribute>

...

</AttributeStatement>

```

## Logge på en FINT tjeneste
Gå til url'en som er oppgitt for den tjenesten du skal inn på. Dette kan feks være https://flyt.vigoiks.no/"fylkesid" eller https://samtykke.vigoiks.no/"fylkesid"

Hvis du ikke allrede er innlogget i Office365 til fylket vil du bli videresendt til en autentiseringsvelger. Se under:

![](_media/vigo-idp/authSelector.png)

Klikk på pilen i [Velg tilhøringhet]-boksen og velg din fylkeskommune fra listen som dukker opp. Se under:

![](_media/vigo-idp/authSelectorList.png)

Når du har valgt fylkeskommune vil [FORTSETT]-knappen bli grønn. Klikk på denne. Da sendes du til din vanlige pålogging for Office365 til din fylkeskommune. Se under:

![](_media/vigo-idp/authSelectorSelected.png)

Logg deg inn på vanlig måte i Office365. Du vil nå komme inn i tjenesten hvis din fylkeskommune har gitt deg tilgang til det.

## Feilsøking federert FINT-pålogging
### Attributter i SAML-token
Når man logger på en FINT-tjeneste som er federerert (VIGO-IDP) overføres det utvalgte attributter fra fylkets Azure-tennant til Vigo sin access manager. Disse attributtene sendes så videre til tjenesten brukeren skal aksesere. Hvilke attributter som de ulike tjenestene har behov for varierer utifra hvilken tjeneste du skal aksesere. Påse at de attributtene som tjenesten krever ligger i SAML-tokenet som overføres fra fylkenes Azure til Vigo sin access manager.

### Tilgangsroller
For å få tilgang til en federert FINT-tjeneste kreves det ofte at brukeren har fått tildelt en rolle i fylkenes Azure-tennant. Se "Oppsett av Azure AD Federering - VIGO-IDP" ovenfor hvordan dette gjøres. VIGO Iks forvalter disse rollene.

Oversikt over roller finner du her: https://role-catalog.vigoiks.no

### Sjekke SAML-token - SAMLtracer
For å sjekke om de nødvendige attributter overføres fra fylkenes Azure til VIGO sin access manager kan man benytte en SAML-tracer. Dette er ett nettlesertilegg. 
- Innstaller saml-tracer som tilegg i nettleseren din
- Start SAML-tracer og gå til tjenesten i nettleseren
- Se etter SAML taggen på høyre side i SAML-traceren og klikk på denne linjen (er det flere linjer med denne taggen er det oftest den siste linjen vi er ute etter)
- I den nederste ruten klikker du på SAML fanen

Attributtene som overføres i tokenet ligger da mellom 
``` <AttributeStatement> ``` og  ``` </AttributeStatement> ``` taggene.

Se under:

![](_media/vigo-idp/samlTracer.png)





