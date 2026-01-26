#!/bin/sh
set -eu

cd /app
export PYTHONPATH="/app/lib/python3.11/site-packages:/app"
exec python3 -m zoia_lib.backend.startup "$@"
