#!/usr/bin/env bash

set -e

find . -type f \
    ! -path "./*/migrations/*" \
	! -path "./*manage.py" \
	-name "*.py" -regex '.*\(crypto_assets\)/.*' \
	-exec "$@" {} +
