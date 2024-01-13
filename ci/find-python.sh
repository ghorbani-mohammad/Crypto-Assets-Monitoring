#!/usr/bin/env bash

set -e

find . -type d -name "crypto_assets_db" -prune -o \
    ! -path "./*/migrations/*" \
    ! -path "./*manage.py" \
    -type f -name "*.py" -regex '.*\(crypto_assets\)/.*' \
    -exec "$@" {} +
