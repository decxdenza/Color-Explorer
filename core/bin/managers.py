from core.libraries import *

class ColorManager():

    @staticmethod
    def to_hex(col: RGB | HSV | YIQ) -> HEX:
        if (type(col) == RGB):
            r, g, b = col.r, col.g, col.b
        elif (type(col) == HSV or type(col) == YIQ):
            rgb = ColorManager.to_rgb(col)
            r, g, b = rgb.r, rgb.g, rgb.b
        return HEX('#{:02X}{:02X}{:02X}'.format(max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255))))
    
    @staticmethod
    def to_rgb(col: HEX | HSV | HSL | YIQ) -> RGB:
        if (type(col) == HEX):
            return RGB(tuple(int(col.code.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
        elif (type(col) == HSV):
            h_i = math.floor(col.h / 60) % 6
            vmin = (100-col.s)*col.v/100
            a = (col.v - vmin) * (col.h % 60) / 60
            vinc = vmin + a
            vdec = col.v - a
            r, g, b = 0, 0, 0
            match(h_i):
                case 0:
                    r, g, b = col.v, vinc, vmin
                case 1:
                    r, g, b = vdec, col.v, vmin
                case 2:
                    r, g, b = vmin, col.v, vinc
                case 3:
                    r, g, b = vmin, vdec, col.v
                case 4:
                    r, g, b = vinc, vmin, col.v
                case 5:
                    r, g, b = col.v, vmin, vdec
            return RGB((round(r*255/100), round(g*255/100), round(b*255/100)))
        elif (type(col) == HSL):
            pass
            h, s, l = col.h, col.s / 100, col.l / 100
            c = (1-abs(2*l-1))*s
            hc = h/60
            x = c*(1-abs((hc)%2-1))
            m = l-(c/2)
            rc, gc, bc = 0, 0, 0
            if (hc <= 0 and hc < 1):
                rc, gc, bc = c, x, 0
            if (hc <= 1 and hc < 2):
                rc, gc, bc = x, c, 0
            if (hc <= 2 and hc < 3):
                rc, gc, bc = 0, c, x
            if (hc <= 3 and hc < 4):
                rc, gc, bc = 0, x, c
            if (hc <= 4 and hc < 5):
                rc, gc, bc = x, 0, c
            if (hc <= 5 and hc < 6):
                rc, gc, bc = c, 0, x
            return RGB((round((rc+m)*255), round((gc+m)*255), round((bc+m)*255)))
        elif (type(col) == YIQ):
            r = col.y+0.956*col.i+0.623*col.q
            g = col.y-0.272*col.i-0.648*col.q
            b = col.y-1.105*col.i+1.705*col.q
            return RGB((round(r), round(g), round(b)))
    
    @staticmethod
    def to_hsv(col: RGB | HEX | YIQ, _round: bool = False) -> HSV:
        if (type(col) == RGB):
            r, g, b = col.r/255, col.g/255, col.b/255
        elif (type(col) == HEX or type(col) == YIQ):
            rgb = ColorManager.to_rgb(col)
            r, g, b = rgb.r/255, rgb.g/255, rgb.b/255
        max_ = max(r, g, b)
        min_ = min(r, g, b)
        range = max_-min_
        if max_ == min_:
            h = 0
        elif max_ == r:
            h = (60 * ((g-b)/range) + 360) % 360
        elif max_ == g:
            h = (60 * ((b-r)/range) + 120) % 360
        elif max_ == b:
            h = (60 * ((r-g)/range) + 240) % 360
        if max_ == 0:
            s = 0
        else:
            s = (range/max_)*100
        v = max_*100
        if (_round):
            return HSV((round(h), round(s), round(v)))
        return HSV((h, s, v))
    
    @staticmethod
    def to_hsl(col: RGB | HEX | HSV | YIQ, _round: bool = False) -> HSL:
        if (type(col) == RGB):
            r, g, b = col.r/255, col.g/255, col.b/255
        elif (type(col) == HEX or type(col) == HSV or type(col) == YIQ):
            rgb = ColorManager.to_rgb(col)
            r, g, b = rgb.r/255, rgb.g/255, rgb.b/255
        min_ = min(r, g, b)
        max_ = max(r, g, b)
        h, s, l = 0, 0, 0
        dlt = max_-min_
        if (dlt == 0):
            h = 0
        elif (max_ == r):
            h = ((g-b) / dlt) % 6
        elif (max == g):
            h = (b-r) / dlt + 2
        else:
            h = (r-g) / dlt + 4
        h = round(h * 60, 0)
        if (h < 0):
            h += 360
        l = (max_+min_) / 2
        s = 0 if (dlt == 0) else dlt / (1-abs(2 * l-1))
        s = round(+(s*100), 1)
        l = round(+(l*100), 1)
        if (_round):
            return HSL((round(h), round(s), round(l)))
        return HSL((h, s, l))

    @staticmethod
    def to_yiq(col: RGB | HEX | HSV, _round: bool = False) -> YIQ:
        if (type(col) == RGB):
            r, g, b = col.r, col.g, col.b
        elif (type(col) == HEX or type(col) == HSV):
            rgb = ColorManager.to_rgb(col)
            r, g, b = rgb.r, rgb.g, rgb.b
        y = 0.299*r+0.587*g+0.114*b
        i = 0.596*r-0.274*g-0.322*b
        q = 0.211*r-0.522*g+0.311*b
        if (_round):
            return YIQ((round(y), round(i), round(q)))
        return YIQ((y, i, q))
    
    @staticmethod
    def bright(col: RGB | HEX | HSV | YIQ) -> bool:
        rgb = ColorManager.to_rgb(col) if (type(col) in [HEX, HSV, YIQ]) else col
        hsp = math.sqrt(0.299 * (rgb.r * rgb.r) + 0.587 * (rgb.g * rgb.g) + 0.114 * (rgb.b * rgb.b))
        if (hsp > 127.5): return True
        else: return False

class Sequencer():

    @staticmethod
    def get_matches_stw(pattern, seq) -> list | None:
        matches = []
        for obj in seq:
            if (str(obj).startswith(pattern)):
                matches.append(obj)
        return matches
    
    @staticmethod
    def get_matches_lstw(pattern, seq) -> list | None:
        matches = []
        for obj in seq:
            if (str(obj).lower().startswith(str(pattern).lower())):
                matches.append(obj)
        return matches

    @staticmethod
    def get_matches_cts(pattern, seq) -> list | None:
        matches = []
        for obj in seq:
            if (pattern in str(obj)):
                matches.append(obj)
        return matches

    @staticmethod
    def get_matches_esw(pattern, seq) -> list | None:
        matches = []
        for obj in seq:
            if (str(obj).endswith(pattern)):
                matches.append(obj)
        return obj