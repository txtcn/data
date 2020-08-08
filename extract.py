#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed
from fire import Fire
from hashlib import blake2b
from os import makedirs
from html import unescape
from os import walk, cpu_count
from os.path import dirname, abspath, join, exists
from pathlib import Path
from tqdm import tqdm
import re
import zd

RE_N = re.compile("</(p|br|li)>", re.DOTALL)
RE_TAG = re.compile(r'<[^>]+>', re.DOTALL)

ARROW = "➜"


class Exist:
  def __init__(self):
    self.exist = set()

  def add(self, key):
    d = blake2b(key.strip().lower().encode('utf8')).digest()
    self.exist.add(d)

  def __contains__(self, key):
    d = blake2b(key.strip().lower().encode('utf8')).digest()
    return d in self.exist


EXIST = Exist()


def export(pbar, root, outdir, file_li):
  for fname in file_li:
    pbar.update(1)
    day = fname * 86400
    fname = str(fname)
    fpath = join(root, fname)
    outpath = join(outdir, fname) + "."
    with open(fpath, "rb") as f:
      txt = f.read()

      b2bpath = outpath + "bzb"
      b2b = blake2b(txt).digest()
      if exists(b2bpath):
        with open(b2bpath, "rb") as b:
          if b.read() == b2b:
            continue

      txt = txt.decode('utf8', 'ignore')[1:]
      with zd.open(outpath + "zstd", "w", level=19) as out:
        for post in txt.split(ARROW):
          r = post.split("\n", 2)
          title, url_time = r[:2]
          if len(r) == 3:
            txt = r[2]
          else:
            txt = 0
          url, time = url_time.split("\t")
          time = int(time) + day
          if txt:
            if title in EXIST:
              continue
            EXIST.add(title)
            out.write(ARROW + title + "\n")
            out.write(url + "\t" + str(time) + "\n")
            if txt:
              txt = txt.replace("\r",
                                "\n").replace("\n\n", "\n"
                                              ).replace("\n", " ")
              txt = RE_N.sub("\n", txt)
              txt = RE_TAG.sub("", txt)
              txt = tuple(
                filter(bool, [i.strip() for i in txt.split("\n")])
              )
              out.write(unescape("\n".join(txt)) + "\n")

      with open(b2bpath, "wb") as out:
        out.write(b2b)


@Fire
def main(outpath="/share/txt/cn"):

  dirpath = abspath(dirname(__file__))

  total = 0
  with tqdm(total=total) as pbar:
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
      todo = {}
      for root, dir_li, file_li in walk(dirpath):
        now = root[len(dirpath) + 1:]
        if not now or now[0] in "._":
          continue

        file_li = sorted(
          map(int, (i for i in file_li if i.isdigit()))
        )
        if not file_li:
          continue
        outdir = join(outpath, now)
        makedirs(outdir, exist_ok=True)
        total += len(file_li)
        # Path(outdir).mkdir(parents=True, exist_ok=True)
        todo[executor.submit(export, pbar, root, outdir,
                             file_li)] = outdir
      pbar.total = total

      for future in as_completed(todo):
        filepath = todo[future]
        print(filepath)
        try:
          future.result()
        except Exception as exc:
          print(exc)
