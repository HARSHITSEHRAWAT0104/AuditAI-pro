"""
AuditAI Pro - Core Audit Engine
Performs comprehensive business, sales, and funnel health audits for companies.
"""

from typing import List, Dict, Any, Optional
import math

class AuditEngine:
    def __init__(self, business_model: str = "b2b_saas", company_name: str = "Growing Venture"):
        self.business_model = business_model.lower()
        self.company_name = company_name

    def analyze(self, records: List[Dict[str, Any]], current_stack: Optional[List[str]] = None) -> Dict[str, Any]:
        """Runs the complete multi-dimensional sales & operations audit."""
        if not records:
            raise ValueError("No sales records provided for audit.")

        current_stack = current_stack or []
        n_months = len(records)

        # 1. Financial & Revenue Metrics
        revenues = [float(r.get("revenue", 0)) for r in records]
        total_revenue = sum(revenues)
        avg_monthly_rev = total_revenue / n_months if n_months else 0
        latest_rev = revenues[-1] if revenues else 0
        first_rev = revenues[0] if revenues else 1

        growth_pct = ((latest_rev - first_rev) / first_rev * 100) if first_rev > 0 else 0
        arr_run_rate = latest_rev * 12

        # 2. Unit Economics (CAC, LTV, Churn)
        cacs = [float(r.get("cac", 0)) for r in records if "cac" in r]
        ltvs = [float(r.get("ltv", 0)) for r in records if "ltv" in r]
        avg_cac = sum(cacs) / len(cacs) if cacs else 0
        avg_ltv = sum(ltvs) / len(ltvs) if ltvs else 0
        ltv_cac_ratio = (avg_ltv / avg_cac) if avg_cac > 0 else 0

        # Payback period (months)
        avg_deal_size = 0
        deal_sizes = [float(r.get("avg_contract_value", r.get("aov", r.get("avg_deal_size", 0)))) for r in records]
        if any(deal_sizes):
            avg_deal_size = sum(deal_sizes) / len(deal_sizes)

        # Churn or repeat rates
        churn_rates = [float(r.get("churn_rate_pct", 0)) for r in records if "churn_rate_pct" in r]
        repeat_rates = [float(r.get("repeat_rate_pct", 0)) for r in records if "repeat_rate_pct" in r]
        avg_churn = sum(churn_rates) / len(churn_rates) if churn_rates else 0
        avg_repeat = sum(repeat_rates) / len(repeat_rates) if repeat_rates else 0

        # Sales cycle length
        sales_cycles = [float(r.get("sales_cycle_days", 0)) for r in records if "sales_cycle_days" in r]
        avg_sales_cycle = sum(sales_cycles) / len(sales_cycles) if sales_cycles else 45

        # Ad Spend & ROAS
        ad_spends = [float(r.get("ad_spend", 0)) for r in records if "ad_spend" in r]
        total_ad_spend = sum(ad_spends)
        roas_values = [float(r.get("roas", 0)) for r in records if "roas" in r]
        avg_roas = sum(roas_values) / len(roas_values) if roas_values else (
            (total_revenue / total_ad_spend) if total_ad_spend > 0 else 0
        )

        # 3. Funnel Analysis & Leaks
        funnel_data = self._calculate_funnel(records)

        # 4. Multi-Factor Scoring (0 to 100)
        scores = self._calculate_audit_scores(
            growth_pct=growth_pct,
            ltv_cac_ratio=ltv_cac_ratio,
            avg_churn=avg_churn,
            avg_repeat=avg_repeat,
            funnel=funnel_data,
            avg_sales_cycle=avg_sales_cycle,
            current_stack=current_stack,
            avg_roas=avg_roas
        )

        overall_score = round(
            scores["revenue_health"] * 0.20 +
            scores["funnel_conversion"] * 0.20 +
            scores["unit_economics"] * 0.20 +
            scores["retention_health"] * 0.15 +
            scores["acquisition_efficiency"] * 0.15 +
            scores["tech_stack_maturity"] * 0.10,
            1
        )

        # Grade classification
        if overall_score >= 88:
            grade = "A+ (Elite Scaler)"
            health_status = "Exceptional"
            status_color = "emerald"
        elif overall_score >= 75:
            grade = "A- (Strong Foundation)"
            health_status = "Healthy with Growth Leaks"
            status_color = "blue"
        elif overall_score >= 60:
            grade = "B (Moderate Efficiency)"
            health_status = "Sub-Optimal / Margin Leakage"
            status_color = "amber"
        elif overall_score >= 45:
            grade = "C (High Friction)"
            health_status = "Urgent Optimization Required"
            status_color = "orange"
        else:
            grade = "D/F (Critical Burn)"
            health_status = "At-Risk / High Vulnerability"
            status_color = "rose"

        # 5. Bottlenecks & Value Leaks
        bottlenecks = self._identify_bottlenecks(
            funnel_data=funnel_data,
            ltv_cac_ratio=ltv_cac_ratio,
            avg_churn=avg_churn,
            avg_repeat=avg_repeat,
            avg_sales_cycle=avg_sales_cycle,
            avg_roas=avg_roas,
            current_stack=current_stack,
            latest_monthly_rev=latest_rev
        )

        return {
            "company_name": self.company_name,
            "business_model": self.business_model,
            "overall_score": overall_score,
            "grade": grade,
            "health_status": health_status,
            "status_color": status_color,
            "score_pillars": scores,
            "financial_summary": {
                "total_revenue": round(total_revenue, 2),
                "avg_monthly_revenue": round(avg_monthly_rev, 2),
                "latest_monthly_revenue": round(latest_rev, 2),
                "annual_run_rate_arr": round(arr_run_rate, 2),
                "period_growth_pct": round(growth_pct, 1),
                "avg_deal_size": round(avg_deal_size, 2),
                "total_ad_spend": round(total_ad_spend, 2),
                "avg_roas": round(avg_roas, 2)
            },
            "unit_economics": {
                "cac": round(avg_cac, 2),
                "ltv": round(avg_ltv, 2),
                "ltv_cac_ratio": round(ltv_cac_ratio, 2),
                "ltv_cac_rating": "Optimal (3.5x - 5x)" if ltv_cac_ratio >= 3.5 else ("Fair (2.5x - 3.5x)" if ltv_cac_ratio >= 2.5 else "Dangerous (< 2.5x)"),
                "avg_churn_pct": round(avg_churn, 2),
                "avg_repeat_pct": round(avg_repeat, 2),
                "sales_cycle_days": round(avg_sales_cycle, 1)
            },
            "funnel_metrics": funnel_data,
            "bottlenecks": bottlenecks,
            "monthly_history": records
        }

    def _calculate_funnel(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates stage-by-stage conversions across the pipeline."""
        if "new_leads" in records[0] or "mql" in records[0]:
            # B2B SaaS Funnel
            leads = sum(r.get("new_leads", 0) for r in records)
            mql = sum(r.get("mql", 0) for r in records)
            sql = sum(r.get("sql", 0) for r in records)
            deals = sum(r.get("deals_won", 0) for r in records)

            lead_to_mql = (mql / leads * 100) if leads else 0
            mql_to_sql = (sql / mql * 100) if mql else 0
            sql_to_deal = (deals / sql * 100) if sql else 0
            overall_conv = (deals / leads * 100) if leads else 0

            return {
                "type": "b2b_saas",
                "stages": [
                    {"name": "Total Leads", "count": leads, "pct_of_top": 100.0},
                    {"name": "Marketing Qualified (MQL)", "count": mql, "pct_of_top": round(lead_to_mql, 1), "conversion_from_prev": round(lead_to_mql, 1)},
                    {"name": "Sales Qualified (SQL)", "count": sql, "pct_of_top": round((sql / leads * 100) if leads else 0, 1), "conversion_from_prev": round(mql_to_sql, 1)},
                    {"name": "Deals Closed Won", "count": deals, "pct_of_top": round(overall_conv, 2), "conversion_from_prev": round(sql_to_deal, 1)}
                ],
                "lead_to_mql_pct": round(lead_to_mql, 1),
                "mql_to_sql_pct": round(mql_to_sql, 1),
                "sql_to_deal_pct": round(sql_to_deal, 1),
                "overall_conversion_pct": round(overall_conv, 2)
            }
        elif "visitors" in records[0] or "add_to_cart" in records[0]:
            # E-Commerce Funnel
            visitors = sum(r.get("visitors", 0) for r in records)
            adds = sum(r.get("add_to_cart", 0) for r in records)
            checkouts = sum(r.get("checkouts", 0) for r in records)
            orders = sum(r.get("orders", 0) for r in records)

            v_to_cart = (adds / visitors * 100) if visitors else 0
            cart_to_check = (checkouts / adds * 100) if adds else 0
            check_to_order = (orders / checkouts * 100) if checkouts else 0
            overall_conv = (orders / visitors * 100) if visitors else 0

            return {
                "type": "ecommerce",
                "stages": [
                    {"name": "Store Visitors", "count": visitors, "pct_of_top": 100.0},
                    {"name": "Added to Cart", "count": adds, "pct_of_top": round(v_to_cart, 1), "conversion_from_prev": round(v_to_cart, 1)},
                    {"name": "Checkouts Initiated", "count": checkouts, "pct_of_top": round((checkouts / visitors * 100) if visitors else 0, 1), "conversion_from_prev": round(cart_to_check, 1)},
                    {"name": "Completed Orders", "count": orders, "pct_of_top": round(overall_conv, 2), "conversion_from_prev": round(check_to_order, 1)}
                ],
                "visitor_to_cart_pct": round(v_to_cart, 1),
                "cart_to_checkout_pct": round(cart_to_check, 1),
                "checkout_to_order_pct": round(check_to_order, 1),
                "overall_conversion_pct": round(overall_conv, 2)
            }
        else:
            # Agency / Consultative Funnel
            inquiries = sum(r.get("inquiries", 0) for r in records)
            discovery = sum(r.get("discovery_calls", 0) for r in records)
            proposals = sum(r.get("proposals_sent", 0) for r in records)
            deals = sum(r.get("deals_won", 0) for r in records)

            inq_to_disc = (discovery / inquiries * 100) if inquiries else 0
            disc_to_prop = (proposals / discovery * 100) if discovery else 0
            prop_to_deal = (deals / proposals * 100) if proposals else 0
            overall_conv = (deals / inquiries * 100) if inquiries else 0

            return {
                "type": "agency",
                "stages": [
                    {"name": "Client Inquiries", "count": inquiries, "pct_of_top": 100.0},
                    {"name": "Discovery Calls", "count": discovery, "pct_of_top": round(inq_to_disc, 1), "conversion_from_prev": round(inq_to_disc, 1)},
                    {"name": "Proposals Sent", "count": proposals, "pct_of_top": round((proposals / inquiries * 100) if inquiries else 0, 1), "conversion_from_prev": round(disc_to_prop, 1)},
                    {"name": "Contracts Signed", "count": deals, "pct_of_top": round(overall_conv, 1), "conversion_from_prev": round(prop_to_deal, 1)}
                ],
                "inquiry_to_discovery_pct": round(inq_to_disc, 1),
                "discovery_to_proposal_pct": round(disc_to_prop, 1),
                "proposal_to_deal_pct": round(prop_to_deal, 1),
                "overall_conversion_pct": round(overall_conv, 1)
            }

    def _calculate_audit_scores(self, growth_pct: float, ltv_cac_ratio: float, avg_churn: float,
                                avg_repeat: float, funnel: Dict[str, Any], avg_sales_cycle: float,
                                current_stack: List[str], avg_roas: float) -> Dict[str, float]:
        """Scores 6 fundamental dimensions between 0 and 100."""
        # 1. Revenue Health (Growth % benchmark: 30%+ is 90+, 100%+ is 100)
        rev_score = min(100.0, max(30.0, 50.0 + (growth_pct * 0.5)))

        # 2. Funnel Conversion
        conv_pct = funnel.get("overall_conversion_pct", 1.5)
        if funnel.get("type") == "ecommerce":
            # 2.5%+ is elite
            funnel_score = min(100.0, (conv_pct / 2.5) * 85.0)
        elif funnel.get("type") == "b2b_saas":
            # 2.0%+ lead-to-close is elite
            funnel_score = min(100.0, (conv_pct / 2.0) * 85.0)
        else:
            # Agency: 6-10% inquiry to signed
            funnel_score = min(100.0, (conv_pct / 7.0) * 85.0)

        # 3. Unit Economics
        if ltv_cac_ratio >= 4.0:
            unit_score = 95.0
        elif ltv_cac_ratio >= 3.0:
            unit_score = 85.0
        elif ltv_cac_ratio >= 2.0:
            unit_score = 68.0
        elif ltv_cac_ratio >= 1.0:
            unit_score = 45.0
        else:
            unit_score = 30.0

        # 4. Retention Health
        if avg_churn > 0:
            # Lower churn is better (<2% monthly is elite)
            retention_score = max(20.0, 100.0 - (avg_churn * 12.0))
        elif avg_repeat > 0:
            # E-commerce repeat rate (>30% is elite)
            retention_score = min(100.0, max(35.0, (avg_repeat / 30.0) * 90.0))
        else:
            retention_score = 70.0

        # 5. Acquisition Efficiency & ROAS
        if avg_roas >= 3.5:
            acq_score = 95.0
        elif avg_roas >= 2.5:
            acq_score = 80.0
        elif avg_roas >= 1.8:
            acq_score = 65.0
        else:
            acq_score = 45.0

        # 6. Tech Stack & Automation
        # Evaluates presence of modern CRM, marketing automation, AI
        stack_str = " ".join([s.lower() for s in current_stack])
        tech_score = 50.0
        if any(w in stack_str for w in ["hubspot", "salesforce", "pipedrive", "attio", "close"]):
            tech_score += 20.0
        if any(w in stack_str for w in ["klaviyo", "customer.io", "apollo", "clay", "instantly"]):
            tech_score += 15.0
        if any(w in stack_str for w in ["ai", "gong", "posthog", "fireflies", "intercom"]):
            tech_score += 15.0
        tech_score = min(100.0, tech_score)

        return {
            "revenue_health": round(rev_score, 1),
            "funnel_conversion": round(funnel_score, 1),
            "unit_economics": round(unit_score, 1),
            "retention_health": round(retention_score, 1),
            "acquisition_efficiency": round(acq_score, 1),
            "tech_stack_maturity": round(tech_score, 1)
        }

    def _identify_bottlenecks(self, funnel_data: Dict[str, Any], ltv_cac_ratio: float,
                              avg_churn: float, avg_repeat: float, avg_sales_cycle: float,
                              avg_roas: float, current_stack: List[str],
                              latest_monthly_rev: float) -> List[Dict[str, Any]]:
        """Identifies high-impact leaks and calculated dollar loss."""
        leaks = []

        # Check Funnel Leaks
        f_type = funnel_data.get("type")
        if f_type == "b2b_saas":
            mql_sql = funnel_data.get("mql_to_sql_pct", 0)
            if mql_sql < 35:
                est_loss = latest_monthly_rev * 0.18
                leaks.append({
                    "id": "leak_mql_sql",
                    "severity": "CRITICAL",
                    "area": "Pipeline Qualification",
                    "title": f"MQL-to-SQL Conversion Drop-Off ({mql_sql}% vs 45% benchmark)",
                    "impact_monthly_dollars": round(est_loss, 2),
                    "diagnosis": "Marketing leads are stalling before becoming qualified sales opportunities. Likely cause is slow speed-to-lead (>30 mins) and absence of automated lead enrichment.",
                    "ai_recommendation": "Deploy instant AI lead qualification (Clay / Apollo) and automated calendar booking within 90 seconds of form submission."
                })

            sql_deal = funnel_data.get("sql_to_deal_pct", 0)
            if sql_deal < 25:
                est_loss = latest_monthly_rev * 0.22
                leaks.append({
                    "id": "leak_deal_close",
                    "severity": "HIGH",
                    "area": "Sales Closing Velocity",
                    "title": f"Opportunity-to-Close Win Rate ({sql_deal}% vs 28-35% benchmark)",
                    "impact_monthly_dollars": round(est_loss, 2),
                    "diagnosis": "Qualified opportunities are stalling in proposal or negotiation stages, losing momentum to competitor evaluation or internal indecision.",
                    "ai_recommendation": "Implement AI meeting intelligence (Gong or Fireflies) to diagnose objections and trigger automated executive multithreading."
                })

        elif f_type == "ecommerce":
            cart_check = funnel_data.get("cart_to_checkout_pct", 0)
            if cart_check < 50:
                est_loss = latest_monthly_rev * 0.25
                leaks.append({
                    "id": "leak_cart_abandonment",
                    "severity": "CRITICAL",
                    "area": "Cart & Checkout Abandonment",
                    "title": f"Severe Cart Drop-Off ({round(100 - cart_check, 1)}% abandon before checkout)",
                    "impact_monthly_dollars": round(est_loss, 2),
                    "diagnosis": "Shoppers add items to cart but abandon before initiating checkout due to hidden shipping charges, lack of 1-click Express Pay, or absence of instant exit-intent incentives.",
                    "ai_recommendation": "Activate 3-touch SMS + Email abandoned cart sequence within 15 minutes (Klaviyo) and enable Shop Pay / Apple Pay 1-click checkout."
                })

            if avg_repeat < 25:
                est_loss = latest_monthly_rev * 0.19
                leaks.append({
                    "id": "leak_repeat_ltv",
                    "severity": "HIGH",
                    "area": "Customer Retention & LTV",
                    "title": f"Low Repeat Purchase Rate ({avg_repeat}% vs 32% benchmark)",
                    "impact_monthly_dollars": round(est_loss, 2),
                    "diagnosis": "The company relies heavily on expensive first-time ad acquisition rather than extracting lifetime value from existing customers.",
                    "ai_recommendation": "Launch automated replenishment reminders, VIP loyalty tier, and post-purchase AI upsell flows."
                })

        elif f_type == "agency":
            disc_prop = funnel_data.get("discovery_to_proposal_pct", 0)
            prop_deal = funnel_data.get("proposal_to_deal_pct", 0)
            if prop_deal < 35:
                est_loss = latest_monthly_rev * 0.30
                leaks.append({
                    "id": "leak_agency_proposals",
                    "severity": "CRITICAL",
                    "area": "Proposal Win Rate",
                    "title": f"Proposal-to-Contract Stall ({prop_deal}% closed vs 45% benchmark)",
                    "impact_monthly_dollars": round(est_loss, 2),
                    "diagnosis": "Proposals take too long to send (lagging 3-7 days after discovery) and suffer from lack of interactive scope selection and auto-followup.",
                    "ai_recommendation": "Use dynamic proposal software (PandaDoc or Qwilr) with 24-hour turnaround and automated video walkthrough."
                })

        # Unit economics checks
        if ltv_cac_ratio < 3.0 and ltv_cac_ratio > 0:
            est_loss = latest_monthly_rev * 0.15
            leaks.append({
                "id": "leak_ltv_cac",
                "severity": "HIGH",
                "area": "Unit Economics",
                "title": f"Compressed LTV:CAC Ratio ({ltv_cac_ratio}x vs 3.5x-5.0x target)",
                "impact_monthly_dollars": round(est_loss, 2),
                "diagnosis": "Acquisition cost is eating too much of customer margin. Payback period exceeds healthy thresholds.",
                "ai_recommendation": "Diversify away from pure paid ads into high-intent organic search, referral engines, and outbound cold email infrastructure."
            })

        # Churn check
        if avg_churn >= 3.5:
            est_loss = latest_monthly_rev * 0.20
            leaks.append({
                "id": "leak_churn",
                "severity": "CRITICAL",
                "area": "Customer Retention",
                "title": f"Elevated Monthly Churn Rate ({avg_churn}% / month)",
                "impact_monthly_dollars": round(est_loss, 2),
                "diagnosis": "Annualized churn is eroding growth momentum. Compounding churn creates a 'leaky bucket' where new sales merely replace departing customers.",
                "ai_recommendation": "Implement automated onboarding triggers, customer health scoring, and predictive churn prevention alerts in CRM."
            })

        # Stack maturity check
        stack_str = " ".join([s.lower() for s in current_stack])
        if "sheets" in stack_str or "excel" in stack_str or len(current_stack) <= 3:
            est_loss = latest_monthly_rev * 0.12
            leaks.append({
                "id": "leak_manual_stack",
                "severity": "MEDIUM",
                "area": "Sales Automation Infrastructure",
                "title": "Manual Spreadsheet & Fragmented Tooling Overhead",
                "impact_monthly_dollars": round(est_loss, 2),
                "diagnosis": "Team relies on manual tracking across spreadsheets and disconnected inboxes, causing missed follow-ups and lost deal momentum.",
                "ai_recommendation": "Migrate to a dedicated modern CRM (HubSpot or Attio) with automated pipeline triggers and native calendar sync."
            })

        return leaks
