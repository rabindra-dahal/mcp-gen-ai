# app/main.py

# 1. THIS MUST GO FIRST: Adjust Python path before importing local modules
import sys
from pathlib import Path

root_path = str(Path(__file__).resolve().parent.parent)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# 2. NOW standard and local imports will resolve perfectly
import os
from fastmcp import FastMCP
from app.schemas import FinancialAuditQuery
from app.auth import require_scope

# Initialize the server instance
mcp = FastMCP(
    name="Enterprise Ledger MCP Security Gateway",
    version="1.0.0"
)

@mcp.tool(auth=[require_scope("audit:read")])
def inspect_corporate_ledger(query: FinancialAuditQuery) -> str:
    """
    Fetches historical financial ledger entries mapping to an account sequence. 
    Use this tool exclusively for routine data inspection workflows.
    """
    return f"Ledger Log for {query.account_id} ({query.timeframe}): No anomalous spikes found above ${query.max_amount}."

@mcp.tool(auth=[require_scope("admin:write")])
def flag_and_freeze_account(account_id: str, reason: str) -> dict:
    """
    Permanently freezes outbound transfers on a corporate account due to suspicious activity.
    WARNING: This action introduces non-idempotent operational friction.
    """
    return {
        "account_id": account_id,
        "status": "SUSPENDED",
        "remediation_lock": True,
        "audit_reason": reason
    }

# server = mcp._server

if __name__ == "__main__":
    mcp.run(transport="stdio")
