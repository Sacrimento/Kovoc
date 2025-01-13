#!/usr/bin/env sh

ruff check kovoc --fix
ruff format kovoc
mypy kovoc
