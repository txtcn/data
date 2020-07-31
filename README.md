# 中文语料库-每日自动更新版


## 创作初衷

网上有一些中文语料库，但是居然都不是自动更新的。

是可忍，孰不可忍。我想自动挖掘研究市场热点炒股票，没有新数据搞毛线。

于是，有了这个项目 : 《中文语料库-每日自动更新版》 。

核心思想，通过[RSS订阅](//www.ruanyifeng.com/blog/2006/01/rss.html)，存档内容。

然后通过[GitHub Actions](//github.com/features/actions)来实现每日运行，这样就实现了一个无服务器的自动更新语料库。

Github仓库有1GB容量的限制，但热度高的项目能申请更多存储空间。

**为了避免空间不足导致语料库无法更新，请大家给[语料仓库](https://github.com/txtcn/data)多多加星。**

* 语料仓库 : [github.com/txtcn/data](//github.com/txtcn/data)
* 爬虫仓库 : [github.com/txtcn/dump](//github.com/txtcn/dump)

为了节约空间，历史语料被打包发布到了 [github release](//github.com/txtcn/data/releases) ，克隆语料仓库后，首先运行 `./init.sh` 导入历史语料。

## 已收录网站

### 含历史数据（为这些网站定制了爬虫，抓取了全部的文章）

1. [奇客资讯 solidot.org](//solidot.org) 👉 [语料库](https://github.com/txtcn/data/tree/master/solidot.org)

### 不含历史数据（只订阅了RSS，没写历史数据爬虫，仅含订阅日之后的文章）

#### 媒体

1. [知乎每日精选](//zhihu.com) 👉 [语料库](//github.com/txtcn/data/tree/master/知乎每日精选)
1. [知乎日报](//daily.zhihu.com) 👉 [语料库](//t.cn/A6yBoMi7)
1. [游研社](//yystv.cn) 👉 [语料库](//github.com/txtcn/data/tree/master/yystv.cn)
1. [虎嗅](//huxiu.com) 👉  [语料库](//github.com/txtcn/data/tree/master/huxiu.com)
1. [好奇心日报](//qdaily.com) 👉  [语料库](//github.com/txtcn/data/tree/master/qdaily.com)
1. [少数派](//sspai.com) 👉 [语料库](//github.com/txtcn/data/tree/master/sspai.com) 
1. [小众软件](//appinn.com) 👉 [语料库](//github.com/txtcn/data/tree/master/小众软件)
1. [超能网](//expreview.com) 👉 [语料库](//github.com/txtcn/data/tree/master/expreview.com)
1. [爱范儿](//ifanr.com) 👉 [语料库](//github.com/txtcn/data/tree/master/ifanr.com)
1. [极客公园](//main_test.geekpark.net/rss.rss) 👉 [语料库](//github.com/txtcn/data/tree/master/geekpark.net)
1. [理想生活实验室](//toodaylab.com) 👉 [语料库](//github.com/txtcn/data/tree/master/toodaylab.com)
1. [科学松鼠会](//songshuhui.net) 👉 [语料库](//github.com/txtcn/data/tree/master/songshuhui.net)
1. [PanSci 泛科学](//pansci.asia) 👉 [语料库](//github.com/txtcn/data/tree/master/pansci.asia)
1. [人人都是产品经理](//woshipm.com) 👉 [语料库](//github.com/txtcn/data/tree/master/woshipm.com)
1. [优设网 – UISDC](//uisdc.com) 👉 [语料库](//github.com/txtcn/data/tree/master/uisdc.com)

#### 个人博客

1. [阮一峰的网络日志 ruanyifeng.com](//ruanyifeng.com) 👉 [语料库](//github.com/txtcn/data/tree/master/ruanyifeng.com)
1. [月光博客](//williamlong.info) 👉 [语料库](//github.com/txtcn/data/tree/master/williamlong.info)
1. [若望的翻译车间](//untranslatable.home.blog) 👉 [语料库](//github.com/txtcn/data/tree/master/untranslatable.home.blog)


#### 添加新源

欢迎大家共享有价值的RSS源。如何添加新的RSS内容源呢？流程如下：

1. 找到高质量全文输出的RSS
2. 参考 [rss/zhihu-daily.coffee](https://github.com/txtcn/dump/blob/master/rss/zhihu-daily.coffee)、[rss/williamlong.info.coffee](https://github.com/txtcn/dump/blob/master/rss/williamlong.info.coffee)、[rss/solidot.org.coffee](https://github.com/txtcn/dump/blob/master/rss/solidot.org.coffee) 创建一个文件
3. 修改 [dump/README.md](https://github.com/txtcn/dump/blob/master/README.md)，在上面添加新源的介绍。
4. 提交代码合并请求


#### 暂不收录

以下RSS有问题，暂不收录

1. [36氪](//36kr.com) 会随机把少数字符替换为乱码

## 目录结构

以 [data/ruanyifeng.com](https://github.com/txtcn/data/tree/master/ruanyifeng.com) 为例

* [rss.yml](https://github.com/txtcn/data/blob/master/ruanyifeng.com/rss.yml) 有`rss`的元信息
* 以数字为名称的文件，这里是内容存档，文件名含义是 `int(时间戳/86400)`

## 格式说明

* 第一行 : ➜标题
* 第二行 : 链接链接   时间（中间的分隔符是TAB）
* 之后的行 : 正文的HMTL (直到出现下一个➜)

示例如下 :

```
➜标题
链接   时间
正文
```

[演示文档](https://github.com/txtcn/data/blob/master/solidot.org/18465)

标题、内容中的 `➜` 都被替换为了 `➔` （这两个箭头不是同一个字符），`TAB`都被替换为了`空格`，所以解析的时候直接split即可。

文件名为日期 : `日期 = 取整(时间戳/86400)`

文档中时间为 : 时间戳秒数减去当日零点的秒数

`实际时间戳 = 文件名*86400 + 文档中第二行的时间`

文本解析的代码可以[参考这里](https://github.com/txtcn/dump/blob/master/txtcn/load.coffee)

## 抽取纯文本

上面存档的正文是HTML，但往往搞挖掘需要的是纯文本。

语料仓库自带了纯文本抽取工具。

[data/extract.py](https://github.com/txtcn/data/blob/master/extract.py)

进入`data` 目录，首先用`python3`的`pip`运行（有些系统是`pip3`）

```
pip install -r requirements.txt
```

然后运行 `./extract.py 输出路径`

运行后输出一堆类似 `知乎日报.zd` 的文件。

`.zd`文件是`Zstandard`压缩后的纯文本文件 ( 参见 [Zstandard - Real-time data compression algorithm](https://facebook.github.io/zstd/) )

使用 `zdcat` 命令可以查看， 比如：

```
zdcat /share/txt/data/ifanr.com.zd
```

运行后可以看到正文，文档格式和上文一致（时间戳被还原为绝对时间）。

在程序中读取`zd`文件，可用如下方法。

```
import zd

with zd.open(
  "/share/wiki/zhwiki-20200701-pages-articles.txt.zd"
) as f:
  for i in f:
    print(i)
```

`zd`的python依赖可以单独安装，如：`pip install zd`，`zdcat`会随着`zd`附带安装。

`zd`项目的源码见[gitee.com/znlp/zd](https://gitee.com/znlp/zd)

ubuntu 用户也可以安装 [`zstd`软件包](https://www.systutorials.com/docs/linux/man/1-zstd/)，然后用 `zstdcat` 、`unzstd` 等命令。

## 我的其他项目友情推荐

### 1. [从维基百科抽取中文语料](//github.com/txtcn/wiki)

### 2. 谷歌浏览器实用插件：[六度空间 · 短链接](//t.cn/AiBLK07q)

> 可以生成短链接（短网址）、二维码，一键复制标题和链接。

![](https://tqimg.github.io/20200723050312.png)

现有的chrome插件，没有一个能自动复制并带上标题的，所以自己写了一个，很实用，欢迎试用。

安装地址：[Chrome 网上应用店](//t.cn/AiBLK07q)

如果没法访问Chrome网上应用店，可以按照以下步骤安装。

[点击这里下载源码](//github.com/6du-space/url-short/archive/master.zip) ，并解压

在Chrome浏览器中输入 `chrome://extensions` ，并开启开发者模式（点击右上角）

点击「加载已解压的扩展程序」选择刚刚解压的目录。

这是[开源项目](//github.com/6du-space/url-short)，欢迎参与改进。

## 关于作者

[张沈鹏](mailto:zsp042@gmail.com)，欢迎扫码关注我的微信公众号。

![](./touzi-world.svg)
