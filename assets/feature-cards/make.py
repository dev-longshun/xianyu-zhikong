"""功能宣传图：1280×720，上面一行标题和副标题，下面是官网的真实界面截图，配色同官网和 logo。

用法（在 public/ 目录下）：python3 assets/feature-cards/make.py
需要本机装有 Google Chrome，图片取自 ../web/img/，字体取自 ../web/fonts/（只含官网用过的字，标题出现新字时先在官网重切字体，否则会退回系统宋体）。
改标题、换截图、加一张：改下面的 CARDS 再跑一遍。2026-11-09 为新趣集产品页制作，也可用于其他平台和宣传物料。
"""
from pathlib import Path
import subprocess, tempfile

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

TEMPLATE = '''<!doctype html><html><head><meta charset="utf-8"><style>
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
<div class="top"><div><h1>{title}</h1><p>{sub}</p></div><div class="brand"><img src="file://{web}/img/logo.webp">闲鱼智控</div></div>
<div class="frame"><div><img src="file://{web}/img/{shot}.webp"></div></div></body></html>'''

with tempfile.TemporaryDirectory() as tmp:
    for name, shot, title, sub in CARDS:
        page, big = Path(tmp) / f'{name}.html', Path(tmp) / f'{name}@2x.png'
        page.write_text(TEMPLATE.format(web=WEB, shot=shot, title=title, sub=sub))
        # 按 2 倍渲染再缩回 1280×720，文字更清楚
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                        '--window-size=1280,720', '--force-device-scale-factor=2', f'--screenshot={big}', page.as_uri()],
                       check=True, capture_output=True)
        subprocess.run(['sips', '-z', '720', '1280', str(big), '--out', str(HERE / f'{name}.png')], check=True, capture_output=True)
        print(name, (HERE / f'{name}.png').stat().st_size // 1024, 'KB')
