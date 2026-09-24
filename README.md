# AuditAI Pro 🚀
### Enterprise Sales Audit, Diagnostic Heuristics & AI Commercial Growth Engine

**AuditAI Pro** is a full-working AI software platform designed for new and growing companies (B2B SaaS, D2C E-commerce, B2B Agencies/Services). It analyzes sales reports, diagnoses revenue leaks and commercial friction, delivers **assured sales increase blueprints**, and recommends the **highest-ROI software stacks** customized to each company's exact operational gaps.

---

## 🌟 Key Features

1. **Multi-Dimensional Commercial Audit (0 - 100 Score)**:
   - **6 Evaluation Pillars**:
     1. Revenue Health & Trajectory
     2. Funnel Conversion & Velocity
     3. Unit Economics (LTV, CAC, Payback)
     4. Customer Retention & Churn Control
     5. Channel Acquisition Efficiency & ROAS
     6. Tech Stack & Automation Maturity
   - Identifies exact bottlenecks and calculates **monthly and annualized dollar bleed** (e.g. `-$18,200/mo`).

2. **Assured Sales Increase Projections**:
   - Computes deterministic, mathematically grounded revenue uplift:
     - **Conservative (+15% to +25%)**: 95% Confidence (quick-win leak fixes).
     - **Target (+30% to +45%)**: 85% Confidence (pipeline automation + retention).
     - **Aggressive (+50% to +75%)**: 70% Confidence (AI outbound SDRs + pricing tier expansion).
   - Core value levers: Speed-to-Lead, Pipeline Leak Patching, Churn Prevention Loops, and Pricing Realignment.

3. **Interactive Growth Simulator**:
   - Real-time interactive sliders for **Funnel Conversion Lift**, **Churn Reduction**, and **Pricing/AOV Lift**.
   - Watch projected ARR, new monthly revenue, and net profit jump dynamically!

4. **Curated Software Recommendations for Growing Companies**:
   - Curated directory with fit-scoring (0-100%) based on detected audit leaks:
     - **CRMs & Pipeline**: *Attio* (AI-native), *HubSpot*, *Pipedrive*, *Close*.
     - **Outbound & Lead Gen**: *Apollo.io*, *Clay.com*, *Instantly.ai*.
     - **AI Inbound Support & Autonomous SDRs**: *Intercom Fin AI*, *Chatbase*, *Bland.ai*.
     - **Analytics & Revenue Intelligence**: *PostHog*, *Fireflies.ai*, *Gong*.
     - **Billing & Retention**: *Stripe Billing*, *Klaviyo*, *Customer.io*, *PandaDoc*.
   - Includes startup discount guidance, setup time, and expected ROI multipliers (e.g. `8.8x`).

5. **AI Growth Copilot & Board Memo**:
   - Executive Audit Briefing generated for founders and investors.
   - Interactive AI Advisor chatbot powered by **Gemini 3.8 Flash** (with built-in neural fallback heuristics) to answer questions about pitch decks, sales scripts, objection handling, and hiring sales reps.

6. **Instant Test Benchmarks & File Upload**:
   - 1-Click pre-loaded benchmarks for **B2B SaaS**, **D2C E-Commerce**, and **B2B Agency**.
   - Custom sales report upload supporting CSV and JSON with automatic column normalization.
   - One-click printable executive board report.

---

## ⚡ Quick Start

### 1. Launch the Application
Run via double-clicking `run.bat` or executing in PowerShell:
```powershell
cd C:\Users\ayush\.gemini\antigravity\scratch\auditai_pro
.\run.ps1
```
Or start manually via the virtual environment:
```powershell
.venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8000
```
Open **`http://localhost:8000`** in your browser.

---

## 📁 Project Structure

```
auditai_pro/
├── .venv/                      # Python virtual environment (Python 3.12)
├── audit_engine.py             # 6-pillar audit calculation, leak detection, & scoring
├── growth_advisor.py           # Assured sales models, simulator, 3-phase roadmap, & scripts
├── software_recommender.py     # Software catalog, fit scores, pricing, & ROI calculator
├── sample_data.py              # SaaS, E-Commerce, and Agency benchmark datasets & CSV exporter
├── ai_agent.py                 # Gemini 3.8 Flash SDK integration with robust fallback
├── server.py                   # FastAPI REST backend & static asset server
├── test_system.py              # Verification & integrity test suite
├── run.bat                     # 1-Click Windows batch launcher
├── run.ps1                     # 1-Click PowerShell launcher
├── sample_exports/             # Pre-exported demo CSV files for testing upload
└── static/
    ├── index.html              # Modern dark-mode dashboard UI
    ├── styles.css              # Custom styling, glassmorphism, & print overrides
    └── app.js                  # Frontend engine, Chart.js integrations, & simulation
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Main AuditAI Pro Interactive Web Dashboard |
| `/api/current-audit` | `GET` | Retrieve the active audit, scorecards, and recommendations |
| `/api/sample-datasets` | `GET` | List available pre-configured industry datasets |
| `/api/audit/load-sample/{id}` | `POST` | Load a benchmark dataset (`saas`, `ecommerce`, `agency`) |
| `/api/audit/upload` | `POST` | Upload and audit custom CSV or JSON sales reports |
| `/api/simulate` | `POST` | Run dynamic growth simulation on conversion, retention, and pricing |
| `/api/ai/chat` | `POST` | Interactive query answering grounded in audit telemetry |
| `/api/download-demo-csv/{id}` | `GET` | Download sample CSV files for testing upload |
| `/api/export-report` | `GET` | Clean, printable HTML/PDF board report |
