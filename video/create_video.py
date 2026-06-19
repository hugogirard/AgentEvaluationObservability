"""
Animated video: Agent hallucination gone wrong + Azure AI Foundry fix.
Wealth Advisory Assistant scenario from this repo.

Features: animated character faces (friendly -> evil morph), screen shake,
glitch/scanline effects, red flashes, typewriter text, smooth fades.
~35s total, 1920x1080, 24fps, black background.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, concatenate_videoclips

W, H = 1920, 1080
FPS = 24
BG = (0, 0, 0)
FONT_B = "C:/Windows/Fonts/arialbd.ttf"
FONT_R = "C:/Windows/Fonts/arial.ttf"

_font_cache = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    return _font_cache[key]


# ── animation helpers ────────────────────────────────────────────────

def ease(t, d):
    """Smooth ease-in-out (hermite)."""
    x = max(0.0, min(t / d, 1.0))
    return x * x * (3 - 2 * x)


def fade_env(t, dur, fi=0.5, fo=0.5):
    """Brightness multiplier: ramp up then ramp down at edges."""
    if t < fi:
        return t / fi
    if t > dur - fo:
        return max(0, (dur - t) / fo)
    return 1.0


def typewriter(text, t, cps=25):
    return text[: min(int(t * cps), len(text))]


# ── centered-text helper ────────────────────────────────────────────

def ctext(draw, y, text, f, fill=(255, 255, 255)):
    bbox = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - bbox[2] + bbox[0]) // 2, y), text, font=f, fill=fill)


# ── character drawing ────────────────────────────────────────────────

def draw_user(draw, cx, cy, r, t=0):
    """Blue circle face — the Relationship Manager."""
    bob = int(math.sin(t * 2) * 3)
    cy += bob
    c = (100, 180, 255)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    er = max(r // 8, 3)
    ey = cy - r // 5
    draw.ellipse([cx - r // 3 - er, ey - er, cx - r // 3 + er, ey + er], fill=c)
    draw.ellipse([cx + r // 3 - er, ey - er, cx + r // 3 + er, ey + er], fill=c)
    draw.arc(
        [cx - r // 3, cy + r // 8, cx + r // 3, cy + r // 3],
        start=10, end=170, fill=c, width=2,
    )


def draw_agent(draw, cx, cy, r, morph=0.0, t=0):
    """
    Circle face that smoothly morphs from friendly (morph=0) to evil (morph=1).
    Colour shifts white->red, smile->zigzag grin, eyebrows appear.
    """
    bob = int(math.sin(t * 2.5) * 4)
    cy += bob

    pulse = 0.85 + 0.15 * math.sin(t * 8) * morph
    hr = int((200 + 55 * morph) * pulse)
    hg = int(200 * (1 - morph) * pulse)
    hb = int(200 * (1 - morph) * pulse)
    hc = (min(hr, 255), max(hg, 0), max(hb, 0))

    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        outline=hc, width=3 + int(2 * morph),
    )

    # eyes
    er = max(r // 8 + int(r // 16 * morph), 3)
    ey = cy - int(r * 0.15) - int(r * 0.1 * morph)
    ec_r = min(255, int(255 * max(morph, 0.8 - 0.8 * morph)))
    ec = (ec_r, int(255 * (1 - morph)), int(255 * (1 - morph)))
    draw.ellipse([cx - r // 3 - er, ey - er, cx - r // 3 + er, ey + er], fill=ec)
    draw.ellipse([cx + r // 3 - er, ey - er, cx + r // 3 + er, ey + er], fill=ec)

    # angry eyebrows (fade in with morph)
    if morph > 0.1:
        bw = max(2, int(3 * morph))
        bc = tuple(int(c * morph) for c in hc)
        draw.line(
            [cx - r // 2, ey - r // 4 - int(5 * (1 - morph)),
             cx - r // 6, ey - r // 4 - int(12 * morph)],
            fill=bc, width=bw,
        )
        draw.line(
            [cx + r // 6, ey - r // 4 - int(12 * morph),
             cx + r // 2, ey - r // 4 - int(5 * (1 - morph))],
            fill=bc, width=bw,
        )

    # mouth: arc smile -> zigzag evil grin
    if morph < 0.3:
        arc_h = max(1, int(r * 0.45 * (1 - morph / 0.3)))
        draw.arc(
            [cx - r // 2, cy, cx + r // 2, cy + arc_h],
            start=10, end=170, fill=hc, width=2,
        )
    else:
        gi = (morph - 0.3) / 0.7
        teeth = 6
        gw = r * 0.45 * (0.5 + 0.5 * gi)
        gd = r * 0.18 * gi
        my = cy + int(r * 0.25)
        pts = []
        for i in range(teeth * 2 + 1):
            px = cx - gw + (2 * gw * i) / (teeth * 2)
            py = my - gd if i % 2 == 0 else my + gd
            pts.append((int(px), int(py)))
        if len(pts) >= 2:
            draw.line(pts, fill=hc, width=max(2, int(3 * morph)))


def draw_shield(draw, cx, cy, s, t=0):
    """Green shield with animated checkmark."""
    s = int(s * (1 + 0.03 * math.sin(t * 4)))
    gc = (0, 200, 100)
    pts = [
        (cx, cy - s),
        (cx + int(s * 0.8), cy - int(s * 0.4)),
        (cx + int(s * 0.6), cy + int(s * 0.6)),
        (cx, cy + s),
        (cx - int(s * 0.6), cy + int(s * 0.6)),
        (cx - int(s * 0.8), cy - int(s * 0.4)),
    ]
    draw.polygon(pts, outline=gc, width=3)
    draw.line(
        [(cx - int(s * 0.25), cy), (cx - int(s * 0.05), cy + int(s * 0.25))],
        fill=gc, width=4,
    )
    draw.line(
        [(cx - int(s * 0.05), cy + int(s * 0.25)),
         (cx + int(s * 0.3), cy - int(s * 0.2))],
        fill=gc, width=4,
    )


# ── post-processing effects ─────────────────────────────────────────

def fx_shake(frame, intensity):
    if intensity < 1:
        return frame
    h, w = frame.shape[:2]
    dx = int(np.random.uniform(-intensity, intensity))
    dy = int(np.random.uniform(-intensity, intensity))
    out = np.zeros_like(frame)
    sx1, sy1 = max(0, dx), max(0, dy)
    sx2, sy2 = min(w, w + dx), min(h, h + dy)
    dx1, dy1 = max(0, -dx), max(0, -dy)
    out[dy1 : dy1 + sy2 - sy1, dx1 : dx1 + sx2 - sx1] = frame[sy1:sy2, sx1:sx2]
    return out


def fx_red(frame, intensity):
    if intensity <= 0:
        return frame
    f = frame.astype(np.float32)
    f[:, :, 0] = np.clip(f[:, :, 0] + 120 * intensity, 0, 255)
    f[:, :, 1] *= 1 - 0.5 * intensity
    f[:, :, 2] *= 1 - 0.5 * intensity
    return f.astype(np.uint8)


def fx_glitch(frame, intensity):
    if intensity <= 0:
        return frame
    out = frame.copy()
    h = out.shape[0]
    for _ in range(int(intensity * 15)):
        y = np.random.randint(0, h)
        shift = np.random.randint(-int(intensity * 40), int(intensity * 40) + 1)
        out[y] = np.roll(out[y], shift, axis=0)
    return out


def fx_scanlines(frame, alpha=0.15):
    out = frame.astype(np.float32)
    out[::3] *= 1 - alpha
    return np.clip(out, 0, 255).astype(np.uint8)


def fx_fade(frame, factor):
    if factor >= 1.0:
        return frame
    return (frame.astype(np.float32) * max(factor, 0)).astype(np.uint8)


# ═════════════════════════════════════════════════════════════════════
# SCENE 1 — Title (3.5 s)
# ═════════════════════════════════════════════════════════════════════
def scene_title():
    dur = 5.0

    def mf(t):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        a1 = ease(t, 1.5)
        c = int(255 * a1)
        ctext(d, 340, "When AI Agents Hallucinate...", font(72, True), (c, c, c))
        if t > 1.2:
            a2 = ease(t - 1.2, 1.2)
            ctext(d, 450, "...things can go very wrong",
                  font(40), (0, int(120 * a2), int(212 * a2)))
        if t > 2.4:
            a3 = ease(t - 2.4, 1.0)
            g = int(180 * a3)
            ctext(d, 550,
                  "Wealth Advisory Assistant  |  Azure AI Foundry",
                  font(26), (g, g, g))
        f = np.array(img)
        return fx_fade(f, fade_env(t, dur, fi=0.0, fo=0.8))

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# SCENE 2 — User asks the question (5.5 s)
# ═════════════════════════════════════════════════════════════════════
def scene_user_asks():
    dur = 7.5
    q_line1 = "Client 1042 is asking about"
    q_line2 = "rebalancing. What do you recommend?"

    def mf(t):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)

        # user face slides in from left
        ux = int(-100 + 380 * ease(t, 1.2))
        draw_user(d, ux, 400, 90, t)
        if t > 0.5:
            a = ease(t - 0.5, 0.8)
            lc = tuple(int(v * a) for v in (100, 180, 255))
            d.text((ux - 110, 520), "Relationship Manager", font=font(20), fill=lc)

        # speech bubble
        if t > 1.5:
            ba = ease(t - 1.5, 0.8)
            bx, by, bw, bh = ux + 150, 330, 680, 140
            bc = tuple(int(v * ba) for v in (80, 80, 90))
            bf = tuple(int(v * ba) for v in (20, 20, 30))
            d.rounded_rectangle([bx, by, bx + bw, by + bh],
                                radius=15, outline=bc, fill=bf, width=2)
            # tail pointing left
            d.polygon([(bx, by + 50), (bx - 18, by + 65), (bx, by + 72)], fill=bf)

            if t > 2.0:
                tc = int(255 * ba)
                shown1 = typewriter(q_line1, t - 2.0, 22)
                shown2 = typewriter(q_line2, max(0, t - 2.0 - len(q_line1) / 22), 22)
                d.text((bx + 30, by + 30), shown1, font=font(28), fill=(tc, tc, tc))
                d.text((bx + 30, by + 70), shown2, font=font(28), fill=(tc, tc, tc))

        # agent face slides in from right
        if t > 3.5:
            aa = ease(t - 3.5, 1.0)
            ax = int(2020 - 500 * aa)
            draw_agent(d, ax, 400, 90, morph=0.0, t=t)
            if t > 4.2:
                la = ease(t - 4.2, 0.6)
                gc = int(200 * la)
                d.text((ax - 40, 520), "AI Agent", font=font(20), fill=(gc, gc, gc))

        # thinking dots
        if t > 5.5:
            dots = "." * (1 + int((t - 5.5) * 2) % 3)
            d.text((1480, 370), dots, font=font(44, True), fill=(200, 200, 200))

        f = np.array(img)
        return fx_fade(f, fade_env(t, dur, fi=0.5, fo=0.7))

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# SCENE 3 — Hallucination horror (11 s)
# ═════════════════════════════════════════════════════════════════════
def scene_hallucination():
    dur = 18.0
    answers = [
        (2.5,  '[X]  "Client 1042 has 70% bonds, 30% equities"',
               "      INVENTED DATA -- never called the tool!"),
        (7.0,  '[X]  "I recommend our Premium Growth Fund"',
               "      FUND DOESN\'T EXIST -- hallucinated product!"),
        (11.5, '[X]  "Expected annual return: 12%"',
               "      FABRICATED NUMBERS -- compliance violation!"),
    ]

    def mf(t):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)

        morph = min(t / 5.0, 1.0)

        # agent face — gets bigger and morphs
        ar = 100 + int(30 * morph)
        draw_agent(d, 1520, 280, ar, morph=morph, t=t)
        lc_r = int(200 + 55 * morph)
        lc_g = int(200 * (1 - morph))
        label = "AI Agent" if morph < 0.5 else "AI Agent !!!"
        d.text((1440, 280 + ar + 30), label,
               font=font(22, True), fill=(lc_r, lc_g, lc_g))

        # user face (smaller, on the left)
        draw_user(d, 180, 280, 75, t)
        d.text((100, 380), "Relationship Mgr", font=font(18), fill=(80, 140, 220))

        # wrong answers slide in one by one with plenty of reading time
        for i, (trigger, ans, note) in enumerate(answers):
            if t < trigger:
                continue
            aa = ease(t - trigger, 0.8)
            x_off = int(200 * (1 - aa))
            yb = 480 + i * 120
            ac = int(255 * aa)
            d.text((280 + x_off, yb), ans, font=font(28, True), fill=(ac, ac, ac))
            if t > trigger + 1.0:
                na = ease(t - trigger - 1.0, 0.6)
                d.text((280 + x_off, yb + 38), note,
                       font=font(22), fill=(int(255 * na), int(60 * na), int(60 * na)))

        # climax pulsing text — only at the very end
        if t > 15.5:
            pulse = 0.5 + 0.5 * math.sin(t * 10)
            pc = int(255 * pulse)
            ctext(d, 180, "!! HALLUCINATION !!",
                  font(60, True), (pc, int(pc * 0.25), int(pc * 0.1)))

        frame = np.array(img)

        # subtle colour/scanline effects only — no shake
        red = morph * 0.04 + (0.06 if t > 11 else 0)
        frame = fx_red(frame, max(0, red))

        if t > 12:
            frame = fx_scanlines(frame, 0.06)

        return fx_fade(frame, fade_env(t, dur, fi=0.4, fo=0.6))

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# SCENE 3b — Static glitch transition (0.6 s)
# ═════════════════════════════════════════════════════════════════════
def scene_static():
    dur = 0.6

    def mf(t):
        noise = np.random.randint(0, 50, (H, W, 3), dtype=np.uint8)
        brightness = max(0, 1.0 - t / dur)
        return (noise * brightness).astype(np.uint8)

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# SCENE 4 — Azure AI Foundry saves the day (11 s)
# ═════════════════════════════════════════════════════════════════════
def scene_foundry():
    dur = 14.0
    evals = [
        (3.0, "Groundedness",       "FAIL", True),
        (4.5, "Tool Call Accuracy",  "FAIL", True),
        (6.0, "Task Adherence",      "FAIL", True),
        (7.5, "Coherence",           "PASS", False),
        (8.5, "Relevance",           "PASS", False),
        (9.5, "Fluency",             "PASS", False),
    ]

    def mf(t):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)

        # title
        ta = ease(t, 1.5)
        ctext(d, 60, "Azure AI Foundry",
              font(58, True), (0, int(120 * ta), int(212 * ta)))
        if t > 1.0:
            sa = ease(t - 1.0, 1.2)
            sc = int(220 * sa)
            ctext(d, 145, "14 Built-in Evaluators Run Automatically",
                  font(30), (sc, sc, sc))

        # shield
        if t > 2.0:
            draw_shield(d, W // 2, 420, int(80 * ease(t - 2.0, 1.2)), t)

        # evaluator results
        for i, (tr, name, result, fail) in enumerate(evals):
            if t < tr:
                continue
            ea = ease(t - tr, 0.8)
            y = 260 + i * 50
            x = int(-300 + 500 * ea)
            nc = int(220 * ea)
            d.text((x, y), name, font=font(26), fill=(nc, nc, nc))
            if fail:
                rc = (int(255 * ea), int(60 * ea), int(60 * ea))
            else:
                rc = (int(80 * ea), int(220 * ea), int(130 * ea))
            d.text((x + 380, y), "-> " + result, font=font(26, True), fill=rc)

        # quality gate stamp
        if t > 10.5:
            sta = ease(t - 10.5, 0.5)
            sw, sh = 750, 80
            sx = (W - sw) // 2
            sy = 570
            bc = (int(255 * sta), int(80 * sta), int(80 * sta))
            d.rectangle([sx, sy, sx + sw, sy + sh], outline=bc, width=4)
            ctext(d, sy + 18, "QUALITY GATE : DEPLOY BLOCKED",
                  font(36, True), bc)

        if t > 11.5:
            ba = ease(t - 11.5, 1.0)
            gc = int(180 * ba)
            ctext(d, 720, "Hallucination caught BEFORE reaching production",
                  font(28), (gc, gc, gc))

        f = np.array(img)
        return fx_fade(f, fade_env(t, dur, fi=0.7, fo=0.8))

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# SCENE 5 — Observability pillars (5.5 s)
# ═════════════════════════════════════════════════════════════════════
def scene_observability():
    dur = 10.0
    items = [
        (1.2, "[1]  CI/CD Evaluation",
              "Every PR measured before merge"),
        (3.0, "[2]  Production Sampling",
              "Live traffic scored for quality drift"),
        (4.8, "[3]  Scheduled Evaluation",
              "Full regression runs with alerts"),
        (6.6, "[4]  OpenTelemetry Tracing",
              "Every agent turn captured as spans"),
    ]

    def mf(t):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)

        ta = ease(t, 1.0)
        ctext(d, 100, "Continuous Observability",
              font(52, True), (0, int(120 * ta), int(212 * ta)))

        for i, (tr, title, desc) in enumerate(items):
            if t < tr:
                continue
            ia = ease(t - tr, 0.8)
            y = 260 + i * 130
            y_off = int(40 * (1 - ia))
            c = int(255 * ia)
            d.text((300, y + y_off), title, font=font(34, True), fill=(c, c, c))
            if t > tr + 0.5:
                da = ease(t - tr - 0.5, 0.5)
                dc = int(160 * da)
                d.text((340, y + 46 + y_off), desc, font=font(24), fill=(dc, dc, dc))

        if t > 8.5:
            ba = ease(t - 8.5, 0.6)
            gc = (int(80 * ba), int(220 * ba), int(130 * ba))
            ctext(d, 820,
                  "Every change measured  |  Drift detected early  |  Quality proven",
                  font(28), gc)

        f = np.array(img)
        return fx_fade(f, fade_env(t, dur, fi=0.7, fo=0.8))

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# SCENE 6 — Closing (6 s)
# ═════════════════════════════════════════════════════════════════════
def scene_closing():
    dur = 6.0

    def mf(t):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)

        a = ease(t, 1.2)
        ctext(d, 340, "Azure AI Foundry",
              font(64, True), (0, int(120 * a), int(212 * a)))
        if t > 1.0:
            ta = ease(t - 1.0, 1.0)
            tc = int(240 * ta)
            ctext(d, 440, "Turn agent development from guesswork",
                  font(34), (tc, tc, tc))
            ctext(d, 490, "into an engineering discipline",
                  font(34), (tc, tc, tc))
        if t > 2.0:
            la = ease(t - 2.0, 0.8)
            lc = int(140 * la)
            ctext(d, 600, "learn.microsoft.com/azure/ai-foundry",
                  font(22), (lc, lc, lc))

        f = np.array(img)
        return fx_fade(f, fade_env(t, dur, fi=0.4, fo=1.5))

    return VideoClip(frame_function=mf, duration=dur)


# ═════════════════════════════════════════════════════════════════════
# BUILD & RENDER
# ═════════════════════════════════════════════════════════════════════
def main():
    print("Building scenes...")
    clips = [
        scene_title(),          # 5.0 s
        scene_user_asks(),      # 7.5 s
        scene_hallucination(),  # 18  s
        scene_static(),         # 0.6 s
        scene_foundry(),        # 14  s
        scene_observability(),  # 10  s
        scene_closing(),        # 6   s
    ]                           # ~61 s total

    final = concatenate_videoclips(clips, method="compose")
    out = "video/agent_hallucination_demo.mp4"

    print(f"Rendering {final.duration:.1f}s video to {out} ...")
    final.write_videofile(out, fps=FPS, codec="libx264",
                          audio=False, preset="medium", logger="bar")
    print(f"Done! Saved to {out}")


if __name__ == "__main__":
    main()
