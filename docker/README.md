# Docker 3-tier stack: Nginx (:8091) + Tryton/uWSGI (:8000) + PostgreSQL 15.
#
# ```bash
# cp docker/gnuhealth/trytond.conf.example docker/gnuhealth/trytond.conf  # + secrets
# docker compose -f docker/docker-compose.yml up --build -d
# ```
#
# Images pin: python:3.11-slim, trytond 7.0.*, gnuhealth-all-modules 5.0.*,
# postgres:15-alpine, nginx:1.27-alpine.
