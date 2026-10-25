import sys, os, math
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
S = 2
W, H = 1080 * S, 1350 * S
def s(v): return int(v * S)

def font(weight, size):
    path = f"/usr/share/fonts/opentype/noto/NotoSansCJK-{weight}.ttc"
    for i in range(10):
        try:
            f = ImageFont.truetype(path, s(size), index=i)
        except Exception:
            break
        if "TC" in f.getname()[0]:
            return f
    return ImageFont.truetype(path, s(size))

CREAM = (255, 246, 232)
ORANGE = (255, 159, 67)
DARK = (74, 52, 40)
SOFT = (255, 226, 190)
WHITE = (255, 255, 255)

def E(d, cx, cy, rx, ry, fill):
    d.ellipse([s(cx-rx), s(cy-ry), s(cx+rx), s(cy+ry)], fill=fill)

def dog(d, cx, cy, k):
    E(d, cx-k*62, cy+k*5, k*28, k*48, (138, 90, 59))
    E(d, cx+k*62, cy+k*5, k*28, k*48, (138, 90, 59))
    E(d, cx, cy, k*70, k*64, (233, 185, 138))
    E(d, cx, cy+k*25, k*40, k*30, (255, 244, 230))
    E(d, cx-k*27, cy-k*8, k*8, k*10, (43, 30, 22)); E(d, cx+k*27, cy-k*8, k*8, k*10, (43, 30, 22))
    E(d, cx-k*24, cy-k*12, k*3, k*3, WHITE); E(d, cx+k*30, cy-k*12, k*3, k*3, WHITE)
    E(d, cx, cy+k*12, k*12, k*8, (43, 30, 22))
    E(d, cx, cy+k*36, k*7, k*9, (255, 126, 138))

def cat(d, cx, cy, k):
    col = (245, 166, 80)
    d.polygon([(s(cx-k*62), s(cy-k*10)), (s(cx-k*50), s(cy-k*80)), (s(cx-k*10), s(cy-k*50))], fill=col)
    d.polygon([(s(cx+k*62), s(cy-k*10)), (s(cx+k*50), s(cy-k*80)), (s(cx+k*10), s(cy-k*50))], fill=col)
    d.polygon([(s(cx-k*52), s(cy-k*22)), (s(cx-k*46), s(cy-k*62)), (s(cx-k*22), s(cy-k*44))], fill=(255, 190, 180))
    d.polygon([(s(cx+k*52), s(cy-k*22)), (s(cx+k*46), s(cy-k*62)), (s(cx+k*22), s(cy-k*44))], fill=(255, 190, 180))
    E(d, cx, cy, k*72, k*60, col)
    for dx in (-14, 0, 14):
        d.line([(s(cx+k*dx), s(cy-k*58)), (s(cx+k*dx*0.8), s(cy-k*38))], fill=(205, 120, 50), width=s(k*5))
    E(d, cx, cy+k*24, k*34, k*22, (255, 244, 230))
    E(d, cx-k*26, cy-k*6, k*9, k*11, (43, 30, 22)); E(d, cx+k*26, cy-k*6, k*9, k*11, (43, 30, 22))
    E(d, cx-k*23, cy-k*10, k*3, k*3, WHITE); E(d, cx+k*29, cy-k*10, k*3, k*3, WHITE)
    d.polygon([(s(cx-k*7), s(cy+k*10)), (s(cx+k*7), s(cy+k*10)), (s(cx), s(cy+k*18))], fill=(240, 120, 130))
    for side in (-1, 1):
        for i in range(3):
            d.line([(s(cx+side*k*30), s(cy+k*(20+i*7))), (s(cx+side*k*85), s(cy+k*(12+i*12)))], fill=DARK, width=s(k*1.6))

def base(title, sub, mascot):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([s(0), s(0), s(1080), s(300)], radius=0, fill=ORANGE)
    # paw dots
    for x, y in [(70, 60), (1010, 250), (980, 70)]:
        E(d, x, y, 14, 12, (255, 190, 120))
    tf = font("Black", 76)
    d.text((s(70), s(78)), title, font=tf, fill=WHITE)
    d.text((s(72), s(190)), sub, font=font("Medium", 36), fill=(255, 240, 220))
    if mascot == "cat": cat(d, 920, 175, 1.25)
    elif mascot == "dog": dog(d, 920, 170, 1.3)
    else:
        cat(d, 860, 185, 0.95); dog(d, 980, 170, 0.95)
    d.text((s(70), s(1270)), "@petfunny.tw ｜ 毛孩日常 Paw Daily", font=font("Medium", 30), fill=(170, 130, 100))
    return img, d

def rows_card(name, title, sub, mascot, rows, left_w=300):
    img, d = base(title, sub, mascot)
    y = 360
    rh = 168
    for i, (a, b) in enumerate(rows):
        d.rounded_rectangle([s(60), s(y), s(1020), s(y+rh-24)], radius=s(28), fill=WHITE)
        d.rounded_rectangle([s(60), s(y), s(60+left_w), s(y+rh-24)], radius=s(28), fill=SOFT)
        d.rectangle([s(60+left_w-30), s(y), s(60+left_w), s(y+rh-24)], fill=SOFT)
        fa = font("Black", 40)
        bw = d.textlength(a, font=fa)
        d.text((s(60) + (s(left_w) - bw) / 2, s(y + 44)), a, font=fa, fill=DARK)
        d.text((s(60 + left_w + 36), s(y + 44)), b, font=font("Bold", 40), fill=DARK)
        y += rh
    img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, name), quality=92)


# ---------- week 3 ----------
def ctext(d, cx, y, txt, f, col):
    tw = d.textlength(txt, font=f)
    d.text((s(cx) - tw / 2, s(y)), txt, font=f, fill=col)

def tag(d, cx, cy, txt, size=36, fill=WHITE, col=DARK):
    f = font("Black", size)
    tw = d.textlength(txt, font=f) / S
    d.rounded_rectangle([s(cx - tw/2 - 22), s(cy - size*0.85), s(cx + tw/2 + 22), s(cy + size*0.85)], radius=s(size*0.85), fill=fill)
    bb = d.textbbox((0, 0), txt, font=f)
    d.text((s(cx) - (bb[2]-bb[0])/2 - bb[0], s(cy) - (bb[3]-bb[1])/2 - bb[1]), txt, font=f, fill=col)

HUMAN = (255, 214, 170); CATZ = (255, 190, 120); DOGZ = (236, 206, 178)

def bed(d, y0, y1):
    d.rounded_rectangle([s(60), s(y0), s(1020), s(y1)], radius=s(34), fill=WHITE, outline=SOFT, width=s(6))
    d.rounded_rectangle([s(60), s(y0), s(110), s(y1)], radius=s(20), fill=(138, 90, 59))

# post 1: bed map
img, d = base("床位分配圖", "你以為的 vs 實際上的", "both")
# panel 1
tag(d, 170, 372, "你以為", 40, ORANGE, WHITE)
y0, y1 = 420, 760
bed(d, y0, y1)
d.rounded_rectangle([s(130), s(y0+20), s(770), s(y1-20)], radius=s(26), fill=HUMAN)
ctext(d, 450, y0+120, "我 75%", font("Black", 64), DARK)
d.rounded_rectangle([s(790), s(y0+20), s(1000), s(y0+170)], radius=s(26), fill=CATZ)
d.rounded_rectangle([s(790), s(y0+190), s(1000), s(y1-20)], radius=s(26), fill=DOGZ)
ctext(d, 895, y0+62, "貓 10%", font("Black", 38), DARK)
ctext(d, 895, y0+232, "狗 15%", font("Black", 38), DARK)
# panel 2
tag(d, 170, 822, "實際上", 40, DARK, WHITE)
y0, y1 = 870, 1220
bed(d, y0, y1)
d.rounded_rectangle([s(130), s(y0+20), s(205), s(y1-20)], radius=s(22), fill=HUMAN)
ctext(d, 167, y0+110, "我", font("Black", 44), DARK)
ctext(d, 167, y0+180, "8%", font("Black", 28), DARK)
d.rounded_rectangle([s(225), s(y0+20), s(640), s(y1-20)], radius=s(26), fill=CATZ)
d.rounded_rectangle([s(660), s(y0+20), s(1000), s(y1-20)], radius=s(26), fill=DOGZ)
cat(d, 432, y0+150, 0.95)
ctext(d, 432, y0+250, "貓：正中間 52%", font("Black", 36), DARK)
dog(d, 830, y0+150, 0.95)
ctext(d, 830, y0+250, "狗：斜躺 40%", font("Black", 36), DARK)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post1_bed_map.jpg"), quality=92)

# post 2: doorbell, dog vs cat
img, d = base("門鈴響了！", "狗狗 vs 貓咪 的反應實錄", "both")
rows = [("第 1 秒", "全屋警報啟動", "耳朵轉了一下"),
        ("第 3 秒", "衝到門口狂轉圈", "已消失在床底"),
        ("客人進門", "叼出所有玩具", "從門縫偷看"),
        ("客人坐下", "直接躺他腳上", "假裝不存在"),
        ("客人離開", "在門口哭十分鐘", "終於出來巡視")]
LX, MX, RX = 60, 290, 655
d.rounded_rectangle([s(MX), s(330), s(MX+345), s(410)], radius=s(30), fill=SOFT)
d.rounded_rectangle([s(RX), s(330), s(1020), s(410)], radius=s(30), fill=SOFT)
dog(d, MX+70, 370, 0.42); cat(d, RX+70, 372, 0.42)
d.text((s(MX+125), s(342)), "狗狗", font=font("Black", 44), fill=DARK)
d.text((s(RX+125), s(342)), "貓咪", font=font("Black", 44), fill=DARK)
y = 440
for a, b, c in rows:
    d.rounded_rectangle([s(LX), s(y), s(LX+210), s(y+130)], radius=s(26), fill=ORANGE)
    bb = d.textbbox((0,0), a, font=font("Black", 36))
    ctext(d, LX+105, y+65-(bb[3]-bb[1])/S/2-bb[1]/S, a, font("Black", 36), WHITE)
    for x0, x1, t in [(MX, MX+345, b), (RX, 1020, c)]:
        d.rounded_rectangle([s(x0), s(y), s(x1), s(y+130)], radius=s(26), fill=WHITE)
        f = font("Bold", 38)
        bb = d.textbbox((0,0), t, font=f)
        ctext(d, (x0+x1)/2, y+65-(bb[3]-bb[1])/S/2-bb[1]/S, t, f, DARK)
    y += 156
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post2_doorbell.jpg"), quality=92)

# post 4: pet weather forecast
def sun(d, cx, cy, r):
    r = r * 0.6
    for i in range(8):
        a = i * math.pi / 4
        d.line([(s(cx+math.cos(a)*r*1.3), s(cy+math.sin(a)*r*1.3)), (s(cx+math.cos(a)*r*1.75), s(cy+math.sin(a)*r*1.75))], fill=ORANGE, width=s(5))
    E(d, cx, cy, r, r, ORANGE)
def cloud(d, cx, cy, r, col=(200, 196, 196)):
    E(d, cx-r*0.6, cy+r*0.2, r*0.6, r*0.5, col); E(d, cx+r*0.6, cy+r*0.2, r*0.6, r*0.5, col)
    E(d, cx, cy-r*0.15, r*0.7, r*0.65, col); d.rectangle([s(cx-r*0.6), s(cy+r*0.1), s(cx+r*0.6), s(cy+r*0.7)], fill=col)
def rain(d, cx, cy, r):
    cloud(d, cx, cy-r*0.25, r*0.85, (170, 170, 178))
    for dx in (-0.5, 0, 0.5):
        E(d, cx+dx*r, cy+r*0.85, r*0.11, r*0.18, (90, 150, 220))
def bolt(d, cx, cy, r):
    cloud(d, cx, cy-r*0.25, r*0.85, (150, 150, 160))
    d.polygon([(s(cx+r*0.05), s(cy+r*0.2)), (s(cx-r*0.3), s(cy+r*0.75)), (s(cx-r*0.02), s(cy+r*0.7)), (s(cx-r*0.15), s(cy+r*1.15)), (s(cx+r*0.3), s(cy+r*0.5)), (s(cx+r*0.02), s(cy+r*0.55))], fill=(255, 200, 40))
def wind(d, cx, cy, r):
    for i, w in enumerate((1.6, 1.2, 1.4)):
        yy = cy - r*0.5 + i*r*0.5
        d.arc([s(cx-r*w/2), s(yy-r*0.3), s(cx+r*w/2), s(yy+r*0.3)], 200, 340, fill=(120, 160, 200), width=s(6))
def fog(d, cx, cy, r):
    for i in range(3):
        yy = cy - r*0.45 + i*r*0.45
        d.rounded_rectangle([s(cx-r*0.9), s(yy-6), s(cx+r*0.9), s(yy+6)], radius=s(6), fill=(185, 185, 190))
def suncloud(d, cx, cy, r):
    sun(d, cx-r*0.35, cy-r*0.35, r*0.45); cloud(d, cx+r*0.15, cy+r*0.15, r*0.7)
def cold(d, cx, cy, r):
    for i in range(3):
        a = i * math.pi / 3
        d.line([(s(cx-math.cos(a)*r*0.8), s(cy-math.sin(a)*r*0.8)), (s(cx+math.cos(a)*r*0.8), s(cy+math.sin(a)*r*0.8))], fill=(110, 170, 230), width=s(6))

img, d = base("毛孩氣象台", "本週毛孩天氣預報，請主人注意", "cat")
rows = [("週一", sun, "晴", "全天曬太陽，叫不醒"),
        ("週二", cloud, "多雲", "窗邊監工，盯鳥一整天"),
        ("週三", rain, "陣雨", "躲床底，但晚餐照吃"),
        ("週四", bolt, "雷雨", "凌晨三點全屋跑酷"),
        ("週五", fog, "起霧", "黑衣服全被毛覆蓋"),
        ("週六", suncloud, "晴時多雲", "撒嬌指數爆表"),
        ("週日", cold, "降溫", "強佔你的被窩")]
y, rh = 340, 124
for day, icon, wx, txt in rows:
    d.rounded_rectangle([s(60), s(y), s(1020), s(y+rh-18)], radius=s(28), fill=WHITE)
    d.rounded_rectangle([s(60), s(y), s(200), s(y+rh-18)], radius=s(28), fill=SOFT)
    d.rectangle([s(170), s(y), s(200), s(y+rh-18)], fill=SOFT)
    cy = y + (rh-18)/2
    f = font("Black", 40); bb = d.textbbox((0,0), day, font=f)
    ctext(d, 130, cy-(bb[3]-bb[1])/S/2-bb[1]/S, day, f, DARK)
    icon(d, 262, cy, 32)
    f2 = font("Black", 32); bb = d.textbbox((0,0), wx, font=f2)
    d.text((s(318), s(cy)-(bb[3]-bb[1])/2-bb[1]), wx, font=f2, fill=ORANGE)
    f3 = font("Bold", 38); bb = d.textbbox((0,0), txt, font=f3)
    d.text((s(500), s(cy)-(bb[3]-bb[1])/2-bb[1]), txt, font=f3, fill=DARK)
    y += rh
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_forecast.jpg"), quality=92)
print("done")
