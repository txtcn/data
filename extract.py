#!/usr/bin/env python3

import zd
from os.path import dirname, abspath, join
from os import walk
from fire import Fire
from html import unescape
from pathlib import Path
import re
from tqdm import tqdm

RE_N = re.compile("</(p|br|li)>", re.DOTALL)
RE_TAG = re.compile(r'<[^>]+>', re.DOTALL)

ARROW = "➜"


@Fire
def main(outpath):

  dirpath = abspath(dirname(__file__))

  for root, dir_li, file_li in walk(dirpath):
    now = root[len(dirpath) + 1:]
    if not now or now[0] in "._":
      continue

    file_li = sorted(map(int, (i for i in file_li if i.isdigit())))
    if not file_li:
      continue
    outfile = join(outpath, now) + ".zd"
    Path(dirname(outfile)).mkdir(parents=True, exist_ok=True)

    print(outfile)
    with zd.open(outfile, "w", level=22) as out:
      for fname in tqdm(file_li):
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
