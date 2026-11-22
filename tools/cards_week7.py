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


# ---------- week 7 ----------
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
STAR_ON = (255, 180, 40)
STAR_OFF = (230, 215, 195)

def star(d, cx, cy, r, col):
    pts = []
    for i in range(10):
        ang = -math.pi/2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((s(cx + rr*math.cos(ang)), s(cy + rr*math.sin(ang))))
    d.polygon(pts, fill=col)

def stars(d, x, cy, n, r=16, gap=36):
    for i in range(5):
        star(d, x + i*gap, cy, r, STAR_ON if i < n else STAR_OFF)

# post 1: reviews of my home, written by the pets
img, d = base("本宅評論區", "住戶評分 2.1 ★（評論者：貓、狗）", "both")
reviews = [("貓", 1, "服務生（主人）態度敷衍，罐罐只開一個。", "床太小，人類竟然佔了一半。"),
           ("狗", 5, "超棒！！門口每天都有人回來！！", "雖然是同一個人，但我每次都很驚喜！！"),
           ("貓", 2, "凌晨四點叫餐，等了整整三十秒。", "管理員還敢翻身繼續睡，負評。"),
           ("貓", 1, "沙發品質太差，抓兩下就爛了。", "建議老闆換一張，用他的年終。")]
y = 340
for who, n, l1, l2 in reviews:
    d.rounded_rectangle([s(60), s(y), s(1020), s(y+184)], radius=s(26), fill=WHITE)
    E(d, 120, y+48, 32, 32, SOFT)
    vtext(d, 0, y+48, who, font("Black", 34), DARK, center=120)
    vtext(d, 176, y+48, f"在地嚮導・{'住了三年' if who=='貓' else '住了兩年'}", font("Bold", 28), MUTED)
    stars(d, 800, y+48, n)
    vtext(d, 100, y+108, l1, font("Bold", 33), DARK)
    vtext(d, 100, y+152, l2, font("Bold", 33), DARK)
    y += 200
d.rounded_rectangle([s(60), s(1150), s(1020), s(1236)], radius=s(30), fill=DARK)
vtext(d, 0, 1193, "業主回覆：對不起，我會再努力賺錢。", font("Black", 34), WHITE, center=540)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post1_home_reviews.jpg"), quality=92)
print("p1")

# post 2: under-sofa archaeology report
img, d = base("沙發底下考古報告", "挖掘人：我　埋藏者：狗與貓", "both")
rows = [("髮圈 ×37", "全家只有我綁頭髮，我只買過三條"),
        ("瓶蓋 ×12", "貓的私人收藏，碰一下會被巴"),
        ("耳機 ×1", "左耳。右耳下落不明，嫌犯裝睡"),
        ("襪子 ×9", "全部單隻，另一半被狗帶去埋了"),
        ("零錢 $46", "我上個月剩下的全部生活費"),
        ("狗毛 ×∞", "量多到可以再組裝一隻狗"),
        ("我的青春", "出土時已風化，無法修復")]
label_rows(d, rows, 340, 130, 250, 36, 35)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post2_sofa_dig.jpg"), quality=92)

# post 4: year-end party lucky draw, pets' edition
img, d = base("毛孩尾牙抽獎", "得獎名單公布　主人請自備紅包", "both")
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), fill=WHITE)
d.rounded_rectangle([s(60), s(340), s(1020), s(1235)], radius=s(26), outline=SOFT, width=s(6))
ctext(d, 540, 366, "獎項　／　獎品　／　得主", font("Bold", 30), MUTED)
prizes = [("頭獎", "主人一整天不准出門", "貓"),
          ("二獎", "全新沙發一張（拿來抓）", "貓"),
          ("三獎", "主人的枕頭永久使用權", "狗"),
          ("四獎", "冰箱裡那塊雞胸肉", "狗"),
          ("特別獎", "主人的年終獎金全額", "貓狗平分")]
y = 430
for i, (a, prize, who) in enumerate(prizes):
    cy = y + 46
    d.rounded_rectangle([s(95), s(cy-30), s(255), s(cy+30)], radius=s(30), fill=ORANGE)
    vtext(d, 0, cy, a, font("Black", 32), WHITE, center=175)
    vtext(d, 285, cy, prize, font("Bold", 34), DARK)
    wf = font("Black", 32)
    vtext(d, 0, cy, who, wf, RED, center=905)
    if i < len(prizes)-1:
        d.line([(s(95), s(y+96)), (s(985), s(y+96))], fill=(240, 228, 210), width=s(2))
    y += 106
d.rounded_rectangle([s(95), s(990), s(985), s(1120)], radius=s(30), fill=DARK)
vtext(d, 0, 1030, "主人抽到：銘謝惠顧", font("Black", 44), WHITE, center=540)
vtext(d, 0, 1085, "另附贈：獎品全部由你出錢", font("Bold", 32), (255, 210, 160), center=540)
vtext(d, 0, 1180, "＊本抽獎由貓全權主辦，結果不接受任何申訴", font("Medium", 28), MUTED, center=540)
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_lucky_draw.jpg"), quality=92)
print("done")
