from cubelet import Cubelet
import attridict

SLICE = attridict({
		"U": (slice(None), 0, slice(None)),
		"D": (slice(None), -1, slice(None)),
		"L": (slice(None), slice(None), 0),
		"R": (slice(None), slice(None), -1),
		"F": (0, slice(None), slice(None)),
		"B": (-1, slice(None), slice(None)),
	})

DEFAULT_CUBE = [
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
