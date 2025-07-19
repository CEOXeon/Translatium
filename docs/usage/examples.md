# Examples

## Preparation of Translations

Name the translation files `<language_code>.yml` or `<language_code>.json` and place them in the `locales` directory.
For example, for English, you would create a file named `en.yml` or `en.json`.

### YAML

```yaml
hello_message: "Hello, world!"
```

### JSON

```json
{
  "hello_message": "Hello, world!"
}
```

## Example 1: Basic Translation

```python
from translatium import Translator
translator = Translator(LOCALES_PATH, used_language, fallback_language) # i.e.: Translator("locales/", "en", "en")
result = translator.translate("hello_message")
print(result)

# Output
> Hello, world!
```
