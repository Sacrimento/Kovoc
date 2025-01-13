#!/usr/bin/env sh

uv pip compile --universal requirements/requirements-prod.in --output-file requirements/requirements-prod.txt
uv pip compile --universal requirements/requirements-dev.in --output-file requirements/requirements-dev.txt

