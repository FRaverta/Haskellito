# Haskellito Makefile
# Run on the server: assumes latest code is already there (e.g. git pull).
# make deploy = build frontend, install deps, copy static files, update systemd/nginx, restart service.

.PHONY: build-frontend deploy clean help

# Paths (run from app root, e.g. /opt/haskellito)
FRONTEND_DIST := frontend/dist
WWW_ROOT := /var/www/haskellito

help:
	@echo "Haskellito Makefile (run on server)"
	@echo ""
	@echo "  make build-frontend   Build frontend for production ($(FRONTEND_DIST)/)"
	@echo "  make deploy          Build, install, copy static files, restart haskellito"
	@echo "  make clean           Remove frontend build artifacts"
	@echo ""
	@echo "Assumes: latest code already on server (e.g. git pull). Run from app root."
	@echo ""

# Build frontend for production (Vite build)
build-frontend:
	cd frontend && npm ci && npm run build
	@echo "Frontend built: $(FRONTEND_DIST)/"

# Deploy: build frontend, install backend deps, copy static files, update systemd/nginx, restart
deploy: build-frontend
	@echo "Installing Python dependencies..."
	[ -d venv ] || python3.11 -m venv venv
	. venv/bin/activate && pip install -q --upgrade pip && pip install -q -r requirements.txt
	@echo "Copying frontend to $(WWW_ROOT)..."
	sudo mkdir -p $(WWW_ROOT)
	sudo cp -r $(FRONTEND_DIST)/* $(WWW_ROOT)/
	@echo "Updating systemd service..."
	sudo cp deploy/haskellito.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable haskellito 2>/dev/null || true
	@echo "Updating nginx..."
	sudo cp deploy/nginx.conf /etc/nginx/sites-available/haskellito
	sudo ln -sf /etc/nginx/sites-available/haskellito /etc/nginx/sites-enabled/ 2>/dev/null || true
	sudo nginx -t && sudo systemctl reload nginx
	@echo "Restarting haskellito..."
	sudo systemctl restart haskellito
	sudo systemctl status haskellito --no-pager
	@echo "Deploy complete."

clean:
	rm -rf $(FRONTEND_DIST)
	@echo "Cleaned $(FRONTEND_DIST)"
