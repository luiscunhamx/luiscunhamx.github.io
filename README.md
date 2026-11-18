# Luís Cunha — personal academic portfolio

Source of https://luiscunhamx.github.io/ (Quarto website, published by GitHub Actions on every push to `main`).

## Updating
1. Keep the CV workbook (`cv.xlsx`) private — it is **not** in this repository and `*.xlsx` is ignored.
2. After editing it, refresh the public data: `python tools/make_public_data.py PATH/TO/cv.xlsx`
   Only the sheets and columns listed in `PUBLIC` (in that script) are copied to `data/*.yml`.
   Referees, non-approved projects, external services, funding amounts, notes and annexes never leave the workbook.
3. Check the diff of `data/`, commit and push. The site rebuilds itself.

Preview locally: `quarto preview`.

Related: [EnGeL website](https://envigenomics.eu) · [EnGeL protocol handbook](https://luiscunhamx.github.io/EnGeL-Repository/)

Licence: text CC BY 4.0 (LICENSE); code MIT (LICENSE-CODE).
