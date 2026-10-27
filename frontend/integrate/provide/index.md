# Levere data

Adapterne som leverer data til FINT finnes i to ulike generasjoner. Den første generasjonen baserer seg på SSE (server-sent events) hvor FINT er den aktive part og ber normalt om oppdaterte data hvert 15. minutt. Andre generasjons adaptere baserer seg hovedsakelig av REST API hvor leverandøren overfører data på avtalte intervaller.  

Se [Hva ligger hvor](integrate/consume/platforms.md) for hvilke domener som ligger på Core 1 og Core 2.


| Plattform | Dokument                                                  | Beskrivelse                                           |
|:----------|:----------------------------------------------------------|:------------------------------------------------------|
| Core 1    | [Develop adapter](integrate/provide/core1-tutorial.md)    | Hvordan et SSE-adapter fungerer                       |
| Core 1    | [Java adapter](integrate/provide/core1-java-adapter.md)   | Vårt Java-baserte adapterrammeverk                    |
| Core 1    | [.NET adapter](integrate/provide/core1-dotnet-adapter.md) | Vårt .NET-baserte adapterrammeverk                    |
| Core 2    | [Hvorfor Core 2](integrate/provide/core2-why.md)          | Grunnen til at vi har laget en ny generasjon adaptere |
| Core 2    | [Autorelasjon](integrate/provide/core2-autorelation.md)   | Relasjoner FINT bygger automatisk                     |
| Core 2    | [Adapter API](integrate/provide/core2-adapter-api.md)     | Om APIet som adapteret skal snakke med                |
| Core 2    | [Java adapter](integrate/provide/core2-java-adapter.md)   | Vårt Java-baserte adapterrammeverk for Core 2         |

