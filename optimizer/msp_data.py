"""
MSP and Market Pricing Reference for 55 Major Indian Crops
Prices are standardized in INR (₹) per Unit:
- Most Field Crops: ₹ per Tonne (1 Tonne = 10 Quintals = 1000 Kg)
- Coconut: ₹ per Nut (average farmgate price ₹12-18/nut)
"""

CROP_METADATA = {
    # Cereals & Millets
    "Rice": {"category": "Cereals", "unit": "Tonne", "price_per_unit": 22000, "msp_declared": True},
    "Wheat": {"category": "Cereals", "unit": "Tonne", "price_per_unit": 22750, "msp_declared": True},
    "Maize": {"category": "Cereals", "unit": "Tonne", "price_per_unit": 20900, "msp_declared": True},
    "Bajra": {"category": "Millets", "unit": "Tonne", "price_per_unit": 25000, "msp_declared": True},
    "Jowar": {"category": "Millets", "unit": "Tonne", "price_per_unit": 31800, "msp_declared": True},
    "Ragi": {"category": "Millets", "unit": "Tonne", "price_per_unit": 38460, "msp_declared": True},
    "Barley": {"category": "Cereals", "unit": "Tonne", "price_per_unit": 18500, "msp_declared": True},
    "Small millets": {"category": "Millets", "unit": "Tonne", "price_per_unit": 28000, "msp_declared": True},
    "Other Cereals": {"category": "Cereals", "unit": "Tonne", "price_per_unit": 20000, "msp_declared": False},

    # Pulses
    "Gram": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 54400, "msp_declared": True},
    "Arhar/Tur": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 70000, "msp_declared": True},
    "Moong(Green Gram)": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 85580, "msp_declared": True},
    "Urad": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 69500, "msp_declared": True},
    "Masoor": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 64250, "msp_declared": True},
    "Peas & beans (Pulses)": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 45000, "msp_declared": False},
    "Cowpea(Lobia)": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 52000, "msp_declared": False},
    "Horse-gram": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 42000, "msp_declared": False},
    "Khesari": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 38000, "msp_declared": False},
    "Moth": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 48000, "msp_declared": False},
    "Other  Rabi pulses": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 48000, "msp_declared": False},
    "Other Kharif pulses": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 50000, "msp_declared": False},
    "Other Summer Pulses": {"category": "Pulses", "unit": "Tonne", "price_per_unit": 50000, "msp_declared": False},

    # Oilseeds
    "Groundnut": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 63770, "msp_declared": True},
    "Soyabean": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 46000, "msp_declared": True},
    "Rapeseed &Mustard": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 56500, "msp_declared": True},
    "Sesamum": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 86350, "msp_declared": True},
    "Sunflower": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 67600, "msp_declared": True},
    "Safflower": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 58000, "msp_declared": True},
    "Niger seed": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 77340, "msp_declared": True},
    "Castor seed": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 55000, "msp_declared": False},
    "Linseed": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 52000, "msp_declared": False},
    "Oilseeds total": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 55000, "msp_declared": False},
    "other oilseeds": {"category": "Oilseeds", "unit": "Tonne", "price_per_unit": 50000, "msp_declared": False},

    # Commercial & Cash Crops
    "Sugarcane": {"category": "Cash Crops", "unit": "Tonne", "price_per_unit": 3150, "msp_declared": True}, # FRP
    "Cotton(lint)": {"category": "Commercial", "unit": "Tonne", "price_per_unit": 70200, "msp_declared": True},
    "Jute": {"category": "Commercial", "unit": "Tonne", "price_per_unit": 50500, "msp_declared": True},
    "Mesta": {"category": "Commercial", "unit": "Tonne", "price_per_unit": 38000, "msp_declared": False},
    "Tobacco": {"category": "Commercial", "unit": "Tonne", "price_per_unit": 65000, "msp_declared": False},
    "Guar seed": {"category": "Commercial", "unit": "Tonne", "price_per_unit": 52000, "msp_declared": False},
    "Sannhamp": {"category": "Commercial", "unit": "Tonne", "price_per_unit": 32000, "msp_declared": False},

    # Plantation & Spices
    "Coconut": {"category": "Plantation", "unit": "Nuts", "price_per_unit": 15.0, "msp_declared": True}, # Approx ₹15 per nut
    "Arecanut": {"category": "Plantation", "unit": "Tonne", "price_per_unit": 280000, "msp_declared": False},
    "Cashewnut": {"category": "Plantation", "unit": "Tonne", "price_per_unit": 120000, "msp_declared": False},
    "Black pepper": {"category": "Spices", "unit": "Tonne", "price_per_unit": 450000, "msp_declared": False},
    "Cardamom": {"category": "Spices", "unit": "Tonne", "price_per_unit": 1100000, "msp_declared": False},
    "Coriander": {"category": "Spices", "unit": "Tonne", "price_per_unit": 85000, "msp_declared": False},
    "Dry chillies": {"category": "Spices", "unit": "Tonne", "price_per_unit": 160000, "msp_declared": False},
    "Garlic": {"category": "Spices", "unit": "Tonne", "price_per_unit": 75000, "msp_declared": False},
    "Ginger": {"category": "Spices", "unit": "Tonne", "price_per_unit": 60000, "msp_declared": False},
    "Turmeric": {"category": "Spices", "unit": "Tonne", "price_per_unit": 90000, "msp_declared": False},

    # Vegetables & Tubers
    "Potato": {"category": "Vegetables", "unit": "Tonne", "price_per_unit": 14000, "msp_declared": False},
    "Onion": {"category": "Vegetables", "unit": "Tonne", "price_per_unit": 18000, "msp_declared": False},
    "Sweet potato": {"category": "Vegetables", "unit": "Tonne", "price_per_unit": 15000, "msp_declared": False},
    "Tapioca": {"category": "Vegetables", "unit": "Tonne", "price_per_unit": 12000, "msp_declared": False},
    "Banana": {"category": "Fruits", "unit": "Tonne", "price_per_unit": 20000, "msp_declared": False},
}

def get_crop_price(crop_name: str) -> float:
    """Returns the market/MSP price per unit for the crop."""
    return CROP_METADATA.get(crop_name, {}).get("price_per_unit", 25000.0)

def get_crop_unit(crop_name: str) -> str:
    """Returns unit of measurement (Tonne or Nuts)."""
    return CROP_METADATA.get(crop_name, {}).get("unit", "Tonne")

def get_crop_category(crop_name: str) -> str:
    """Returns category of the crop."""
    return CROP_METADATA.get(crop_name, {}).get("category", "General")
