import sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
W, H, FPS, DUR = 1080, 1920, 30, 16.0
SS = 2  # sprite supersample

def font(weight, size):
    path = f"/usr/share/fonts/opentype/noto/NotoSansCJK-{weight}.ttc"
    for i in range(10):
        try: f = ImageFont.truetype(path, size, index=i)
        except Exception: break
        if "TC" in f.getname()[0]: return f
    return ImageFont.truetype(path, size)

CREAM = (255, 246, 232); ORANGE = (255, 159, 67); DARK = (74, 52, 40)
SOFT = (255, 226, 190); WHITE = (255, 255, 255)

def ease_out_back(t):
    t = max(0, min(1, t)); c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def ease_out(t):
    t = max(0, min(1, t)); return 1 - (1 - t) ** 3

def cat_sprite(k):
    sz = int(240 * k * SS)
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = cy = sz / 2; k = k * SS
    def E(x, y, rx, ry, f): d.ellipse([x-rx, y-ry, x+rx, y+ry], fill=f)
    col = (245, 166, 80)
    d.polygon([(cx-62*k, cy-10*k), (cx-50*k, cy-80*k), (cx-10*k, cy-50*k)], fill=col)
    d.polygon([(cx+62*k, cy-10*k), (cx+50*k, cy-80*k), (cx+10*k, cy-50*k)], fill=col)
    d.polygon([(cx-52*k, cy-22*k), (cx-46*k, cy-62*k), (cx-22*k, cy-44*k)], fill=(255, 190, 180))
    d.polygon([(cx+52*k, cy-22*k), (cx+46*k, cy-62*k), (cx+22*k, cy-44*k)], fill=(255, 190, 180))
    E(cx, cy, 72*k, 60*k, col)
    for dx in (-14, 0, 14):
        d.line([(cx+dx*k, cy-58*k), (cx+dx*0.8*k, cy-38*k)], fill=(205, 120, 50), width=int(5*k))
    E(cx, cy+24*k, 34*k, 22*k, (255, 244, 230))
    E(cx-26*k, cy-6*k, 9*k, 11*k, (43, 30, 22)); E(cx+26*k, cy-6*k, 9*k, 11*k, (43, 30, 22))
    E(cx-23*k, cy-10*k, 3*k, 3*k, WHITE); E(cx+29*k, cy-10*k, 3*k, 3*k, WHITE)
    d.polygon([(cx-7*k, cy+10*k), (cx+7*k, cy+10*k), (cx, cy+18*k)], fill=(240, 120, 130))
    for side in (-1, 1):
        for i in range(3):
            d.line([(cx+side*30*k, cy+(20+i*7)*k), (cx+side*85*k, cy+(12+i*12)*k)], fill=DARK, width=max(2, int(1.6*k)))
    return im.resize((sz // SS, sz // SS), Image.LANCZOS)

def dog_sprite(k):
    sz = int(240 * k * SS)
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = cy = sz / 2; k = k * SS
    def E(x, y, rx, ry, f): d.ellipse([x-rx, y-ry, x+rx, y+ry], fill=f)
    E(cx-62*k, cy+5*k, 28*k, 48*k, (138, 90, 59)); E(cx+62*k, cy+5*k, 28*k, 48*k, (138, 90, 59))
    E(cx, cy, 70*k, 64*k, (233, 185, 138))
    E(cx, cy+25*k, 40*k, 30*k, (255, 244, 230))
    E(cx-27*k, cy-8*k, 8*k, 10*k, (43, 30, 22)); E(cx+27*k, cy-8*k, 8*k, 10*k, (43, 30, 22))
    E(cx-24*k, cy-12*k, 3*k, 3*k, WHITE); E(cx+30*k, cy-12*k, 3*k, 3*k, WHITE)
    E(cx, cy+12*k, 12*k, 8*k, (43, 30, 22))
    E(cx, cy+36*k, 7*k, 9*k, (255, 126, 138))
    return im.resize((sz // SS, sz // SS), Image.LANCZOS)

def pill(w, h, fill, text, fnt, color, align="center", pad=36):
    im = Image.new("RGBA", (w*SS, h*SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w*SS-1, h*SS-1], radius=30*SS, fill=fill)
    f = font(*fnt) if isinstance(fnt, tuple) else fnt
    f = font(fnt[0], fnt[1]*SS)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    x = (w*SS - tw)/2 - bb[0] if align == "center" else pad*SS - bb[0]
    d.text((x, (h*SS - th)/2 - bb[1]), text, font=f, fill=color)
    return im.resize((w, h), Image.LANCZOS)

rows = [("1", "把你的杯子推下桌"),
        ("2", "凌晨三點踩你的臉"),
        ("3", "坐在你的鍵盤上開會"),
        ("4", "睡在你剛洗好的衣服上"),
        ("5", "一直盯著你，直到你投降")]
LW, RW, RH = 150, 780, 170
lefts = [pill(LW, RH, ORANGE, a, ("Black", 64), WHITE) for a, _ in rows]
rights = [pill(RW, RH, WHITE, b, ("Bold", 46), DARK, align="left", pad=44) for _, b in rows]

def pumpkin_sprite(k):
    sz = int(200 * k * SS)
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = cy = sz / 2; k = k * SS
    d.rounded_rectangle([cx-8*k, cy-78*k, cx+8*k, cy-48*k], radius=int(4*k), fill=(110, 140, 60))
    for dx, rx in [(-34, 40), (34, 40), (0, 44)]:
        d.ellipse([cx+dx*k-rx*k, cy-52*k, cx+dx*k+rx*k, cy+58*k], fill=(240, 130, 40) if dx else (250, 150, 55))
    d.polygon([(cx-36*k, cy-14*k), (cx-18*k, cy-14*k), (cx-27*k, cy-32*k)], fill=DARK)
    d.polygon([(cx+36*k, cy-14*k), (cx+18*k, cy-14*k), (cx+27*k, cy-32*k)], fill=DARK)
    d.chord([cx-40*k, cy-10*k, cx+40*k, cy+40*k], 0, 180, fill=DARK)
    return im.resize((sz // SS, sz // SS), Image.LANCZOS)
pump = pumpkin_sprite(0.9)
pump_end = pumpkin_sprite(1.6)
cat_big = cat_sprite(1.3)
cat_end = cat_sprite(2.2)
dog_end = dog_sprite(2.2)

# static background
bg = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(bg)
d.rectangle([0, 0, W, 420], fill=ORANGE)
for x, y, r in [(80, 70, 16), (1000, 380, 14), (960, 90, 12)]:
    d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 190, 120))
d.text((60, 1790), "@petfunny.tw ｜ 毛孩日常 Paw Daily", font=font("Medium", 34), fill=(170, 130, 100))

title_f, sub_f = font("Black", 88), font("Medium", 44)

def paste_scaled(frame, spr, cx, cy, sc, alpha=1.0):
    if sc <= 0.01 or alpha <= 0: return
    w, h = max(1, int(spr.width*sc)), max(1, int(spr.height*sc))
    s2 = spr.resize((w, h), Image.BILINEAR)
    if alpha < 1:
        a = s2.split()[3].point(lambda v: int(v*alpha)); s2.putalpha(a)
    frame.paste(s2, (int(cx - w/2), int(cy - h/2)), s2)

ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
    "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)

N = int(DUR * FPS)
for n in range(N):
    t = n / FPS
    fr = bg.copy(); d = ImageDraw.Draw(fr)
    # title slide down
    ty = -140 + 240 * ease_out(t / 0.6)
    d.text((60, ty), "不給罐罐就搗蛋", font=title_f, fill=WHITE)
    if t > 0.7:
        a = ease_out((t - 0.7) / 0.5)
        d.text((64, 250 + 20 * (1 - a)), "萬聖節特輯：主子的搗蛋清單", font=sub_f,
               fill=tuple(int(ORANGE[k] + ((255, 240, 220)[k] - ORANGE[k]) * a) for k in range(3)))
    # mascot bounce
    sc = ease_out_back((t - 0.2) / 0.6)
    bob = 10 * math.sin(t * 4)
    paste_scaled(fr, cat_big, 950, 220 + bob, sc)
    paste_scaled(fr, pump, 830, 330 - bob*0.6, ease_out_back((t - 0.5) / 0.6))
    # rows
    for i in range(5):
        t0 = 1.6 + i * 2.1
        y = 520 + i * (RH + 40) + RH / 2
        paste_scaled(fr, lefts[i], 60 + LW / 2, y, ease_out_back((t - t0) / 0.45))
        tr = ease_out((t - t0 - 0.5) / 0.45)
        if tr > 0:
            x = 60 + LW + 30 + RW / 2 + (1 - tr) * 500
            paste_scaled(fr, rights[i], x, y, 1.0, tr)
    # end card
    te = 12.6
    if t > te:
        a = ease_out((t - te) / 0.5)
        ov = Image.new("RGB", (W, H), ORANGE)
        fr = Image.blend(fr, ov, a); d = ImageDraw.Draw(fr)
        if t > te + 0.3:
            es = ease_out_back((t - te - 0.3) / 0.6)
            paste_scaled(fr, cat_end, W / 2 - 220, 700 + 14 * math.sin(t * 5), es)
            paste_scaled(fr, pump_end, W / 2 + 220, 720 + 14 * math.sin(t * 5 + 1.5), es)
            ta = ease_out((t - te - 0.6) / 0.5)
            for txt, f, yy in [("你家主子今天", font("Black", 84), 1060), ("搗蛋了沒？", font("Black", 84), 1170),
                               ("留言交出牠的搗蛋紀錄", font("Bold", 56), 1330), ("@petfunny.tw", font("Medium", 44), 1700)]:
                tw = d.textlength(txt, font=f)
                col = tuple(int(ORANGE[k] + (255 - ORANGE[k]) * ta) for k in range(3))
                d.text(((W - tw) / 2, yy + 30 * (1 - ta)), txt, font=f, fill=col)
    ff.stdin.write(fr.convert("RGB").tobytes())
ff.stdin.close(); ff.wait()
print("ok", ff.returncode)
