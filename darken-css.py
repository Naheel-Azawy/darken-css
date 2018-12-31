import sys
import re
import statistics
import argparse

parser = argparse.ArgumentParser(description="Darken CSS style sheets")
parser.add_argument('--darkness', help='How much darkness to be added',
                    metavar="N", type=float, default=7)
parser.add_argument('--sd-thr', help='Standard deviation threshold. The higher the more colorful colors will be darkened (0 will only darken grayscale colors)',
                    metavar="N", type=float, default=2)
parser.add_argument('--avg-thr', help='Average threshold. The higher the more light colors will be dimmed',
                    metavar="N", type=float, default=80)

args = parser.parse_args()

darkness = args.darkness
sd_thr = args.sd_thr
avg_thr = args.avg_thr

def hex2str(i):
    return "#%06x" % i

def rgba2str(r, g, b, a):
    return "rgba(%d, %d, %d, %s)" % (r, g, b, a)

for line in sys.stdin:
    m = re.findall(r'#([\da-fA-F]{6})', line)
    if m:
        for color_str in m:
            c = int(color_str, 16)
            r = c >> 16
            g = (c >> 8) & 0xff
            b = c & 0xff
            sd = statistics.stdev([r, g, b])
            if sd < sd_thr: # grayscale (sd = 0) or sort of grayscale
                avg = int((r + g + b) / 3)
                if avg < avg_thr:
                    avg = int(avg / darkness) # darken
                    r = g = b = avg # force grayscale
                    c2 = (r << 16) + (g << 8) + b
                    line = line.replace(hex2str(c), hex2str(c2))
    m = re.findall(r'(rgba\(\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\))', line)
    if m:
        for color_str in m:
            m = re.findall(r'rgba\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)', color_str)
            r = int(m[0][0])
            g = int(m[0][1])
            b = int(m[0][2])
            a = m[0][3]
            sd = statistics.stdev([r, g, b])
            if sd < sd_thr: # grayscale (sd = 0) or sort of grayscale
                avg = int((r + g + b) / 3)
                if avg < avg_thr:
                    avg = int(avg / darkness) # darken
                    r = g = b = avg # force grayscale
                    line = line.replace(color_str, rgba2str(r, g, b, a))
    print(line[:-1])

