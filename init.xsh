#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

from os.path import join,dirname,abspath
import tempfile

_DIR=dirname(abspath(__file__))

version = $(curl -s https://api.github.com/repos/txtcn/data/releases/latest|awk -F '"' '/tag_name/{print $4}')
prefix,version = version.rsplit(".",1)
version = int(version)

tmpdir = tempfile.mkdtemp()
mkdir -p @(tmpdir)

for i in range(1,version+1):
  i = str(i)
  downfile = join(tmpdir,i)
  print(downfile)
  wget -c https://github.com/txtcn/data/releases/download/@(prefix).@(i)/data.tar.xz -O @(downfile)
  tar -Jxf @(downfile) -C @(_DIR)/

rm -rf @(tmpdir)
