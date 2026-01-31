# Haskellito

A web-based interactive Haskell REPL powered by GHCi. Write, edit, and evaluate Haskell code directly in your browser with a modern, responsive interface.

## Features

- **Interactive GHCi Sessions** - Each user gets their own isolated GHCi session
- **Code Editor** - Full-featured editor with Haskell syntax highlighting (CodeMirror)
- **Live Console** - Evaluate expressions and see results in real-time
- **Multi-line Support** - Write and load multi-line function definitions
- **Safe Haskell** - Runs in GHCi's Safe mode for security
- **Keyboard Shortcuts** - Press `⌘+Enter` (Mac) or `Ctrl+Enter` (Windows/Linux) to load code

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

## Prerequisites

- Python 3.11+
- GHC (Glasgow Haskell Compiler) - provides GHCi
- Node.js 20+

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd haskellito
```

### 2. Install backend dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

### 4. Run the development servers

Start the backend (from project root):

```bash
source venv/bin/activate
python main.py
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
- Nginx as reverse proxy
- Systemd service for the backend
- Static file serving for the frontend

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sessions/` | Create a new GHCi session |
| POST | `/api/sessions/{id}/eval` | Evaluate code in a session |
| POST | `/api/sessions/{id}/close` | Close a session |

## Project Structure

```
haskellito/
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.vue              # Main application
│   │   ├── components/
│   │   │   ├── CodeEditor.vue   # CodeMirror editor
│   │   │   └── Interpreter.vue  # Console output
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── deploy/
    ├── setup.sh         # Server setup script
    ├── nginx.conf       # Nginx configuration
    └── haskellito.service # Systemd service
```

## License

MIT
