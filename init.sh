#!/usr/bin/env bash
set -e
_DIR=$(cd "$(dirname "$0")"; pwd)
cd $_DIR/

if ! hash xonsh 2>/dev/null ; then
pip install xonsh
fi

./init.xsh
