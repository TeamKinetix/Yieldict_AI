"""
CropYield AI: Core Optimization & Farmer Decision Support Engine
This module loads the trained crop yield model in read-only mode and executes:
1. Multi-Crop Profitability & Yield Ranking
2. Fertilizer ROI & Input Sweet-Spot Optimization
3. Climate & Drought Stress Vulnerability Assessment
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional

try:
    from .msp_data import CROP_METADATA, get_crop_price, get_crop_unit, get_crop_category
except ImportError:
    from msp_data import CROP_METADATA, get_crop_price, get_crop_unit, get_crop_category


class CropOptimizer:
    def __init__(self, model_path: Optional[str] = None, dataset_path: Optional[str] = None):
        """
        Initializes the Crop Optimizer by locating and loading the pre-trained pipeline
        and historical training data without modifying any existing files.
        """
        self.model_path = model_path or self._find_file("crop_yield_model.pkl")
        self.dataset_path = dataset_path or self._find_file("crop_yield_cleaned.csv")

        if not self.model_path or not os.path.exists(self.model_path):
            raise FileNotFoundError("Could not locate 'crop_yield_model.pkl'. Please provide a valid model path.")
        
        self.model = joblib.load(self.model_path)
        
        if self.dataset_path and os.path.exists(self.dataset_path):
            self.df = pd.read_csv(self.dataset_path)
        else:
            self.df = None

        self._init_metadata()

    def _find_file(self, filename: str) -> Optional[str]:
        search_paths = [
            os.path.join(os.path.dirname(__file__), "..", "important code", filename),
            os.path.join(os.path.dirname(__file__), "..", filename),
            os.path.join(os.path.dirname(__file__), filename),
            os.path.join(r"d:/CropYeild ML/important code", filename),
            os.path.join(r"d:/CropYeild ML", filename),
        ]
        for p in search_paths:
            if os.path.exists(p):
                return os.path.abspath(p)
        return None

    def _init_metadata(self):
        if self.df is not None:
            self.unique_states = sorted(self.df['state'].unique().tolist())
            self.unique_seasons = sorted(self.df['season'].unique().tolist())
            self.unique_crops = sorted(self.df['crop'].unique().tolist())
        else:
            self.unique_states = []
            self.unique_seasons = ['Kharif', 'Rabi', 'Whole Year', 'Summer', 'Autumn', 'Winter']
            self.unique_crops = list(CROP_METADATA.keys())

    def get_states(self) -> List[str]:
        return self.unique_states

    def get_seasons(self) -> List[str]:
        return self.unique_seasons

    def get_crops(self) -> List[str]:
        return self.unique_crops

    def get_viable_crops_for_region(self, state: str, season: str) -> List[str]:
        """
        Returns crops historically cultivated in the given state and season.
        Falls back to all crops if not in database.
        """
        if self.df is not None:
            filtered = self.df[(self.df['state'] == state) & (self.df['season'] == season)]
            viable = filtered['crop'].unique().tolist()
            if viable:
                return sorted(viable)
            # If season-specific not found, check state-level
            state_filtered = self.df[self.df['state'] == state]
            if not state_filtered.empty:
                return sorted(state_filtered['crop'].unique().tolist())
        return self.unique_crops

    def predict_yield(self, crop: str, season: str, state: str, area: float,
                      annual_rainfall: float, fertilizer: float, pesticide: float) -> float:
        """
        Predicts yield (production per hectare) for a single input record.
        """
        input_df = pd.DataFrame([{
            'crop': crop,
            'season': season,
            'state': state,
            'area': float(area),
            'annual_rainfall': float(annual_rainfall),
            'fertilizer': float(fertilizer),
            'pesticide': float(pesticide)
        }])
        pred = self.model.predict(input_df)[0]
        return max(0.0, float(pred))

    def recommend_crops(self, state: str, season: str, area: float,
                        annual_rainfall: float, fertilizer: Optional[float] = None,
                        pesticide: Optional[float] = None, top_n: int = 5,
                        only_viable: bool = True) -> List[Dict[str, Any]]:
        """
        Module 1: Multi-Crop Profitability & Yield Maximizer
        Evaluates viable crops for the farmer's region and returns ranked recommendations.
        """
        # Default fertilizer & pesticide estimates based on land area if not specified
        if fertilizer is None:
            fertilizer = float(area * 60.0) # ~60 kg/ha average
        if pesticide is None:
            pesticide = float(area * 0.35)  # ~0.35 kg/ha average

        candidate_crops = self.get_viable_crops_for_region(state, season) if only_viable else self.unique_crops
        if not candidate_crops:
            candidate_crops = self.unique_crops

        rows = []
        for c in candidate_crops:
            rows.append({
                'crop': c,
                'season': season,
                'state': state,
                'area': float(area),
                'annual_rainfall': float(annual_rainfall),
                'fertilizer': float(fertilizer),
                'pesticide': float(pesticide)
            })

        batch_df = pd.DataFrame(rows)
        preds = self.model.predict(batch_df)

        results = []
        for i, row in batch_df.iterrows():
            crop_name = row['crop']
            y_hat = max(0.0, float(preds[i]))
            unit = get_crop_unit(crop_name)
            price_per_unit = get_crop_price(crop_name)
            category = get_crop_category(crop_name)
            
            total_production = y_hat * float(area)
            expected_revenue = total_production * price_per_unit
            revenue_per_ha = expected_revenue / max(1e-5, float(area))

            results.append({
                "crop": crop_name,
                "category": category,
                "predicted_yield": round(y_hat, 2),
                "yield_unit": f"{unit}/ha",
                "total_production": round(total_production, 2),
                "production_unit": unit,
                "price_per_unit_inr": price_per_unit,
                "expected_gross_revenue_inr": round(expected_revenue, 2),
                "revenue_per_ha_inr": round(revenue_per_ha, 2)
            })

        # Rank primarily by expected revenue
        results = sorted(results, key=lambda x: x["expected_gross_revenue_inr"], reverse=True)
        return results[:top_n]

    def optimize_fertilizer(self, crop: str, season: str, state: str, area: float,
                            annual_rainfall: float, base_fertilizer: float,
                            pesticide: float, fertilizer_cost_per_kg: float = 18.0) -> Dict[str, Any]:
        """
        Module 2: Fertilizer Dosage & ROI Sweet-Spot Curve
        Simulates dosage scaling (from 20% to 250%) and identifies optimal net return.
        """
        multipliers = [0.25, 0.50, 0.75, 1.0, 1.25, 1.50, 1.75, 2.0, 2.5]
        price_per_unit = get_crop_price(crop)
        unit = get_crop_unit(crop)

        sim_rows = []
        for m in multipliers:
            fert_val = base_fertilizer * m
            sim_rows.append({
                'crop': crop, 'season': season, 'state': state,
                'area': float(area), 'annual_rainfall': float(annual_rainfall),
                'fertilizer': float(fert_val), 'pesticide': float(pesticide)
            })
        
        sim_df = pd.DataFrame(sim_rows)
        yield_preds = self.model.predict(sim_df)

        curve_points = []
        best_point = None
        max_net_gain = -float('inf')

        for i, m in enumerate(multipliers):
            fert_amount = base_fertilizer * m
            rate_per_ha = fert_amount / max(1e-5, area)
            y_val = max(0.0, float(yield_preds[i]))
            total_prod = y_val * area
            gross_rev = total_prod * price_per_unit
            fert_cost = fert_amount * fertilizer_cost_per_kg
            net_profit_over_fert = gross_rev - fert_cost

            pt = {
                "multiplier": m,
                "dosage_pct": int(m * 100),
                "fertilizer_total_kg": round(fert_amount, 1),
                "fertilizer_rate_kg_ha": round(rate_per_ha, 1),
                "predicted_yield": round(y_val, 2),
                "total_production": round(total_prod, 2),
                "gross_revenue_inr": round(gross_rev, 2),
                "fertilizer_cost_inr": round(fert_cost, 2),
                "net_profit_inr": round(net_profit_over_fert, 2)
            }
            curve_points.append(pt)

            if net_profit_over_fert > max_net_gain:
                max_net_gain = net_profit_over_fert
                best_point = pt

        # Baseline comparison at multiplier=1.0
        baseline_pt = next((p for p in curve_points if p["multiplier"] == 1.0), curve_points[3])
        profit_delta = best_point["net_profit_inr"] - baseline_pt["net_profit_inr"]

        return {
            "crop": crop,
            "unit": unit,
            "baseline_fertilizer_kg": round(base_fertilizer, 1),
            "optimal_dosage_kg": best_point["fertilizer_total_kg"],
            "optimal_dosage_kg_ha": best_point["fertilizer_rate_kg_ha"],
            "optimal_dosage_pct": best_point["dosage_pct"],
            "baseline_net_profit_inr": baseline_pt["net_profit_inr"],
            "optimal_net_profit_inr": best_point["net_profit_inr"],
            "potential_extra_profit_inr": round(profit_delta, 2),
            "dosage_curve": curve_points
        }

    def simulate_climate_stress(self, crop: str, season: str, state: str, area: float,
                                base_rainfall: float, fertilizer: float, pesticide: float) -> Dict[str, Any]:
        """
        Module 3: Climate & Drought Sensitivity Assessment
        Simulates yield under severe drought, deficit, normal, and excess rainfall.
        """
        scenarios = [
            {"name": "Severe Drought (-50%)", "factor": 0.50},
            {"name": "Moderate Deficit (-25%)", "factor": 0.75},
            {"name": "Baseline Rainfall (Normal)", "factor": 1.00},
            {"name": "Above Average (+25%)", "factor": 1.25},
            {"name": "Excessive Monsoon (+50%)", "factor": 1.50},
        ]

        sim_rows = []
        for s in scenarios:
            sim_rows.append({
                'crop': crop, 'season': season, 'state': state,
                'area': float(area),
                'annual_rainfall': float(base_rainfall * s["factor"]),
                'fertilizer': float(fertilizer), 'pesticide': float(pesticide)
            })

        sim_df = pd.DataFrame(sim_rows)
        preds = self.model.predict(sim_df)

        scenario_results = []
        normal_yield = None

        for i, s in enumerate(scenarios):
            y = max(0.0, float(preds[i]))
            if s["factor"] == 1.0:
                normal_yield = y
            scenario_results.append({
                "scenario": s["name"],
                "rainfall_mm": round(base_rainfall * s["factor"], 1),
                "predicted_yield": round(y, 2),
                "total_production": round(y * area, 2)
            })

        # Calculate Drought Resilience Index
        drought_yield = scenario_results[0]["predicted_yield"] # -50%
        normal_y = normal_yield if normal_yield and normal_yield > 0 else 1.0
        yield_retention_pct = round((drought_yield / normal_y) * 100, 1)

        if yield_retention_pct >= 90:
            risk_level = "Low Drought Risk (Highly Resilient)"
        elif yield_retention_pct >= 70:
            risk_level = "Moderate Drought Risk"
        else:
            risk_level = "High Drought Risk (Vulnerable to Monsoon Failure)"

        return {
            "crop": crop,
            "base_rainfall_mm": base_rainfall,
            "yield_retention_in_drought_pct": yield_retention_pct,
            "climate_risk_level": risk_level,
            "scenarios": scenario_results
        }

    def generate_full_advisory(self, state: str, season: str, area: float,
                               annual_rainfall: float, fertilizer: float,
                               pesticide: float, primary_crop: Optional[str] = None) -> Dict[str, Any]:
        """
        Produces a complete decision support report combining all 3 modules.
        """
        recommendations = self.recommend_crops(
            state=state, season=season, area=area,
            annual_rainfall=annual_rainfall, fertilizer=fertilizer,
            pesticide=pesticide, top_n=6
        )

        chosen_crop = primary_crop if primary_crop else (recommendations[0]["crop"] if recommendations else "Rice")

        fertilizer_opt = self.optimize_fertilizer(
            crop=chosen_crop, season=season, state=state,
            area=area, annual_rainfall=annual_rainfall,
            base_fertilizer=fertilizer, pesticide=pesticide
        )

        climate_sim = self.simulate_climate_stress(
            crop=chosen_crop, season=season, state=state,
            area=area, base_rainfall=annual_rainfall,
            fertilizer=fertilizer, pesticide=pesticide
        )

        return {
            "farmer_inputs": {
                "state": state, "season": season, "area_ha": area,
                "annual_rainfall_mm": annual_rainfall,
                "fertilizer_kg": fertilizer, "pesticide_kg": pesticide,
                "analyzed_crop": chosen_crop
            },
            "top_recommended_crops": recommendations,
            "fertilizer_optimization": fertilizer_opt,
            "climate_stress_analysis": climate_sim
        }
