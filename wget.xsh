#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

from os.path import join,dirname,abspath,exists,basename
import tempfile
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

_DIR=dirname(abspath(__file__))
GIT = basename(_DIR)

version = $(curl --retry 5 -s https://api.github.com/repos/txtcn/@(GIT)/releases/latest|awk -F '"' '/tag_name/{print $4}')
print(version)
prefix,version = version.rsplit(".",1)
version = int(version)

xzdir = join(_DIR,"_txz")
mkdir -p @(xzdir)

host_li = [
  "https://github.com",
  "http://github.strcpy.cn",
]


def download(i):
  i = str(i)
  downfile = join(xzdir,i)
  txz = downfile+".txz"
  for host in host_li:
    if exists(txz):
      continue
    print(host, txz)
    try:
      wget -q -c @(host)/txtcn/data/releases/download/@(prefix).@(i)/data.txz -O @(downfile).txz.ing
      mv @(txz).ing @(txz)
      break
    except:
      continue

with ThreadPoolExecutor(max_workers=cpu_count()*3) as executor:
  for i in range(1,version+1):
    executor.submit(download, i)
