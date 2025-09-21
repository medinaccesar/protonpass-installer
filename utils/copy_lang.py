
from pathlib import Path
import shutil
import argparse

def copy_locale_files(force = False) -> None:

        source_locale_dir = Path(__file__).parent.parent / 'locale'
        if not source_locale_dir.exists():
            print(f"Advertencia: No se encontró el directorio de idiomas: {source_locale_dir}")
            return

        base_locale_path = Path.home() / '.local' / 'share' / 'mlogicial' / 'protonpass_installer'
        target_locale_path = base_locale_path / 'locale'

        if target_locale_path.exists() and not force:
            print(f"Advertencia: Los archivos de idioma ya existen en: {target_locale_path}")
            print("Use el parámetro --force para sobreescribirlos")
            return

        target_locale_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copytree(
                source_locale_dir,
                target_locale_path,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('*.po')
            )
            print(f"Se han copiado los archivos de idioma a: {target_locale_path}")
        except Exception as e:
            print(f"Error al copiar los archivos de idioma: {e}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Copiar archivos de idioma')
    parser.add_argument('-f','--force', action='store_true',
                        help='Sobrescribir archivos existentes')

    args = parser.parse_args()
    copy_locale_files(force=args.force)