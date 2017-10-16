from hexgen import generate
from hexgen.enums import MapType

options = {
    "map_type": MapType.terran,
    "surface_pressure": 1000.25,
    "axial_tilt": 27,
    "size": 100,
    "base_temp": 0,
    "avg_temp": 25,
    "sea_percent": 40,
    "hydrosphere": True,
    "num_rivers": 125,
    "random_seed": 1234578
}

gen = generate(options, image=True)
gen.export('bin/exportfile.json')
