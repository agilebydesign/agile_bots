# Secrets Directory

This directory contains sensitive configuration files that should not be committed to version control.

## Cursor API Key Configuration

To use headless mode, create a file named `cursor_api_key.txt` in this directory containing your Cursor API key:

```
sk-your-api-key-here
```

Alternatively, you can set the `CURSOR_API_KEY` environment variable or create a `headless_config.json` file:

```json
{
  "api_key": "sk-your-api-key-here",
  "log_dir": "logs"
}
```

Then set the `HEADLESS_CONFIG_PATH` environment variable to point to this file.

