from hexgen import generate
from hexgen.enums import MapType

options = {
    "map_type": MapType.terran,
    "surface_pressure": 1,
    "axial_tilt": 27,
    "size": 350,
    "base_temp": 0,
    "avg_temp": 25,
    "sea_percent": 65,
    "hydrosphere": True,
    "num_rivers": 800
    #"random_seed": 4649489417720096785
}

gen = generate(options, image=True)
gen.export('bin/exportfile.json')
