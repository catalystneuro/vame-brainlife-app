#!/usr/bin/env bash
# Upload every *.nwb in this directory to a Brainlife project as neuro/nwb,
# one dataset per file with the filename stem as the subject name.
# Run from inside test_assets/. Requires `bl login` first.

set -euo pipefail

PROJECT_ID="69ccbf7d34e13335188ff403"

for f in *.nwb; do
    subject=$(basename "$f" .nwb)
    echo "==> Uploading $f as subject=$subject"
    bl data upload \
        --project "$PROJECT_ID" \
        --datatype neuro/nwb \
        --subject "$subject" \
        --nwb "$f"
done
