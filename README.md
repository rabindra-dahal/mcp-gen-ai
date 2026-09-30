# Enterprise Ledger Model Context Protocol (MCP) Security Gateway

A production-grade **Model Context Protocol (MCP)** server built in Python using the **FastMCP** framework. This server showcases LLM-centric runtime integration, strict Pydantic tool schema validation, JSON Web Token (JWT) bearer authentication, and granular runtime user scoping.

## 🚀 Key Features

*   **Semantic Tool Schema Design:** Implements strict data validations, type safety, and boundaries using Pydantic fields that LLM engines interpret natively at runtime.
*   **Zero-Trust Authorization & Scoping:** Features a dynamic validation gate (`require_scope`) that inspects inbound JWT claims before allowing tool execution.
*   **Multi-Transport Support:** Ready for local development workflows via standard input/output (`stdio`) and production multi-agent setups via Streamable HTTP (ASGI).

---

## 🛠️ Project Structure

```text
mcp-gen-ai/
├── app/
│   ├── __init__.py
│   ├── auth.py      # Token decoding and token scope verification logic
│   ├── schemas.py   # Strict Pydantic schemas (LLM semantic layer)
│   └── main.py      # FastMCP application and tool orchestration
├── .gitignore       # Prevents checking in environments and secrets
├── Dockerfile       # Container definition for cloud deployment
└── README.md        # Documentation
```

---

## 📦 Local Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.10+ installed. Install the official MCP client tools and framework packages:

```bash
pip install "mcp[cli]" fastmcp pydantic python-jose uvicorn
```

### 2. Set the Environment Path
To ensure internal package dependencies resolve correctly during execution, set your python path in your terminal:

```powershell
# Windows (PowerShell)
$env:PYTHONPATH="."

# macOS / Linux
export PYTHONPATH=.
```

---

## 🔬 Local Verification & Testing

### Option A: The FastMCP Interactive Inspector Dashboard
Run the visual inspector tool to safely test parameters, monitor raw JSON-RPC traffic, and manually invoke tools:

```bash
fastmcp dev inspector app/main.py
```
Open **`http://localhost:5173`** in your browser to interact with the visual dashboard.

### Option B: Core Process Stdio Launch
To run the server in raw process execution mode (waiting for standard input/output command hooks):

```bash
python -m app.main
```

---

## 🔌 IDE Integration (Cursor / VS Code)

To link this active server framework directly into an AI agent window for natural language prompting:

### Cursor
1. Navigate to **Cursor Settings** -> **Models** -> **MCP**.
2. Click **+ Add New MCP Server**.
3. Set the fields:
   * **Name:** `EnterpriseLedger`
   * **Type:** `command`
   * **Command:** `python -m app.main`

### VS Code (Cline / Roo Clinic Extensions)
Add the configuration block into your global `mcp_settings.json` file:

```json
{
  "mcpServers": {
    "enterprise-ledger": {
      "command": "python",
      "args": ["-m", "app.main"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

---

## 🛡️ Tool Capabilities & Permissions

| Tool Name | Scope Required | Risk Profile | Intent / Purpose |
| :--- | :--- | :--- | :--- |
| `inspect_corporate_ledger` | `audit:read` | Low | Inspects historic logs within specific timeframe filters. |
| `flag_and_freeze_account` | `admin:write` | High (Mutating) | Places an operational freeze lock on malicious accounts. |

---

## 🐳 Production Deployment

Build the optimized server microservice as an isolated container:

```bash
docker build -t mcp-ledger-gateway:latest .
```

Deploy the container behind an HTTPS endpoint onto your infrastructure cloud provider (such as AWS ECS, Kubernetes, or Render). The container launches an asynchronous ASGI engine via Uvicorn exposing the `/mcp` network protocol endpoint.
