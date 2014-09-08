import numpy as np
from numpy.testing import assert_equal
from terrapin.flow_direction import aread8, convert_d8_directions

test_sets = [
    # source:
    # http://resources.arcgis.com/en/help/main/10.1/index.html#//009z00000051000000 
    # lower right corner of flow accumulation array is 2 in url but it should be 1
    # confirmed in example in url -> http://www.nws.noaa.gov/ohd/hrl/gis/data.html   
    ['esri', 
    np.array([
        [  2,   2,   2,   4,   4,   8],
        [  2,   2,   2,   4,   4,   8],
        [  1,   1,   2,   4,   8,   4],
        [128, 128,   1,   2,   4,   8],
        [  2,   2,   1,   4,   4,   4],
        [  1,   1,   1,   1,   4,  16],
        ]),
    np.array([
        [0,  0,  0,  0,  0,  0],
        [0,  1,  1,  2,  2,  0],
        [0,  3,  7,  5,  4,  0],
        [0,  0,  0, 20,  0,  1],
        [0,  0,  0,  1, 24,  0],
        [0,  2,  4,  7, 35,  1] # 
        ])
    ],
    # source: http://www.geo.uzh.ch/microsite/geo372/PDF/GEO372_W7_Hydrology_2013.pdf
    ['esri', 
    np.array([
        [32, 16, 16, 16, 16, 16],
        [64, 32, 16, 32, 16, 16], 
        [64, 64, 32, 64, 64, 32], 
        [64, 32, 32, 32, 32, 32], 
        [64, 32, 16, 32, 32, 32], 
        [64, 16, 32, 32, 32, 16],
        ]),
    np.array([
        [35, 13, 12,  2,  1,  0], 
        [10,  9,  0,  8,  4,  0], 
        [ 9,  4,  2,  2,  1,  0], 
        [ 7,  0,  3,  1,  1,  0], 
        [ 2,  3,  1,  2,  0,  0], 
        [ 1,  0,  0,  0,  1,  0],
        ])
    ],
    # source: http://www.geospatialworld.net/paper/application/ArticleView.aspx?aid=1356
    ['esri',
    np.array([
        [ 1, 64,  1, 64, 16, 16],
        [ 4, 64, 32, 64, 32,  4], 
        [16, 16, 16,  1,  1,  1], 
        [64, 32,  2,  4,  8,  4], 
        [ 4,  4,  1,  4, 16,  4], 
        [ 4,  4,  1,  4, 16, 16],
        ]),
    np.array([
        [0, 3, 0, 4, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [5, 1, 0, 0, 1, 3],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 1],
        [1, 1, 0, 11, 3, 2], #the 11 is a 9 in the paper which is wrong. 
        ])
    ],

]


def test_flow_accumulation():
    for fmt, d8, area in test_sets:
        d8 = convert_d8_directions(d8, fmt, inverse=True)
        a = aread8(d8)
        a.accumulate()
        assert_equal(area, a.accumulation)
