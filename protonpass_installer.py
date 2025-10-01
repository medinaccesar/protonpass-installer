#!/usr/bin/env python3
"""
Descarga, verifica e instala ProtonPass automáticamente en Debian/Ubuntu.
Autor: CésarM
"""

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
import requests
import gettext
import locale

from typing import Dict, Tuple, Callable
from pathlib import Path
from dotenv import load_dotenv


class ProtonPassInstaller:
    BASE_URL = "https://proton.me/download/PassDesktop/linux/x64"
    VERSION_URL = f"{BASE_URL}/version.json"

    def __init__(self, version: str):

        self.version = version
        self.temp_dir = None
        self.mp_to_install = ''
        self.file = None
        self.expected_checksum = None
        self.env = self.get_environment()

    def __enter__(self):
        __version__ = self.get_installed_version(self.env)
        self.temp_dir = tempfile.mkdtemp(prefix="protonpass_")
        self.pm_to_install = ProtonPassInstaller.get_package_manager_type()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()

    def _cleanup(self):

        try:
            if self.file and os.path.exists(self.file):
                os.remove(self.file)
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
        except OSError as e:
            print(_("{} Advertencia: No se han podido limpiar los archivos temporales: {}").format("⚠️", str(e)))

    def _get_version_info(self) -> Dict:

        try:
            print(_("{} Obteniendo la información de las versiones...").format("🔍"))
            response = requests.get(self.VERSION_URL, timeout=30)
            response.raise_for_status()

            version_data = response.json()

            # Buscar la versión específica
            for release in version_data.get("Releases", []):
                if release.get("Version") == self.version:
                    return release

            raise ValueError(_("La versión {} no se ha encontrado en el JSON").format(self.version))

        except requests.RequestException as e:
            raise requests.RequestException(_("Error al obtener la información de las versiones: {}").format(e))

    def _get_pack_info(self, release_info: Dict, ext=".deb") -> Tuple[str, str]:

        files = release_info.get("File", [])
        for file_info in files:
            if file_info.get("Identifier", "").startswith(ext):
                return file_info.get("Url"), file_info.get("Sha512CheckSum")

        raise ValueError(_("No se ha encontrado el archivo {} en la información de la versión").format(ext))

    def _download_file(self, url: str) -> str:

        filename = os.path.basename(url)
        file_path = os.path.join(self.temp_dir, filename)

        print(_("{} Descargando {}...").format("⬇️", filename))

        try:
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print("\r" + _("{} Progreso: {percent:.1f}%").format("📊", percent=percent), end="",
                                  flush=True)
            print("\n" + _("{} Descarga finalizada: {}").format("✅", file_path))
            return file_path

        except requests.RequestException as e:
            raise requests.RequestException(_("Error al descargar el archivo: {}").format(e))

    def _calculate_sha512(self, file_path: str) -> str:

        print(_("{} Calculando la suma de verificación (SHA512)...").format("🔐"))
        sha512_hash = hashlib.sha512()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha512_hash.update(chunk)

        return sha512_hash.hexdigest()

    def _verify_checksum(self, file_path: str, expected_checksum: str) -> bool:

        calculated_checksum = self._calculate_sha512(file_path)

        print(_("{} Suma de verificación esperada:  {}").format("🔍", expected_checksum))
        print(_("{} Suma de verificación calculada: {}").format("🔍", calculated_checksum))

        return calculated_checksum.lower() == expected_checksum.lower()

    def _install_rpm(self, file_path: str) -> bool:

        print(_("{} Instalando ProtonPass desde RPM...").format("📦"))

        try:
            # Usar dnf para instalar el paquete local
            cmd = ['sudo', 'dnf', 'install', '-y', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(_("{} ProtonPass se ha instalado correctamente").format("✅"))
                return True
            else:
                print(_("{} Error durante la instalación del paquete RPM:").format("❌"))
                print(result.stderr)
                return False

        except Exception as e:
            print(_("{} Error inesperado durante la instalación: {}").format("❌", str(e)))
            return False
    def _install_deb(self, file_path: str, force_deps: bool = False) -> bool:

        print(_("{} Instalando ProtonPass...").format("📦"))

        result = self._run_dpkg_install(file_path)

        if result.returncode == 0:
            print(_("{} ProtonPass se ha instalado correctamente").format("✅"))
            return True

        print(_("{} Error durante la instalación:").format("❌"))
        print(result.stderr)
        return False

    def _run_dpkg_install(self, file_path: str) -> subprocess.CompletedProcess:

        return subprocess.run(
            ['sudo', 'dpkg', '-i', file_path],
            capture_output=True,
            text=True,
            check=False
        )
    def install(self, instalar=True) -> bool:

        try:
            if instalar:
                print(_("{} Iniciando la instalación de ProtonPass v{}").format("🚀", self.version))

            version_info = self._get_version_info()
            print(_("{} Se ha obtenido la información de la versión").format("✅"))

            download_url, expected_checksum = self._get_pack_info(version_info, '.' + self.pm_to_install)
            self.expected_checksum = expected_checksum

            self.file = self._download_file(download_url)

            if not self._verify_checksum(self.file, expected_checksum):
                print(_("{} ¡AVISO! La suma de verificación no coincide.").format("❌"))
                print(_("   El archivo descargado podría estar corrupto o comprometido."))
                print(_("   Por seguridad, no se procederá con la instalación.")) if instalar else None
                return False

            print(_("{} La suma de verificación coincide").format("✅"))
            if instalar:
                if self.pm_to_install == 'deb':
                    return self._install_deb(self.file)
                elif self.pm_to_install == 'rpm':
                    return self._install_rpm(self.file)

            return True

        except Exception as e:
            print(_("{} Se ha producido un error durante el proceso: {}").format("❌", str(e)))
            return False

    @staticmethod
    def get_package_manager_type() -> str:
        if os.path.exists('/usr/bin/dnf') or os.path.exists('/usr/bin/yum'):
            return 'rpm'
        if os.path.exists('/usr/bin/apt'):
            return 'deb'
        return ''

    @staticmethod
    def get_environment() -> dict:

        base_path = Path(__file__).parent
        base_locale_path = base_path

        is_pyinstaller = getattr(sys, 'frozen', False)

        is_deb =  False
        if ProtonPassInstaller.get_package_manager_type() == 'deb':
            is_deb = (
                    os.path.exists('/.deb_installed') or
                    str(base_path).startswith(('/usr/', '/opt/'))
            )
        is_local_bin = str(Path(__file__).resolve()).startswith('/usr/local/bin/')
        if is_deb or is_pyinstaller or is_local_bin:
            config_home = Path(os.environ.get('XDG_CONFIG_HOME', '~/.config')).expanduser()
            base_path = config_home / 'mlogicial' / 'protonpass_installer'
            base_locale_path = Path.home() / '.local' / 'share' / 'mlogicial' / 'protonpass_installer'
            if is_pyinstaller:
                base_locale_path = Path(sys._MEIPASS)

        return {
            'is_deb': is_deb,
            'is_pyinstaller': is_pyinstaller,
            'is_system': is_deb,
            'env_type': 'local_bin' if is_local_bin else 'deb' if is_deb else 'pyinstaller' if is_pyinstaller else 'source',
            'base_path': base_path,
            'base_locale_path': base_locale_path
        }

    @staticmethod
    def make_env_file(env_path) -> None:

        if not os.path.exists(env_path):
            env_path.parent.mkdir(parents=True, exist_ok=True)
            locale.setlocale(locale.LC_ALL, '')
            lang_info = locale.getlocale()
            language = lang_info[0] if lang_info and lang_info[0] else 'es'
            with open(env_path, 'w') as f:
                f.write("# Archivo de configuración de idioma\n")
                f.write("IDIOMA=" + language + "\n")
            print("Se ha creado el archivo con los valores por defecto.", env_path)

    @staticmethod
    def check_sudo_permissions() -> bool:

        try:
            subprocess.run(
                ['sudo', '-n', 'true'],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            print(_("{} Error: Se requieren permisos de superusuario para instalar el paquete").format("❌"))
            return False

    @staticmethod
    def get_installed_version(env=None) -> str:

        try:
            if env is None:
                env = ProtonPassInstaller.get_environment()
            version_file = env['base_path'] / 'VERSION'

            return version_file.read_text().strip()
        except:
            return "1.0.0"

    @staticmethod
    def get_languages() -> list:
        env = ProtonPassInstaller.get_environment()
        locale_dir = env['base_locale_path'] / 'locale'
        try:
            return [d for d in os.listdir(locale_dir)
                    if os.path.isdir(os.path.join(locale_dir, d))
                    and d != 'LC_MESSAGES']
        except FileNotFoundError:
            return []

    @staticmethod
    def set_language(lang: str) -> bool:
        available_langs = ProtonPassInstaller.get_languages()
        available_langs.append("es")

        if not lang or not isinstance(lang, str) or lang not in available_langs:
            print("Error: El idioma debe ser uno de los soportados.")
            return False
        try:
            env = ProtonPassInstaller.get_environment()
            env_file = env['base_path'] / '.env'
            config = {}
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            try:
                                key, value = line.split('=', 1)
                                config[key.strip()] = value.strip()
                            except ValueError:
                                continue

            config['IDIOMA'] = lang
            with open(env_file, 'w') as f:
                for key, value in config.items():
                    f.write(f"{key}={value}\n")

            return True

        except Exception as e:
            print(f"No se ha podido actualizar el idioma: {e}", file=sys.stderr)
            return False


def validate() -> bool:
    is_debian = os.path.exists('/etc/debian_version')
    is_fedora = os.path.exists('/etc/fedora-release')
    is_rhel = os.path.exists('/etc/redhat-release')
    if not (is_debian or is_fedora or is_rhel):
        print(_("{} Este «script» está diseñado para sistemas basados en Debian/Ubuntu o Fedora/RHEL").format("❌"))
        return False

    try:
        requests.get('https://proton.me/es-es', timeout=5)
    except requests.RequestException:
        print(_("{} Error: No se puede conectar a internet").format("❌"))
        return False
    return True


def load_conf() -> Callable[[str], str]:
    env = ProtonPassInstaller.get_environment()
    ProtonPassInstaller.make_env_file(env['base_path'] / ".env")
    load_dotenv(dotenv_path=env['base_path'] / '.env', override=True)
    locale_dir = env['base_locale_path'] / 'locale'
    lang = os.getenv('IDIOMA', 'es').strip()
    t = gettext.translation(lang, locale_dir, [lang], fallback=True)
    # if lang == 'es':
    #     t = gettext.translation(lang, locale_dir, [lang], fallback=True)
    # else:
    #     mo_file = locale_dir / lang / 'LC_MESSAGES' / f'{lang}.mo'
    #     with open(mo_file, 'rb') as fp:
    #         t = gettext.GNUTranslations(fp)
    return t.gettext


def main():
    parser = argparse.ArgumentParser(
        description=_("Descarga, verifica e instala ProtonPass automáticamente"),
        epilog=_("Ejemplo: python3 protonpass_installer.py 1.32.5")
    )

    parser.add_argument(
        'version',
        nargs='?',
        help=_('Versión de ProtonPass a instalar (por ejemplo: 1.32.5)')
    )

    parser.add_argument(
        '-n', '--no-install',
        action='store_true',
        help=_('Únicamente descarga y verifica, no instala')
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-ll', '--list-languages',
        action='store_true',
        help=_('Muestra los idiomas disponibles y sale')
    )

    group.add_argument(
        '-l', '--language',
        help=_('Establece el idioma de la aplicación (por ejemplo: -l es) y sale')
    )

    group.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {ProtonPassInstaller.get_installed_version()}',
        help=_('Muestra la versión del programa y sale')
    )

    args = parser.parse_args()

    if args.list_languages:
        print(_("Idiomas disponibles") + ":")
        print("  es")
        for lang in sorted(ProtonPassInstaller.get_languages()):
            print(f"  {lang}")
        sys.exit(0)

    if args.language:
        if ProtonPassInstaller.set_language(args.language):
            print(_("Se ha actualizado el idioma a: {}").format(args.language))
            sys.exit(0)
        else:
            print(_("No se ha podido actualizar el idioma"))
            sys.exit(1)

    if not args.version:
        parser.print_help()
        sys.exit(1)

    # Instalar ProtonPass
    with ProtonPassInstaller(args.version) as installer:

        success = False

        if args.no_install:
            print(_("{} Se activa el modo de verificación, no se instalará la aplicación").format('✅'))
            installer.install(False)
            sys.exit(0)

        if ProtonPassInstaller.check_sudo_permissions():
            success = installer.install()

        if success:
            print("\n" + _("{} ¡ProtonPass se ha instalado correctamente!").format("🎉"))
            print(_("   Puedes encontrarlo en el menú de aplicaciones o ejecutar 'proton-pass'"))
            sys.exit(0)
        else:
            print("\n" + _("{} Ha fallado la instalación. Revisa los errores anteriores.").format("💥"))
            sys.exit(1)


if __name__ == "__main__":
    global _
    _ = load_conf()

    if not validate():
        sys.exit(1)

    main()
