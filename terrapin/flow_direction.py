import numpy as np

def d8(dem):
	"""
	Implements D8 Flow Direction algorithm
	D8 Flow Direction Coding: 0 - East, 1 - Northeast, 2 - North, 3 - Northwest , 4 - West, 5 - Southwest, 6 - South, 7 - Southeast.
	"""
	inv_sqrt2 = 1/np.sqrt(2)

	d0 = dem[1:-1,1:-1] - dem[1:-1,2:]
	d1 = (dem[1:-1,1:-1] - dem[:-2,2:]) * inv_sqrt2
	d2 = dem[1:-1,1:-1] - dem[:-2,1:-1]
	d3 = (dem[1:-1,1:-1] - dem[:-2,:-2]) * inv_sqrt2
	d4 = dem[1:-1,1:-1] - dem[1:-1,:-2]
	d5 = (dem[1:-1,1:-1] - dem[2:,:-2]) * inv_sqrt2
	d6 = dem[1:-1,1:-1] - dem[2:,1:-1]
	d7 = (dem[1:-1,1:-1] - dem[2:,2:]) * inv_sqrt2 

	stacked = np.dstack([d0, d1, d2, d3, d4, d5, d6, d7])
	directions = stacked.argmax(axis=2)

	# find indetermate points, argmax returns first occurance of max so lets reverse it 
	# and try again. If the indices don't match then the point is indeterminate
	reversed_indices = 7 - stacked[:,:,::-1].argmax(axis=2) 
	directions[reversed_indices!=directions] = -1

	return directions


def convert_d8_directions(directions, fmt):
	if fmt not in ['esri', 'taudem', 'degrees', 'radians']:
		raise NotImplementedError('Format %s not implemented' % fmt)

	if fmt=='esri':
		convert = np.vectorize(lambda x:2**((8-x)%8))
		converted = convert(directions)

	if fmt=='taudem':
		converted = directions + 1

	if fmt=='degrees':
		converted = directions * 45

	if fmt=='radians':
		converted = directions * np.pi * 0.25

	# maintain indeterminate points
	converted[directions==-1] = -1 

	return converted	
