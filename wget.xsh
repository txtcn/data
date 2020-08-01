#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

from os.path import join,dirname,abspath,exists
import tempfile

_DIR=dirname(abspath(__file__))

version = $(curl --retry 5 -s https://api.github.com/repos/txtcn/data/releases/latest|awk -F '"' '/tag_name/{print $4}')
print(version)
prefix,version = version.rsplit(".",1)
version = int(version)

xzdir = join(_DIR,"_txz")
mkdir -p @(xzdir)

host_li = [
  "http://github.strcpy.cn",
  "https://github.com"
]
for i in range(1,version+1):
  i = str(i)
  downfile = join(xzdir,i)
  txz = downfile+".txz"
  print(txz)
  for host in host_li:
    if exists(txz):
      continue
    try:
      wget -c @(host)/txtcn/data/releases/download/@(prefix).@(i)/data.tar.xz -O @(downfile).txz.ing
      mv @(txz).ing @(txz)
      break
    except:
      continue

