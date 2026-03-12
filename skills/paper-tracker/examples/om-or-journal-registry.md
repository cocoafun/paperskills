# Journal Registry

This file is example-specific. It is not part of the core `paper-tracker` contract.

Use this file when the user asks about the operations-management / operations-research journal bundle in this repo.

The point of this registry is to avoid weak free-text matching. Resolve journals to stable identifiers first.

| Journal | ISSN / eISSN | Publisher hint |
| --- | --- | --- |
| Management Science | 0025-1909 / 1526-5501 | INFORMS |
| Operations Research | 0030-364X / 1526-5463 | INFORMS |
| Manufacturing & Service Operations Management | 1523-4614 / 1526-5498 | INFORMS |
| Production and Operations Management | 1059-1478 / 1937-5956 | SAGE / POMS |
| Journal of Operations Management | 0272-6963 / 1873-1317 | Wiley |
| Omega-International Journal of Management Science | 0305-0483 | Elsevier |
| INFORMS Journal on Computing | 0899-1499 / 1526-5528 | INFORMS |
| Annals of Operations Research | 0254-5330 / 1572-9338 | Springer |
| European Journal of Operational Research | 0377-2217 / 1872-6860 | Elsevier |
| International Journal of Production Economics | 0925-5273 / 1873-7579 | Elsevier |
| International Journal of Production Research | 0020-7543 / 1366-588X | Taylor & Francis |

## Notes

- Some publishers expose only one ISSN cleanly through Crossref journal endpoints. Try both print and electronic ISSNs, then dedupe by DOI.
- INFORMS and Wiley pages may block terminal clients. When blocked, do not infer absence from the HTML response alone.
- Elsevier journals often lag between visible article pages and Crossref registration. Mark low-confidence gaps explicitly.
