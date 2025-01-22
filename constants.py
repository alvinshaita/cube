from cubelet import Cubelet
import attridict


SLICES = {
		"U": attridict({"slice_index_to_move": 1, "slice_to_move": 0}),
		"D": attridict({"slice_index_to_move": 1, "slice_to_move": -1}),
		"L": attridict({"slice_index_to_move": 2, "slice_to_move": 0}),
		"R": attridict({"slice_index_to_move": 2, "slice_to_move": -1}),
		"F": attridict({"slice_index_to_move": 0, "slice_to_move": 0}),
		"B": attridict({"slice_index_to_move": 0, "slice_to_move": -1}),
	}


from functools import partial

def twotwo(index, letter):
	bbb = SLICES[letter]
	
	ccc = index
	if bbb.slice_to_move == -1: ccc = -(index+1)

	_slice = [slice(None) for i in range(3)]
	_slice[bbb.slice_index_to_move] = ccc
	return tuple(_slice)


SLICE = attridict({
		"U": partial(twotwo, letter="U"),
		"D": partial(twotwo, letter="D"),
		"L": partial(twotwo, letter="L"),
		"R": partial(twotwo, letter="R"),
		"F": partial(twotwo, letter="F"),
		"B": partial(twotwo, letter="B"),
	})



DEFAULT_CUBE_2X2 = [
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": "red", "b": None})
		],
		
		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": "red", "b": None})
		]
	],
	
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": "orange"})
		],
		
		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": "orange"})
		]
	]
]





DEFAULT_CUBE_3X3 = [
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": "yellow", "d": None, "l": None, "r": None, "f": "red", "b": None}),
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": "red", "b": None})
		],

		[
			Cubelet({"u": None, "d": None, "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": None, "l": None, "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": None, "l": None, "r": "green", "f": "red", "b": None})
		],
		
		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": "white", "l": None, "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": "red", "b": None})
			]
	],
	
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": None}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": None, "f": None, "b": None}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": None})
		],

		[
			Cubelet({"u": None, "d": None, "l": "blue", "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": None, "l": None, "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": None, "l": None, "r": "green", "f": None, "b": None})
		],

		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": None})
		]
	],
	
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": "orange"})
		],
		
		[
			Cubelet({"u": None, "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": None, "l": None, "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": None, "l": None, "r": "green", "f": None, "b": "orange"})
		],
		
		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": "orange"})
		]
	]
]
