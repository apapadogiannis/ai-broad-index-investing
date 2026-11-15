#!/usr/bin/env bash
# Reproduces every number in the paper's empirical exhibits and both figures. Runs in a few seconds.
set -e
cd "$(dirname "$0")/scripts"
for f in build_etf_monthly make_exhibits fig1_five_layers fig2_rent_value; do
  echo "== $f"; python3 "$f.py"
done
