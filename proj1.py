from dataclasses import dataclass
import math
import sys

sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class GlobeRect:
    lo_lat:float
    hi_lat:float
    west_long:float
    east_long:float


@dataclass(frozen=True)
class Region:
    rect:GlobeRect
    name:str
    terrain:str

@dataclass(frozen=True)
class RegionCondition:
    region:Region
    year:int
    pop:int
    ghg_rate:float

region_conditions = [
    RegionCondition(
        region=Region(
            rect=GlobeRect(lo_lat=48.8, hi_lat=49.0, west_long=2.2, east_long=2.5),
            name="Paris",
            terrain="other"
        ),
        year=2020,
        pop=11000000,
        ghg_rate=30000000.0
    ),
    RegionCondition(
        region=Region(
            rect=GlobeRect(lo_lat=-33.9, hi_lat=-33.7, west_long=151.0, east_long=151.3),
            name="Sydney",
            terrain="other"
        ),
        year=2020,
        pop=5312000,
        ghg_rate=25000000.0
    ),
    RegionCondition(
        region=Region(
            rect=GlobeRect(lo_lat=10.0, hi_lat=20.0, west_long=-60.0, east_long=-40.0),
            name="Atlantic Ocean",
            terrain="ocean"
        ),
        year=2020,
        pop=0,
        ghg_rate=1500000.0
    ),
    RegionCondition(
        region=Region(
            rect=GlobeRect(lo_lat=35.2, hi_lat=35.4, west_long=-120.8, east_long=-120.5),
            name="San Luis Obispo",
            terrain="other"
        ),
        year=2020,
        pop=280000,
        ghg_rate=1200000.0
    )
]



def emissions_per_capita(rc: RegionCondition) -> float:
    if not isinstance(rc, RegionCondition):
        raise TypeError('Input for emissions_per_capita must be a RegionCondition')
    if rc.pop <= 0:
        return 0.0
    return rc.ghg_rate / rc.pop


def area(gr: GlobeRect) -> float:
    if not isinstance(gr, GlobeRect):
        raise TypeError('Input for area must be a GlobeRect')
    if gr.lo_lat < -90 or gr.lo_lat > 90:
        raise ValueError("lo_lat must be between -90 and 90")
    if gr.hi_lat < -90 or gr.hi_lat > 90:
        raise ValueError("hi_lat must be between -90 and 90")
    if gr.lo_lat > gr.hi_lat:
        raise ValueError("lo_lat cannot be greater than hi_lat")
    if gr.west_long < -180 or gr.west_long > 180:
        raise ValueError("west_long must be between -180 and 180")
    if gr.east_long < -180 or gr.east_long > 180:
        raise ValueError("east_long must be between -180 and 180")
    radius = 6378.1
    low_lat = math.radians(gr.lo_lat)
    high_lat = math.radians(gr.hi_lat)
    west = math.radians(gr.west_long)
    east = math.radians(gr.east_long)

    long_diff = east - west
    if long_diff < 0:
        long_diff = long_diff + 2 * math.pi

    return (radius ** 2) * abs(long_diff) * abs(math.sin(high_lat) - math.sin(low_lat))


def emissions_per_square_km(rc: RegionCondition) -> float:
    if not isinstance(rc,RegionCondition):
        raise TypeError('Input for emissions_per_square_km must be a RegionCondition')
    if area(rc.region.rect) <= 0:
        return 0.0
    return rc.ghg_rate/area(rc.region.rect)


def population_density(rc: RegionCondition) -> float:
    if not isinstance(rc, RegionCondition):
        raise TypeError("rc must be a RegionCondition")
    if area(rc.region.rect) <= 0:
        return 0.0
    return rc.pop/area(rc.region.rect)


def densest(rc_list: list[RegionCondition]) -> str:
    if not isinstance(rc_list,list):
        raise TypeError('Input for densest must be a list')
    if len(rc_list) == 0:
        raise ValueError("Empty list")
    return density_object(rc_list).region.name

def density_object(rc_list:list[RegionCondition]) -> RegionCondition:
    if not isinstance(rc_list[0],RegionCondition):
        raise TypeError('Input for densest must be a list of RegionCondition')
    if len(rc_list) == 1:
        return rc_list[0]
    first = rc_list[0]
    next = density_object(rc_list[1:])
    if population_density(first) > population_density(next):
        return first
    return next

def terrain_growth_rate(terrain: str) -> float:
    if not isinstance(terrain, str):
        raise TypeError('Input for terrain_growth_rate must be a str')
    if terrain == "ocean":
        return 0.0001
    if terrain == "mountains":
        return 0.0005
    if terrain == "forest":
        return -0.00001
    return 0.0003


def projected_population(pop: int, rate: float, years: int) -> int:
    if not isinstance(pop, int):
        raise TypeError("pop must be an int")
    if not isinstance(rate, (int, float)):
        raise TypeError("rate must be a number")
    if not isinstance(years, int):
        raise TypeError("years must be an int")
    if pop < 0:
        raise ValueError("population cannot be negative")
    if years < 0:
        raise ValueError("years cannot be negative")
    if years == 0:
        return pop
    next_pop = int(pop * (1 + rate))
    return projected_population(next_pop, rate, years - 1)


def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    if not isinstance(rc, RegionCondition):
        raise TypeError("rc must be a RegionCondition")
    if not isinstance(years, int):
        raise TypeError("years must be an int")
    if years < 0:
        raise ValueError("years cant be negative")
    rate = terrain_growth_rate(rc.region.terrain)
    new_pop = projected_population(rc.pop, rate, years)

    if rc.pop <= 0:
       new_ghg = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(
        region=rc.region,
        year=rc.year + years,
        pop=new_pop,
        ghg_rate=new_ghg
    )
