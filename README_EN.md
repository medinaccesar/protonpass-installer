# protonpass-installer

![Status](https://img.shields.io/badge/Status-Stable-yellow?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/Licence-GPL_v3-blue.svg?style=for-the-badge)

🇺🇸 English | [🇪🇸 Versión en español](README.md)

## 📋 Description

Automatically download, verify, and install ProtonPass in linux (Debian/Ubuntu and Fedora/RHEL)

## ✨ Features

- ✅ **Download** the specified version of the ProtonPass installer
- 🔍 **Verify the integrity** of the installer (checksum)
- 🚀 **Automatically run** the installer
- 🌍 **Multi-language support** (internationalization with gettext)

## 🛠️ Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## 📦 Installing dependencies

```
    pip install -r requirements.txt
```

## 🚀 Use
```
usage: protonpass_installer.py [-h] [-n] [-ll | -l LANGUAGE | -v] [version]

Automatically download, verify, and install ProtonPass

positional arguments:
  version               ProtonPass version to install (e.g.: 1.32.5)

options:
  -h, --help            show this help message and exit
  -n, --no-install      Only download and verify, do not install 
  -ll, --list-languages
                        Displays the available languages and exits
  -l LANGUAGE, --language LANGUAGE
                        Sets the application language (e.g., -l es) and exits
  -v, --version         Displays the program version and exits



```
For example: 
* **Install a specific version :**
```
python3 protonpass_installer.py 1.32.6

🚀 Starting installation of ProtonPass v1.32.6
🔍 Retrieving version information...
✅ Version information obtained
⬇️ Downloading proton-pass_1.32.6_amd64.deb...
📊 Progress: 100.0%
✅ Download complete: /tmp/protonpass_4um36w21/proton-pass_1.32.6_amd64.deb
🔐 Calculating checksum (SHA512)...
🔍 Expected checksum:   6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
🔍 Calculated checksum: 6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
✅ The checksum matches
📦 Installing ProtonPass...
✅ ProtonPass has been installed successfully

🎉 ProtonPass has been installed successfully!
   You can find it in the applications menu or run 'proton-pass'


```
* **Verify a specific version :**
```
python3 protonpass_installer.py 1.32.6 -n

✅ verify-only mode enabled
🔍 Retrieving version information...
✅ Version information obtained
⬇️ Downloading proton-pass_1.32.6_amd64.deb...
📊 Progress: 100.0%
✅ Download complete: /tmp/protonpass_uobbk5_3/proton-pass_1.32.6_amd64.deb
🔐 Calculating checksum (SHA512)...
🔍 Expected checksum:   6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
🔍 Calculated checksum: 6aacd53738514a29317a0340281120e3171b46233121e26cbf21500d04de82432de4d2ab41522a8fa61df2fa04a860b40ffa3ddc6dba079c53c2ce1b3771c69d
✅ The checksum matches
```

## 💻 Installation methods
* **Manual installation:**
   - Step 1:
        ```
        # Compile languages
        python3 ./utils/compile_lang.py
        
        # Copy them to the system
        python3 ./utils/copy_lang.py
        ```
   - Step 2:
        ```bash
        # Copy it to the system
        sudo cp ./protonpass_installer.py /usr/local/bin/protonpass-installer
        # Give it execution permissions
        sudo chmod +x /usr/local/bin/protonpass-installer
        # Now you can run it from any location
        protonpass-installer -h
        ```


## 🌍 Internationalitation

The script supports multiple languages using gettext. The translation files are located in the locales/ folder.
**The `.env` configuration file with the preferred language is automatically created during the first run** of the program.
Available languages:

    🇪🇸 Spanish (default)
    🇺🇸 English        
    🇩🇪 German
    🇫🇷 French
    🇮🇹 Italian
    🇵🇹 Portuguese
    🇳🇱 Dutch
    🇵🇱 Polish
    🇷🇴 Romanian
    🇷🇺 Russian
    🇧🇬 Bulgarian
    🇸🇪 Swedish
    🇸🇦 Arabic
    🇨🇳 Chinese
    🇬🇷 Greek
    🇭🇺 Hungarian
    

### Automatic configuration
When first run, the script:
1. ✅ Detects the operating system language
2. ✅ Creates the `.env` file with the language settings
3. ✅ The script allows you to set another language later

### List available languages
```
   python3 protonpass_installer.py -ll
   ```
### Change language
 You can set another language from those available.
  ```
   python3 protonpass_installer.py -l en
   ```
### Contribute with translations
1. Edit the .po file in: locales/[language]/LC_MESSAGES/
   If the language does not exist, add it using the same file structure.
2. Compile the translations:
 ```
   python3 ./utils/compile_lang.py 
   ```
## 📄 License

This project is licensed under GPL v3. See the [LICENSE](LICENSE) file for more details.

## 🆘 Support

If you find any errors or have suggestions or questions:
   
1. 📧 Open a [issue](https://github.com/medinaccesar/protonpass-installer/issues)


