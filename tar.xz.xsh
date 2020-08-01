#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True
# trace on

from time import time
from os import walk
import os
import tempfile
import shutil
from os.path import dirname,join,basename,abspath,getsize
from pathlib import Path

SIZE_MIN = int(20*1024*1024*2.4)
TODAY = int(time() / 86400) - 7

def main(version, filedir):
  tmpdir = tempfile.mkdtemp()
  if '.' not in version:
    version = '0.2.1'
  else:
    version = version.rsplit(".",1)
    version[-1] = str(int(version[-1])+1)
    version = ".".join(version)
  $version=version
  prefix_len = len(filedir)+1
  to_rm = []
  total_size = 0

  for root, dir_li, file_li in walk(filedir):
    now = root[prefix_len:]
    if not now or now[0] in "._":
      continue
    file_li = [int(i) for i in file_li if i.isdigit()]
    if not file_li:
      continue

    outdir = join(tmpdir, root[prefix_len:])
    Path(outdir).mkdir(parents=True,exist_ok=True)

    for i in file_li:
      if i > TODAY:
        continue
      i = str(i)
      filepath = join(root, i)

      to_rm.append(filepath)
      outpath = join(outdir, i)
      shutil.copyfile(filepath, outpath)
      total_size += getsize(filepath)
      if total_size > SIZE_MIN:
        break
  if total_size < SIZE_MIN:
    print("还需",round((SIZE_MIN - total_size)/1024/1024,2),"MB")
    return
  cd @(tmpdir)
  xzpath = f"/tmp/data.{TODAY}.tar.xz"
  tar -I 'pixz -9' -cf @(xzpath)  ./

  # go get github.com/github-release/github-release

  github-release release --user txtcn --repo data --tag "v$version" --name "$version" --description "$version"
  github-release upload --user txtcn --repo data --tag "v$version" --name "data.tar.xz" --file @(xzpath)
  os.remove(xzpath)
  shutil.rmtree(tmpdir)
  for i in to_rm:
    os.remove(i)
  return version

if __name__ == "__main__":
  $GITHUB_TOKEN=$(cat ~/.config/github.token).strip(" \n")
  version = $(curl -s "https://api.github.com/repos/txtcn/data/releases/latest" | jq -r .tag_name)
  filedir = dirname(abspath(__file__))
  while 1:
    cd @(filedir)
    version = main(version, filedir)
    if not version:
      break
    print(version)



