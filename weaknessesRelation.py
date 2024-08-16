
def relations():
	relations = {
		"planta": { "normal" : 1, "lucha":  1 , "volador" : 1/2, "veneno" : 1/2, "tierra": 2, "roca": 2, "bicho": 1/2,
		            "fantasma": 1, "acero": 1/2, "fuego": 1/2, "agua": 2, "planta": 1/2, "electrico": 1, "psiquico": 1,
		            "hielo": 1, "dragon": 1/2, "siniestro": 1, "hada": 1},

		"veneno": {"normal" : 1, "lucha":  1 , "volador" : 1, "veneno" : 1/2, "tierra": 1/2, "roca": 1/2, "bicho": 1,
		            "fantasma": 1/2, "acero": 0, "fuego": 1, "agua": 1, "planta": 2, "electrico": 1, "psiquico": 1,
		            "hielo": 1, "dragon": 1, "siniestro": 1, "hada": 2},

		"fuego": {"normal" : 1, "lucha":  1 , "volador" : 1, "veneno" : 1, "tierra": 1, "roca": 1/2, "bicho": 2,
		            "fantasma": 2, "acero": 1/2, "fuego": 1/2, "agua": 2, "planta": 2, "electrico": 1, "psiquico": 1,
		            "hielo": 2, "dragon": 1/2, "siniestro": 1, "hada": 1},

		"volador": {"normal" : 1, "lucha": 2 , "volador" : 1, "veneno" : 1, "tierra": 1, "roca": 1/2, "bicho": 2,
		            "fantasma": 1, "acero": 1/2, "fuego": 1, "agua": 1, "planta": 2, "electrico": 1/2, "psiquico": 1,
		            "hielo": 1, "dragon": 1, "siniestro": 1, "hada": 1},

		"agua": {"normal": 1, "lucha": 1, "volador": 1, "veneno": 1, "tierra": 2, "roca": 2, "bicho":1,
		           "fantasma": 1, "acero": 1, "fuego": 2, "agua": 1/2, "planta": 1 / 2, "electrico": 1,
		           "psiquico": 1, "hielo": 1, "dragon": 1/2, "siniestro": 1, "hada": 1},

		"bicho": {"normal": 1, "lucha": 1/2, "volador": 1/2, "veneno": 1 / 2, "tierra": 1, "roca": 1, "bicho": 1,
		           "fantasma": 1/2, "acero": 1/2, "fuego": 1/2, "agua": 1, "planta": 2, "electrico": 1, "psiquico": 2,
		           "hielo": 1, "dragon": 1, "siniestro": 2, "hada": 1/2},

		"normal": {"normal": 1, "lucha": 1, "volador": 1, "veneno": 1, "tierra": 1, "roca": 1 / 2, "bicho": 1,
		          "fantasma": 0, "acero": 1/2, "fuego": 1, "agua": 1, "planta": 1, "electrico": 1, "psiquico": 1,
		          "hielo": 1, "dragon": 1, "siniestro": 1, "hada": 1},

		"electrico": {"normal": 1, "lucha": 1, "volador": 2, "veneno": 1, "tierra": 0, "roca": 1, "bicho": 1,
		            "fantasma": 1, "acero": 1, "fuego": 1, "agua": 2, "planta": 1/2, "electrico": 1 / 2,
		            "psiquico": 1, "hielo": 1, "dragon": 1/2 , "siniestro": 1, "hada": 1},

		"tierra": {"normal": 1, "lucha": 1, "volador": 0, "veneno": 2, "tierra": 1, "roca": 2, "bicho": 1/2,
		          "fantasma": 1, "acero": 2, "fuego": 2, "agua": 1, "planta": 1/2, "electrico": 2,
		          "psiquico": 1, "hielo": 1, "dragon": 1, "siniestro": 1, "hada": 1},

		"hada": {"normal": 1, "lucha": 2, "volador": 1, "veneno": 1/2, "tierra": 1, "roca": 1, "bicho": 1,
		           "fantasma": 1, "acero": 1 / 2, "fuego": 1/2, "agua": 1, "planta": 1, "electrico": 1, "psiquico": 1,
		           "hielo": 1, "dragon": 2, "siniestro": 2, "hada": 1},

		"lucha": {"normal": 2, "lucha": 1, "volador": 1/2, "veneno": 1/2, "tierra": 1, "roca": 2, "bicho": 1/2,
		              "fantasma": 0, "acero": 2, "fuego": 1, "agua": 1, "planta": 1, "electrico": 1,
		              "psiquico": 1/2, "hielo": 2, "dragon": 1, "siniestro": 2, "hada": 1/2},

		"psiquico": {"normal": 1, "lucha": 2, "volador": 1, "veneno": 2, "tierra": 1, "roca": 1, "bicho": 1,
		          "fantasma": 1, "acero": 1/2, "fuego": 1, "agua": 1, "planta": 1, "electrico": 1,
		          "psiquico": 1 / 2, "hielo": 1, "dragon": 1, "siniestro": 0, "hada": 1},

		"roca": {"normal": 1, "lucha": 1/2, "volador": 2, "veneno": 1, "tierra": 1/2, "roca": 1, "bicho": 2,
		          "fantasma": 1, "acero": 1/2, "fuego": 2, "agua": 1, "planta": 1, "electrico": 1,
		          "psiquico": 1, "hielo": 2, "dragon": 1, "siniestro": 1, "hada": 1},

		"acero": {"normal": 1, "lucha": 1, "volador": 1, "veneno": 1, "tierra": 1, "roca": 2, "bicho": 1,
		          "fantasma": 1, "acero": 1/2, "fuego": 1/2, "agua": 1/2, "planta": 1, "electrico": 1/2,
		          "psiquico": 1, "hielo": 2, "dragon": 1, "siniestro": 1, "hada": 2},

		"fantasma": {"normal": 0, "lucha": 1, "volador": 1, "veneno": 1, "tierra": 1, "roca": 1, "bicho": 1,
		          "fantasma": 2, "acero": 1, "fuego": 1, "agua": 1, "planta": 1, "electrico": 1,
		          "psiquico": 2, "hielo": 2, "dragon": 1, "siniestro": 1/2, "hada": 1 / 2},

		"hielo": {"normal": 1, "lucha": 1, "volador": 2, "veneno": 1, "tierra": 2, "roca": 1, "bicho": 1,
		          "fantasma": 1, "acero": 1/2, "fuego": 1/2, "agua": 1/2, "planta": 2, "electrico": 1,
		          "psiquico": 1, "hielo": 1/2, "dragon": 2, "siniestro": 1, "hada": 1},

		"hielo": {"normal": 1, "lucha": 1, "volador": 1, "veneno": 1, "tierra": 1, "roca": 1, "bicho": 1,
		          "fantasma": 1, "acero": 1/2, "fuego": 1, "agua": 1, "planta": 1, "electrico": 1,
		          "psiquico": 1, "hielo": 1, "dragon": 2, "siniestro": 1, "hada": 0},

		"siniestro": {"normal": 1, "lucha": 1/2, "volador": 1, "veneno": 1, "tierra": 1, "roca": 1, "bicho": 1,
		          "fantasma": 2, "acero": 1, "fuego": 1, "agua": 1, "planta": 1, "electrico": 1,
		          "psiquico": 2, "hielo": 1, "dragon": 1, "siniestro": 1/2, "hada": 1/2},

		"dragon": {"normal": 1, "lucha": 1, "volador": 1, "veneno": 1, "tierra": 1, "roca": 1, "bicho": 1,
		              "fantasma": 1, "acero": 1/2, "fuego": 1/2, "agua": 1/2, "planta": 1, "electrico": 1/2,
		              "psiquico": 1, "hielo": 1, "dragon": 2, "siniestro": 1, "hada": 0},

	}

	return relations