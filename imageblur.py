from PIL import Image
import os
import statistics
strenght=5
imagename="combolevel1_blurred"
def get_pixel_next():
	

	
	for i in range(strenght):
		base_dir = os.path.dirname(os.path.abspath(__file__))
		IMAGEPATH = os.path.join(base_dir, "..", "assets", "{0}.png".format(imagename))
		im = Image.open(IMAGEPATH)
		px = im.load()
		width, height = im.size
		updatedpixels = []
		for x in range(width):
			for y in range(height):
				left  = px[x-1, y] if x > 0 else px[x, y]
				right = px[x+1, y] if x < width-1 else px[x, y]
				top   = px[x, y+1] if y < height-1 else px[x, y]
				bottom= px[x, y-1] if y > 0 else px[x, y]

				R = int(statistics.mean([top[0], bottom[0], left[0], right[0]]))
				G = int(statistics.mean([top[1], bottom[1], left[1], right[1]]))
				B = int(statistics.mean([top[2], bottom[2], left[2], right[2]]))
				A = int(statistics.mean([top[3], bottom[3], left[3], right[3]]))
				
				updatedpixels.append([x, y, (R, G, B, A)])
		new_im = im.copy()
		new_px = new_im.load()
		for value in updatedpixels:
			x, y, color = value[0], value[1], value[2]
			new_px[int(x), int(y)] = (int(color[0]), int(color[1]), int(color[2]), int(color[3]))

		OUTPATH = os.path.join(base_dir, "..", "assets", "{0}.png".format(imagename))
		new_im.save(OUTPATH)
		print(f"Saved to {OUTPATH}")		

	

get_pixel_next()
