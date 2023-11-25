#!/usr/bin/env bash

set -e

find . -type f \
    ! -path "./*/migrations/*" \
	-name "*.py" -regex '.*\(crypto_assets\)/.*' \
	-exec "$@" {} +
