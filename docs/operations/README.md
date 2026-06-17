# Operations and Reliability

## MCP Server 503 Troubleshooting Under Evaluation Load

If Azure App Service returns frequent 503 errors during concurrent evaluation runs, one common root cause is runtime worker saturation, not Cosmos DB RU exhaustion.

### Why It Happens

When gunicorn runs with a single worker, all incoming requests are funneled through one process and one event loop. Under high parallel evaluation load, requests queue faster than they are completed and App Service eventually returns 503 for backlog and timeout protection.

### Gunicorn Production Tuning Used in This Project

This project uses [src/wealth-data-mcp/gunicorn.conf.py](../../src/wealth-data-mcp/gunicorn.conf.py):

- workers = (cpu_count * 2) + 1
- worker_class = uvicorn.workers.UvicornWorker
- timeout = 120
- max_requests = 1000
- max_requests_jitter = 50

### Why Each Setting Matters

| Setting | Purpose |
|---------|---------|
| workers | Enables multiple independent worker processes so concurrent evaluation requests are distributed instead of serialized behind one worker. |
| worker_class | Uses Uvicorn ASGI workers, required for efficient async FastAPI or FastMCP handling. |
| timeout | Recycles workers stuck on slow calls and avoids long-lived hung workers. |
| max_requests | Periodically recycles workers to mitigate gradual memory growth in long-running containers. |
| max_requests_jitter | Staggers worker restarts to avoid synchronized restart gaps. |

### Production Guardrail: Disable Reload

`reload` should only be enabled for local development. In production, reload creates file-watch overhead and can trigger unnecessary worker restarts.

In [src/wealth-data-mcp/gunicorn.conf.py](../../src/wealth-data-mcp/gunicorn.conf.py):

```python
if not os.getenv("RUNNING_IN_PRODUCTION"):
    reload = True
```

In [infra/core/web/web.bicep](../../infra/core/web/web.bicep), set:

- RUNNING_IN_PRODUCTION = true

This keeps local DX convenient while ensuring stable production runtime behavior.
