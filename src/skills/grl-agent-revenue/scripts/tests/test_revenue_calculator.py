import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from revenue_calculator import allocate_cost, compute_kpis, compute_price


class RevenueCalculatorTests(unittest.TestCase):
    def test_kpis_use_available_and_sold_denominators(self):
        result = compute_kpis(100, 70, 9000, total_revenue=10000)
        self.assertEqual(result["occupancy_pct"], 70.0)
        self.assertEqual(result["adr"], round(9000 / 70, 2))
        self.assertEqual(result["revpar"], 90.0)
        self.assertEqual(result["trevpar"], 100.0)

    def test_zero_inventory_is_not_zero_kpi(self):
        result = compute_kpis(0, 0, 0)
        self.assertIsNone(result["revpar"])
        self.assertTrue(any("inventario disponibile" in warning for warning in result["warnings"]))

    def test_total_revenue_is_required_for_total_revenue_kpis(self):
        result = compute_kpis(100, 70, 9000)
        self.assertIsNone(result["trevpar"])
        self.assertIsNone(result["goppar"])
        self.assertTrue(any("total_revenue non fornito" in warning for warning in result["warnings"]))

    def test_cost_allocation(self):
        result = allocate_cost(10000, 25, 5)
        self.assertEqual(result["allocated_cost_for_type_and_date"], 2500.0)
        self.assertEqual(result["cost_per_unit_and_date"], 500.0)

    def test_forced_price_wins_over_minimum(self):
        result = compute_price(
            cost_per_unit=100,
            mol_pct=20,
            adjustment_pct=10,
            min_guaranteed=130,
            forced=95,
        )
        self.assertEqual(result["mup"], 120.0)
        self.assertEqual(result["revenue_price"], 132.0)
        self.assertEqual(result["final_price"], 95.0)

    def test_band_selects_last_eligible_threshold(self):
        result = compute_price(
            cost_per_unit=100,
            mol_pct=0,
            occupancy_pct=75,
            bands={"0": -20, "60": 0, "80": 10},
        )
        self.assertEqual(result["occupancy_adjustment_pct"], 0.0)
        self.assertEqual(result["revenue_price"], 100.0)

    def test_invalid_occupancy_is_rejected_even_with_explicit_adjustment(self):
        with self.assertRaises(ValueError):
            compute_price(100, 0, occupancy_pct=101, adjustment_pct=0)

    def test_forced_below_floor_is_reported(self):
        result = compute_price(100, 20, min_guaranteed=130, forced=95)
        self.assertTrue(any("floor economico" in warning for warning in result["warnings"]))

    def test_non_finite_input_is_rejected(self):
        with self.assertRaises(ValueError):
            compute_kpis(float("nan"), 1, 100)


if __name__ == "__main__":
    unittest.main()
