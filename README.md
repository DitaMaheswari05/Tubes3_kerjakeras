# Running Python Project with `uv` and Virtual Environment

This project uses [`uv`](https://github.com/astral-sh/uv), a fast alternative to `pip` and `virtualenv`.

## Requirements

* Python 3.8 or higher
* `uv` installed on your system. If not, install it using:

```bash
pip install uv
```
## Docker

### 1. Open root directory in terminal
```bash
cd path
```

### 2. Run MySQL container with docker
#### Make sure port 3306:3306 is available
```bash
docker compose up -d
```


## How to Run

### 1. Create and activate virtual environment with `uv`

```bash
uv venv
source .venv/bin/activate  # For bash (Linux/macOS)

# For Windows PowerShell
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Run the application

```bash
uv run src/main.py
```