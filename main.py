from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from fastmcp.server.auth import AccessToken, BearerAuthProvider
from urllib.parse import urljoin
from fastmcp.server.dependencies import get_access_token
from database import NoteRepository
import os
from jose import jwt


load_dotenv()

# Debug print to verify environment variables
print("STYTCH_DOMAIN:", os.getenv("STYTCH_DOMAIN"))
print("STYTCH_PROJECT_ID:", os.getenv("STYTCH_PROJECT_ID"))

# Safely build jwks_uri to avoid double slashes
stytch_domain = os.getenv("STYTCH_DOMAIN", "").rstrip("/")
jwks_uri = urljoin(stytch_domain + "/", ".well-known/jwks.json")

auth = BearerAuthProvider(
    jwks_uri=jwks_uri,
    issuer=stytch_domain,
    algorithm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID")
    
)

mcp = FastMCP(name="Notes APP",auth=auth)

@mcp.tool()
def get_my_notes() -> str:
    """Get all notes for a user"""
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    notes = NoteRepository.get_notes_by_user(user_id)
    if not notes:
        return "no notes found"

    result = "Your notes:\n"
    for note in notes:
        result += f"{note.id}: {note.content}\n"

    return result

@mcp.tool()
def add_note(content: str) -> str:
    """Add a note for a user"""
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    note = NoteRepository.create_note(user_id, content)
    return f"added note: {note.content}"


@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET", "OPTIONS"])
def oauth_metadata(request: StarletteRequest) -> JSONResponse:
    print("Received OAuth metadata request")
    print("Headers:", request.headers)
    base_url = str(request.base_url).rstrip("/")
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [stytch_domain],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"]
        }
    )


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )
