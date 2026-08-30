"""
CropYield AI: Interactive CLI Demonstration for Hackathon Judges
Run: python optimizer/demo_cli.py
"""

import sys
import os

try:
    from .crop_optimizer import CropOptimizer
except ImportError:
    from crop_optimizer import CropOptimizer


def format_currency(val: float) -> str:
    return f"Rs. {val:,.2f}"


def print_banner():
    print("=" * 80)
    print("  *  CropYield AI: Intelligent Decision Support & Optimization System  *")
    print("     (Pre-Harvest Forecasting, Multi-Crop Ranking & Climate Stress Analysis)")
    print("=" * 80)


def run_demo():
    print_banner()
    opt = CropOptimizer()

    print("\n[+] Model and Indian Agricultural Catalog Loaded Successfully!")
    print(f"    - Supported States: {len(opt.get_states())} States & UTs")
    print(f"    - Supported Crops:  {len(opt.get_crops())} Crops")
    print(f"    - Supported Seasons: {', '.join(opt.get_seasons())}")

    # Demo Scenario
    state = "Punjab"
    season = "Kharif"
    area = 1000.0  # Hectares
    rainfall = 800.0  # mm
    fertilizer = 60000.0  # kg
    pesticide = 250.0  # kg

    print("\n" + "-" * 80)
    print(f"> SCENARIO: Farmer in {state} | Season: {season} | Land Area: {area:,.0f} ha | Rainfall: {rainfall} mm")
    print("-" * 80)

    # 1. Multi-crop recommendation
    print("\n[1] MULTI-CROP PROFITABILITY & YIELD RANKING (TOP 5 RECOMMENDED CROPS):")
    print("-" * 80)
    print(f"{'Rank':<5} {'Crop Name':<20} {'Category':<14} {'Yield/ha':<12} {'Total Prod':<15} {'Expected Revenue (INR)':<25}")
    print("-" * 80)

    recs = opt.recommend_crops(state, season, area, rainfall, fertilizer, pesticide, top_n=5)
    for idx, r in enumerate(recs, 1):
        prod_str = f"{r['total_production']:,.1f} {r['production_unit']}"
        yield_str = f"{r['predicted_yield']:.2f} {r['yield_unit']}"
        print(f"#{idx:<4} {r['crop']:<20} {r['category']:<14} {yield_str:<12} {prod_str:<15} {format_currency(r['expected_gross_revenue_inr']):<25}")
    print("-" * 80)

    # 2. Fertilizer Optimization
    primary_crop = "Rice"
    print(f"\n[2] FERTILIZER ROI & INPUT SWEET-SPOT ANALYSIS (Crop: {primary_crop}):")
    print("-" * 80)
    fert_res = opt.optimize_fertilizer(primary_crop, season, state, area, rainfall, fertilizer, pesticide)
    print(f"  * Baseline Fertilizer Applied: {fert_res['baseline_fertilizer_kg']:,.0f} kg ({fert_res['baseline_fertilizer_kg']/area:.1f} kg/ha)")
    print(f"  * Recommended Optimal Dosage:  {fert_res['optimal_dosage_kg']:,.0f} kg ({fert_res['optimal_dosage_kg_ha']:.1f} kg/ha) [{fert_res['optimal_dosage_pct']}% of baseline]")
    print(f"  * Baseline Net Revenue:        {format_currency(fert_res['baseline_net_profit_inr'])}")
    print(f"  * Optimized Net Revenue:       {format_currency(fert_res['optimal_net_profit_inr'])}")
    print(f"  * Potential Profit Uplift:     {format_currency(fert_res['potential_extra_profit_inr'])}")

    print("\n   [Dosage Response Steps]:")
    for pt in fert_res["dosage_curve"][1:7]:
        marker = " <-- OPTIMAL SWEET-SPOT" if pt["dosage_pct"] == fert_res["optimal_dosage_pct"] else ""
        print(f"     - Dosage {pt['dosage_pct']:>3}% ({pt['fertilizer_rate_kg_ha']:>5.1f} kg/ha): Yield={pt['predicted_yield']:>4.2f} t/ha | Net Profit={format_currency(pt['net_profit_inr'])}{marker}")

    # 3. Climate & Drought Stress
    print(f"\n[3] CLIMATE RESILIENCE & DROUGHT STRESS TEST (Crop: {primary_crop}):")
    print("-" * 80)
    clim_res = opt.simulate_climate_stress(primary_crop, season, state, area, rainfall, fertilizer, pesticide)
    print(f"  * Drought Resilience Score: {clim_res['yield_retention_in_drought_pct']}% Yield Retained under -50% Rainfall")
    print(f"  * Climate Risk Assessment:  {clim_res['climate_risk_level']}")
    print("\n   [Rainfall Stress Curves]:")
    for sc in clim_res["scenarios"]:
        print(f"     - {sc['scenario']:<30} | Rain: {sc['rainfall_mm']:>6.1f} mm | Predicted Yield: {sc['predicted_yield']:>4.2f} t/ha | Total: {sc['total_production']:>7,.1f} Tonnes")

    print("\n" + "=" * 80)
    print("  [SUCCESS] Hackathon Demo: End-to-end forecasting, ROI optimization, and climate testing complete.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_demo()
