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


# ---------- week 6 ----------
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


RED = (220, 80, 70)
MUTED = (170, 130, 100)

# post 1: phone gallery composition (bar chart)
img, d = base("我的手機相簿", "容量已滿　請刪除：我自己", "both")
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), fill=WHITE)
ctext(d, 540, 366, "相簿分類統計（共 10,088 張）", font("Bold", 32), MUTED)
bars = [("貓在睡覺", 4812), ("狗在吐舌頭", 3207), ("貓擋住螢幕", 1066),
        ("狗的模糊殘影", 988), ("朋友聚會", 12), ("我自己", 3)]
mx = 4812
y = 436
for name, v in bars:
    vtext(d, 100, y+22, name, font("Bold", 34), DARK)
    bw = max(14, 600 * v / mx)
    col = ORANGE if name != "我自己" else RED
    d.rounded_rectangle([s(100), s(y+52), s(100+bw), s(y+92)], radius=s(18), fill=col)
    vtext(d, 100+bw+18, y+72, f"{v:,} 張", font("Black", 32), col)
    y += 102
vtext(d, 100, y+14, "＊「我自己」其中兩張被貓擋住臉", font("Medium", 28), MUTED)
d.rounded_rectangle([s(100), s(1110), s(980), s(1200)], radius=s(30), fill=DARK)
vtext(d, 0, 1155, "雲端空間已滿：建議刪除「我自己」", font("Black", 38), WHITE, center=540)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post1_phone_gallery.jpg"), quality=92)

# post 2: dog IQ test report card
img, d = base("狗狗智商測驗", "成績單　考生：家裡那隻", "dog")
rows = [("自己的尾巴", "追了四十分鐘，仍在調查中"),
        ("假裝丟球", "被騙第 87 次，每次都很開心"),
        ("電視門鈴", "衝去門口狂吠，門外沒有人"),
        ("照鏡子", "跟裡面那隻對峙一整個下午"),
        ("坐下", "會。前提是你手上有肉"),
        ("總分", "無法計算，但吃飯從不遲到"),
        ("評語", "主人每月繳學費，可能比牠笨")]
label_rows(d, rows, 340, 130, 240, 36, 36)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post2_dog_iq_test.jpg"), quality=92)

# post 4: year-end performance review, by the cat
img, d = base("年度考績表", "考核人：貓　受考人：鏟屎官", "cat")
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), fill=WHITE)
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), outline=SOFT, width=s(6))
ctext(d, 540, 366, "考核項目　／　等第　／　主管評語", font("Bold", 30), MUTED)
items = [("開罐速度", "C", "慢了三秒，記小過一支"),
         ("鏟屎頻率", "B", "尚可，但鏟的時候表情不敬"),
         ("暖腿服務", "A", "三小時沒動，值得肯定"),
         ("出勤狀況", "D", "竟敢出門上班九小時"),
         ("逗貓棒", "C-", "揮得像在敷衍本主管"),
         ("薪資上繳", "A+", "全數充公，堪為表率")]
y = 436
for i, (a, g, c) in enumerate(items):
    cy = y + 46
    vtext(d, 100, cy, a, font("Black", 36), DARK)
    E(d, 330, cy, 40, 40, ORANGE if g[0] in "AB" else RED)
    vtext(d, 0, cy, g, font("Black", 36), WHITE, center=330)
    vtext(d, 395, cy, c, font("Bold", 33), DARK)
    if i < len(items)-1:
        d.line([(s(95), s(y+96)), (s(985), s(y+96))], fill=(240, 228, 210), width=s(2))
    y += 102
d.rounded_rectangle([s(100), s(1060), s(980), s(1140)], radius=s(26), fill=SOFT)
vtext(d, 0, 1100, "總評：留用察看　年終獎金：無（你的）", font("Black", 36), DARK, center=540)
vtext(d, 100, 1180, "主管簽章：", font("Bold", 30), MUTED)
paw(d, 300, 1176, 0.85, RED)
vtext(d, 560, 1180, "受考人：不得申訴", font("Bold", 30), MUTED)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_cat_review.jpg"), quality=92)
print("done")
