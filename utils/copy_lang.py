
from pathlib import Path


def copy_locale_files(env:dict) -> None:
        base_locale_path = Path.home() / '.local' / 'share' / 'mlogicial' / 'protonpass_installer'

        target_locale_path = base_locale_path /  'LC_MESSAGES'

        if target_locale_path.exists():
            return

        source_locale_dir = Path(__file__).parent.parent / 'locale'
        if not source_locale_dir.exists():
            print(f"Advertencia: No se encontró el directorio de idiomas: {source_locale_dir}")
            return

        target_locale_path.parent.mkdir(parents=True, exist_ok=True)

        for source_file in source_locale_dir.rglob('*.mo'):
            relative_path = source_file.relative_to(source_locale_dir)
            target_file = target_locale_path.parent / relative_path

            target_file.parent.mkdir(parents=True, exist_ok=True)

            with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                dst.write(src.read())

        print(f"Se han copiado los archivos de idioma a: {target_locale_path}")

if __name__ == "__main__":

    copy_locale_files()