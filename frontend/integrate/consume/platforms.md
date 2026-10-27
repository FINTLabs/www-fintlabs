# Hva ligger hvor

Siden viser hvilke domener og pakker som kommer fra Core 1, og hvilke som kommer fra [Core 2](integrate/consume/core2.md), 
i produksjon (`api.felleskomponent.no`). Klienter bruker de samme adressene uansett plattform, og FINT sender hver forespørsel 
videre til riktig sted.

## Bare Core 1

| Domene        | Pakker                                                           |
|:--------------|:-----------------------------------------------------------------|
| `arkiv`       | `kodeverk`, `kulturminnevern`, `noark`, `personal`, `samferdsel` |
| `felles`      | `kodeverk`                                                       |
| `okonomi`     | `faktura`, `kodeverk`                                            |
| `profilbilde` |                                                                  |

## Både Core 1 og Core 2

| Domene           | Pakker                                                           | Plattform                                                           |
|:-----------------|:-----------------------------------------------------------------|:--------------------------------------------------------------------|
| `administrasjon` | `fullmakt`, `kodeverk`, `organisasjon`, `personal`               | Core 2 for Rogaland, Telemark, Trøndelag og Vestfold, ellers Core 1 |
| `utdanning`      | `elev`, `kodeverk`, `timeplan`, `utdanningsprogram`, `vurdering` | Versjon 3 fra Core 1, versjon 4 fra Core 2                          |

For `utdanning` velges versjonen for klienten i Kundeportalen, og en enkelt forespørsel kan be om den andre versjonen. Se 
[Versjon 3 og 4 av informasjonsmodellen](integrate/consume/core2.md?id=versjon-3-og-4-av-informasjonsmodellen).

## Bare Core 2

| Domene       | Pakker                             |
|:-------------|:-----------------------------------|
| `okonomi`    | `regnskap`                         |
| `personvern` | `kodeverk`, `samtykke`             |
| `ressurs`    | `datautstyr`, `eiendel`, `tilgang` |
| `utdanning`  | `larling`, `ot`                    |

## Beta

I beta (`beta.felleskomponent.no`) kommer hele `utdanning` fra Core 2, så der finnes bare versjon 4. Resten er som i produksjon.

## For leverandører

Domener på Core 1 leveres med et Core 1-adapter, og domener på Core 2 med et Core 2-adapter. Se [Levere data](integrate/provide/index.md).
