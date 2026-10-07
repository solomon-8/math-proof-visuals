#!/bin/sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
mkdir -p episodes/017/frames episodes/017/renders episodes/017/subtitles
exec python video/render.py "$@"
