# Markout

[![License](https://img.shields.io/badge/license-MIT-informational.svg)](https://opensource.org/licenses/MIT)

A small Python script I made to extract Markdown from HTML pages. It is very customizable and I made to suit my needs (extract many pages code in Markdown, but only some tags). Due to its purpose being to be able to convert specific HTML tags into a disered Markdown format, this script does not generate standard Markdown, rather, it uses custom tokens specified by you.

### Configuration

All configurations are put into a single file `.markourc.json` (you can specify another one). If you don't load a configuration file the script will use its default values.

**Configurations:**
The examples below are the same values set on the `.markourc.json` that is in this repository.
`links` - object of links to extract, each link has a destination (path) value.
Example:

``
{
  "links": {
    "http://cursos.unipampa.edu.br/cursos/ppges/": "out/sobre.md"
  }
}
``

The example above will get the HTML from `http://cursos.unipampa.edu.br/cursos/ppges/` and extract the Markdown into `out/sobre.md`.

`only_on` - string that specify where (which tag) to extract the results from (e.g. : html, body, main).
Example:

``
{
  "only_on": "article"
}
``

`tokens` - object in which each specified HTML tag will be replaced with a formatable Markdown string.
Example:

``
{
  "tokens": {
    "header": "# {}",
    "h1": "\n# {}",
    "h2": "\n# {}",
    "b": "\n## {}",
    "li": "+ {}",
    "i": "** {} **",
    "p": "\n{}",
    "span": "{}"
  }
}
``

On the example above, the HTML tag `<header>` will be replaced with `#` and its contents will be put after that (the `{}` represents the contents and it will be formated).   

### Running

To run this script, you will need `Python 3` installed. After that, just run the commands below:

``
pip install -r requirements.txt
python markout.py
``

### Final Thogths

Feel free to leave your contribution here, I would really appreciate!
Also, if you have any doubts or troubles using this script just contact me or leave a issue.
