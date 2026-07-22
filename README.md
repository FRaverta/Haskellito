# Haskellito

A web-based interactive Haskell REPL powered by GHCi. Write, edit, and evaluate Haskell code directly in your browser with a modern, responsive interface.

## Features

- **Interactive GHCi Sessions** - Each user gets their own isolated GHCi session
- **Code Editor** - Full-featured editor with Haskell syntax highlighting (CodeMirror)
- **Live Console** - Evaluate expressions and see results in real-time
- **Multi-line Support** - Write and load multi-line function definitions
- **Keyboard Shortcuts** - Press `⌘+Enter` (Mac) or `Ctrl+Enter` (Windows/Linux) to load code

### Security

- **Safe Haskell** - Runs in GHCi's Safe mode (`-XSafe`)
- **Command Filtering** - Dangerous GHCi commands (`:!`, `:shell`, `:load`, etc.) are blocked
- **Resource Limits** - Each GHCi process is limited to 64MB memory and 60s CPU time
- **Sandboxed Containers** - Docker development environment with dropped capabilities and read-only filesystem
- **Hardened Production** - Systemd service with extensive security directives

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- GHCi (Glasgow Haskell Compiler interactive)

**Frontend:**
- Vue 3
- Vite
- CodeMirror 6
- Axios

## Getting Started

### Option A: Docker (Recommended)

The easiest way to run Haskellito locally with full sandboxing (from repo root):

```bash
docker compose -f docker/docker-compose.yml up
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

To rebuild after changes:

```bash
docker compose -f docker/docker-compose.yml up --build
```

### Option B: Native Development

#### Prerequisites

- Python 3.11+
- GHC (Glasgow Haskell Compiler) - provides GHCi
- Node.js 20+

#### 1. Clone the repository

```bash
git clone <repository-url>
cd haskellito
```

#### 2. Install backend dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

#### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

#### 4. Run the development servers

Start the backend (from project root, run uvicorn with backend as cwd):

```bash
source venv/bin/activate
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Start the frontend (in a separate terminal):

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## Usage

1. Click **"Connect to GHCi"** to start a new session
2. Write Haskell code in the editor panel
3. Click **"Load"** or press `⌘/Ctrl+Enter` to load definitions into GHCi
4. Use the console input to evaluate expressions
5. Click **"Disconnect"** when finished

### Example

```haskell
-- Define a function in the editor
double x = x * 2

factorial 0 = 1
factorial n = n * factorial (n - 1)
```

Then evaluate in the console:

```
ghci> double 21
42
ghci> factorial 5
120
```

## Production Deployment

The `deploy/` folder contains scripts and configurations for deploying to Ubuntu 22.04 (tested on AWS Lightsail):

```bash
# On server as root
./deploy/setup.sh

# Then follow the post-setup instructions
```

This sets up:
- Nginx as reverse proxy with static file serving
- Hardened systemd service with security restrictions:
  - `ProtectSystem=strict` - Read-only filesystem
  - `PrivateDevices=true` - Device isolation
  - `NoNewPrivileges=true` - Prevent privilege escalation
  - `CapabilityBoundingSet=` - All capabilities dropped
  - System call filtering and namespace restrictions

### Authentication with AWS Cognito

The app can stay public for browsing while requiring login only for execution:
creating GHCi sessions, evaluating code, closing sessions, and submitting
challenge solutions.

In Cognito, configure a User Pool app client for a browser SPA:

- Use a public app client with no client secret.
- Enable the authorization-code grant. The frontend uses PKCE.
- Enable scopes: `openid`, `email`, `profile`.
- Enable Google as the app client's identity provider.
- Add callback URLs:
  - local: `http://localhost:5173/auth/callback`
  - production: `https://<your-domain>/auth/callback`
- Add logout URLs:
  - local: `http://localhost:5173/`
  - production: `https://<your-domain>/`
- In Google OAuth, add the Cognito redirect URI:
  `https://<your-cognito-domain>/oauth2/idpresponse`

Frontend build-time environment:

```bash
VITE_AUTH_ENABLED=true
VITE_COGNITO_DOMAIN=https://<your-cognito-domain>
VITE_COGNITO_APP_CLIENT_ID=<app-client-id>
VITE_COGNITO_REDIRECT_URI=https://<your-domain>/auth/callback
VITE_COGNITO_LOGOUT_URI=https://<your-domain>/
VITE_COGNITO_IDENTITY_PROVIDER=Google
```

Backend runtime environment:

```bash
COGNITO_AUTH_ENABLED=true
COGNITO_REGION=<aws-region>
COGNITO_USER_POOL_ID=<user-pool-id>
COGNITO_APP_CLIENT_ID=<app-client-id>
CORS_ALLOW_ORIGINS=https://<your-domain>
```

If `COGNITO_AUTH_ENABLED` is omitted, the backend enables auth automatically
when both `COGNITO_USER_POOL_ID` and `COGNITO_APP_CLIENT_ID` are present.
Without these variables, local development remains unauthenticated.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sessions/` | Create a new GHCi session |
| POST | `/api/sessions/{id}/eval` | Evaluate code in a session |
| POST | `/api/sessions/{id}/close` | Close a session |

## Project Structure

```
haskellito/
├── backend/
│   ├── main.py              # FastAPI backend
│   ├── requirements.txt     # Python dependencies
│   └── challenges/          # Challenge definitions and data
├── docker/
│   ├── Dockerfile           # Backend container image
│   └── docker-compose.yml   # Local development environment
├── frontend/
│   ├── src/
│   │   ├── App.vue              # Main application
│   │   ├── components/
│   │   │   ├── CodeEditor.vue   # CodeMirror editor
│   │   │   └── Interpreter.vue  # Console output
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── deploy/
│   ├── setup.sh           # Server setup script (Ubuntu 22.04)
│   ├── nginx.conf         # Nginx reverse proxy config
│   └── haskellito.service # Systemd service (hardened)
└── Makefile               # Deploy (run on server)
```

## License

MIT
