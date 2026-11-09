"""功能宣传图：横版 1280×720（新趣集等产品页）和方图 1080×1080（闲鱼商品主图，输出到 square/），上面一行标题和副标题，下面是官网的真实界面截图，配色同官网和 logo。

用法（在 public/ 目录下）：python3 assets/feature-cards/make.py          两种都出
      只出一种：python3 assets/feature-cards/make.py wide | square
      高清：后面加 hd，保留 2 倍原图不缩小，输出到 hd/（如 make.py wide hd）
需要本机装有 Google Chrome，图片取自 ../web/img/，字体取自 ../web/fonts/（只含官网用过的字，标题出现新字时先在官网重切字体，否则会退回系统宋体）。
改标题、换截图、加一张：改下面的 CARDS 再跑一遍。2026-11-09 为新趣集产品页制作，也可用于其他平台和宣传物料。
"""
from pathlib import Path
import shutil, subprocess, sys, tempfile

HERE = Path(__file__).resolve().parent
WEB = HERE.parents[2] / 'web'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CARDS = [
    ('1-多店铺一个窗口回消息', 't-msg', '多个闲鱼店铺，一个窗口回消息', '顶栏切换店铺，右栏就是这位买家的每一单'),
    ('2-付款自动发卡密和链接', 't-ship', '买家付款，自动发卡密和网盘链接', '固定内容、卡密库存、多规格，按模板自动发出'),
    ('3-关键词自动回复', 't-reply', '关键词自动回复，文字和图片一起发', '规则分组，违禁词兜底，买家语音也能匹配'),
    ('4-提醒收货与自动好评', 't-remind', '到点提醒收货，有售后的单自动跳过', '发货后按时提醒，确认收货后自动好评'),
    ('5-经营数据逐笔对账', 't-data', '支付、退款、实际收入，逐笔对账', '多个店铺合计，每张数据卡点进去是明细'),
]

# 截图里要额外遮住的区域，值为 (左, 上, 宽, 高)，按截图宽高的百分比，只对方图生效。
# t-reply 违禁词那一行的敏感词（翻墙、科学上网等）2026-11-09 已在源图 web/img/t-reply.webp 里模糊，这里不用再遮。
SQUARE_MASKS = {}

WIDE = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"XGJ Serif SC";font-weight:600;src:url("file://{web}/fonts/serif-sc-600.woff2")}}
html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#f5f4ed}}
.top{{position:absolute;left:80px;right:80px;top:46px;display:flex;justify-content:space-between;align-items:flex-start}}
h1{{margin:0;font:600 40px/1.2 "XGJ Serif SC","Songti SC",serif;color:#2f2d2a;letter-spacing:.02em}}
p{{margin:10px 0 0;font:400 19px/1.4 -apple-system,"PingFang SC",sans-serif;color:#77756d}}
.brand{{display:flex;align-items:center;gap:10px;font:600 22px/1 "XGJ Serif SC","Songti SC",serif;color:#2f2d2a;margin-top:6px}}
.brand img{{width:34px;height:34px}}
.frame{{position:absolute;left:80px;right:80px;top:178px;bottom:-40px;background:#ebe8dd;border-radius:22px;padding:18px 18px 0}}
.frame div{{width:100%;height:100%;border-radius:12px 12px 0 0;overflow:hidden;box-shadow:0 6px 24px rgba(47,45,42,.12)}}
.frame img{{width:100%;display:block}}
</style></head><body>
<div class="top"><div><h1>{title}</h1><p>{sub}</p></div><div class="brand"><img src="file://{here}/logo-1024.png">闲鱼智控</div></div>
<div class="frame"><div><img src="file://{web}/img/{shot}.webp"></div></div></body></html>'''

SQUARE = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"XGJ Serif SC";font-weight:600;src:url("file://{web}/fonts/serif-sc-600.woff2")}}
html,body{{margin:0;width:1080px;height:1080px;overflow:hidden;background:#f5f4ed}}
.brand{{position:absolute;left:64px;top:60px;display:flex;align-items:center;gap:12px;font:600 26px/1 "XGJ Serif SC","Songti SC",serif;color:#2f2d2a}}
.brand img{{width:40px;height:40px}}
h1{{position:absolute;left:64px;right:64px;top:150px;margin:0;font:600 54px/1.28 "XGJ Serif SC","Songti SC",serif;color:#2f2d2a;letter-spacing:.02em}}
p{{position:absolute;left:64px;right:64px;top:300px;margin:0;font:400 26px/1.45 -apple-system,"PingFang SC",sans-serif;color:#77756d}}
.frame{{position:absolute;left:40px;right:40px;top:400px;background:#ebe8dd;border-radius:26px;padding:20px}}
.frame div{{position:relative;border-radius:12px;overflow:hidden;box-shadow:0 6px 24px rgba(47,45,42,.12)}}
.frame img{{width:100%;display:block}}
.frame i{{position:absolute;backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);background:rgba(255,255,255,.35);border-radius:6px}}
</style></head><body>
<div class="brand"><img src="file://{here}/logo-1024.png">闲鱼智控</div>
<h1>{title}</h1><p>{sub}</p>
<div class="frame"><div><img src="file://{web}/img/{shot}.webp">{masks}</div></div></body></html>'''

# 方图标题按逗号断成两行，读起来更像主图卖点
LAYOUTS = {'wide': (WIDE, 1280, 720, HERE, lambda t: t), 'square': (SQUARE, 1080, 1080, HERE / 'square', lambda t: t.replace('，', '，<br>', 1))}
HD = 'hd' in sys.argv  # hd：保留 2 倍原图（2560×1440 / 2160×2160）不缩小，放进 hd/，给少数派这类大图显示的文章用
wanted = [a for a in sys.argv[1:] if a in LAYOUTS] or list(LAYOUTS)

with tempfile.TemporaryDirectory() as tmp:
    for layout in wanted:
        template, w, h, out, wrap = LAYOUTS[layout]
        out.mkdir(exist_ok=True)
        for name, shot, title, sub in CARDS:
            page, big = Path(tmp) / f'{layout}-{name}.html', Path(tmp) / f'{layout}-{name}@2x.png'
            masks = ''.join(f'<i style="left:{l}%;top:{t}%;width:{w_}%;height:{h_}%"></i>' for l, t, w_, h_ in SQUARE_MASKS.get(shot, [])) if layout == 'square' else ''
            page.write_text(template.format(web=WEB, here=HERE, shot=shot, title=wrap(title), sub=sub, masks=masks))
            # 按 2 倍渲染再缩回目标尺寸，文字更清楚
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                            f'--window-size={w},{h}', '--force-device-scale-factor=2', f'--screenshot={big}', page.as_uri()],
                           check=True, capture_output=True)
            dest = out / 'hd' / f'{name}.png' if HD else out / f'{name}.png'
            dest.parent.mkdir(exist_ok=True)
            if HD:
                shutil.copy(big, dest)
            else:
                subprocess.run(['sips', '-z', str(h), str(w), str(big), '--out', str(dest)], check=True, capture_output=True)
            print(layout, name, dest.stat().st_size // 1024, 'KB')
