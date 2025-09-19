import os
import subprocess
from pathlib import Path

utils_dir = Path(__file__).resolve().parent
locale_dir = utils_dir / '..' / 'locale'


def compile_po_files():
    for root, dirs, files in os.walk(locale_dir):
        print(root, 'rooo')
        for file in files:
            if file.endswith('.po') and root is not locale_dir:
                po_file = os.path.join(root, file)
                # lang = os.path.splitext(po_file)[1][1:]
                print('Se compila', root)
                mo_file = po_file.replace('.po', '.mo')
                msgfmt_cmd = f'msgfmt {po_file} -o {mo_file}'
                subprocess.call(msgfmt_cmd, shell=True)


if __name__ == "__main__":
    compile_po_files()