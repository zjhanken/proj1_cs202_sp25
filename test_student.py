import unittest
from proj1 import (
    GlobeRect,
    Region,
    RegionCondition,
    emissions_per_capita,
    area,
    emissions_per_square_km,
    population_density,
    densest,
    terrain_growth_rate,
    projected_population,
    project_condition,
)


class TestProj1(unittest.TestCase):

    def test_emissions_per_capita(self):
        rc1 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "A", "other"), 2020, 100, 200.0)
        rc2 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "B", "other"), 2020, 0, 200.0)

        self.assertAlmostEqual(emissions_per_capita(rc1), 2.0, places=2)
        self.assertEqual(emissions_per_capita(rc2), 0.0)
        with self.assertRaises(TypeError):
            emissions_per_capita("bad input")

    def test_area(self):
        gr1 = GlobeRect(0, 1, 0, 1)
        gr2 = GlobeRect(10, 10, 0, 1)

        self.assertAlmostEqual(area(gr1), 12391.4, places=0)
        self.assertEqual(area(gr2), 0.0)
        with self.assertRaises(ValueError):
            area(GlobeRect(100, 101, 0, 1))

    def test_emissions_per_square_km(self):
        rc1 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "A", "other"), 2020, 100, 24782.8)
        rc2 = RegionCondition(Region(GlobeRect(5, 5, 0, 1), "B", "other"), 2020, 100, 500.0)

        self.assertAlmostEqual(emissions_per_square_km(rc1), 2.0, places=1)
        self.assertEqual(emissions_per_square_km(rc2), 0.0)
        with self.assertRaises(TypeError):
            emissions_per_square_km(5)

    def test_population_density(self):
        rc1 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "A", "other"), 2020, 12391, 100.0)
        rc2 = RegionCondition(Region(GlobeRect(5, 5, 0, 1), "B", "other"), 2020, 300, 100.0)

        self.assertAlmostEqual(population_density(rc1), 1.0, places=1)
        self.assertEqual(population_density(rc2), 0.0)
        with self.assertRaises(TypeError):
            population_density(None)

    def test_densest(self):
        rc1 = RegionCondition(Region(GlobeRect(0, 2, 0, 2), "Sparse", "other"), 2020, 1000, 10.0)
        rc2 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "Dense", "other"), 2020, 5000, 10.0)

        self.assertEqual(densest([rc2]), "Dense")
        self.assertEqual(densest([rc1, rc2]), "Dense")
        with self.assertRaises(TypeError):
            densest("bad input")

    def test_terrain_growth_rate(self):
        self.assertAlmostEqual(terrain_growth_rate("ocean"), 0.0001, places=6)
        self.assertAlmostEqual(terrain_growth_rate("forest"), -0.00001, places=6)
        self.assertAlmostEqual(terrain_growth_rate("other"), 0.0003, places=6)
        with self.assertRaises(TypeError):
            terrain_growth_rate(3)

    def test_projected_population(self):
        self.assertEqual(projected_population(1000, 0.0003, 0), 1000)
        self.assertEqual(projected_population(1000, 0.0003, 2), int(int(1000 * 1.0003) * 1.0003))
        with self.assertRaises(ValueError):
            projected_population(1000, 0.0003, -1)
        with self.assertRaises(TypeError):
            projected_population("1000", 0.0003, 2)

    def test_project_condition(self):
        rc1 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "Town", "other"), 2020, 1000, 500.0)
        rc2 = RegionCondition(Region(GlobeRect(0, 1, 0, 1), "Ocean", "ocean"), 2020, 0, 100.0)

        projected1 = project_condition(rc1, 2)
        self.assertEqual(projected1.year, 2022)
        self.assertEqual(projected1.region, rc1.region)

        projected2 = project_condition(rc2, 5)
        self.assertEqual(projected2.pop, 0)
        self.assertEqual(projected2.ghg_rate, 0.0)

        with self.assertRaises(ValueError):
            project_condition(rc1, -1)
        with self.assertRaises(TypeError):
            project_condition("bad input", 2)


if __name__ == "__main__":
    unittest.main()
