"""
CropYield AI: Zero-Dependency Interactive Web Dashboard
Run: python optimizer/server.py
Access via browser at: http://localhost:8501
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

try:
    from .crop_optimizer import CropOptimizer
except ImportError:
    from crop_optimizer import CropOptimizer

opt_engine = None

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CropYield AI | Decision Support & Optimizer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #0a0f18;
            --bg-card: #121a29;
            --bg-card-hover: #172236;
            --bg-input: #1a253a;
            --border: #22324d;
            --primary: #10b981;
            --primary-glow: rgba(16, 185, 129, 0.25);
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.25);
            --warning: #f59e0b;
            --danger: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Top Header */
        header {
            background: linear-gradient(180deg, rgba(18, 26, 41, 0.9) 0%, rgba(10, 15, 24, 0.9) 100%);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 16px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #10b981, #0284c7);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 0 20px var(--primary-glow);
        }

        .brand-title h1 {
            font-size: 20px;
            font-weight: 800;
            background: linear-gradient(90deg, #34d399, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        .brand-title p {
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .badge-group {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .pill {
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .pill.active {
            border-color: #10b981;
            color: #34d399;
            background: rgba(16, 185, 129, 0.1);
        }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 10px #10b981;
        }

        /* Layout Grid */
        .main-container {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 24px;
            padding: 24px 32px;
            flex: 1;
        }

        /* Control Sidebar */
        .sidebar {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            height: fit-content;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .sidebar-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }

        .preset-buttons {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .preset-btn {
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 5px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .preset-btn:hover {
            color: var(--accent);
            border-color: var(--accent);
            background: rgba(56, 189, 248, 0.1);
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .form-group label {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }

        .val-badge {
            color: var(--accent);
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        }

        select, input[type="number"], input[type="range"] {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 12px;
            color: var(--text-main);
            font-size: 13px;
            font-weight: 500;
            outline: none;
            transition: border-color 0.2s;
        }

        select:focus, input[type="number"]:focus {
            border-color: var(--accent);
            box-shadow: 0 0 10px var(--accent-glow);
        }

        input[type="range"] {
            padding: 0;
            height: 6px;
            cursor: pointer;
            accent-color: var(--primary);
        }

        .submit-btn {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px var(--primary-glow);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
        }

        /* Dashboard Content */
        .content {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }

        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            position: relative;
            overflow: hidden;
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--primary);
        }

        .kpi-card.accent::before { background: var(--accent); }
        .kpi-card.warning::before { background: var(--warning); }
        .kpi-card.purple::before { background: #a855f7; }

        .kpi-title {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .kpi-value {
            font-size: 22px;
            font-weight: 800;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
        }

        .kpi-sub {
            font-size: 11px;
            color: var(--text-dim);
            font-weight: 500;
        }

        /* Section Cards */
        .section-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-title-icon {
            font-size: 18px;
        }

        /* Recommendations Table */
        .table-wrap {
            overflow-x: auto;
            border-radius: 10px;
            border: 1px solid var(--border);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }

        th {
            background: var(--bg-input);
            padding: 12px 16px;
            font-weight: 700;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        td {
            padding: 14px 16px;
            border-bottom: 1px solid rgba(34, 50, 77, 0.5);
            color: var(--text-main);
            font-weight: 500;
        }

        tr:hover td {
            background: var(--bg-card-hover);
        }

        .badge-rank {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: 6px;
            font-weight: 800;
            font-size: 12px;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent);
        }

        .badge-rank.top1 {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            box-shadow: 0 0 10px var(--primary-glow);
        }

        .chart-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .chart-box {
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            height: 280px;
            position: relative;
        }

        /* Loading Spinner */
        .spinner {
            display: none;
            width: 18px;
            height: 18px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @media (max-width: 1024px) {
            .main-container { grid-template-columns: 1fr; }
            .kpi-grid { grid-template-columns: 1fr 1fr; }
            .chart-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="brand-icon">🌱</div>
            <div class="brand-title">
                <h1>CropYield AI Optimizer</h1>
                <p>Agricultural Decision Support & Multi-Crop Economic Forecaster</p>
            </div>
        </div>
        <div class="badge-group">
            <div class="pill active"><div class="dot"></div> Model: Random Forest (R²=98.05%)</div>
            <div class="pill">55 Crops Supported</div>
            <div class="pill">30 States</div>
        </div>
    </header>

    <div class="main-container">
        <!-- Controls -->
        <aside class="sidebar">
            <div class="sidebar-title">
                <span>🌾 Farm Parameters</span>
                <span style="font-size: 11px; color: var(--text-dim);">Pre-Harvest Mode</span>
            </div>

            <div class="form-group">
                <label>Quick Presets</label>
                <div class="preset-buttons">
                    <button class="preset-btn" onclick="applyPreset('Punjab','Kharif',1000,800,60000,250,'Rice')">Punjab Rice</button>
                    <button class="preset-btn" onclick="applyPreset('Uttar Pradesh','Rabi',2000,750,100000,600,'Wheat')">UP Wheat</button>
                    <button class="preset-btn" onclick="applyPreset('Maharashtra','Whole Year',5000,1100,400000,1500,'Sugarcane')">MH Sugarcane</button>
                    <button class="preset-btn" onclick="applyPreset('Kerala','Whole Year',10000,2500,800000,3000,'Coconut')">Kerala Coconut</button>
                </div>
            </div>

            <div class="form-group">
                <label for="stateSelect">State / UT</label>
                <select id="stateSelect" onchange="onRegionChange()"></select>
            </div>

            <div class="form-group">
                <label for="seasonSelect">Cropping Season</label>
                <select id="seasonSelect" onchange="onRegionChange()"></select>
            </div>

            <div class="form-group">
                <label for="cropSelect">Focus Crop (for Fertilizer & Drought)</label>
                <select id="cropSelect"></select>
            </div>

            <div class="form-group">
                <label for="areaInput">Land Area (Hectares): <span class="val-badge" id="areaVal">1,000 ha</span></label>
                <input type="range" id="areaRange" min="1" max="25000" step="10" value="1000" oninput="syncVal('area', this.value, ' ha')">
                <input type="number" id="areaInput" value="1000" min="0.5" onchange="syncRange('area', this.value)">
            </div>

            <div class="form-group">
                <label for="rainfallInput">Annual Rainfall (mm): <span class="val-badge" id="rainfallVal">800 mm</span></label>
                <input type="range" id="rainfallRange" min="200" max="4500" step="25" value="800" oninput="syncVal('rainfall', this.value, ' mm')">
                <input type="number" id="rainfallInput" value="800" min="50" onchange="syncRange('rainfall', this.value)">
            </div>

            <div class="form-group">
                <label for="fertInput">Total Fertilizer (kg): <span class="val-badge" id="fertVal">60,000 kg</span></label>
                <input type="number" id="fertInput" value="60000" min="0">
            </div>

            <div class="form-group">
                <label for="pestInput">Total Pesticide (kg): <span class="val-badge" id="pestVal">250 kg</span></label>
                <input type="number" id="pestInput" value="250" min="0">
            </div>

            <button class="submit-btn" onclick="runOptimization()">
                <div class="spinner" id="btnSpinner"></div>
                <span>⚡ Run AI Crop Optimizer</span>
            </button>
        </aside>

        <!-- Main Dashboard Results -->
        <main class="content">
            <!-- KPIs -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Top Recommended Crop</div>
                    <div class="kpi-value" id="kpiTopCrop" style="color: #34d399;">--</div>
                    <div class="kpi-sub" id="kpiTopYield">Predicted: --</div>
                </div>
                <div class="kpi-card accent">
                    <div class="kpi-title">Max Expected Revenue</div>
                    <div class="kpi-value" id="kpiMaxRev">₹ 0.00</div>
                    <div class="kpi-sub" id="kpiRevPerHa">₹ 0 / ha</div>
                </div>
                <div class="kpi-card warning">
                    <div class="kpi-title">Fertilizer Sweet-Spot</div>
                    <div class="kpi-value" id="kpiFertUplift">+ ₹ 0.00</div>
                    <div class="kpi-sub" id="kpiFertDosage">Recommended: --</div>
                </div>
                <div class="kpi-card purple">
                    <div class="kpi-title">Climate Resilience Score</div>
                    <div class="kpi-value" id="kpiDroughtScore">-- %</div>
                    <div class="kpi-sub" id="kpiDroughtRisk">Risk Level: --</div>
                </div>
            </div>

            <!-- Recommendation Leaderboard -->
            <section class="section-card">
                <div class="card-header">
                    <div class="card-title">
                        <span class="card-title-icon">🏆</span>
                        <span>Multi-Crop Profitability & Yield Leaderboard</span>
                    </div>
                    <span style="font-size: 12px; color: var(--text-dim);">Ranked by Expected Gross Revenue (₹ MSP)</span>
                </div>

                <div class="table-wrap">
                    <table id="recsTable">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Crop Name</th>
                                <th>Category</th>
                                <th>Predicted Yield</th>
                                <th>Total Production</th>
                                <th>MSP / Rate</th>
                                <th>Expected Gross Revenue</th>
                            </tr>
                        </thead>
                        <tbody id="recsTbody">
                            <tr><td colspan="7" style="text-align: center; color: var(--text-dim);">Click 'Run AI Crop Optimizer' to calculate recommendations.</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Diagnostic Charts Grid -->
            <div class="chart-grid">
                <section class="section-card">
                    <div class="card-header">
                        <div class="card-title">
                            <span class="card-title-icon">📊</span>
                            <span>Expected Revenue Comparison</span>
                        </div>
                    </div>
                    <div class="chart-box">
                        <canvas id="revChart"></canvas>
                    </div>
                </section>

                <section class="section-card">
                    <div class="card-header">
                        <div class="card-title">
                            <span class="card-title-icon">📈</span>
                            <span>Fertilizer ROI & Net Profit Curve</span>
                        </div>
                    </div>
                    <div class="chart-box">
                        <canvas id="fertChart"></canvas>
                    </div>
                </section>
            </div>

            <!-- Climate Stress Simulator -->
            <section class="section-card">
                <div class="card-header">
                    <div class="card-title">
                        <span class="card-title-icon">🌧️</span>
                        <span>Climate & Drought Stress Simulation for <span id="stressCropTitle" style="color: var(--accent);">Rice</span></span>
                    </div>
                    <span id="stressRiskPill" class="pill">Risk Assessment</span>
                </div>
                <div class="chart-box" style="height: 240px;">
                    <canvas id="climateChart"></canvas>
                </div>
            </section>
        </main>
    </div>

    <script>
        let revChartInstance = null;
        let fertChartInstance = null;
        let climateChartInstance = null;
        let metadata = { states: [], seasons: [], crops: [] };

        async function init() {
            try {
                const res = await fetch('/api/metadata');
                metadata = await res.json();

                const stateSel = document.getElementById('stateSelect');
                metadata.states.forEach(s => {
                    const opt = document.createElement('option');
                    opt.value = s; opt.textContent = s;
                    if (s === 'Punjab') opt.selected = true;
                    stateSel.appendChild(opt);
                });

                const seasonSel = document.getElementById('seasonSelect');
                metadata.seasons.forEach(s => {
                    const opt = document.createElement('option');
                    opt.value = s; opt.textContent = s;
                    if (s === 'Kharif') opt.selected = true;
                    seasonSel.appendChild(opt);
                });

                const cropSel = document.getElementById('cropSelect');
                metadata.crops.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c; opt.textContent = c;
                    if (c === 'Rice') opt.selected = true;
                    cropSel.appendChild(opt);
                });

                runOptimization();
            } catch (err) {
                console.error("Init failed:", err);
            }
        }

        function syncVal(id, val, suffix) {
            document.getElementById(id + 'Val').textContent = Number(val).toLocaleString() + suffix;
            document.getElementById(id + 'Input').value = val;
        }

        function syncRange(id, val) {
            document.getElementById(id + 'Range').value = val;
            document.getElementById(id + 'Val').textContent = Number(val).toLocaleString() + (id === 'area' ? ' ha' : ' mm');
        }

        function applyPreset(state, season, area, rain, fert, pest, crop) {
            document.getElementById('stateSelect').value = state;
            document.getElementById('seasonSelect').value = season;
            document.getElementById('areaInput').value = area;
            document.getElementById('areaRange').value = area;
            document.getElementById('areaVal').textContent = Number(area).toLocaleString() + ' ha';
            document.getElementById('rainfallInput').value = rain;
            document.getElementById('rainfallRange').value = rain;
            document.getElementById('rainfallVal').textContent = Number(rain).toLocaleString() + ' mm';
            document.getElementById('fertInput').value = fert;
            document.getElementById('pestInput').value = pest;
            document.getElementById('cropSelect').value = crop;
            runOptimization();
        }

        function formatINR(num) {
            return '₹ ' + Number(num).toLocaleString('en-IN', { maximumFractionDigits: 2 });
        }

        async function runOptimization() {
            const spinner = document.getElementById('btnSpinner');
            spinner.style.display = 'block';

            const payload = {
                state: document.getElementById('stateSelect').value,
                season: document.getElementById('seasonSelect').value,
                area: parseFloat(document.getElementById('areaInput').value),
                annual_rainfall: parseFloat(document.getElementById('rainfallInput').value),
                fertilizer: parseFloat(document.getElementById('fertInput').value),
                pesticide: parseFloat(document.getElementById('pestInput').value),
                crop: document.getElementById('cropSelect').value
            };

            try {
                const res = await fetch('/api/optimize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                renderDashboard(data);
            } catch (err) {
                console.error("Optimization failed:", err);
            } finally {
                spinner.style.display = 'none';
            }
        }

        function renderDashboard(data) {
            const topCrop = data.top_recommended_crops[0];
            if (topCrop) {
                document.getElementById('kpiTopCrop').textContent = topCrop.crop;
                document.getElementById('kpiTopYield').textContent = `Predicted: ${topCrop.predicted_yield} ${topCrop.yield_unit}`;
                document.getElementById('kpiMaxRev').textContent = formatINR(topCrop.expected_gross_revenue_inr);
                document.getElementById('kpiRevPerHa').textContent = formatINR(topCrop.revenue_per_ha_inr) + ' / ha';
            }

            const fert = data.fertilizer_optimization;
            document.getElementById('kpiFertUplift').textContent = (fert.potential_extra_profit_inr >= 0 ? '+ ' : '') + formatINR(fert.potential_extra_profit_inr);
            document.getElementById('kpiFertDosage').textContent = `Optimal: ${fert.optimal_dosage_pct}% (${fert.optimal_dosage_kg_ha} kg/ha)`;

            const clim = data.climate_stress_analysis;
            document.getElementById('kpiDroughtScore').textContent = `${clim.yield_retention_in_drought_pct}%`;
            document.getElementById('kpiDroughtRisk').textContent = clim.climate_risk_level;
            document.getElementById('stressCropTitle').textContent = clim.crop;
            document.getElementById('stressRiskPill').textContent = clim.climate_risk_level;

            // Render Table
            const tbody = document.getElementById('recsTbody');
            tbody.innerHTML = '';
            data.top_recommended_crops.forEach((r, idx) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><span class="badge-rank ${idx === 0 ? 'top1' : ''}">#${idx + 1}</span></td>
                    <td style="font-weight: 700;">${r.crop}</td>
                    <td><span class="pill" style="font-size: 11px;">${r.category}</span></td>
                    <td style="font-family: 'JetBrains Mono';">${r.predicted_yield} ${r.yield_unit}</td>
                    <td style="font-family: 'JetBrains Mono';">${r.total_production.toLocaleString()} ${r.production_unit}</td>
                    <td style="color: var(--text-dim); font-family: 'JetBrains Mono';">${formatINR(r.price_per_unit_inr)}</td>
                    <td style="color: #34d399; font-weight: 700; font-family: 'JetBrains Mono';">${formatINR(r.expected_gross_revenue_inr)}</td>
                `;
                tbody.appendChild(tr);
            });

            // Render Charts
            renderRevenueChart(data.top_recommended_crops);
            renderFertilizerChart(fert);
            renderClimateChart(clim);
        }

        function renderRevenueChart(recs) {
            const ctx = document.getElementById('revChart').getContext('2d');
            if (revChartInstance) revChartInstance.destroy();

            revChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: recs.map(r => r.crop),
                    datasets: [{
                        label: 'Gross Revenue (₹)',
                        data: recs.map(r => r.expected_gross_revenue_inr),
                        backgroundColor: ['#10b981', '#38bdf8', '#818cf8', '#fbbf24', '#f87171', '#a78bfa'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(34, 50, 77, 0.4)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(34, 50, 77, 0.4)' }, ticks: { color: '#94a3b8' } }
                    }
                }
            });
        }

        function renderFertilizerChart(fert) {
            const ctx = document.getElementById('fertChart').getContext('2d');
            if (fertChartInstance) fertChartInstance.destroy();

            const pts = fert.dosage_curve;
            fertChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: pts.map(p => p.dosage_pct + '%'),
                    datasets: [
                        {
                            label: 'Net Profit (₹)',
                            data: pts.map(p => p.net_profit_inr),
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            fill: true,
                            tension: 0.3
                        },
                        {
                            label: 'Fertilizer Cost (₹)',
                            data: pts.map(p => p.fertilizer_cost_inr),
                            borderColor: '#ef4444',
                            borderDash: [5, 5],
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(34, 50, 77, 0.4)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(34, 50, 77, 0.4)' }, ticks: { color: '#94a3b8' } }
                    }
                }
            });
        }

        function renderClimateChart(clim) {
            const ctx = document.getElementById('climateChart').getContext('2d');
            if (climateChartInstance) climateChartInstance.destroy();

            const scs = clim.scenarios;
            climateChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: scs.map(s => s.scenario),
                    datasets: [{
                        label: 'Predicted Yield (' + clim.crop + ')',
                        data: scs.map(s => s.predicted_yield),
                        backgroundColor: ['#ef4444', '#f59e0b', '#10b981', '#38bdf8', '#6366f1'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(34, 50, 77, 0.4)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(34, 50, 77, 0.4)' }, ticks: { color: '#94a3b8' } }
                    }
                }
            });
        }

        window.onload = init;
    </script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif parsed.path == "/api/metadata":
            global opt_engine
            if opt_engine is None:
                opt_engine = CropOptimizer()
            meta = {
                "states": opt_engine.get_states(),
                "seasons": opt_engine.get_seasons(),
                "crops": opt_engine.get_crops()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(meta).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/optimize":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                global opt_engine
                if opt_engine is None:
                    opt_engine = CropOptimizer()

                state = data.get("state", "Punjab")
                season = data.get("season", "Kharif")
                area = float(data.get("area", 1000.0))
                rainfall = float(data.get("annual_rainfall", 800.0))
                fertilizer = float(data.get("fertilizer", 60000.0))
                pesticide = float(data.get("pesticide", 250.0))
                focus_crop = data.get("crop", None)

                advisory = opt_engine.generate_full_advisory(
                    state=state, season=season, area=area,
                    annual_rainfall=rainfall, fertilizer=fertilizer,
                    pesticide=pesticide, primary_crop=focus_crop
                )

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(advisory).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence default request logging for cleaner terminal output
        return


def start_server(port: int = 8000):
    global opt_engine
    print("[*] Initializing CropOptimizer engine...", flush=True)
    opt_engine = CropOptimizer()
    
    server_address = ("", port)
    try:
        httpd = HTTPServer(server_address, DashboardHandler)
    except OSError as e:
        if e.errno == 10048 or "Address already in use" in str(e):
            port = 8080
            server_address = ("", port)
            httpd = HTTPServer(server_address, DashboardHandler)
        else:
            raise e

    print("=" * 75, flush=True)
    print(f"  * CropYield AI Optimizer Dashboard running live at: http://localhost:{port}", flush=True)
    print(f"    Open your web browser at: http://localhost:{port}", flush=True)
    print("=" * 75, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down dashboard server.", flush=True)
        httpd.server_close()


if __name__ == "__main__":
    port_num = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_server(port_num)
