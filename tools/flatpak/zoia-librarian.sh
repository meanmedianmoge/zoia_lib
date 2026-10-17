#!/bin/sh
set -eu

cd /app

site_packages=""
for path in /app/lib/python3*/site-packages; do
    if [ -d "$path" ]; then
        site_packages="$path"
        break
    fi
done

if [ -n "$site_packages" ]; then
    export PYTHONPATH="$site_packages:/app"
else
    export PYTHONPATH="/app"
fi

exec python3 -m zoia_lib.backend.startup "$@"
