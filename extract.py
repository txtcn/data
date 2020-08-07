#!/usr/bin/env python3

import zd
from tqdm import tqdm
from os.path import dirname, abspath, join
from os import walk, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed
from fire import Fire
from html import unescape
from pathlib import Path
import re
from tqdm import tqdm
from hashlib import blake2b

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


def export(root, outfile, file_li):
  with zd.open(outfile, "w", level=19) as out:
    for fname in file_li:
      fpath = join(root, str(fname))
      day = fname * 86400
      with open(fpath) as f:
        for post in f.read()[1:].split(ARROW):
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


@Fire
def main(outpath):

  dirpath = abspath(dirname(__file__))

  with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
    todo = {}
    for root, dir_li, file_li in walk(dirpath):
      now = root[len(dirpath) + 1:]
      if not now or now[0] in "._":
        continue

      file_li = sorted(map(int, (i for i in file_li if i.isdigit())))
      if not file_li:
        continue
      outfile = join(outpath, now) + ".zd"
      Path(dirname(outfile)).mkdir(parents=True, exist_ok=True)
      todo[executor.submit(export, root, outfile, file_li)] = outfile

    with tqdm(total=len(todo)) as pbar:
      for future in as_completed(todo):
        filepath = todo[future]
        print(filepath)
        pbar.update(1)
        try:
          future.result()
        except Exception as exc:
          print(exc)
