
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```shell
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"
uv venv --python=3.12 .venv 
source .venv/bin/activate
uv sync
uv pip install -r requirements.txt
uv run alembic upgrade head
uv run fastapi dev app/main.py --host 0.0.0.0 --port 8000
```

```shell
uv run alembic revision -m "Added posts table"
uv run alembic upgrade head


uv run python -m commands.generate_openapi_schema
```
