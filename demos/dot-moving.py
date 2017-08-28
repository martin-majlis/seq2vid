import numpy as np
import cv2
import random
import argparse
import wavelength

# How to run experiment
# for size in 8 10 16 20; do for rev in "" --rev; do echo $size $rev; python dot-moving.py --size $size $rev;  done; done

parser = argparse.ArgumentParser(description='Render moving dot.')
parser.add_argument('--size', dest='size', type=int, nargs='?', default=20, help='Dot size')
parser.add_argument('--keep', dest='keep', type=int, nargs='?', default=1, help='How many frames it should stay on one spot')
parser.add_argument('--prob', dest='prob', type=float, nargs='?', default=0.1, help='Probability of new dot')
parser.add_argument('--rev', dest='rev', default=False, help='Move in reverse order', action='store_true')

args = parser.parse_args()
print("Size: %d" % args.size)
print("Keep: %d" % args.keep)
print("Prob: %f" % args.prob)
print("Reverse: %s" % str(args.rev))

WIDTH = 1280
HEIGHT = 720

if WIDTH % args.size != 0 or HEIGHT % args.size != 0:
	print("%d is not dividing %d and %d" % (args.size, WIDTH, HEIGHT))
	exit(1)

rows = HEIGHT // args.size
cols = WIDTH // args.size

codec = ['X','2','6','4']
fourcc = cv2.VideoWriter_fourcc(*codec)
out = cv2.VideoWriter(('XXout-dot-moving-%s-size-%02d-keep-%02d-prob-%f-rev-%s.avi' % (''.join(codec), args.size, args.keep, args.prob, str(args.rev))),fourcc, 25, (WIDTH,HEIGHT))

fontFace = cv2.FONT_HERSHEY_DUPLEX
fontScale = 1
fonthThickness = 1
colors = {}

bufferSize = WIDTH // args.size * HEIGHT // args.size
cBuffer = np.zeros(bufferSize, np.uint32)
bufferPos = -1
minWave = 415
maxWave = 660
waveLengthSpectrum = maxWave - minWave

colors = []
for wave in range(minWave, maxWave):
	colors.append(map(lambda c: (int)(255 * c), wavelength.wavelengthToRGB(wave)))


print("Screen: %d x %d" % (rows, cols))
print("Buffer size: %d" % bufferSize)

for i in range(1, 25 * 60 * 20): #bufferSize):
	if i % 100 == 0:
		print("I: %d" %i)

	if random.random() < args.prob:
		bufferPos += 1
		cBuffer[bufferPos % bufferSize] = i
		# print("Adding to buffer at pos %4d value %4d - (%s)" % (bufferPos, i, ", ".join(map(lambda x: str(x), color2)))) 

	# Create a black image
	img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
	j = bufferPos
	while True:
		actBufPos = (j + bufferSize) % bufferSize
		val = cBuffer[actBufPos]
		diff = i - val
		# print("%4d: j: %d; actBufPos: %d; val: %4d; diff: %d" % (i, j, actBufPos, val, diff))
		if val == 0:
			break
		if diff > bufferSize:
			break

		xPos = diff % cols
		yPos = diff // cols
	
		xCoo = xPos * args.size
		if args.rev and yPos % 2 == 1:
			xCoo = (cols - xPos) * args.size
		yCoo = yPos * args.size

		# print("%4d: val: %4d; xPos: %d, yPos: %d; xCoo: %d, yCoo: %d" % (i, val, xPos, yPos, xCoo, yCoo))

		square = triangle = np.array([ 
			[xCoo, yCoo], 
			[xCoo, yCoo + args.size], 
			[xCoo + args.size, yCoo + args.size], 
			[xCoo + args.size, yCoo] 
		], np.int32)

		cv2.fillConvexPoly(
			img, 
			square,
			#(255 * (val % 3), 255 * ((val+1) % 3), 255 * ((val+2) % 3))
			colors[val % waveLengthSpectrum]
		)
		j -= 1

#	cv2.imshow('img',img)
#	cv2.waitKey(0)

	out.write(img)

out.release()
cv2.destroyAllWindows()
