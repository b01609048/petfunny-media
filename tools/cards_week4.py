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


# ---------- week 4 ----------
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

# post 1: obituary for the sofa
def sofa(d, cx, cy, k):
    body = (196, 120, 84); dark = (150, 88, 60)
    d.rounded_rectangle([s(cx-170*k), s(cy-90*k), s(cx+170*k), s(cy+10*k)], radius=s(30*k), fill=dark)  # back
    d.rounded_rectangle([s(cx-200*k), s(cy-30*k), s(cx-140*k), s(cy+80*k)], radius=s(26*k), fill=body)
    d.rounded_rectangle([s(cx+140*k), s(cy-30*k), s(cx+200*k), s(cy+80*k)], radius=s(26*k), fill=body)
    d.rounded_rectangle([s(cx-150*k), s(cy), s(cx+150*k), s(cy+70*k)], radius=s(18*k), fill=body)
    for lx in (-170, 160):
        d.rectangle([s(cx+lx*k), s(cy+80*k), s(cx+(lx+10)*k), s(cy+105*k)], fill=DARK)
    # scratches / tufts
    for x0 in (-185, -175, 150, 162, 174):
        for j in range(4):
            d.line([(s(cx+x0*k+j*0), s(cy+(70+j*3)*k)), (s(cx+(x0+4)*k), s(cy+(92+j*4)*k))], fill=(240, 220, 190), width=s(3*k))
    for x, y in [(-120, -60), (-40, -70), (60, -55), (110, -75), (-160, 0), (175, 10)]:
        for j in range(3):
            d.line([(s(cx+(x+j*9)*k), s(cy+y*k)), (s(cx+(x+j*9-6)*k), s(cy+(y+30)*k))], fill=(255, 236, 210), width=s(3*k))
    E(d, cx+20*k, cy+40*k, 18*k, 10*k, (255, 236, 210))  # stuffing
    E(d, cx+45*k, cy+35*k, 14*k, 9*k, (255, 236, 210))

img, d = base("沉痛告別", "本人的沙發 享壽八個月", "both")
# frame
d.rounded_rectangle([s(250), s(345), s(830), s(745)], radius=s(20), fill=DARK)
d.rounded_rectangle([s(272), s(367), s(808), s(723)], radius=s(12), fill=(255, 250, 242))
sofa(d, 540, 505, 1.1)
# black ribbon corner
d.polygon([(s(720), s(345)), (s(830), s(345)), (s(830), s(455))], fill=(40, 30, 25))
ctext(d, 540, 655, "R.I.P. 2026.03 – 2026.11", font("Bold", 30), (150, 110, 90))
rows = [("生前身價", "一萬二千元，分期還沒繳完"),
        ("死因", "被抓＋被咬，多重外傷"),
        ("兇手", "貓（主謀）、狗（共犯）"),
        ("兇手態度", "毫無悔意，正睡在遺體上"),
        ("家屬", "主人的存款（亦病危中）")]
label_rows(d, rows, 780, 96, 230, 36, 37)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post1_sofa_obituary.jpg"), quality=92)

# post 2: job ad
img, d = base("急徵：鏟屎官", "終身職・無薪・不得離職", "cat")
rows = [("工作內容", "開罐、鏟屎、當人肉暖爐"),
        ("工時", "24 小時待命，凌晨三點加班"),
        ("薪資", "無，還要倒貼罐罐錢"),
        ("福利", "偶爾被踩，視為免費按摩"),
        ("升遷", "無，老闆永遠是貓"),
        ("面試", "被聞一下，看心情錄取"),
        ("離職", "不開放，合約簽到老")]
label_rows(d, rows, 340, 130, 240, 38, 38)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post2_job_ad.jpg"), quality=92)

# post 4: salary pie chart
img, d = base("本月薪水流向圖", "我的錢，都去哪了？", "both")
data = [("罐罐飼料", 34, (255, 159, 67)), ("獸醫", 26, (138, 90, 59)), ("被咬壞的重買", 18, (233, 185, 138)),
        ("貓砂尿布墊", 12, (255, 205, 130)), ("牠們不玩的玩具", 9, (196, 120, 84)), ("我自己", 1, (40, 30, 25))]
cx, cy, r = 540, 640, 250
a0 = -90
for name, p, col in data:
    a1 = a0 + p * 3.6
    d.pieslice([s(cx-r), s(cy-r), s(cx+r), s(cy+r)], a0, a1, fill=col, outline=CREAM, width=s(4))
    mid = math.radians((a0 + a1) / 2)
    if p >= 9:
        tx, ty = cx + math.cos(mid) * r * 0.62, cy + math.sin(mid) * r * 0.62
        f = font("Black", 40)
        bb = d.textbbox((0, 0), f"{p}%", font=f)
        tcol = WHITE if col in [(138, 90, 59), (196, 120, 84), (255, 159, 67)] else DARK
        d.text((s(tx) - (bb[2]-bb[0])/2 - bb[0], s(ty) - (bb[3]-bb[1])/2 - bb[1]), f"{p}%", font=f, fill=tcol)
    a0 = a1
# callout for 我自己 (last slice just left of top)
mid = math.radians(-90 - 1.8)
px, py = cx + math.cos(mid) * r, cy + math.sin(mid) * r
d.line([(s(px), s(py)), (s(px-60), s(py-40)), (s(px-170), s(py-40))], fill=DARK, width=s(4))
E(d, px, py, 7, 7, DARK)
d.rounded_rectangle([s(px-410), s(py-75), s(px-170), s(py-5)], radius=s(30), fill=DARK)
vtext(d, 0, py-40, "我自己 1%", font("Black", 36), WHITE, center=px-290)
# legend
y = 925
for i, (name, p, col) in enumerate(data):
    col_i, row_i = i % 2, i // 2
    x = 70 + col_i * 480
    yy = y + row_i * 105
    d.rounded_rectangle([s(x), s(yy), s(x+460), s(yy+85)], radius=s(24), fill=WHITE)
    E(d, x+45, yy+42, 20, 20, col)
    vtext(d, x+82, yy+42, name, font("Bold", 34), DARK)
    fp = font("Black", 34); bb = d.textbbox((0, 0), f"{p}%", font=fp)
    vtext(d, x+435-(bb[2]-bb[0])/S, yy+42, f"{p}%", fp, ORANGE if name != "我自己" else DARK)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_salary_pie.jpg"), quality=92)
print("done")
