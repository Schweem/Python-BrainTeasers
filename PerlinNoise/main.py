import random 
from PIL import Image

def generate_permutation_table(seed=None) -> list:
	"""
	Generate a seeded, shuffled list of numbers from 0 to 256. 
	Duplicates the list to avoid overflow
	"""

	if seed is not None:
		random.seed(seed)

	p = list(range(256))
	random.shuffle(p)
	p.extend(p) # Duplication step to avoid overflow

	return p

def lerp(a : int, b : int, t : float):
	"""
	Linear interpolation from a to b by t
	"""
	return a + t * (b-a)

def smooth(t : float):
	"""
	Applies a quintic smoothing curve (6t^5 - 15t^4 + 10t^3)
	to passed value t (fraction)
	"""
	return t * t * t * (t * (t * 6 - 15) + 10)

def get_gradient_1d(i, perm_table : list):
	"""
	Produces a gradient value for a given point in 1D
	"""
	hash_value = perm_table[i]

	if hash_value % 2 == 0:
		return 1
	
	return -1

def get_gradient_2d(ix, iy, perm_table : list):
	"""
	Produces a gradient value for two given points in 2D
	"""

	x0 = perm_table[ix % 256]
	x1 = x0 + iy
	index = perm_table[x1 % 256]

	gradient = index % 4
	if gradient == 0:
		return (1,1)
	elif gradient == 1:
		return (-1,1)
	elif gradient == 2:
		return (-1,-1)
	elif gradient == 3:
		return (1,-1)
	else:
		pass

def generate_1d_noise(x : float, perm_table : list):
	"""
	Generates 1d perlin noise
	"""
	# boundaries
	x0 = int(x)
	x1 = x0 + 1

	# directions
	g0, g1 = get_gradient_1d(x0, perm_table), get_gradient_1d(x1, perm_table)

	# distances 
	v0, v1 = g0 * (x - x0), g1 * (x - x1)

	# weight
	t = x - x0

	# generate noise with calculated values 
	noise = lerp(v0, v1, smooth(t))

	return noise

def generate_2d_noise(x, y, perm_table):
	"""
	Generates 2d perlin noise 
	"""
	ix0 = int(x)
	iy0 = int(y)

	# directions
	TL = (ix0, iy0)
	TR = (ix0 + 1, iy0)
	BL = (ix0, iy0 + 1)
	BR = (ix0 + 1, iy0 + 1)

	# gradients
	gradTL = get_gradient_2d(TL[0], TL[1], perm_table)
	gradTR = get_gradient_2d(TR[0], TR[1], perm_table)
	gradBL = get_gradient_2d(BL[0], BL[1], perm_table)
	gradBR = get_gradient_2d(BR[0], BR[1], perm_table)

	# distances
	distanceTL = (x - TL[0], y - TL[1])
	distanceTR = (x - TR[0], y - TR[1])
	distanceBL = (x - BL[0], y - BL[1])
	distanceBR = (x - BR[0], y - BR[1])

	# dot products
	dotTL = (gradTL[0] * distanceTL[0]) + (gradTL[1] * distanceTL[1])
	dotTR = (gradTR[0] * distanceTR[0]) + (gradTR[1] * distanceTR[1])
	dotBL = (gradBL[0] * distanceBL[0]) + (gradBL[1] * distanceBL[1])
	dotBR = (gradBR[0] * distanceBR[0]) + (gradBR[1] * distanceBR[1])

	# weight
	smooth_x = smooth(x - ix0)
	smooth_y = smooth(y - iy0)
	
	# smoothing
	top_interpolation = lerp(dotTL, dotTR, smooth_x)
	bottom_interpolation = lerp(dotBL, dotBR, smooth_x)
	square_interpolation = lerp(top_interpolation, bottom_interpolation, smooth_y)

	return square_interpolation


def visualize_1d_noise():
	"""
	Render 1D perlin noise in the terminal with # characters
	"""
	PERMUTATION_TABLE = generate_permutation_table(seed=20)

	print("-- 1D Noise --")
	for i in range(100):
		x = i * 0.1

		noise_value = generate_1d_noise(x, PERMUTATION_TABLE)

		num_hashes = int((noise_value + 0.7) * 30)
		bar = '#' * num_hashes
		print(bar)

def visualize_2d_noise(WIDTH : int, HEIGHT : int):
	"""
	Generate 2D perlin noise, store as PNG with Pillow
	"""
	PERMUTATION_TABLE = generate_permutation_table(seed=20)

	image = Image.new('L', (WIDTH, HEIGHT))

	pixel_data = []

	for y in range(HEIGHT):
		for x in range(WIDTH):
			# scalars on x and y change 'zoom'  
			noise_value = generate_2d_noise(x * 0.05, y * 0.05, PERMUTATION_TABLE)

			#define colors for rendering
			color = int((noise_value + 0.7) * 182)
			pixel_data.append(color)

	image.putdata(pixel_data)
	image.save('perlin2d.png')

	print("Noise saved as perlin2d.png!")

def main() -> None:
	#visualize_1d_noise()
	visualize_2d_noise(1080, 1920)

if __name__ == "__main__":
	main()
