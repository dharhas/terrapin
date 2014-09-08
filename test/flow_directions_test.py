import numpy as np
from numpy.testing import assert_equal
from terrapin.flow_direction import d8, convert_d8_directions


def test_convert_d8_directions():
	test_sets = [	
		('esri', 
		np.array([0, 1, 2, 3, 4, 5, 6, 7]),
		np.array([1, 128, 64, 32, 16, 8, 4, 2])
		),
		('taudem',
		np.array([0, 1, 2, 3, 4, 5, 6, 7]),
		np.array([1, 2, 3, 4, 5, 6, 7, 8])
		),
		('degrees',
		np.array([0, 1, 2, 3, 4, 5, 6, 7]),
		np.array([0, 45, 90, 135, 180, 225, 270, 315])
		),
		('radians',
		np.array([0, 1, 2, 3, 4, 5, 6, 7]),
		np.array([0, 1, 2, 3, 4, 5, 6, 7]) * (0.25 * np.pi)
		),
	]

	for fmt, directions, converted in test_sets:
		assert_equal(convert_d8_directions(directions, fmt), converted)

	for fmt, converted, directions in test_sets:
		assert_equal(convert_d8_directions(directions, fmt, inverse=True), converted)


def test_d8_cardinal_directions():
	test_sets = [
				((1,2), 0), 
				((0,2), 1),
				((0,1), 2),
				((0,0), 3),
				((1,0), 4),
				((2,0), 5),
				((2,1), 6),
				((2,2), 7),
				] 

	for idx, direction in test_sets:
		dem = np.array([[10,20,30],	
						[40,50,60],
						[70,80,90]])

		dem[idx] = 5
		directions = d8(dem)
		assert directions[0,0] == direction
		print idx, directions[0][0]


d8_test_sets = [
	{
		'dem': np.array([[10,20,30],
						 [40,50,60],
						 [60,70,80]]),
		'dirs': np.array([[2]]),
		'format': None,

	},
	{
		'dem': np.array([[ 10, 20, 30, 40],
						 [ 50, 60, 70, 80],
						 [ 90,100,110,120],
						 [130,140,150,160]]),
		'dirs': np.array([[2, 2],
						  [2, 2]]),
		'format': None,
	},
	{
		'dem': np.array([[ 78, 72, 69, 71, 58, 49],
						 [ 74, 67, 56, 49, 46, 50],
						 [ 69, 53, 44, 37, 38, 48],
						 [ 64, 58, 55, 22, 31, 24],
						 [ 68, 61, 47, 21, 16, 19],
						 [ 74, 53, 34, 12, 11, 12]]),
		'dirs': np.array([[  2, 2, 4, 4],
						  [  1, 2, 4, 8],
						  [128, 1, 2, 4],
						  [  2, 1, 4, 4]]),
		'format': 'esri',
		# source: http://www.nws.noaa.gov/oh/hrl/gis/data.html
	},
	{
		'dem': np.array([[  1,  4,  6, 12, 20, 44 ],
						 [  3,  4,  8, 11, 13, 24 ],
						 [  5,  8, 15, 20, 25, 39 ],
						 [  9, 14, 22, 32, 37, 47 ],
						 [ 12, 18, 31, 39, 44, 52 ],
						 [ 14, 26, 36, 43, 48, 58 ]]),
		'dirs': np.array([[ 32, 16, 32, 16],
						  [ 64, 32, 64, 64],
						  [ 32, 32, 32, 32],
						  [ 32, 16, 32, 32]]),
		'format': 'esri',
		# source: http://www.geo.uzh.ch/microsite/geo372/PDF/GEO372_W7_Hydrology_2013.pdf
	},	
]


def test_d8():
	for test_set in d8_test_sets:
		directions = d8(test_set['dem'])
		if test_set['format']:
			directions = convert_d8_directions(directions, test_set['format'])

		assert_equal(directions, test_set['dirs'])
