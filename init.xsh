#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

from os.path import join,dirname,abspath
import tempfile
from glob import glob
_DIR=dirname(abspath(__file__))

@(_DIR)/wget.xsh

for txz in glob(join(_DIR,"_txz/*.txz")):
  tar -Jxf @(txz) -C @(_DIR)/

