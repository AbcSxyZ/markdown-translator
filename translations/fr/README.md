# Traducteur Markdown

**\[Mode développement, création de prototype\]**

**Lang :** [EN](/README.md), [FR](/translations/fr)

Traduction automatique pour les fichiers Markdown versionnés et les dépôts.

## Installation

Obtenez une [clé API à partir de DeepL](https://support.deepl.com/hc/en-us/articles/360020695820-Authentication-Key) en créant un compte.

Le projet utilise à la fois Python et Node.Js, avec des dépendances pour chaque langage.

**Installation de Node.Js :**

```shell
# Node installation
sudo apt-get install nodejs npm

# Node dependencies
npm install turndown
```

**Installation de Python :**

```shell
pip install requests mistletoe
```

## Démarrage

Pour traduire un seul fichier Markdown

```python
import markdown_translator

markdown_text = """
## First title to translate

This is a paragraph with content to translate.
"""

markdown_translator.config(api_key="YOUR-API-KEY")

source_md = markdown_translator.Markdown(markdown_text)
translated_md = source_md.translate(lang_to="FR", lang_from="EN")
translated_md.save("translated-text.md")
print(translated_md)
```

Pour mettre à jour un fichier traduit existant :

```python
# Require to enable versioning
markdown_translator.config(versioning="sql")

# Perform your first translation as explained previously.
# [first translations...]

# Then to update an already translated file
translated_md = Markdown(filename="translated-text.md", restore_hashes=True)
new_version = Markdown(filename="update.md")

translated_md.update(new_version, lang_to="FR", lang_from="EN")
```

Pour gérer les traductions de tous les fichiers Markdown dans un dossier :

```python
import markdown_translator

markdown_translator.config(
        api_key="YOUR-API-KEY",
        dest_lang=["fr"],
        include_files=["include1", "file2"],
        edit_links=False,
        versioning="sql",
        #...
      )

repo = markdown_translator.RepositoryTranslator("src-folder", "dest-folder")
repo.update()
```

## Documentation (en anglais)

Voir la [documentation](docs/README.md) pour plus de détails.

## Tests

Vous devez installer les paquets pip `pytest` et `decorator` afin d'exécuter les tests.

Une clé API est nécessaire pour certains tests. Vous devez configurer un fichier `translations.ini`, voir `translations.template.ini`.

```bash
python -m pytest
```

## Licence

Projet sous licence [GNU Affero General Public License](/translations/fr/LICENSE) (GNU AGPL).
