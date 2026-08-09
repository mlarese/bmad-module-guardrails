#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Deterministic KPI and QuoProfit-style revenue calculations.

The script deliberately exposes transparent primitives. It does not forecast
demand, infer elasticity, or publish prices to a PMS.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def money(value: float | None, digits: int = 2) -> float | None:
    return None if value is None else round(finite(value, "value"), digits)


def ratio(numerator: float, denominator: float, label: str) -> float:
    if denominator == 0:
        raise ValueError(f"{label}: denominatore uguale a zero")
    return numerator / denominator


def non_negative(value: float, label: str) -> float:
    value = finite(value, label)
    if value < 0:
        raise ValueError(f"{label}: il valore non può essere negativo")
    return float(value)


def finite(value: float, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label}: atteso un numero finito")
    return number


def compute_kpis(
    available: float,
    sold: float,
    room_revenue: float,
    total_revenue: float | None = None,
    acquisition_cost: float | None = None,
    operating_costs: float | None = None,
) -> dict[str, Any]:
    available = non_negative(available, "available")
    sold = non_negative(sold, "sold")
    room_revenue = non_negative(room_revenue, "room_revenue")
    if total_revenue is not None:
        total_revenue = non_negative(total_revenue, "total_revenue")
    else:
        total_revenue = None
    if acquisition_cost is not None:
        acquisition_cost = non_negative(acquisition_cost, "acquisition_cost")
    if operating_costs is not None:
        operating_costs = non_negative(operating_costs, "operating_costs")

    warnings: list[str] = []
    if total_revenue is not None and total_revenue < room_revenue:
        warnings.append(
            "total_revenue è inferiore a room_revenue: verificare perimetro dei ricavi"
        )
    result: dict[str, Any] = {
        "occupancy_pct": money(ratio(sold, available, "occupancy") * 100, 4)
        if available
        else None,
        "adr": money(ratio(room_revenue, sold, "ADR")) if sold else None,
        "revpar": money(ratio(room_revenue, available, "RevPAR"))
        if available
        else None,
        "trevpar": money(ratio(total_revenue, available, "TRevPAR"))
        if available and total_revenue is not None
        else None,
        "nrevpar": None,
        "goppar": None,
        "warnings": warnings,
    }
    if acquisition_cost is not None and available:
        result["nrevpar"] = money((room_revenue - acquisition_cost) / available)
    if operating_costs is not None and available and total_revenue is not None:
        result["goppar"] = money((total_revenue - operating_costs) / available)
    if total_revenue is None:
        result["warnings"].append(
            "TRevPAR e GopPAR non calcolabili: total_revenue non fornito"
        )
    if available and sold > available:
        result["warnings"].append(
            "sold supera available: possibile overbooking o base inventario incoerente"
        )
    if not sold:
        result["warnings"].append("ADR non calcolabile: nessuna unità venduta")
    if not available:
        result["warnings"].append(
            "KPI per unità disponibile non calcolabili: inventario disponibile uguale a zero"
        )
    result["basis"] = {
        "available": available,
        "sold": sold,
        "room_revenue": money(room_revenue),
        "total_revenue": money(total_revenue),
        "acquisition_cost": money(acquisition_cost),
        "operating_costs": money(operating_costs),
    }
    return result


def allocate_cost(total_cost: float, weight_pct: float, units: float) -> dict[str, Any]:
    total_cost = non_negative(total_cost, "total_cost")
    units = non_negative(units, "units")
    if weight_pct < 0 or weight_pct > 100:
        raise ValueError("weight_pct: atteso un peso normalizzato tra 0 e 100")
    if units == 0:
        raise ValueError("units: numero di unità uguale a zero")
    allocated = total_cost * weight_pct / 100
    return {
        "allocated_cost_for_type_and_date": money(allocated),
        "cost_per_unit_and_date": money(allocated / units),
        "basis": {
            "total_cost": money(total_cost),
            "weight_pct": money(weight_pct, 4),
            "units": units,
        },
        "formula": "total_cost * weight_pct / 100 / units",
    }


def select_adjustment(occupancy_pct: float | None, bands: dict[str, Any] | None) -> float:
    if occupancy_pct is None or not bands:
        return 0.0
    if not isinstance(bands, dict):
        raise ValueError("bands: atteso un oggetto JSON soglia:variazione")
    occupancy_pct = finite(occupancy_pct, "occupancy_pct")
    if occupancy_pct < 0 or occupancy_pct > 100:
        raise ValueError("occupancy_pct: atteso tra 0 e 100")
    parsed = []
    for threshold, adjustment in bands.items():
        threshold = finite(threshold, "band threshold")
        adjustment = finite(adjustment, "band adjustment")
        if threshold < 0 or threshold > 100:
            raise ValueError("band threshold: atteso tra 0 e 100")
        if adjustment < -100:
            raise ValueError("band adjustment: non può portare il prezzo sotto zero")
        parsed.append((threshold, adjustment))
    parsed.sort()
    eligible = [adjustment for threshold, adjustment in parsed if threshold <= occupancy_pct]
    return eligible[-1] if eligible else 0.0


def compute_price(
    cost_per_unit: float,
    mol_pct: float,
    occupancy_pct: float | None = None,
    adjustment_pct: float | None = None,
    bands: dict[str, Any] | None = None,
    base: str = "revenue",
    custom_base: float | None = None,
    global_change_pct: float = 0.0,
    unit_change_pct: float = 0.0,
    min_guaranteed: float | None = None,
    forced: float | None = None,
) -> dict[str, Any]:
    cost_per_unit = non_negative(cost_per_unit, "cost_per_unit")
    mol_pct = finite(mol_pct, "mol_pct")
    if mol_pct < -100:
        raise ValueError("mol_pct: non può portare il MUP sotto zero")
    if occupancy_pct is not None:
        occupancy_pct = finite(occupancy_pct, "occupancy_pct")
        if occupancy_pct < 0 or occupancy_pct > 100:
            raise ValueError("occupancy_pct: atteso tra 0 e 100")
    if min_guaranteed is not None:
        min_guaranteed = non_negative(min_guaranteed, "min_guaranteed")
    if forced is not None:
        forced = non_negative(forced, "forced")
    if custom_base is not None:
        custom_base = non_negative(custom_base, "custom_base")
    global_change_pct = finite(global_change_pct, "global_change_pct")
    unit_change_pct = finite(unit_change_pct, "unit_change_pct")
    if global_change_pct < -100 or unit_change_pct < -100:
        raise ValueError("percentage changes: non possono portare il prezzo sotto zero")
    selected_adjustment = (
        finite(adjustment_pct, "adjustment_pct")
        if adjustment_pct is not None
        else select_adjustment(occupancy_pct, bands)
    )
    if selected_adjustment < -100:
        raise ValueError("adjustment_pct: non può portare il prezzo sotto zero")
    mup = cost_per_unit * (1 + mol_pct / 100)
    revenue_price = mup * (1 + selected_adjustment / 100)
    if base == "mup":
        base_price = mup
    elif base == "revenue":
        base_price = revenue_price
    elif base == "custom" and custom_base is not None:
        base_price = custom_base
    else:
        raise ValueError("base deve essere 'mup', 'revenue' oppure 'custom' con custom_base")
    modified = base_price * (1 + global_change_pct / 100) * (1 + unit_change_pct / 100)
    after_min = max(modified, min_guaranteed) if min_guaranteed is not None else modified
    final_price = forced if forced is not None else after_min
    warnings = []
    if min_guaranteed is not None and min_guaranteed < mup:
        warnings.append("min_guaranteed è sotto il MUP calcolato")
    if forced is not None and forced < after_min:
        warnings.append("forced è sotto il prezzo dopo minimo garantito e variazioni")
    if forced is not None and forced < mup:
        warnings.append("forced è sotto il MUP calcolato: verificare il floor economico")
    return {
        "mup": money(mup),
        "occupancy_adjustment_pct": money(selected_adjustment, 4),
        "revenue_price": money(revenue_price),
        "selected_base": money(base_price),
        "after_percentage_changes": money(modified),
        "after_min_guaranteed": money(after_min),
        "final_price": money(final_price),
        "rules": [
            "MUP = cost_per_unit * (1 + mol_pct / 100)",
            "revenue_price = MUP * (1 + occupancy_adjustment_pct / 100)",
            "percentage changes are applied before minimum guaranteed",
            "forced price overrides minimum guaranteed",
        ],
        "basis": {
            "cost_per_unit": money(cost_per_unit),
            "mol_pct": money(mol_pct, 4),
            "occupancy_pct": money(occupancy_pct, 4),
            "global_change_pct": money(global_change_pct, 4),
            "unit_change_pct": money(unit_change_pct, 4),
            "min_guaranteed": money(min_guaranteed),
            "forced": money(forced),
        },
        "warnings": warnings,
    }


def read_json(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON non valido: {exc.msg}") from exc


def emit(payload: dict[str, Any], output: str | None) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calcola KPI e prezzi QuoProfit-style senza dipendenze esterne."
    )
    parser.add_argument("--verbose", action="store_true", help="include diagnostica estesa su stderr")
    parser.add_argument("-o", "--output", help="scrive il JSON in questo file invece che su stdout")
    sub = parser.add_subparsers(dest="command", required=True)

    kpi = sub.add_parser("kpi", help="calcola OCC, ADR, RevPAR e KPI profit-oriented")
    kpi.add_argument("--available", type=float, required=True)
    kpi.add_argument("--sold", type=float, required=True)
    kpi.add_argument("--room-revenue", type=float, required=True)
    kpi.add_argument("--total-revenue", type=float)
    kpi.add_argument("--acquisition-cost", type=float)
    kpi.add_argument("--operating-costs", type=float)

    cost = sub.add_parser("cost", help="alloca un costo per tipologia e data")
    cost.add_argument("--total-cost", type=float, required=True)
    cost.add_argument("--weight-pct", type=float, required=True)
    cost.add_argument("--units", type=float, required=True)

    price = sub.add_parser("price", help="calcola MUP, prezzo revenue e prezzo finale")
    price.add_argument("--cost-per-unit", type=float, required=True)
    price.add_argument("--mol-pct", type=float, required=True)
    price.add_argument("--occupancy-pct", type=float)
    price.add_argument("--adjustment-pct", type=float)
    price.add_argument("--bands", help='JSON soglia:variazione, ad es. \'{"0":-20,"60":0,"80":10}\'')
    price.add_argument("--base", choices=("mup", "revenue", "custom"), default="revenue")
    price.add_argument("--custom-base", type=float)
    price.add_argument("--global-change-pct", type=float, default=0.0)
    price.add_argument("--unit-change-pct", type=float, default=0.0)
    price.add_argument("--min-guaranteed", type=float)
    price.add_argument("--forced", type=float)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "kpi":
            payload = compute_kpis(
                args.available,
                args.sold,
                args.room_revenue,
                args.total_revenue,
                args.acquisition_cost,
                args.operating_costs,
            )
        elif args.command == "cost":
            payload = allocate_cost(args.total_cost, args.weight_pct, args.units)
        else:
            payload = compute_price(
                args.cost_per_unit,
                args.mol_pct,
                args.occupancy_pct,
                args.adjustment_pct,
                read_json(args.bands) if args.bands else None,
                args.base,
                args.custom_base,
                args.global_change_pct,
                args.unit_change_pct,
                args.min_guaranteed,
                args.forced,
            )
        emit(payload, args.output)
        if args.verbose:
            print("Calcolo completato; il risultato non è una previsione della domanda.", file=sys.stderr)
        return 0
    except (TypeError, ValueError, OSError) as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
