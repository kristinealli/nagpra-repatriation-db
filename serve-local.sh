#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/docs"
python3 -m http.server 8000
