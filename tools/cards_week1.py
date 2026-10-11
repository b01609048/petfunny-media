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

rows_card("post1_before_after.jpg", "養貓前 vs 養貓後", "你以為你養了一隻貓，其實是貓收留了你", "cat", [
    ("床", "我的床 → 牠的床，我睡邊邊"),
    ("鍵盤", "打字用 → 貓的電熱毯"),
    ("紙箱", "資源回收 → 豪宅，禁止丟"),
    ("杯子", "放桌上 → 等著被推下去"),
    ("薪水", "我的 → 罐罐基金"),
], left_w=220)

rows_card("post2_dog_schedule.jpg", "狗狗的一日行程", "行程滿檔，非常忙碌", "dog", [
    ("06:00", "叫醒人類（不接受賴床）"),
    ("07:00", "吃早餐"),
    ("07:01", "假裝沒吃過，再要一次"),
    ("09:00–17:00", "睡覺、睡覺、還是睡覺"),
    ("18:00", "門口罰站等你回家"),
], left_w=300)

rows_card("post3_cat_translate.jpg", "貓語翻譯機", "主子的行為，其實都有含義", "cat", [
    ("睡你鍵盤上", "你工作太久了，該陪我"),
    ("把杯子推下桌", "做物理實驗：地心引力"),
    ("凌晨三點跑酷", "這是我的健身時間"),
    ("對你慢慢眨眼", "我愛你（但不准抱我）"),
    ("盯著空氣看", "你不懂，那裡有東西"),
], left_w=330)

# post 4: poll
img, d = base("你家毛孩是哪一型？", "留言 A / B / C / D 告訴我們", "both")
opts = [("A", "吃貨型", "聽到塑膠袋聲音就衝過來"), ("B", "睡神型", "一天睡 20 小時，醒著也在發呆"),
        ("C", "拆家大師", "沙發、拖鞋、衛生紙，無一倖免"), ("D", "黏人精", "上廁所也要跟，關門就哭給你聽")]
y = 360
for i, (k, t, desc) in enumerate(opts):
    d.rounded_rectangle([s(60), s(y), s(1020), s(y+200)], radius=s(32), fill=WHITE)
    E(d, 150, y+100, 56, 56, ORANGE)
    kf = font("Black", 64)
    kw = d.textlength(k, font=kf)
    d.text((s(150) - kw/2, s(y+56)), k, font=kf, fill=WHITE)
    d.text((s(240), s(y+38)), t, font=font("Black", 48), fill=DARK)
    d.text((s(240), s(y+112)), desc, font=font("Medium", 34), fill=(130, 100, 80))
    y += 220
img.resize((1080, 1350), Image.LANCZOS).save(os.path.join(OUT, "post4_poll.jpg"), quality=92)
print("done")
