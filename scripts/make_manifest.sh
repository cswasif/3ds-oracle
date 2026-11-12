#!/usr/bin/env bash
# Writes SHA-256 hashes of every file in evidence/ to evidence/SHA256SUMS
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidence
find evidence -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 -r sha256sum > evidence/SHA256SUMS
echo "Wrote evidence/SHA256SUMS ($(wc -l < evidence/SHA256SUMS) files)"
