# Markout

[![License](https://img.shields.io/badge/license-MIT-informational.svg)](https://opensource.org/licenses/MIT)

A small Python package I made to extract HTML content from web pages. It is very customizable and I made it to fit my needs (extract multiple pages' code to Markdown, but only some HTML tags I needed). Due to its purpose being able to convert specific HTML tags into a desired Markdown format this script does not generate any standard output, rather, it uses custom tokens specified in a configuration file, so the output can be formated into any anything.

## Usage

### Importing into your code

To use this package you'll need to install it using `pip`:

```sh
pip install markout-html
```

Then just import it into your code:

```python
import markout-html
```

After that you can use the `extract` function:

```python
result = markout-html.extract(
  # HTML page link
  'http://example.page.com/blog/some_post.html',

  # Tokens to format each HTML tags contents (you can extract only the ones you want)
  {
    'p': "\n** {} **"
  },

  # Only extract contents inside this tag
  'article'
)
```

### Using the CLI command

Below are a few examples with better description on how to use this package command if you don't want to create a Python script:

#### Configuration

All configurations can be found into a single file: `.markoutrc.json` (you can specify another name in the terminal), if you don't load a configuration file the script will use its default values. There is an example of configuration in the repository root!

To specify a different configuration file use:

```sh
markout <file_name>
```

#### The configuration file values

`links` - *object* of links to be extracted, each link has a destination value (output file).
Example:

```json
{
  "links": {
    "http://example.page.com/blog/some_post.html": "out/post.md",
    "http://example.page.com/blog/some_other_post.html": "out/other_post.md"
  }
}
```

The example above will get the HTML from `http://example.page.com/blog/some_post.html` and extract the results into `out/post.md`.

`only_on` - *string* that specify where (which HTML tag) to extract the contents from (e.g. : html, body, main).
Example:

```json
{
  "only_on": "article"
}
```

`tokens` - *object* in which each specified HTML tag will be extract into a formatted string and then placed on the output file.
Example:

```json
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
```

On the example above, the contents of the HTML tag `<header>` will be extract into the `# {}` string, so for example, if we had `<header>Some text here!</header>` the result would've been `# Some text here!` (this formats the text into Markdown).

---

## Contributions

Feel free to leave your contribution here, I would really appreciate it!
Also, if you have any doubts or troubles using this package just contact me or leave an issue.
