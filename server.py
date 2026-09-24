"""
AuditAI Pro - FastAPI Backend Application
High-performance API serving company audit analytics, sales growth intelligence, software recommendations, and AI copilot.
"""

import os
import io
import json
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv

from audit_engine import AuditEngine
from growth_advisor import GrowthAdvisor
from software_recommender import SoftwareRecommender, SOFTWARE_CATALOG
from sample_data import get_sample_saas_data, get_sample_ecommerce_data, get_sample_agency_data, export_sample_csvs
from ai_agent import AIAuditAdvisor

app = FastAPI(
    title="AuditAI Pro - Enterprise Sales Audit & AI Growth Engine",
    description="Full-stack AI software that analyzes sales reports, audits company commercial health, guarantees sales increase advice, and recommends optimal software stacks for growing companies.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
SAMPLES_DIR = os.path.join(BASE_DIR, "sample_exports")

# Ensure static and sample directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)
export_sample_csvs(SAMPLES_DIR)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# In-memory session store for current active audit
CURRENT_SESSION: Dict[str, Any] = {}

def initialize_default_session():
    """Sets up default SaaS audit state on startup."""
    default_data = get_sample_saas_data()
    engine = AuditEngine(business_model=default_data["business_model"], company_name=default_data["company_name"])
    audit_res = engine.analyze(default_data["monthly_records"], current_stack=default_data["current_stack"])
    advisor = GrowthAdvisor(audit_res)
    growth_res = advisor.generate_growth_plan()
    recommender = SoftwareRecommender(audit_res)
    sw_res = recommender.get_recommendations()
    ai_agent = AIAuditAdvisor()
    memo = ai_agent.generate_executive_audit_memo(audit_res, growth_res)

    CURRENT_SESSION["audit"] = audit_res
    CURRENT_SESSION["growth"] = growth_res
    CURRENT_SESSION["software"] = sw_res
    CURRENT_SESSION["memo"] = memo
    CURRENT_SESSION["ai_agent"] = ai_agent

initialize_default_session()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>AuditAI Pro is initializing... Please refresh shortly.</h1>")

@app.get("/api/current-audit")
async def get_current_audit():
    """Returns the current active audit, growth projections, and recommendations."""
    if not CURRENT_SESSION.get("audit"):
        initialize_default_session()
    return {
        "audit": CURRENT_SESSION["audit"],
        "growth": CURRENT_SESSION["growth"],
        "software": CURRENT_SESSION["software"],
        "memo": CURRENT_SESSION.get("memo", "")
    }

@app.get("/api/sample-datasets")
async def list_sample_datasets():
    """Returns pre-configured demo datasets."""
    return [
        {
            "id": "saas",
            "name": "CloudScale Systems (B2B SaaS)",
            "description": "$85k MRR, fast growing with qualification leaks and 4.2% monthly churn.",
            "business_model": "b2b_saas",
            "benchmark_arr": "$1,182,000"
        },
        {
            "id": "ecommerce",
            "name": "NovaGlow Organics (D2C Brand)",
            "description": "$145k monthly sales, high cart abandonment, and low repeat purchase LTV.",
            "business_model": "ecommerce_d2c",
            "benchmark_arr": "$2,580,000"
        },
        {
            "id": "agency",
            "name": "Apex Growth Advisory (High-Ticket Agency)",
            "description": "$96k monthly revenue, high deal value ($12.5k) but proposal delay bottleneck.",
            "business_model": "b2b_agency",
            "benchmark_arr": "$1,500,000"
        }
    ]

@app.post("/api/audit/load-sample/{dataset_id}")
async def load_sample_dataset(dataset_id: str):
    """Loads a benchmark industry dataset and executes the audit pipeline."""
    if dataset_id == "saas":
        raw_data = get_sample_saas_data()
    elif dataset_id == "ecommerce":
        raw_data = get_sample_ecommerce_data()
    elif dataset_id == "agency":
        raw_data = get_sample_agency_data()
    else:
        raise HTTPException(status_code=400, detail="Invalid sample dataset ID")

    engine = AuditEngine(business_model=raw_data["business_model"], company_name=raw_data["company_name"])
    audit_res = engine.analyze(raw_data["monthly_records"], current_stack=raw_data.get("current_stack", []))
    advisor = GrowthAdvisor(audit_res)
    growth_res = advisor.generate_growth_plan()
    recommender = SoftwareRecommender(audit_res)
    sw_res = recommender.get_recommendations()

    ai_agent = CURRENT_SESSION.get("ai_agent") or AIAuditAdvisor()
    memo = ai_agent.generate_executive_audit_memo(audit_res, growth_res)

    CURRENT_SESSION["audit"] = audit_res
    CURRENT_SESSION["growth"] = growth_res
    CURRENT_SESSION["software"] = sw_res
    CURRENT_SESSION["memo"] = memo

    return {
        "status": "success",
        "audit": audit_res,
        "growth": growth_res,
        "software": sw_res,
        "memo": memo
    }

@app.post("/api/audit/upload")
async def upload_sales_report(
    file: UploadFile = File(...),
    company_name: str = Form("Uploaded Venture"),
    business_model: str = Form("b2b_saas"),
    current_stack: str = Form("Google Sheets, Email")
):
    """Uploads CSV, Excel, or JSON sales reports and runs diagnostic audit."""
    contents = await file.read()
    filename = file.filename.lower()

    records = []
    try:
        if filename.endswith(".csv"):
            text = contents.decode("utf-8", errors="ignore")
            reader = csv.DictReader(io.StringIO(text))
            raw_rows = list(reader)
        elif filename.endswith(".json"):
            data = json.loads(contents.decode("utf-8"))
            if isinstance(data, list):
                raw_rows = data
            elif isinstance(data, dict) and "monthly_records" in data:
                raw_rows = data["monthly_records"]
            else:
                raw_rows = [data]
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or JSON.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if not raw_rows:
        raise HTTPException(status_code=400, detail="Uploaded file contains no data rows.")

    for i, row in enumerate(raw_rows):
        cleaned_row = {}
        for k, v in row.items():
            k_clean = str(k).strip().lower().replace(" ", "_").replace("-", "_")
            try:
                num_v = float(str(v).replace("$", "").replace(",", "").replace("%", "").strip())
            except (ValueError, TypeError):
                num_v = str(v).strip()

            if k_clean in ["month", "date", "period"]:
                cleaned_row["month"] = str(v).strip()
            elif k_clean in ["revenue", "sales", "mrr", "total_sales", "income"]:
                cleaned_row["revenue"] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["leads", "new_leads", "inquiries", "visitors", "traffic"]:
                field_key = "new_leads" if business_model == "b2b_saas" else ("visitors" if business_model == "ecommerce_d2c" else "inquiries")
                cleaned_row[field_key] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["mql", "marketing_qualified_leads", "add_to_cart", "cart_adds", "discovery_calls"]:
                field_key = "mql" if business_model == "b2b_saas" else ("add_to_cart" if business_model == "ecommerce_d2c" else "discovery_calls")
                cleaned_row[field_key] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["sql", "sales_qualified_leads", "checkouts", "proposals", "proposals_sent"]:
                field_key = "sql" if business_model == "b2b_saas" else ("checkouts" if business_model == "ecommerce_d2c" else "proposals_sent")
                cleaned_row[field_key] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["deals", "deals_won", "orders", "customers", "closed_won"]:
                field_key = "orders" if business_model == "ecommerce_d2c" else "deals_won"
                cleaned_row[field_key] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["cac", "acquisition_cost", "cpa"]:
                cleaned_row["cac"] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["ltv", "clv", "lifetime_value"]:
                cleaned_row["ltv"] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["churn", "churn_rate", "churn_rate_pct"]:
                cleaned_row["churn_rate_pct"] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["ad_spend", "marketing_spend", "spend"]:
                cleaned_row["ad_spend"] = float(num_v) if isinstance(num_v, (int, float)) else 0.0
            elif k_clean in ["sales_cycle", "sales_cycle_days", "days_to_close"]:
                cleaned_row["sales_cycle_days"] = float(num_v) if isinstance(num_v, (int, float)) else 45.0
            else:
                cleaned_row[k_clean] = num_v

        if "month" not in cleaned_row:
            cleaned_row["month"] = f"M{i+1}"
        if "revenue" not in cleaned_row:
            raise HTTPException(status_code=400, detail="Sales report must contain a 'revenue' or 'sales' column.")

        records.append(cleaned_row)

    stack_list = [s.strip() for s in current_stack.split(",") if s.strip()]

    engine = AuditEngine(business_model=business_model, company_name=company_name)
    audit_res = engine.analyze(records, current_stack=stack_list)
    advisor = GrowthAdvisor(audit_res)
    growth_res = advisor.generate_growth_plan()
    recommender = SoftwareRecommender(audit_res)
    sw_res = recommender.get_recommendations()

    ai_agent = CURRENT_SESSION.get("ai_agent") or AIAuditAdvisor()
    memo = ai_agent.generate_executive_audit_memo(audit_res, growth_res)

    CURRENT_SESSION["audit"] = audit_res
    CURRENT_SESSION["growth"] = growth_res
    CURRENT_SESSION["software"] = sw_res
    CURRENT_SESSION["memo"] = memo

    return {
        "status": "success",
        "audit": audit_res,
        "growth": growth_res,
        "software": sw_res,
        "memo": memo
    }

class SimRequest(BaseModel):
    conversion_lift_pct: float = 0.0
    churn_reduction_pct: float = 0.0
    price_lift_pct: float = 0.0

@app.post("/api/simulate")
async def run_simulation(req: SimRequest):
    """Calculates live interactive sales uplift based on slider changes."""
    audit = CURRENT_SESSION.get("audit")
    if not audit:
        initialize_default_session()
        audit = CURRENT_SESSION["audit"]

    advisor = GrowthAdvisor(audit)
    sim_res = advisor.simulate(
        conv_lift_pct=req.conversion_lift_pct,
        churn_reduction_pct=req.churn_reduction_pct,
        price_lift_pct=req.price_lift_pct
    )
    return sim_res

class ChatRequest(BaseModel):
    message: str
    api_key: Optional[str] = None

@app.post("/api/ai/chat")
async def chat_with_copilot(req: ChatRequest):
    """Interactively brainstorms with the AI growth advisor in the context of the audit."""
    audit = CURRENT_SESSION.get("audit")
    growth = CURRENT_SESSION.get("growth")

    if not audit:
        initialize_default_session()
        audit = CURRENT_SESSION["audit"]
        growth = CURRENT_SESSION["growth"]

    agent = AIAuditAdvisor(api_key=req.api_key)
    reply = agent.ask_copilot(req.message, audit, growth)
    return {"reply": reply}

@app.get("/api/download-demo-csv/{dataset_id}")
async def download_demo_csv(dataset_id: str):
    """Allows users to download realistic sample CSVs to test the upload feature."""
    filename_map = {
        "saas": "saas_cloudscale_sample.csv",
        "ecommerce": "ecommerce_novaglow_sample.csv",
        "agency": "agency_apex_sample.csv"
    }
    filename = filename_map.get(dataset_id, "saas_cloudscale_sample.csv")
    filepath = os.path.join(SAMPLES_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename, media_type="text/csv")
    raise HTTPException(status_code=404, detail="Demo file not found")

@app.get("/api/export-report", response_class=HTMLResponse)
async def export_printable_report():
    """Generates an executive, printable HTML report of the full audit & growth blueprint."""
    audit = CURRENT_SESSION.get("audit")
    growth = CURRENT_SESSION.get("growth")
    software = CURRENT_SESSION.get("software", [])
    memo = CURRENT_SESSION.get("memo", "")

    if not audit:
        initialize_default_session()
        audit = CURRENT_SESSION["audit"]
        growth = CURRENT_SESSION["growth"]
        software = CURRENT_SESSION["software"]
        memo = CURRENT_SESSION.get("memo", "")

    fin = audit["financial_summary"]
    unit = audit["unit_economics"]
    projections = growth["projections"]

    bottlenecks_html = "".join([
        f"""
        <div style="background:#fff;border-left:4px solid #ef4444;padding:16px;margin-bottom:12px;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <strong style="color:#111827;font-size:15px;">{b['title']}</strong>
                <span style="background:#fee2e2;color:#991b1b;padding:2px 8px;border-radius:12px;font-size:12px;font-weight:bold;">Monthly Impact: -${b.get('impact_monthly_dollars', 0):,.2f}</span>
            </div>
            <p style="color:#4b5563;font-size:13px;margin:4px 0;"><strong>Diagnosis:</strong> {b['diagnosis']}</p>
            <p style="color:#059669;font-size:13px;margin:4px 0;"><strong>AI Remediation:</strong> {b['ai_recommendation']}</p>
        </div>
        """
        for b in audit.get("bottlenecks", [])
    ])

    software_html = "".join([
        f"""
        <div style="border:1px solid #e5e7eb;padding:14px;border-radius:8px;margin-bottom:10px;background:#f9fafb;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <h4 style="margin:0;color:#111827;font-size:15px;">{sw['name']} <span style="font-size:12px;color:#6b7280;font-weight:normal;">({sw['category']})</span></h4>
                <span style="background:#dbeafe;color:#1e40af;font-weight:bold;padding:2px 8px;border-radius:12px;font-size:12px;">Fit Score: {sw.get('fit_score')}%</span>
            </div>
            <p style="margin:6px 0;font-size:13px;color:#374151;">{sw['tagline']}</p>
            <div style="font-size:12px;color:#4b5563;margin-top:6px;">
                <strong>Startup Pricing:</strong> {sw['startup_pricing']} | <strong>Expected ROI:</strong> {sw['roi_multiplier']} | <strong>Setup:</strong> {sw['setup_time']}
            </div>
        </div>
        """
        for sw in software[:6]
    ])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AuditAI Pro - Official Business Audit & Sales Growth Report</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #1f2937; margin: 0; padding: 40px; background: #fff; }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e5e7eb; padding-bottom: 20px; margin-bottom: 25px; }}
            .badge-score {{ font-size: 32px; font-weight: 800; color: #2563eb; }}
            .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }}
            .kpi-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }}
            .kpi-val {{ font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 4px; }}
            .kpi-label {{ font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.5px; }}
            h2 {{ color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-top: 35px; }}
            .print-btn {{ background: #2563eb; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; }}
            @media print {{ .no-print {{ display: none; }} body {{ padding: 0; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1 style="margin:0;color:#0f172a;font-size:26px;">AuditAI Pro™ Commercial Audit & Growth Report</h1>
                    <p style="margin:4px 0;color:#64748b;font-size:14px;">Target Entity: <strong>{audit.get('company_name')}</strong> | Model: {audit.get('business_model').upper()}</p>
                </div>
                <div style="text-align:right;">
                    <div class="kpi-label">Commercial Health Score</div>
                    <div class="badge-score">{audit.get('overall_score')}/100</div>
                    <span style="font-size:13px;color:#10b981;font-weight:600;">{audit.get('grade')}</span>
                </div>
            </div>

            <div class="no-print" style="margin-bottom:20px;text-align:right;">
                <button class="print-btn" onclick="window.print()">🖨️ Print or Save as PDF</button>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Current ARR</div>
                    <div class="kpi-val">${fin.get('annual_run_rate_arr', 0):,.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Target ARR Potential</div>
                    <div class="kpi-val" style="color:#059669;">${projections.get('target', {}).get('projected_arr', 0):,.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">LTV to CAC Ratio</div>
                    <div class="kpi-val">{unit.get('ltv_cac_ratio')}x</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Sales Cycle</div>
                    <div class="kpi-val">{unit.get('sales_cycle_days')} Days</div>
                </div>
            </div>

            <h2>1. Executive Strategic Memo</h2>
            <div style="background:#f8fafc;padding:20px;border-radius:8px;border:1px solid #e2e8f0;white-space:pre-wrap;font-size:14px;color:#334155;">
{memo}
            </div>

            <h2>2. Identified Bottlenecks & Monthly Financial Bleed</h2>
            {bottlenecks_html}

            <h2>3. Recommended Modern Software Stack for Growing Companies</h2>
            {software_html}

            <div style="margin-top:40px;border-top:1px solid #e5e7eb;padding-top:15px;font-size:12px;color:#9ca3af;text-align:center;">
                Generated by AuditAI Pro | AI-Powered Enterprise Commercial Intelligence Platform
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

from billing import BillingManager, PLANS, ACTIVE_SUBSCRIPTION

@app.get("/api/billing/plans")
async def get_billing_plans():
    """Returns subscription plan tiers and current status."""
    return BillingManager.get_plans()

class CheckoutRequest(BaseModel):
    plan_id: str
    customer_email: Optional[str] = "customer@company.com"

@app.post("/api/billing/checkout")
async def create_checkout(req: CheckoutRequest):
    """Creates Stripe checkout session or instant test upgrade."""
    success_url = "http://localhost:8000/?checkout_success=true"
    cancel_url = "http://localhost:8000/?checkout_cancelled=true"
    try:
        res = BillingManager.create_checkout_session(
            plan_id=req.plan_id,
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=req.customer_email
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class SetTierRequest(BaseModel):
    tier: str
    agency_name: Optional[str] = None

@app.post("/api/billing/set-tier")
async def set_active_tier_endpoint(req: SetTierRequest):
    """Allows instant switching of tiers for demo and verification."""
    BillingManager.set_active_tier(req.tier, req.agency_name)
    return {"status": "success", "subscription": BillingManager.get_current_subscription()}

class WhiteLabelRequest(BaseModel):
    agency_name: str
    agency_logo_url: Optional[str] = ""

@app.post("/api/billing/whitelabel-config")
async def update_whitelabel_config(req: WhiteLabelRequest):
    """Updates custom agency branding for white-label reports."""
    BillingManager.set_active_tier(ACTIVE_SUBSCRIPTION["tier"], req.agency_name)
    ACTIVE_SUBSCRIPTION["agency_logo_url"] = req.agency_logo_url
    return {"status": "success", "subscription": BillingManager.get_current_subscription()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)

