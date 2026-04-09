# pdf-scraper

This is a python script with `uv`-specific inline metadata. It allows you to run the script easily with `uv` while
automatically handling dependencies and environments.

## Running script

> Only if Python and `uv` are installed

```bash
uv run main.py
```

## Installing uv if necessary

Official installation instructions from [uv
documentation](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

<div>
    <details>
        <summary>Windows</summary>
        <br>
        <p>Open PowerShell and run this command:</p>
        <pre><code>powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"</code></pre>
    </details>
    <details>
        <summary>macOS and Linux</summary>
        <br>
        <p>Use <code>curl</code> to download the script and execute it with <code>sh</code>:</p>
        <pre><code>curl -LsSf https://astral.sh/uv/install.sh | sh</code></pre>
        <p>If your system doesn't have <code>curl</code>, you can use <code>wget</code>:
        </p>
        <pre><code>wget -qO- https://astral.sh/uv/install.sh | sh</code></pre>
        <br>
    </details>
</div>

## Installing python with uv if necessary

To install the latest Python version:

```bash
uv python install
```