# Luís Cunha — personal academic portfolio

Source of https://luiscunhamx.github.io/ (Quarto website, published by GitHub Actions on every push to `main`).

## Updating
The CV workbook is private: it lives in `99_archive/private_LC_not_for_lab/CV/CV_Luis_Cunha_LC.xlsx`, is **not** in this repository, and `*.xlsx` is ignored.

After editing the workbook, refresh the site with one command (from this folder):

| Command | What it does |
|:--|:--|
| `python tools/refresh.py` | Regenerates `data/*.yml` and the page sections, runs the privacy check, lists what changed |
| `python tools/refresh.py --preview` | The same, then opens a local preview (needs Quarto) |
| `python tools/refresh.py --push` | The same, then commits and pushes; GitHub rebuilds the site |

On Windows you can also double-click `refresh.bat`, or in VS Code run *Terminal → Run Task → Portfolio: refresh from CV*.

The privacy check stops the refresh if the public files contain an e-mail address other than the UC or lab contact, a phone number, or a value marked `[TO CONFIRM]`. Only the sheets and columns listed in `PUBLIC` (in `tools/make_public_data.py`) are copied; referees, non-approved projects, external services, funding amounts, notes, annexes, courses and the checklist sheets never leave the workbook.

First time only: `python -m pip install openpyxl pyyaml`.

Preview locally: `quarto preview`.

Related: [EnGeL website](https://envigenomics.eu) · [EnGeL protocol handbook](https://luiscunhamx.github.io/EnGeL-Repository/)

Licence: text CC BY 4.0 (LICENSE); code MIT (LICENSE-CODE).
