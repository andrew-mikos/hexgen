from hexgen import generate
from hexgen.enums import MapType

options = {
    "map_type": MapType.terran,
    "surface_pressure": 1013.25,
    "axial_tilt": 23,
    "size": 30,
    "base_temp": -19.50,
    "avg_temp": 15,
    "sea_percent": 20,
    "hydrosphere": True,
    "num_rivers": 125,
    "num_territories": 2
}

gen = generate(options, image=True)
gen.export('bin/export3.json')
