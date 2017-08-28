import numpy as np
import cv2
import random
import argparse
import wavelength

minWave = 415
maxWave = 660
waveLengthSpectrum = maxWave - minWave
waveWidth = 4

WIDTH = waveWidth * waveLengthSpectrum
HEIGHT = 200

img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

for i in range(minWave, maxWave):
	colors = [
		map(lambda c: (int)(255 * c), wavelength.wavelengthToRGB(i)),
		wavelength.waveLengthToRGB(i)
	]

	print("\tWave: %d, Colors: %s" % (i, repr(colors))) 

	xCoo = (i - minWave) * waveWidth
	for j in range(0, len(colors)):
		square = np.array([ 
			[xCoo, j * 100], 
			[xCoo, (j+1) * 100], 
			[xCoo + waveWidth, (j+1) * 100], 
			[xCoo + waveWidth, j * 100] 
		], np.int32)

		cv2.fillConvexPoly(
			img, 
			square,
			colors[j]
		)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
