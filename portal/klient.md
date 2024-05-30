# Klienter

Menyvalgene Adapter og Klienter fungerer på samme måte, men de skiller seg basert på hvilket grensesnitt i felleskomponenten de har tilgang til. Adaptere får tilgang til Provider-grensesnittet og kan levere data til felleskomponenten, mens Klienter får tilgang til Consumer-grensesnittet og kan hente data fra felleskomponenten. Adaptere leverer vanligvis data til én komponent, mens Klienter kan hente data fra flere komponenter.

## Opprette en ny klient

Følg denne veiledningen for å opprette en ny FINT-klient. Denne kan brukes i [Testklient](technical/testclient.md), verktøy for å teste API-er som Postman eller Insomnia, eller for å opprette OAuth2-klienter i skreddersydde integrasjonstjenester.

?> Det er anbefalt å opprette en egen klient for hvert formål, dvs. ikke gjenbruke den samme klienten til forskjellige oppgaver. Hvis du endrer en klient som er i bruk, kan det føre til at integrasjonen slutter å fungere. Funksjonene **Basistest** og **Relasjonstest** i kundeportalen kan automatisk endre passord på klienten, så vi anbefaler at du ALLTID bruker egne klienter for disse funksjonene.

![ill11](../_media/kundeportal-11.png)

For å legge til en klient så klikker man på det store grønne symbolet med en svart plus i.

![ill12](../_media/kundeportal-12.png)

Fremgangsmåten her er ganske lik den som var for Adapter. Man legger til et brukernavn, som får ditt fylkes domenenavn bak. Den vi lager på bildet, er i første omgang en klient for å kjøre tester, så vi har kalt den basictestclient@mrfylke.no for Møre og Romsdal. Det er viktig at denne ikke blir gitt samme brukernavn som ble brukt i adapteroppsettet. Den korte beskrivelsen, er det som kommer opp som navn på klienten, i listen over klienter. Fyll ut og legg til.

Deretter klikker man på det grå edit-symbolet, som er en blyant, for å sette opp innstillingene til klienten.

![ill13](../_media/kundeportal-13.png)

På første fane kan kan endre beskrivelse og Note.

![ill14](../_media/kundeportal-14.png)

På fanen Komponenter kan man legge til de komponentene som skal kobles til klienten. For en testklient velger man alle komponenter som skal testes. Her klikker man på grønt symbol med en pluss for å koble til, eller et rødt symbol med en minus for å koble fra. Deretter går man videre til Autentisering.

![ill15](../_media/kundeportal-15.png)

På samme måte som for Adapter, må Passord og Klient Hemmelighet genereres manuelt, ved å klikke på symbolene nest bakerst på linjen. Disse autentiseringsdataene må man oppgi til de som skal teste FINT med f.eks. FINTs testklient (<https://www.fintlabs.no/#/test-klient).> Det er ikke denne informasjonen som brukes for å sette opp adapteret mot f.eks HR. Da må du bruke informasjonen fra adapteroppsettet.
