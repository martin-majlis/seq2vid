import argparse
import math
import random
import time

import cv2
from demos import wavelength as w
import numpy as np


def nth(n):
    rem = n % 100
    if rem >= 10 and rem < 20:
        return str(n) + 'th'

    rem = n % 10
    if rem == 1:
        return str(n) + 'st'
    elif rem == 2:
        return str(n) + 'nd'
    elif rem == 3:
        return str(n) + 'rd'
    else:
        return str(n) + 'th'


# seq 1 100000 | sort -R | head -n 3000 | sort -n > inp.txt


parser = argparse.ArgumentParser(description='Render moving dot.')
parser.add_argument('--min', dest='min', type=int,
                    nargs='?', default=1, help='Minimum value')
parser.add_argument('--max', dest='max', type=int,
                    nargs='?', default=100000, help='Maximum value')
parser.add_argument('--keep', dest='keep', type=int, nargs='?',
                    default=1, help='How many frames it should stay on one spot')
parser.add_argument('--inp', dest='inp', type=str,
                    default='-', help='Input file with numbers')
parser.add_argument('--out', dest='out', type=str,
                    help='Output file with numbers')
parser.add_argument('--footer', dest='footer', type=str,
                    nargs='?', default='', help='Text in footer')
parser.add_argument('--header', dest='header', type=str,
                    nargs='?', default='', help='Text in header')

args = parser.parse_args()
print("Min: %d" % args.min)
print("Max: %d" % args.max)
print("Input: %s" % args.inp)
print("Footer: %s" % args.footer)

WIDTH = 1280
HEIGHT = 720

DOT_SIZE = 8  # 80  # 8  # 40
MAIN_BOX_TOP = 40
MAIN_BOX_WIDTH = 1120
MAIN_BOX_HEIGHT = 640
MAIN_BOX_LEFT = WIDTH - MAIN_BOX_WIDTH

SKIP_LINES = (30 // DOT_SIZE) + 1

rows = MAIN_BOX_HEIGHT // DOT_SIZE
cols = MAIN_BOX_WIDTH // DOT_SIZE
infoRowsBuffer = np.zeros(rows // SKIP_LINES, np.uint32)

codec = ['X', '2', '6', '4']
fourcc = cv2.VideoWriter_fourcc(*codec)
out = cv2.VideoWriter(('%s.avi' % (args.out)), fourcc, 25, (WIDTH, HEIGHT))

fontFace = cv2.FONT_HERSHEY_DUPLEX
fontScale = 1
fonthThickness = 1
colors = {}

bufferSize = MAIN_BOX_WIDTH // DOT_SIZE * MAIN_BOX_HEIGHT // DOT_SIZE
cBuffer = np.zeros(bufferSize, np.uint32)
bufferPos = -1
minWave = 415
maxWave = 660
startTime = time.time()
nowTime = time.time()
prevTime = time.time()
waveLengthSpectrum = maxWave - minWave
colors = []
for wave in range(minWave, maxWave):
    colors.append(map(lambda c: (int)(255 * c),
                      w.wavelengthToRGB(wave)))


# Create a black image
template = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

# Render square
# top line
cv2.line(
    template,
        (WIDTH - MAIN_BOX_WIDTH - 2, MAIN_BOX_TOP - 1),
        (WIDTH, MAIN_BOX_TOP - 1),
        (100, 100, 100)
)
# bottom line
cv2.line(
    template,
        (WIDTH - MAIN_BOX_WIDTH - 2, MAIN_BOX_TOP + MAIN_BOX_HEIGHT + 1),
        (WIDTH, MAIN_BOX_TOP + MAIN_BOX_HEIGHT + 1),
        (100, 100, 100)
)
# left line
cv2.line(
    template,
        (WIDTH - MAIN_BOX_WIDTH - 2, MAIN_BOX_TOP - 1),
        (WIDTH - MAIN_BOX_WIDTH - 2, MAIN_BOX_TOP + MAIN_BOX_HEIGHT + 1),
        (100, 100, 100)
)
# right line
cv2.line(
    template,
        (WIDTH - 1, MAIN_BOX_TOP - 1),
        (WIDTH - 1, MAIN_BOX_TOP + MAIN_BOX_HEIGHT + 1),
        (100, 100, 100)
)

# Render header
if len(args.header) > 0:
    (dim, base) = cv2.getTextSize(
        args.header, fontFace, fontScale, fonthThickness)
    cv2.putText(
        template,
        args.header,
        (10, 30),
        fontFace,
        fontScale,
        (100, 100, 100),
        fonthThickness
    )

# Render footer
if len(args.footer) > 0:
    (dim, base) = cv2.getTextSize(
        args.footer, fontFace, fontScale, fonthThickness)
    cv2.putText(
        template,
        args.footer,
        (WIDTH - dim[0], HEIGHT - 10),
        fontFace,
        fontScale,
        (100, 100, 100),
        fonthThickness
    )


with open(args.inp) as f:
    actNum = (int)(f.readline().strip())
    prevNum = actNum

    for i in range(args.min, args.max):
        if i % 100 == 0:
            nowTime = time.time()
            print("I: %10d %6dms %20dms" %
                  (i, 1000 * (nowTime - prevTime), 1000 * (nowTime - startTime))
                  )
            prevTime = nowTime

        if actNum == i:
            bufferPos += 1
            cBuffer[bufferPos % bufferSize] = i
            prevNum = actNum
            actNum = (int)(f.readline().strip())

        img = np.copy(template)

        # Render input values
        if bufferPos >= 0:
            text = "In"
            (dim, base) = cv2.getTextSize(
                text, fontFace, fontScale, fonthThickness)
            cv2.putText(
                img,
                text,
                (MAIN_BOX_LEFT - dim[0] - 10, MAIN_BOX_TOP + dim[1]),
                fontFace,
                fontScale,
                colors[prevNum % waveLengthSpectrum],
                fonthThickness
            )
            text = str(prevNum)
            (dim, base) = cv2.getTextSize(
                text, fontFace, fontScale, fonthThickness)
            cv2.putText(
                img,
                text,
                (MAIN_BOX_LEFT - dim[0] - 10, 28 + MAIN_BOX_TOP + dim[1]),
                fontFace,
                fontScale,
                colors[prevNum % waveLengthSpectrum],
                fonthThickness
            )

            text = str(nth(bufferPos + 1))
            (dim, base) = cv2.getTextSize(
                text, fontFace, fontScale, fonthThickness)
            cv2.putText(
                img,
                text,
                (MAIN_BOX_LEFT - dim[0] - 10, 56 + MAIN_BOX_TOP + dim[1]),
                fontFace,
                fontScale,
                colors[prevNum % waveLengthSpectrum],
                fonthThickness
            )

        #cv2.imshow('aaa', img)
        # cv2.waitKey(0)
        # exit(1)

        j = bufferPos
        bRendered = 0
        while True:
            actBufPos = (j + bufferSize) % bufferSize
            val = cBuffer[actBufPos]
            diff = i - val
            # print("%4d: j: %d; actBufPos: %d; val: %4d; diff: %d" % (i, j, actBufPos, val, diff))
            if val == 0:
                break
            if diff >= bufferSize:
                text = "Out"
                (dim, base) = cv2.getTextSize(
                    text, fontFace, fontScale, fonthThickness)
                cv2.putText(
                    img,
                    text,
                    (MAIN_BOX_LEFT -
                     dim[0] - 10, MAIN_BOX_TOP + MAIN_BOX_HEIGHT - 56),
                    fontFace,
                    fontScale,
                    colors[val % waveLengthSpectrum],
                    fonthThickness
                )
                text = str(val)
                (dim, base) = cv2.getTextSize(
                    text, fontFace, fontScale, fonthThickness)
                cv2.putText(
                    img,
                    text,
                    (MAIN_BOX_LEFT -
                     dim[0] - 10, MAIN_BOX_TOP + MAIN_BOX_HEIGHT - 28),
                    fontFace,
                    fontScale,
                    colors[val % waveLengthSpectrum],
                    fonthThickness
                )

                text = nth(bufferPos - bRendered)
                (dim, base) = cv2.getTextSize(
                    text, fontFace, fontScale, fonthThickness)
                cv2.putText(
                    img,
                    text,
                    (MAIN_BOX_LEFT - dim[0] - 10,
                     MAIN_BOX_TOP + MAIN_BOX_HEIGHT),
                    fontFace,
                    fontScale,
                    colors[val % waveLengthSpectrum],
                    fonthThickness
                )
                break

            xPos = diff % cols
            yPos = diff // cols

            xCoo = (WIDTH - MAIN_BOX_WIDTH - 1) + xPos * DOT_SIZE
            # if args.rev and yPos % 2 == 1:
            #    xCoo = (cols - xPos) * DOT_SIZE
            yCoo = MAIN_BOX_TOP + yPos * DOT_SIZE

            if xPos == 0 and yPos % SKIP_LINES == 0 and yCoo > MAIN_BOX_TOP + 70 and yCoo < MAIN_BOX_TOP + MAIN_BOX_HEIGHT - 70:
                infoRowsBuffer[yPos // SKIP_LINES] = val

            # print("%4d: val: %4d; xPos: %d, yPos: %d; xCoo: %d, yCoo: %d" % (i, val, xPos, yPos, xCoo, yCoo))

            square = triangle = np.array([
                [xCoo, yCoo],
                [xCoo, yCoo + DOT_SIZE],
                [xCoo + DOT_SIZE, yCoo + DOT_SIZE],
                [xCoo + DOT_SIZE, yCoo]
            ], np.int32)

            cv2.fillConvexPoly(
                img,
                square,
                # (255 * (val % 3), 255 * ((val + 1) % 3), 255 * ((val + 2) % 3))
                colors[val % waveLengthSpectrum]
            )
            j -= 1
            bRendered += 1

        for (pos, val) in enumerate(infoRowsBuffer):
            if val > 0:
                text = str(val)
                (dim, base) = cv2.getTextSize(
                    text, fontFace, fontScale, fonthThickness)
                cv2.putText(
                    img,
                    text,
                    (MAIN_BOX_LEFT -
                     dim[0] - 10, MAIN_BOX_TOP + (pos * SKIP_LINES + 1) * DOT_SIZE),
                    fontFace,
                    fontScale,
                    colors[val % waveLengthSpectrum],
                    fonthThickness
                )
        # Render footer
        text = "On screen: " + str(bRendered)
        (dim, base) = cv2.getTextSize(
            text, fontFace, fontScale, fonthThickness)
        cv2.putText(
            img,
            text,
            (10, HEIGHT - 10),
            fontFace,
            fontScale,
            (100, 100, 100),
            fonthThickness
        )

        out.write(img)

    out.release()
    cv2.destroyAllWindows()
