import sys, os
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


# ---------- week 2 ----------
rows_card("post1_cat_levels.jpg", "貓奴升級之路", "你現在是第幾級？留言報上等級", "cat", [
    ("Lv.1", "學會開罐罐，主子賞臉"),
    ("Lv.2", "被踩醒也不敢翻身"),
    ("Lv.3", "椅子被佔，自己坐邊邊"),
    ("Lv.4", "手機相簿九成都是貓"),
    ("Lv.5", "出門前先跟貓報備行程"),
], left_w=200)

def magnifier(d, cx, cy, r, col):
    d.ellipse([s(cx-r), s(cy-r), s(cx+r), s(cy+r)], outline=col, width=s(6))
    d.line([(s(cx+r*0.7), s(cy+r*0.7)), (s(cx+r*1.6), s(cy+r*1.6))], fill=col, width=s(8))

img, d = base("如果狗狗會 Google", "搜尋紀錄不小心外流了", "dog")
qs = ["「等一下」到底是幾分鐘",
      "為什麼人類可以坐沙發，我不行",
      "如何假裝還沒吃過晚餐",
      "郵差每天都來，他到底想幹嘛",
      "尾巴一直追不到，正常嗎",
      "主人拿起鑰匙 ＝ 要去散步嗎"]
y = 350
for q in qs:
    d.rounded_rectangle([s(60), s(y), s(1020), s(y+116)], radius=s(58), fill=WHITE, outline=SOFT, width=s(4))
    magnifier(d, 122, y+52, 18, ORANGE)
    d.text((s(178), s(y+30)), q, font=font("Bold", 40), fill=DARK)
    y += 144
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post2_dog_google.jpg"), quality=92)

# bingo
img, d = base("毛孩行為賓果", "你家連成幾條線？留言告訴我們", "both")
cells = [("推倒", "桌上杯子"), ("霸佔", "你的枕頭"), ("跟你", "進廁所"),
         ("半夜", "突然暴衝"), ("FREE", "超可愛"), ("叫名字", "裝沒聽到"),
         ("對著空氣", "狂叫發呆"), ("咬壞", "拖鞋電線"), ("聽到零食", "瞬間移動")]
cw, gap, x0, y0 = 280, 22, 98, 340
for i, (a, b) in enumerate(cells):
    r, c = divmod(i, 3)
    x, yy = x0 + c*(cw+gap), y0 + r*(cw+gap)
    center = (i == 4)
    d.rounded_rectangle([s(x), s(yy), s(x+cw), s(yy+cw)], radius=s(36), fill=ORANGE if center else WHITE,
                        outline=None if center else SOFT, width=s(5))
    col = WHITE if center else DARK
    fa = font("Black", 56 if center else 44); fb = font("Bold", 38 if center else 36)
    for txt, f, ty in [(a, fa, yy+70), (b, fb, yy+150)]:
        tw = d.textlength(txt, font=f)
        d.text((s(x) + (s(cw)-tw)/2, s(ty)), txt, font=f, fill=col)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_bingo.jpg"), quality=92)
print("done")
