"""
AuditAI Pro - Sample Data Generator
Generates benchmark realistic datasets for SaaS, E-Commerce, and B2B Agency business models.
Uses Python standard library (csv, json) for high speed and zero DLL dependencies.
"""

import os
import csv
import json

def get_sample_saas_data() -> dict:
    """Returns sample 12-month data for a growing B2B SaaS company."""
    return {
        "company_name": "CloudScale Systems",
        "business_model": "b2b_saas",
        "stage": "Seed to Series A",
        "team_size": 14,
        "monthly_records": [
            {"month": "Jan", "revenue": 45000, "new_leads": 1200, "mql": 420, "sql": 110, "deals_won": 18, "avg_contract_value": 2500, "sales_cycle_days": 52, "cac": 1450, "ltv": 4200, "churn_rate_pct": 4.5, "ad_spend": 12000, "organic_pct": 35, "paid_pct": 50, "referral_pct": 15},
            {"month": "Feb", "revenue": 48200, "new_leads": 1280, "mql": 440, "sql": 115, "deals_won": 19, "avg_contract_value": 2530, "sales_cycle_days": 50, "cac": 1420, "ltv": 4250, "churn_rate_pct": 4.3, "ad_spend": 12500, "organic_pct": 36, "paid_pct": 49, "referral_pct": 15},
            {"month": "Mar", "revenue": 52100, "new_leads": 1390, "mql": 480, "sql": 122, "deals_won": 21, "avg_contract_value": 2480, "sales_cycle_days": 49, "cac": 1390, "ltv": 4300, "churn_rate_pct": 4.2, "ad_spend": 13000, "organic_pct": 38, "paid_pct": 47, "referral_pct": 15},
            {"month": "Apr", "revenue": 55800, "new_leads": 1450, "mql": 510, "sql": 130, "deals_won": 22, "avg_contract_value": 2540, "sales_cycle_days": 48, "cac": 1370, "ltv": 4350, "churn_rate_pct": 4.1, "ad_spend": 13500, "organic_pct": 39, "paid_pct": 46, "referral_pct": 15},
            {"month": "May", "revenue": 60400, "new_leads": 1560, "mql": 540, "sql": 138, "deals_won": 24, "avg_contract_value": 2510, "sales_cycle_days": 47, "cac": 1350, "ltv": 4400, "churn_rate_pct": 3.9, "ad_spend": 14200, "organic_pct": 40, "paid_pct": 45, "referral_pct": 15},
            {"month": "Jun", "revenue": 65100, "new_leads": 1640, "mql": 570, "sql": 145, "deals_won": 25, "avg_contract_value": 2600, "sales_cycle_days": 46, "cac": 1340, "ltv": 4450, "churn_rate_pct": 3.8, "ad_spend": 15000, "organic_pct": 41, "paid_pct": 44, "referral_pct": 15},
            {"month": "Jul", "revenue": 69900, "new_leads": 1720, "mql": 600, "sql": 150, "deals_won": 27, "avg_contract_value": 2590, "sales_cycle_days": 45, "cac": 1320, "ltv": 4500, "churn_rate_pct": 3.7, "ad_spend": 15500, "organic_pct": 42, "paid_pct": 43, "referral_pct": 15},
            {"month": "Aug", "revenue": 74500, "new_leads": 1810, "mql": 630, "sql": 158, "deals_won": 29, "avg_contract_value": 2570, "sales_cycle_days": 44, "cac": 1300, "ltv": 4550, "churn_rate_pct": 3.6, "ad_spend": 16200, "organic_pct": 43, "paid_pct": 42, "referral_pct": 15},
            {"month": "Sep", "revenue": 79800, "new_leads": 1920, "mql": 660, "sql": 165, "deals_won": 31, "avg_contract_value": 2570, "sales_cycle_days": 43, "cac": 1280, "ltv": 4600, "churn_rate_pct": 3.5, "ad_spend": 17000, "organic_pct": 44, "paid_pct": 41, "referral_pct": 15},
            {"month": "Oct", "revenue": 85400, "new_leads": 2040, "mql": 700, "sql": 175, "deals_won": 33, "avg_contract_value": 2590, "sales_cycle_days": 42, "cac": 1260, "ltv": 4650, "churn_rate_pct": 3.4, "ad_spend": 17800, "organic_pct": 45, "paid_pct": 40, "referral_pct": 15},
            {"month": "Nov", "revenue": 91800, "new_leads": 2180, "mql": 750, "sql": 185, "deals_won": 35, "avg_contract_value": 2620, "sales_cycle_days": 41, "cac": 1240, "ltv": 4700, "churn_rate_pct": 3.3, "ad_spend": 18600, "organic_pct": 46, "paid_pct": 39, "referral_pct": 15},
            {"month": "Dec", "revenue": 98500, "new_leads": 2300, "mql": 790, "sql": 195, "deals_won": 38, "avg_contract_value": 2590, "sales_cycle_days": 40, "cac": 1210, "ltv": 4800, "churn_rate_pct": 3.2, "ad_spend": 19500, "organic_pct": 47, "paid_pct": 38, "referral_pct": 15}
        ],
        "current_stack": ["Google Sheets", "Mailchimp", "Basic Stripe Checkout", "Slack"],
        "target_growth_rate": "50% ARR Uplift in 6 Months"
    }

def get_sample_ecommerce_data() -> dict:
    """Returns sample 12-month data for a Direct-to-Consumer (D2C) E-commerce brand."""
    return {
        "company_name": "NovaGlow Organics",
        "business_model": "ecommerce_d2c",
        "stage": "Growth Stage",
        "team_size": 8,
        "monthly_records": [
            {"month": "Jan", "revenue": 82000, "visitors": 65000, "add_to_cart": 4550, "checkouts": 2100, "orders": 1205, "aov": 68.0, "cac": 38.0, "ltv": 92.0, "repeat_rate_pct": 16.5, "ad_spend": 32000, "roas": 2.56, "refund_pct": 3.2},
            {"month": "Feb", "revenue": 86500, "visitors": 68000, "add_to_cart": 4800, "checkouts": 2220, "orders": 1270, "aov": 68.1, "cac": 38.5, "ltv": 93.0, "repeat_rate_pct": 17.0, "ad_spend": 33500, "roas": 2.58, "refund_pct": 3.1},
            {"month": "Mar", "revenue": 94000, "visitors": 74000, "add_to_cart": 5250, "checkouts": 2410, "orders": 1380, "aov": 68.1, "cac": 39.0, "ltv": 94.0, "repeat_rate_pct": 17.2, "ad_spend": 37000, "roas": 2.54, "refund_pct": 3.3},
            {"month": "Apr", "revenue": 99500, "visitors": 78000, "add_to_cart": 5580, "checkouts": 2550, "orders": 1460, "aov": 68.2, "cac": 39.5, "ltv": 95.0, "repeat_rate_pct": 17.8, "ad_spend": 39500, "roas": 2.52, "refund_pct": 3.0},
            {"month": "May", "revenue": 108000, "visitors": 85000, "add_to_cart": 6120, "checkouts": 2800, "orders": 1580, "aov": 68.4, "cac": 40.0, "ltv": 96.0, "repeat_rate_pct": 18.1, "ad_spend": 43500, "roas": 2.48, "refund_pct": 2.9},
            {"month": "Jun", "revenue": 115000, "visitors": 91000, "add_to_cart": 6550, "checkouts": 2980, "orders": 1680, "aov": 68.5, "cac": 40.5, "ltv": 97.0, "repeat_rate_pct": 18.5, "ad_spend": 47000, "roas": 2.45, "refund_pct": 3.0},
            {"month": "Jul", "revenue": 121000, "visitors": 96000, "add_to_cart": 6900, "checkouts": 3150, "orders": 1765, "aov": 68.6, "cac": 41.2, "ltv": 98.0, "repeat_rate_pct": 18.9, "ad_spend": 50000, "roas": 2.42, "refund_pct": 3.1},
            {"month": "Aug", "revenue": 128500, "visitors": 102000, "add_to_cart": 7350, "checkouts": 3350, "orders": 1870, "aov": 68.7, "cac": 41.5, "ltv": 99.0, "repeat_rate_pct": 19.2, "ad_spend": 53500, "roas": 2.40, "refund_pct": 2.8},
            {"month": "Sep", "revenue": 136000, "visitors": 108000, "add_to_cart": 7800, "checkouts": 3550, "orders": 1980, "aov": 68.7, "cac": 42.0, "ltv": 101.0, "repeat_rate_pct": 19.8, "ad_spend": 57000, "roas": 2.39, "refund_pct": 2.7},
            {"month": "Oct", "revenue": 145000, "visitors": 116000, "add_to_cart": 8400, "checkouts": 3800, "orders": 2110, "aov": 68.7, "cac": 42.8, "ltv": 103.0, "repeat_rate_pct": 20.2, "ad_spend": 62000, "roas": 2.34, "refund_pct": 2.9},
            {"month": "Nov", "revenue": 182000, "visitors": 148000, "add_to_cart": 11100, "checkouts": 5100, "orders": 2650, "aov": 68.7, "cac": 44.0, "ltv": 106.0, "repeat_rate_pct": 21.0, "ad_spend": 80000, "roas": 2.28, "refund_pct": 3.4},
            {"month": "Dec", "revenue": 215000, "visitors": 172000, "add_to_cart": 13200, "checkouts": 6200, "orders": 3120, "aov": 68.9, "cac": 45.5, "ltv": 109.0, "repeat_rate_pct": 21.5, "ad_spend": 98000, "roas": 2.19, "refund_pct": 3.5}
        ],
        "current_stack": ["Shopify Basic", "Meta Ads Manager", "Generic Email Blasts", "Manual Excel Inventory"],
        "target_growth_rate": "Scale to $3.5M ARR with higher repeat LTV"
    }

def get_sample_agency_data() -> dict:
    """Returns sample 12-month data for a High-Ticket B2B Agency / Professional Services firm."""
    return {
        "company_name": "Apex Growth Advisory",
        "business_model": "b2b_agency",
        "stage": "Bootstrapped Scaling",
        "team_size": 11,
        "monthly_records": [
            {"month": "Jan", "revenue": 48000, "inquiries": 75, "discovery_calls": 32, "proposals_sent": 14, "deals_won": 4, "avg_deal_size": 12000, "sales_cycle_days": 58, "cac": 2800, "ltv": 36000, "churn_rate_pct": 5.0, "ad_spend": 4500, "referral_pct": 45, "cold_outbound_pct": 30, "inbound_pct": 25},
            {"month": "Feb", "revenue": 52000, "inquiries": 80, "discovery_calls": 35, "proposals_sent": 15, "deals_won": 4, "avg_deal_size": 13000, "sales_cycle_days": 56, "cac": 2750, "ltv": 37000, "churn_rate_pct": 4.8, "ad_spend": 4600, "referral_pct": 45, "cold_outbound_pct": 30, "inbound_pct": 25},
            {"month": "Mar", "revenue": 60000, "inquiries": 92, "discovery_calls": 40, "proposals_sent": 18, "deals_won": 5, "avg_deal_size": 12000, "sales_cycle_days": 55, "cac": 2650, "ltv": 37500, "churn_rate_pct": 4.6, "ad_spend": 5000, "referral_pct": 44, "cold_outbound_pct": 31, "inbound_pct": 25},
            {"month": "Apr", "revenue": 62500, "inquiries": 95, "discovery_calls": 42, "proposals_sent": 19, "deals_won": 5, "avg_deal_size": 12500, "sales_cycle_days": 53, "cac": 2600, "ltv": 38000, "churn_rate_pct": 4.5, "ad_spend": 5200, "referral_pct": 44, "cold_outbound_pct": 31, "inbound_pct": 25},
            {"month": "May", "revenue": 72000, "inquiries": 108, "discovery_calls": 48, "proposals_sent": 22, "deals_won": 6, "avg_deal_size": 12000, "sales_cycle_days": 52, "cac": 2500, "ltv": 38500, "churn_rate_pct": 4.2, "ad_spend": 5800, "referral_pct": 43, "cold_outbound_pct": 32, "inbound_pct": 25},
            {"month": "Jun", "revenue": 75000, "inquiries": 112, "discovery_calls": 50, "proposals_sent": 23, "deals_won": 6, "avg_deal_size": 12500, "sales_cycle_days": 50, "cac": 2450, "ltv": 39000, "churn_rate_pct": 4.0, "ad_spend": 6000, "referral_pct": 42, "cold_outbound_pct": 33, "inbound_pct": 25},
            {"month": "Jul", "revenue": 84000, "inquiries": 125, "discovery_calls": 56, "proposals_sent": 25, "deals_won": 7, "avg_deal_size": 12000, "sales_cycle_days": 48, "cac": 2400, "ltv": 40000, "churn_rate_pct": 3.8, "ad_spend": 6500, "referral_pct": 42, "cold_outbound_pct": 33, "inbound_pct": 25},
            {"month": "Aug", "revenue": 87500, "inquiries": 130, "discovery_calls": 58, "proposals_sent": 26, "deals_won": 7, "avg_deal_size": 12500, "sales_cycle_days": 47, "cac": 2350, "ltv": 41000, "churn_rate_pct": 3.7, "ad_spend": 6800, "referral_pct": 41, "cold_outbound_pct": 34, "inbound_pct": 25},
            {"month": "Sep", "revenue": 96000, "inquiries": 142, "discovery_calls": 64, "proposals_sent": 29, "deals_won": 8, "avg_deal_size": 12000, "sales_cycle_days": 45, "cac": 2300, "ltv": 41500, "churn_rate_pct": 3.5, "ad_spend": 7200, "referral_pct": 40, "cold_outbound_pct": 35, "inbound_pct": 25},
            {"month": "Oct", "revenue": 100000, "inquiries": 148, "discovery_calls": 67, "proposals_sent": 30, "deals_won": 8, "avg_deal_size": 12500, "sales_cycle_days": 44, "cac": 2250, "ltv": 42000, "churn_rate_pct": 3.4, "ad_spend": 7500, "referral_pct": 40, "cold_outbound_pct": 35, "inbound_pct": 25},
            {"month": "Nov", "revenue": 112500, "inquiries": 165, "discovery_calls": 75, "proposals_sent": 34, "deals_won": 9, "avg_deal_size": 12500, "sales_cycle_days": 42, "cac": 2200, "ltv": 43000, "churn_rate_pct": 3.2, "ad_spend": 8200, "referral_pct": 39, "cold_outbound_pct": 36, "inbound_pct": 25},
            {"month": "Dec", "revenue": 125000, "inquiries": 180, "discovery_calls": 82, "proposals_sent": 37, "deals_won": 10, "avg_deal_size": 12500, "sales_cycle_days": 40, "cac": 2150, "ltv": 44000, "churn_rate_pct": 3.0, "ad_spend": 9000, "referral_pct": 38, "cold_outbound_pct": 37, "inbound_pct": 25}
        ],
        "current_stack": ["Notion", "Calendly Free", "Manual Gmail Follow-ups", "DocuSign", "QuickBooks Simple Start"],
        "target_growth_rate": "Automate outbound & reach $2.5M run-rate"
    }

def export_sample_csvs(dest_dir: str):
    """Exports demo CSVs so users can test file upload directly."""
    os.makedirs(dest_dir, exist_ok=True)
    datasets = {
        "saas_cloudscale_sample.csv": get_sample_saas_data()["monthly_records"],
        "ecommerce_novaglow_sample.csv": get_sample_ecommerce_data()["monthly_records"],
        "agency_apex_sample.csv": get_sample_agency_data()["monthly_records"],
    }
    for filename, records in datasets.items():
        if not records:
            continue
        filepath = os.path.join(dest_dir, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
