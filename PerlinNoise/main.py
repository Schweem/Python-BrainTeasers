import random 
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def generate_permutation_table(seed=None) -> list:
	"""
	Generate a seeded, shuffled list of numbers from 0 to 256. 
	Duplicates the list to avoid overflow
	"""
	try:
		if seed is not None:
			random.seed(seed)

		p = list(range(256))
		random.shuffle(p)
		p.extend(p) # Duplication step to avoid overflow

	except Exception as e:
		print(f"Error: {e}")

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
	try:
		return t * t * t * (t * (t * 6 - 15) + 10)
	
	except Exception as e:
		print(f"Error: {e}")

def get_gradient_1d(i, perm_table : list):
	"""
	Produces a gradient value for a given point in 1D
	"""
	try:
		hash_value = perm_table[i]

		if hash_value % 2 == 0:
			return 1
		
		return -1
	
	except Exception as e:
		print(f"Error: {e}")

def get_gradient_2d(ix, iy, perm_table : list):
	"""
	Produces a gradient value for two given points in 2D
	"""
	try:
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

	except Exception as e:
		print(f"Error: {e}")

def generate_1d_noise(x : float, perm_table : list):
	"""
	Generates 1d perlin noise
	"""
	try:
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
	
	except Exception as e:
		print(f"Error: {e}")

def generate_2d_noise(x, y, perm_table):
	"""
	Generates 2d perlin noise 
	"""
	try:
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
		
	except Exception as e:
		print(f"Error: {e}")


def visualize_1d_noise():
	"""
	Render 1D perlin noise in the terminal with # characters
	"""
	try:
		PERMUTATION_TABLE = generate_permutation_table(seed=20)

		print("-- 1D Noise --")
		for i in range(100):
			x = i * 0.1

			noise_value = generate_1d_noise(x, PERMUTATION_TABLE)

			num_hashes = int((noise_value + 0.7) * 30)
			bar = '#' * num_hashes
			print(bar)
		
	except Exception as e:
		print(f"Error: {e}")

def visualize_2d_noise(WIDTH : int, HEIGHT : int):
	"""
	Generate 2D perlin noise, store as PNG with Pillow
	"""
	try:
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
		
	except Exception as e:
		print(f"Error: {e}")

def fractal_noise_2d(x, y, perm_table, octaves=4, persistence=0.5):
	"""
	Generates fractal noise by adding multiple octaves of Perlin noise.
	"""
	total = 0.0
	frequency = 1.0
	amplitude = 1.0
	
	for i in range(octaves):
		total += generate_2d_noise(x * frequency, y * frequency, perm_table) * amplitude
		
		# For the next octave, increase frequency and decrease amplitude
		amplitude *= persistence
		frequency *= 2
		
	return total

def pretty_2d_noise(WIDTH : int, HEIGHT : int):
	"""
	Generate 2D perlin noise, store as PNG with Pillow
	"""
	try:
		PERMUTATION_TABLE = generate_permutation_table(seed=20)

		image = Image.new('RGB', (WIDTH, HEIGHT))

		pixel_data = []

		for y in range(HEIGHT):
			for x in range(WIDTH):
				# scalars on x and y change 'zoom'  
				noise_value = fractal_noise_2d(x * 0.05, y * 0.05, PERMUTATION_TABLE)
				normalized_val = (noise_value + 1.5) / 3.0
				elevation = int((normalized_val + 1) * 50)
				

				pixel_color = (elevation, elevation, elevation)

				pixel_data.append(pixel_color)

		image.putdata(pixel_data)
		image.save('perlin2d.png')

		print("Noise saved as perlin2d.png!")
		
	except Exception as e:
		print(f"Error: {e}")

def numpy_2d_noise(WIDTH : int, HEIGHT : int):
	"""
	Generate 2D Perlin noise and render a contour plot with Matplotlib.
	"""
	try:
		PERMUTATION_TABLE = generate_permutation_table(seed=20)
		noise_grid = np.zeros((HEIGHT, WIDTH))

		for y in range(HEIGHT):
			for x in range(WIDTH):
				# scalars on x and y change 'zoom'  
				noise_value = fractal_noise_2d(x * 0.05, y * 0.05, PERMUTATION_TABLE)
				noise_grid[y, x] = noise_value


		levels = 15
		line_widths = [0.5, 1.0, 1.5, 2.0]
		colors = ['turquoise', 'aqua']
		
		fig, ax = plt.subplots(figsize=(10, 10), facecolor='darkslategrey')

		ax.contour(noise_grid,
				   levels=levels,
				   colors=colors,
				   linewidths=line_widths,
				   linestyles=['solid'])

		ax.set_axis_off()
		plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
		ax.margins(0, 0)

		print("Contour plot ready")
		plt.show()
		
	except NameError:
		 print("Error: Make sure 'fractal_noise_2d' and 'PERMUTATION_TABLE' are defined.")
	except Exception as e:
		print(f"Error: {e}")

def main() -> None:
	#visualize_1d_noise()
	#visualize_2d_noise(1080, 1920)
	#pretty_2d_noise(1080, 1920)
	numpy_2d_noise(100, 100)

if __name__ == "__main__":
	main()
