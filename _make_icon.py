import struct, zlib, os

# ---------- Minimal PNG encoder ----------
def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)

def write_png(w, h, rgba):
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw.extend(rgba[y * stride:(y + 1) * stride])
    idat = zlib.compress(bytes(raw), 9)
    return sig + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")

# ---------- Minimal ICO encoder (PNG entries) ----------
def write_ico(images):
    count = len(images)
    header = struct.pack("<HHH", 0, 1, count)
    offset = 6 + count * 16
    entries = b""
    data = b""
    for size, png in images:
        s = 0 if size >= 256 else size
        entries += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(png), offset)
        data += png
        offset += len(png)
    return header + entries + data

# ---------- Icon rendering ----------
def in_rounded_rect(x, y, x0, y0, x1, y1, r):
    if x < x0 or x > x1 or y < y0 or y > y1:
        return False
    cx = min(max(x, x0 + r), x1 - r)
    cy = min(max(y, y0 + r), y1 - r)
    dx = x - cx
    dy = y - cy
    return dx * dx + dy * dy <= r * r

def render(size):
    rgba = bytearray(size * size * 4)
    S = float(size)
    bg_r = int(S * 0.22)
    # key rect
    kx0, ky0, kx1, ky1 = S * 0.24, S * 0.30, S * 0.76, S * 0.70
    kr = S * 0.10
    # T bars
    th_x0, th_x1, th_y0, th_y1 = S * 0.34, S * 0.66, S * 0.365, S * 0.435
    tv_x0, tv_x1, tv_y0, tv_y1 = S * 0.470, S * 0.530, S * 0.435, S * 0.625
    # speed lines (green)
    lines = [(S*0.80, S*0.88, S*0.38, S*0.40),
             (S*0.82, S*0.92, S*0.49, S*0.51),
             (S*0.80, S*0.88, S*0.60, S*0.62)]
    # cursor bar (purple)
    cur_x0, cur_x1, cur_y0, cur_y1 = S*0.30, S*0.70, S*0.80, S*0.845

    for y in range(size):
        for x in range(size):
            i = (y * size + x) * 4
            if not in_rounded_rect(x, y, 0, 0, size - 1, size - 1, bg_r):
                rgba[i+3] = 0
                continue
            # gradient navy -> blue
            t = y / S
            r = int(15 + (79 - 15) * t)
            g = int(17 + (92 - 17) * t)
            b = int(21 + (249 - 21) * t)
            a = 255
            # key
            if in_rounded_rect(x, y, kx0, ky0, kx1, ky1, kr):
                r, g, b = 245, 248, 252
                # T shape
                if (th_x0 <= x <= th_x1 and th_y0 <= y <= th_y1) or \
                   (tv_x0 <= x <= tv_x1 and tv_y0 <= y <= tv_y1):
                    r, g, b = 30, 40, 60
            # speed lines
            for lx0, lx1, ly0, ly1 in lines:
                if lx0 <= x <= lx1 and ly0 <= y <= ly1:
                    r, g, b = 126, 231, 135
            # cursor bar
            if cur_x0 <= x <= cur_x1 and cur_y0 <= y <= cur_y1:
                r, g, b = 124, 92, 255
            rgba[i] = r; rgba[i+1] = g; rgba[i+2] = b; rgba[i+3] = a
    return bytes(rgba)

def main():
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    for s in sizes:
        rgba = render(s)
        png = write_png(s, s, rgba)
        images.append((s, png))
    ico = write_ico(images)
    with open("app_icon.ico", "wb") as f:
        f.write(ico)
    # preview png
    preview = write_png(256, 256, render(256))
    with open("app_icon.png", "wb") as f:
        f.write(preview)
    print("Generated app_icon.ico (%d bytes) and app_icon.png" % len(ico))

if __name__ == "__main__":
    main()
