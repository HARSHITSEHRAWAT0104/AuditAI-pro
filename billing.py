"""
AuditAI Pro - Subscription & Monetization Engine
Handles Stripe Checkout sessions, tiered subscription gating, and agency white-label licensing.
"""

import os
from typing import Dict, Any, Optional
import stripe

# Retrieve keys from environment or fallback to test/demo sandbox
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

PLANS = {
    "free": {
        "id": "free",
        "name": "Free Community Audit",
        "price_monthly": 0,
        "price_annual": 0,
        "features": [
            "1 Diagnostic Audit per month",
            "Commercial Health Score (0-100)",
            "Top 1 Pipeline Leak Preview",
            "Standard Industry Benchmark Comparison",
            "Community Support"
        ],
        "limits": {
            "unlimited_audits": False,
            "full_leaks": False,
            "ai_copilot": False,
            "white_label": False,
            "interactive_simulator": True
        }
    },
    "growth_pro": {
        "id": "growth_pro",
        "name": "Growth Pro",
        "price_monthly": 79,
        "price_annual": 690,
        "stripe_price_id": os.environ.get("STRIPE_PRICE_GROWTH_PRO", "price_growth_pro_placeholder"),
        "popular": True,
        "features": [
            "Unlimited Sales Report Audits (CSV & JSON)",
            "Full Pipeline Leaks with Exact Dollar Bleed",
            "Assured Sales Increase Models (Conservative, Target, Aggressive)",
            "30-60-90-180 Day Phased Growth Roadmap",
            "Curated Software Directory with Startup Discounts",
            "Unlimited AI Growth Copilot Strategy Chat",
            "Interactive Growth Simulator & Scenario Export",
            "Printable Board-Ready Executive Reports"
        ],
        "limits": {
            "unlimited_audits": True,
            "full_leaks": True,
            "ai_copilot": True,
            "white_label": False,
            "interactive_simulator": True
        }
    },
    "agency_whitelabel": {
        "id": "agency_whitelabel",
        "name": "Agency & Consultant White-Label",
        "price_monthly": 299,
        "price_annual": 2490,
        "stripe_price_id": os.environ.get("STRIPE_PRICE_AGENCY", "price_agency_placeholder"),
        "features": [
            "Everything in Growth Pro",
            "Custom Agency Branding (Upload Your Own Logo & Firm Name)",
            "Sell Audits to Clients for $1,500 - $5,000 Each",
            "Unbranded White-Label Executive Board Reports",
            "Multi-Client Dashboard Management",
            "Custom CSV Column Mapping Presets",
            "Dedicated Revenue Architect Priority Onboarding"
        ],
        "limits": {
            "unlimited_audits": True,
            "full_leaks": True,
            "ai_copilot": True,
            "white_label": True,
            "interactive_simulator": True
        }
    }
}

# In-memory subscription state (can be backed by SQLite or PostgreSQL in production)
ACTIVE_SUBSCRIPTION = {
    "tier": "growth_pro", # Default to Pro for local testing, or free
    "status": "active",
    "customer_email": "demo@venture.com",
    "agency_name": "Apex Advisory Group",
    "agency_logo_url": ""
}

class BillingManager:
    @staticmethod
    def get_plans() -> Dict[str, Any]:
        """Returns public plan definitions and active status."""
        return {
            "plans": PLANS,
            "active_tier": ACTIVE_SUBSCRIPTION["tier"],
            "has_stripe_configured": bool(STRIPE_SECRET_KEY)
        }

    @staticmethod
    def create_checkout_session(plan_id: str, success_url: str, cancel_url: str, customer_email: Optional[str] = None) -> Dict[str, Any]:
        """Creates a Stripe Checkout Session or returns simulated checkout link if no Stripe key is configured."""
        plan = PLANS.get(plan_id)
        if not plan:
            raise ValueError(f"Invalid plan ID: {plan_id}")

        # If real Stripe secret key is present
        if STRIPE_SECRET_KEY:
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[{
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"AuditAI Pro - {plan['name']}",
                                "description": f"Subscription to {plan['name']} tier",
                            },
                            "unit_amount": plan["price_monthly"] * 100,
                            "recurring": {"interval": "month"},
                        },
                        "quantity": 1,
                    }],
                    mode="subscription",
                    success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}&plan=" + plan_id,
                    cancel_url=cancel_url,
                    customer_email=customer_email
                )
                return {"checkout_url": session.url, "session_id": session.id, "mode": "stripe"}
            except Exception as e:
                print(f"[Billing] Stripe checkout session error: {e}")

        # Sandbox / Simulated Instant Upgrade (for instant testing & demo without requiring real card)
        ACTIVE_SUBSCRIPTION["tier"] = plan_id
        ACTIVE_SUBSCRIPTION["status"] = "active"
        if customer_email:
            ACTIVE_SUBSCRIPTION["customer_email"] = customer_email

        return {
            "checkout_url": f"{success_url}?simulated=true&plan={plan_id}",
            "session_id": f"sim_sess_{plan_id}_success",
            "mode": "simulated",
            "message": f"Successfully upgraded to {plan['name']} in test mode!"
        }

    @staticmethod
    def set_active_tier(tier: str, agency_name: Optional[str] = None):
        """Sets the active tier manually or after webhook."""
        if tier in PLANS:
            ACTIVE_SUBSCRIPTION["tier"] = tier
            if agency_name:
                ACTIVE_SUBSCRIPTION["agency_name"] = agency_name

    @staticmethod
    def get_current_subscription() -> Dict[str, Any]:
        return dict(ACTIVE_SUBSCRIPTION)
