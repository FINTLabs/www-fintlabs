# Basistest

I kundeportalen ligger det to typer tester som skal brukes for å teste integrasjonene med FINT adapteret.

Den første er en basistest, der du kan sjekke helsestatusen til hver komponent. Test-klienten må ha aktivert felleskomponenten som den skal kjøre basistest mot.

![ill16](../_media/kundeportal-16.jpeg)

Her velger du hvilken komponent du ønsker å sjekke, hvilket miljø og hvilken klient du bruker for å kjøre testen.
Det er viktig å ha en egen testklient for å kjøre testene, som ikke brukes til noen annet, da passordet bli regenerert hver gang.

For å kjøre testen klikker du på det grønne symbolet med en hvit trekant i.

![ill17](../_media/kundeportal-17.jpeg)

Resultatet av testen sier noe om helsen til komponenten, og hvor ferske dataen som ligger der er.
På bildet over ser man en test, som viser en komponent, som kjører og som har oppdaterte data. Komponentene som har oppdaterte data vises med grønt symbol. Her ser man også at det er noen ressurser som ikke er oppdaterte. I dette tilfellet er det fordi disse kompnentene ikke er aktivert i trinn 1 av adapteret.

Man kan også få tilfeller der helsestatusen er grønn, men cachestatusen er oransje. Eller at helsestatus er rød.

![ill18](../_media/kundeportal-18.jpeg)

Hvis helsestatus er grønn og cache er orange, kan det være adapteret nylig har restartet, og man kan vente ca. 15 minutter for å sjekke igjen. Hvis problemet vedvarer, eller om helsestatus er rød, bør man inn på serveren som adapteret er installert på, og restarte tjenestene. Hvis ikke dette hjelper, kan må man kontakte FINT-prosjektet for å undersøke at alt er ok på den siden. I kundeportalen kan du opprette og fylle ut en supportsak fra menyen på venstre side.

