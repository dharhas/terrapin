import numpy as np

def d8(dem):
	"""
	Implements D8 Flow Direction algorithm
	D8 Flow Direction Coding: 1 - East, 2 - Northeast, 3 - North, 4 - Northwest , 5 - West, 6 - Southwest, 7 - South, 8 - Southeast.
	"""
	inv_sqrt2 = 1/np.sqrt(2)
	d1 = dem[1:-1,1:-1] - dem[2:,1:-1]
	d2 = (dem[1:-1,1:-1] - dem[2:,:-2]) * inv_sqrt2
	d3 = dem[1:-1,1:-1] - dem[1:-1,:-2]
	d4 = (dem[1:-1,1:-1] - dem[:-2,:-2]) * inv_sqrt2
	d5 = dem[1:-1,1:-1] - dem[:-2,1:-1]
	d6 = (dem[1:-1,1:-1] - dem[:-2,2:]) * inv_sqrt2
	d7 = dem[1:-1,1:-1] - dem[1:-1,2:]
	d8 = (dem[1:-1,1:-1] - dem[2:,2:]) * inv_sqrt2

	stacked = np.dstack([d1,d2,d3, d4, d5, d6, d7, d8])

	directions = stacked.argmax(axis=2)

	# find indetermate points, argmax returns first occurance of max so lets reverse it 
	# and try again. If the indices don't match then the point is indeterminate
	reversed_indices = 7 - stacked[:,:,::-1].argmax(axis=2) 

	directions[reversed_indices!=directions] = -999

	# clunky conversion to arcgis directions for debugging
	directions[directions==0] = 1
	directions[directions==1] = 128
	directions[directions==2] = 64
	directions[directions==3] = 32
	directions[directions==4] = 16
	directions[directions==5] = 8
	directions[directions==6] = 4
	directions[directions==7] = 2

	return directions
