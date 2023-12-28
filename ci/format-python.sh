#!/usr/bin/env sh

set -e

ci/find-python.sh black -t py311
