.PHONY: help test test-cov lint security up down logs status seed seed-xml compose-config services-up fmt xml-check

help: ## Show this help
	@grep -E '^[a-z-]+: ## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS=": ## "}; {printf "  %-15s %s\n", $$1, $$2}'

test: ## Fast unit + integration suite (no server needed)
	python3 -m pytest tests/unit tests/integration

test-cov: ## Suite with coverage report
	python3 -m pytest tests/unit tests/integration --cov --cov-report=term-missing 2>/dev/null || python3 -m pytest tests/unit tests/integration

lint: ## flake8 + XML well-formedness
	python3 -m flake8 gnuhealth services scripts tests --max-line-length=100 --extend-ignore=E501,W503,E128,E131,E402
	python3 -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in glob.glob('gnuhealth/**/*.xml',recursive=True)+glob.glob('data/*.xml')]"

security: ## bandit + secret scan
	bash scripts/security.sh

up: ## Start 3-tier stack (Nginx :8091 + Tryton + Postgres)
	bash scripts/operational/start.sh

down: ## Stop the stack
	bash scripts/operational/stop.sh

logs: ## Tail stack logs
	bash scripts/operational/logs.sh

status: ## Stack status
	bash scripts/operational/status.sh

seed: ## Generate + import Gombe demo data
	bash scripts/seed-gombe.sh

seed-xml: ## Generate seed XML only (no server needed)
	python3 scripts/seed-gombe.py

compose-config: ## Validate compose files
	docker compose -f docker/docker-compose.yml config > /dev/null
	if [ -f services/docker-compose.services.yml ]; then \
	  docker compose -f services/docker-compose.services.yml config > /dev/null; fi

services-up: ## Run the 5 FastAPI services locally (ports 8081-8085)
	docker compose -f services/docker-compose.services.yml up --build

fmt: ## autopep8 in place
	bash scripts/autopep8.sh

xml-check: ## Validate all Tryton/seed XML
	python3 -c "import xml.dom.minidom,glob; fs=glob.glob('gnuhealth/**/*.xml',recursive=True)+glob.glob('data/*.xml'); [xml.dom.minidom.parse(f) for f in fs]; print('XML OK:', len(fs))"
