#!/usr/bin/env bash
# Build the Docker image and run app.py inside it against config.json.
# CPU-only — Docker Desktop on macOS cannot expose the host GPU to containers,
# and --gpus all only works with the NVIDIA Container Toolkit on Linux.
#
# Platform is pinned to linux/amd64 to match Brainlife's runtime: this matters
# for transitive deps (e.g. cartopy from movement) that ship prebuilt manylinux
# x86_64 wheels but would otherwise compile from source on Apple Silicon.

set -euo pipefail

IMAGE="vame-brainlife-app:dev"
PLATFORM="linux/amd64"

if [ ! -f config.json ]; then
    cp config.json.sample config.json
    echo "==> config.json staged from config.json.sample"
fi

echo "==> Building $IMAGE for $PLATFORM..."
docker build --platform="$PLATFORM" -t "$IMAGE" .

echo "==> Running $IMAGE..."
docker run --rm \
    --platform="$PLATFORM" \
    -v "$PWD:/work" \
    -w /work \
    "$IMAGE" \
    python3 app.py

echo "==> Done. Outputs in output/ and product.json"
