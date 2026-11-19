"""Refresh the portfolio from the private CV workbook in one step.

Usage (from the repository folder):
    python tools/refresh.py              # regenerate data and pages, check, show what changed
    python tools/refresh.py --preview    # ... then open a local preview (needs Quarto)
    python tools/refresh.py --push       # ... then commit and push (the site rebuilds on GitHub)
    python tools/refresh.py --cv PATH    # use another workbook than the default master

Default workbook: ../99_archive/private_LC_not_for_lab/CV/CV_Luis_Cunha_LC.xlsx
(relative to this repository). The workbook itself never enters the repository.
"""
import argparse, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CV = os.path.normpath(os.path.join(
    ROOT, '..', '99_archive', 'private_LC_not_for_lab', 'CV', 'CV_Luis_Cunha_LC.xlsx'))

# Contact details allowed on the public site; any other e-mail address stops the refresh.
ALLOWED_EMAILS = {'luis.cunha@uc.pt', 'ewormuc@gmail.com', 'noreply@anthropic.com'}
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
PHONE = re.compile(r'(?:\+\d{1,3}[\s-]?)?(?:\d[\s-]?){9,}')
FLAGS = ('TO CONFIRM', 'XXXX')


def run(cmd, check=True):
    print('>', ' '.join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    if check and r.returncode:
        sys.exit(f'Stopped: "{" ".join(cmd)}" failed.')
    return r.returncode


def out(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout


def privacy_check():
    """Scan the generated public files for personal contacts and unconfirmed values."""
    problems = []
    for folder in ('data', '_gen'):
        for name in sorted(os.listdir(os.path.join(ROOT, folder))):
            path = os.path.join(ROOT, folder, name)
            if not os.path.isfile(path):
                continue
            for n, line in enumerate(open(path, encoding='utf-8'), 1):
                if line.lstrip().startswith(('#', '<!--')):
                    continue  # comments are not published
                for m in EMAIL.findall(line):
                    if m.lower().rstrip('.') not in ALLOWED_EMAILS:
                        problems.append(f'{folder}/{name}:{n}: e-mail address "{m}"')
                for m in PHONE.findall(line):
                    digits = re.sub(r'\D', '', m)
                    # DOIs, ISBNs, grant numbers and page ranges are long digit runs too;
                    # only flag phone-like runs (9-13 digits) outside DOIs and links.
                    if 9 <= len(digits) <= 13 and 'doi' not in line.lower() and 'http' not in line and '+' in m:
                        problems.append(f'{folder}/{name}:{n}: looks like a phone number "{m.strip()}"')
                for f in FLAGS:
                    if f in line:
                        problems.append(f'{folder}/{name}:{n}: unconfirmed value "{f}"')
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--cv', default=DEFAULT_CV, help='path to the private CV workbook')
    ap.add_argument('--preview', action='store_true', help='open a local preview after refreshing')
    ap.add_argument('--push', action='store_true', help='commit and push after refreshing')
    ap.add_argument('-m', '--message', default='Refresh CV data', help='commit message for --push')
    a = ap.parse_args()

    try:
        import openpyxl, yaml  # noqa: F401
    except ImportError:
        sys.exit('Missing Python packages. Install once with:  python -m pip install openpyxl pyyaml')
    if not os.path.isfile(a.cv):
        sys.exit(f'CV workbook not found: {a.cv}\nPass another path with --cv PATH')
    if os.path.exists(os.path.join(os.path.dirname(a.cv), '~$' + os.path.basename(a.cv))):
        print('Note: the workbook seems to be open in Excel; unsaved changes will not be included.')

    py = sys.executable
    run([py, 'tools/make_public_data.py', a.cv])
    run([py, 'tools/build_pages.py'])

    problems = privacy_check()
    if problems:
        print('\nStopped: the public files contain something that should not be published:')
        print('\n'.join('  ' + p for p in problems))
        print('Fix the workbook (or the whitelist in tools/make_public_data.py) and run again.')
        sys.exit(1)
    print('\nPrivacy check passed: no personal contacts or unconfirmed values in the public files.')

    if out(['git', 'ls-files', '*.xlsx']).strip():
        sys.exit('Stopped: an .xlsx file is tracked by git. Remove it from the repository first.')

    changes = out(['git', 'status', '--porcelain', '--', 'data', '_gen'])
    if not changes.strip():
        print('Nothing changed on the public site.')
    else:
        print('\nChanged files:')
        print(changes.rstrip())
        print(out(['git', 'diff', '--stat', '--', 'data', '_gen']).rstrip())

    if a.preview:
        run(['quarto', 'preview'], check=False)

    if a.push:
        if changes.strip():
            run(['git', 'add', 'data', '_gen'])
            run(['git', 'commit', '-m', a.message])
        ahead = out(['git', 'rev-list', '--count', '@{u}..HEAD']).strip() or '0'
        if ahead != '0':
            run(['git', 'push'])
            print('Pushed. GitHub rebuilds the site in a few minutes: https://luiscunhamx.github.io/')
        else:
            print('Nothing to push.')
    elif changes.strip():
        print('\nTo publish:  python tools/refresh.py --push   (or commit and push in VS Code)')


if __name__ == '__main__':
    main()
