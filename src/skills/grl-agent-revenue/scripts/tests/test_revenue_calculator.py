import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import io
import json
from contextlib import redirect_stdout

from revenue_calculator import allocate_cost, compute_kpis, compute_price, main


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

    def test_net_kpis_divide_by_available_rooms(self):
        """NRevPAR e GopPAR hanno lo stesso denominatore di RevPAR: le camere disponibili."""
        result = compute_kpis(100, 70, 9000, total_revenue=10000, acquisition_cost=900, operating_costs=6000)
        self.assertEqual(result["nrevpar"], 81.0)
        self.assertEqual(result["goppar"], 40.0)

    def test_minimum_guaranteed_lifts_the_final_price(self):
        result = compute_price(100, 0, min_guaranteed=150)
        self.assertEqual(result["final_price"], 150.0)

    def test_percentage_changes_apply_in_sequence(self):
        result = compute_price(100, 0, global_change_pct=10, unit_change_pct=-50)
        self.assertEqual(result["after_percentage_changes"], 55.0)

    def test_mup_base_is_cost_plus_margin(self):
        result = compute_price(100, 20, base="mup")
        self.assertEqual(result["selected_base"], 120.0)


class CommandLineTests(unittest.TestCase):
    """La SKILL.md prescrive la riga di comando: va esercitata, non solo le funzioni."""

    def esegui(self, argv: list[str]) -> dict:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(argv)
        self.assertEqual(code, 0)
        return json.loads(buffer.getvalue())

    def test_kpi_subcommand_returns_json(self):
        payload = self.esegui(
            ["kpi", "--available", "100", "--sold", "70", "--room-revenue", "9000"]
        )
        self.assertEqual(payload["revpar"], 90.0)

    def test_cost_subcommand_uses_available_units(self):
        payload = self.esegui(
            ["cost", "--total-cost", "1000", "--weight-pct", "50", "--available-units", "10"]
        )
        self.assertEqual(payload["cost_per_unit_and_date"], 50.0)

    def test_price_subcommand_returns_json(self):
        payload = self.esegui(["price", "--cost-per-unit", "100", "--mol-pct", "20"])
        self.assertIn("final_price", payload)

    def test_zero_denominator_exits_with_code_two(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["cost", "--total-cost", "1000", "--weight-pct", "50", "--available-units", "0"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
