# protonpass-installer

![Estado](https://img.shields.io/badge/Estado-Estable-yellow?style=for-the-badge)
![Versión](https://img.shields.io/badge/Versión-1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Licencia](https://img.shields.io/badge/Licencia-GPL_v3-blue.svg?style=for-the-badge)

  🇪🇸 Español | [🇺🇸 English Version](README_EN.md)

## 📋 Descripción

Descarga, verifica e instala ProtonPass automáticamente en Debian/Ubuntu

## ✨ Características

- ✅ **Descarga** de la versión indicada del instalador de ProtonPass
- 🔍 **Verificación de la integridad** del mismo (checksum)
- 🚀 **Ejecución automática** del instalador
- 🌍 **Soporte multiidioma** (internacionalización con gettext)
- ⚡ **Interfaz de línea de comandos** intuitiva

## 🛠️ Requisitos previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Conexión a internet para que pueda descargar el instalador oficial de ProtonPass
- Se necesita permiso de superusuario para instalar el paquete (ejecutar con 'sudo')

## 📦 Instalación de dependencias

```
    pip install -r requirements.txt
```

## 🚀 Uso
```
usage: protonpass_installer.py [-h] [-n] [-f] [-ll | -l LANGUAGE | -v] [version]

Descarga, verifica e instala ProtonPass automáticamente

positional arguments:
  version               Versión de ProtonPass a instalar (por ejemplo: 1.32.5)

options:
  -h, --help            show this help message and exit
  -n, --no-install      Únicamente descarga y verifica, no instala
  -f, --force-deps      Forzar la instalación de dependencias
  -ll, --list-languages
                        Muestra los idiomas disponibles y sale
  -l LANGUAGE, --language LANGUAGE
                        Establece el idioma de la aplicación (por ejemplo: -l es) y sale
  -v, --version         Muestra la versión del programa y sale


```
Por ejemplo: 
* **Instalar una versión específica :**
```
python3 protonpass_installer.py 1.32.6

🚀 Iniciando la instalación de ProtonPass 1.32.6
🔍 Obteniendo la información de las versiones...
✅ Se ha obtenido la información de la versión
⬇️ Descargando proton-pass_1.32.6_amd64.deb...
📊 Progreso: 100.0%
✅ Descarga finalizada: /tmp/protonpass_iv04w4mb/proton-pass_1.32.6_amd64.deb
🔐 Calculando la suma de verificación (SHA512)...
🔍 Suma de verificación esperada:  6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
🔍 Suma de verificación calculada: 6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
✅ La suma de verificación coincide
📦 Instalando ProtonPass...
✅ ProtonPass se ha instalado correctamente

🎉 ¡ProtonPass se ha instalado correctamente!
   Puedes encontrarlo en el menú de aplicaciones o ejecutar 'proton-pass'

```
* **Verificar una versión específica :**
```
python3 protonpass_installer.py 1.32.6 -n

✅ Se activa el modo de verificación, no se instalará la aplicación
🔍 Obteniendo la información de las versiones...
✅ Se ha obtenido la información de la versión
⬇️ Descargando proton-pass_1.32.6_amd64.deb...
📊 Progreso: 100.0%
✅ Descarga finalizada: /tmp/protonpass_iv04w4mb/proton-pass_1.32.6_amd64.deb
🔐 Calculando la suma de verificación (SHA512)...
🔍 Suma de verificación esperada:  6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
🔍 Suma de verificación calculada: 6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
✅ La suma de verificación coincide
```
* **Listar los idiomas disponibles :**
```
python3 protonpass_installer.py -ll
```
* **Establecer un idioma (de entre los disponibles) :**
```
python3 protonpass_installer.py -l it
```
## 💻 Formas de instalación
* **Instalación manual :**
  - Paso 1:
    ```
    # Compilar los idiomas
    python3 ./utils/compile_lang.py
    
    # Copiarlos en el sistema
    python3 ./utils/copy_lang.py
    ```
  - Paso 2:
    ```bash
    # Copiarlo en el sistema
    sudo cp ./protonpass_installer.py /usr/local/bin/protonpass-installer
    # Darle permisos de ejecución
    sudo chmod +x /usr/local/bin/protonpass-installer
    # Ahora se puede ejecutar desde cualquier ubicación
    protonpass-installer -h
    ```
* **Otras formas de instalación :**


   -**PyInstaller:** Se puede generar un ejecutable usando PyInstaller.

   -**Paquete .deb:** Se puede crear un paquete instalable para distribuciones basadas en Debian/Ubuntu.

## 🌍 Internacionalización

El script soporta múltiples idiomas mediante gettext. Los archivos de traducción se encuentran en la carpeta locales/.
**El archivo de configuración `.env` con el idioma preferido se crea automáticamente durante la primera ejecución** del programa.

### Idiomas disponibles:

    🇪🇸 Español (predeterminado)
    🇺🇸 Inglés    
    🇩🇪 Alemán
    🇫🇷 Francés
    🇮🇹 Italiano
    🇵🇹 Portugués
    🇳🇱 Neerlandés
    🇵🇱 Polaco
    🇷🇴 Rumano
    🇷🇺 Ruso
    🇧🇬 Búlgaro
    🇸🇪 Sueco
    🇸🇦 Árabe
    🇨🇳 Chino

### Configuración automática
En la primera ejecución, el script:
1. ✅ Detecta el idioma del sistema operativo
2. ✅ Crea el archivo `.env` con la configuración de idioma
3. ✅ Permite la personalización posterior 

### Listar los idiomas disponibles
 ```
   python3 protonpass_installer.py -ll
   ```

### Cambiar de idioma
 Se puede establecer otro idioma de entre los disponibles.
 ```
   python3 protonpass_installer.py -l en
   ```

### Contribuir con las traducciones

1. Se edita el archivo .po en: locales/[idioma]/LC_MESSAGES/
   Si el idioma no existe se añade manteniendo la misma estructura de archivos.
2. Se compilan las traducciones:
 ```
   python3 ./utils/compile_lang.py 
   ```
## 📄 Licencia

Este proyecto está bajo la licencia GPL v3. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

Si encuentras algún error o tienes sugerencias o preguntas:
   
1. 📧 Abre un [issue](https://github.com/medinaccesar/protonpass-installer/issues)

## Líneas futuras
1. ✅ Soportar rpm (Fedora/RHEL)
