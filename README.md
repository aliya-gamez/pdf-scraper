# pdf-scraper

This is a python script with `uv`-specific inline metadata. It allows you to run the script easily with `uv` while automatically handling dependencies and environments.

## Running script

> Only if Python and `uv` are installed

```bash
uv run main.py
```

## Installing uv if necessary

Official installation instructions from [uv documentation](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

<details>
  <summary><b>Windows</b></summary>

<br>

```PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

<br>

</details>



<details>
  <summary><b>macOS and Linux</b></summary>

<br>
  
Use `curl` to download the script and execute it with `sh`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have `curl`, you can use `wget`:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

<br>

</details>

## Installing python with uv if necessary

To install the latest Python version:

```bash
uv python install
```

