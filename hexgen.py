from hexgen import generate
from hexgen.enums import MapType

options = {
    "map_type": MapType.terran,
    "surface_pressure": 1000.25,
    "axial_tilt": 45,
    "size": 60,
    "base_temp": -5.50,
    "avg_temp": 15,
    "sea_percent": 40,
    "hydrosphere": True,
    "num_rivers": 95,
    "num_territories": 0
}

gen = generate(options, image=True)
gen.export('bin/export3.json')
