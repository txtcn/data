#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

from concurrent.futures import ThreadPoolExecutor
from os.path import join,dirname,abspath,basename
import tempfile
from glob import glob
from os import cpu_count

_DIR=dirname(abspath(__file__))

@(_DIR)/wget.xsh

def untxz(txz):
  tar -Jxf @(txz) -C @(_DIR)/

with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
  for txz in glob(join(_DIR,"_txz/*.txz")):
    executor.submit(untxz,txz)

