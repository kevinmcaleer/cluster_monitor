def hsv2rgb(h, s, v):
    """ Convert HSV (0-1, 0-1, 0-1) to an (R, G, B) tuple in 0-255 range """
    if not (0 <= h <= 1 and 0 <= s <= 1 and 0 <= v <= 1):
        raise ValueError("H, S, and V must be in range 0-1")

    i = int(h * 6)  # Which section of the HSV wheel (0-5)
    f = (h * 6) - i  # Fractional part of hue
    p = int(v * (1 - s) * 255)
    q = int(v * (1 - f * s) * 255)
    t = int(v * (1 - (1 - f) * s) * 255)
    v = int(v * 255)

    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return (r, g, b)

# Example usage:
# print(hsv2rgb(0.1667, 1, 1))  # Output: (255, 255, 0) - Yellow
# print(hsv2rgb(0.5, 1, 1))     # Output: (0, 255, 255) - Cyan

def rgb2hsv(r: int, g: int, b: int):
    """ Convert (R, G, B) values (0-255) to (H, S, V) values in range (0-1, 0-1, 0-1) """
    r_normal, g_normal, b_normal = r / 255, g / 255, b / 255
    cmax = max(r_normal, g_normal, b_normal)
    cmin = min(r_normal, g_normal, b_normal)
    delta = cmax - cmin

    # Hue calculation
    if delta == 0:
        h = 0
    elif cmax == r_normal:
        h = (60 * ((g_normal - b_normal) / delta))
        if h < 0:
            h += 360
    elif cmax == g_normal:
        h = (60 * ((b_normal - r_normal) / delta)) + 120
    elif cmax == b_normal:
        h = (60 * ((r_normal - g_normal) / delta)) + 240

    # Normalize hue (0-360° → 0-1)
    h = h / 360  # FIXED: Normalize correctly

    # Saturation calculation
    s = 0 if cmax == 0 else delta / cmax

    # Value calculation
    v = cmax

    print(f"RGB2HSV - r: {r}, g: {g}, b: {b} → h: {h}, s: {s}, v: {v}")
    return h, s, v

def hsv2hex(h, s, v):
    """ Convert HSV (0-1, 0-1, 0-1) to HEX string '#RRGGBB' """
    r, g, b = hsv2rgb(h, s, v)  # Convert HSV to RGB
    return rgb2hex(r, g, b)     # Convert RGB to HEX
def hex2rgb(hex_color):
    """ Convert hex color (e.g. '#FFA500' or 'FFA500') to an (R, G, B) tuple """
    hex_color = hex_color.strip('#')  # Remove '#' if present
    if len(hex_color) != 6:
        raise ValueError("Invalid HEX color. Must be 6 characters long.")
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
#     return (r, g, b)  # Return as tuple
    return (r, g, b)

def rgb2hex(r, g, b):
    """ Convert (R, G, B) tuple (0-255 range) to hex string '#RRGGBB' """
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be in the range 0-255")
    
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

    # Example usage:
    # print(rgb2hex(255, 165, 0))  # Output: #FFA500 (Orange)
    # print(rgb2hex(0, 255, 0))    # Output: #00FF00 (Green)
    # print(rgb2hex(75, 0, 130))   # Output: #4B0082 (Indigo)

