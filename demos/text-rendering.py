import numpy as np
import cv2

# Demo for text rendering and codecs

WIDTH = 1280
HEIGHT = 720

codec = ['X','2','6','4']
#codec = ['M','J','P','G']
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*codec)

out = cv2.VideoWriter('out-text-rendering-' + ''.join(codec) + '.avi',fourcc, 25, (WIDTH,HEIGHT))

# Write some Text
fontFaces = {
	'SIMPLEX': cv2.FONT_HERSHEY_SIMPLEX,
	'DUPLEX': cv2.FONT_HERSHEY_DUPLEX,
	'COMPLEX': cv2.FONT_HERSHEY_COMPLEX,
	'TRIPLEX': cv2.FONT_HERSHEY_TRIPLEX
}

fontScale = 1
fonthThickness = 1
i = 1;
j = 0;
fP = 0;
while i < 1100000:
	if (i % 100 == 0):
		print("Number: " + str(i))
	if j % 30 == 0:
		fontScale = 1 + ((fP % 16) % 4)
		fontThickness = 1 + ((fP % 16) // 4)
		fP += 1

		

	# Create a black image
	img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

	text = ('Scale: %s; Thickness: %s' % (fontScale, fontThickness))
	cv2.putText(
			img,
			text, 
			(50, 50), 
			cv2.FONT_HERSHEY_DUPLEX, 
			1, 
			(255,
			255,
			255), 
			1
		)

	y = 150
	for (k, f) in fontFaces.items():
		text = k + ': ' + str(i)
		fontFace = f
		(dim, base) = cv2.getTextSize(text, fontFace, fontScale, fonthThickness)
		cv2.putText(
			img,
			text, 
			(1260 - dim[0], y), 
			fontFace, 
			fontScale, 
			(255 * (i % 3),
			255 * ((i+1) % 3),
			255 * ((i+2) % 3)), 
			fonthThickness
		)
		y += 150

#	cv2.imshow('img',img)

	out.write(img)
	i += 1111
	j += 1

out.release()
cv2.destroyAllWindows()
