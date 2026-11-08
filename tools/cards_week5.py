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


# ---------- week 5 ----------
def ctext(d, cx, y, txt, f, col):
    tw = d.textlength(txt, font=f)
    d.text((s(cx) - tw / 2, s(y)), txt, font=f, fill=col)

def vtext(d, x, cy, txt, f, col, center=None):
    bb = d.textbbox((0, 0), txt, font=f)
    if center is not None:
        x = center - (bb[2]-bb[0]) / S / 2 - bb[0] / S
    d.text((s(x), s(cy) - (bb[3]-bb[1]) / 2 - bb[1]), txt, font=f, fill=col)

def label_rows(d, rows, y, rh, left_w, lsize=36, rsize=38):
    for a, b in rows:
        d.rounded_rectangle([s(60), s(y), s(1020), s(y+rh-18)], radius=s(26), fill=WHITE)
        d.rounded_rectangle([s(60), s(y), s(60+left_w), s(y+rh-18)], radius=s(26), fill=SOFT)
        d.rectangle([s(60+left_w-30), s(y), s(60+left_w), s(y+rh-18)], fill=SOFT)
        cy = y + (rh-18)/2
        vtext(d, 0, cy, a, font("Black", lsize), DARK, center=60+left_w/2)
        vtext(d, 60+left_w+32, cy, b, font("Bold", rsize), DARK)
        y += rh

def paw(d, cx, cy, k, col):
    E(d, cx, cy+18*k, 30*k, 24*k, col)
    for dx, dy in [(-30, -14), (-11, -32), (11, -32), (30, -14)]:
        E(d, cx+dx*k, cy+dy*k, 10*k, 12*k, col)

# post 1: lease contract, cat = landlord
img, d = base("租賃契約書", "房東：貓　房客：我（自願）", "cat")
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), fill=WHITE)
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), outline=SOFT, width=s(6))
ctext(d, 540, 372, "第一條至第七條　房客不得異議", font("Bold", 32), (170, 130, 100))
clauses = [("租金", "每月罐罐、凍乾、貓砂，按時上繳"),
           ("租期", "房客終身，房東想走隨時走"),
           ("床位", "房東睡中間，房客縮在床角"),
           ("收租", "凌晨五點踩臉，不接受延後"),
           ("押金", "沙發一張，已被房東沒收"),
           ("修繕", "房東弄壞的，房客自費修理"),
           ("違約", "房客晚回家，以嘔吐物罰款")]
y = 432
for i, (a, b) in enumerate(clauses):
    vtext(d, 100, y+40, f"{i+1}", font("Black", 38), ORANGE)
    vtext(d, 145, y+40, a, font("Black", 36), DARK)
    vtext(d, 275, y+40, b, font("Bold", 34), DARK)
    if i < len(clauses)-1:
        d.line([(s(95), s(y+86)), (s(985), s(y+86))], fill=(240, 228, 210), width=s(2))
    y += 94
# signatures
vtext(d, 100, 1150, "房東簽章：", font("Bold", 32), (170, 130, 100))
paw(d, 330, 1150, 1.2, (220, 80, 70))
vtext(d, 560, 1150, "房客：", font("Bold", 32), (170, 130, 100))
d.line([(s(660), s(1175)), (s(960), s(1175))], fill=DARK, width=s(3))
vtext(d, 670, 1150, "（淚痕）", font("Medium", 30), (170, 130, 100))
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post1_cat_lease.jpg"), quality=92)

# post 2: 11.11 shopping cart
img, d = base("雙11購物車", "結帳前，請確認你的人生", "both")
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), fill=WHITE)
items = [("貓抓板（第五片）", "$890", False), ("頂級凍乾 3 包", "$1,580", False),
         ("自動餵食器", "$2,990", False), ("狗狗雨衣（牠不穿）", "$650", False),
         ("耐咬玩具（撐 2 天）", "$480", False), ("給自己的新外套", "$1,990", True),
         ("給自己的保養品", "$1,200", True), ("泡麵一箱（湊免運）", "$299", False)]
y = 362
for name, price, removed in items:
    col = (200, 180, 160) if removed else DARK
    # checkbox
    d.rounded_rectangle([s(100), s(y+20), s(146), s(y+66)], radius=s(10), outline=col, width=s(4),
                        fill=None if removed else ORANGE)
    if not removed:
        d.line([(s(110), s(y+43)), (s(120), s(y+55)), (s(138), s(y+30))], fill=WHITE, width=s(6))
    vtext(d, 175, y+43, name, font("Bold", 36), col)
    fp = font("Black", 36); bb = d.textbbox((0, 0), price, font=fp)
    vtext(d, 980-(bb[2]-bb[0])/S, y+43, price, fp, col)
    if removed:
        tw = d.textlength(name, font=font("Bold", 36)) / S
        d.line([(s(170), s(y+45)), (s(185+tw), s(y+45))], fill=(220, 80, 70), width=s(4))
        d.line([(s(980-(bb[2]-bb[0])/S-6), s(y+45)), (s(985), s(y+45))], fill=(220, 80, 70), width=s(4))
    y += 80
d.line([(s(95), s(y+10)), (s(985), s(y+10))], fill=SOFT, width=s(4))
vtext(d, 100, y+62, "已從購物車移除：所有給自己的東西", font("Bold", 32), (220, 80, 70))
d.rounded_rectangle([s(100), s(y+110), s(980), s(y+200)], radius=s(30), fill=DARK)
vtext(d, 0, y+155, "結帳總額：$6,889　餘額：哈哈", font("Black", 40), WHITE, center=540)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post2_double11_cart.jpg"), quality=92)

# post 4: how to train your human (written by the cat)
img, d = base("人類飼養指南", "作者：貓　譯者：被飼養的我", "cat")
steps = [("STEP 1", "凌晨五點踩臉，完成開機"),
         ("STEP 2", "坐上鍵盤，降低其工作效率"),
         ("STEP 3", "飯碗見底就盯著牠，不必出聲"),
         ("STEP 4", "牠買的床不睡，睡紙箱"),
         ("STEP 5", "偶爾呼嚕一次，防止牠逃跑"),
         ("STEP 6", "牠說「最後一包」時，別信"),
         ("注意", "人類哭了別理，明天照常上工")]
label_rows(d, steps, 340, 130, 220, 36, 37)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_human_manual.jpg"), quality=92)
print("done")
