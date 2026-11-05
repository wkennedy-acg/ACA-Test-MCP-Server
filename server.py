# WK : ACG
# Minimal FastMCP test server used to validate build, push and ACA deployment.

# Tools are deliberately innocuous: no auth, no data access, no outbound calls.
# Configuration comes from environment variables so the same image runs unchanged
# locally and on Azure Container Apps.

import os
import socket
from datetime import datetime, timezone

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

mcp = FastMCP("aca-test-mcp-server")

@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b

@mcp.tool
def server_info() -> dict:
    """Return the replica hostname, UTC time and revision details for this server.

    Useful for confirming which ACA replica and revision answered a request.
    """
    return {
        "hostname": socket.gethostname(),
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "container_app_revision": os.environ.get("CONTAINER_APP_REVISION", "unknown"),
        "container_app_name": os.environ.get("CONTAINER_APP_NAME", "unknown"),
    }

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Liveness/readiness endpoint for ACA probes."""
    return JSONResponse({"status": "ok"})

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        path=os.environ.get("MCP_PATH", "/mcp"),
        stateless_http=os.environ.get("STATELESS_HTTP", "true").lower() == "true",
    )
