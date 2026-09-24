"""
AuditAI Pro - Growth Advisor & Assured Sales Increase Engine
Calculates mathematical revenue uplift projections, phased execution roadmaps, and tactical playbooks.
"""

from typing import Dict, Any, List

class GrowthAdvisor:
    def __init__(self, audit_result: Dict[str, Any]):
        self.audit = audit_result
        self.financials = audit_result.get("financial_summary", {})
        self.bottlenecks = audit_result.get("bottlenecks", [])
        self.business_model = audit_result.get("business_model", "b2b_saas")
        self.unit_econ = audit_result.get("unit_economics", {})

    def generate_growth_plan(self) -> Dict[str, Any]:
        """Generates comprehensive growth projections and phased action plans."""
        current_mrr = self.financials.get("latest_monthly_revenue", 50000)
        current_arr = self.financials.get("annual_run_rate_arr", current_mrr * 12)
        total_leak_impact = sum(b.get("impact_monthly_dollars", 0) for b in self.bottlenecks)

        # Assured Uplift Calculations
        # Conservative: Fixes 35% of detected leaks + 5% natural baseline
        conservative_monthly_gain = (total_leak_impact * 0.35) + (current_mrr * 0.05)
        # Target: Fixes 65% of detected leaks + 10% optimization
        target_monthly_gain = (total_leak_impact * 0.65) + (current_mrr * 0.10)
        # Aggressive: Fixes 85% of leaks + expansion & outbound acceleration
        aggressive_monthly_gain = (total_leak_impact * 0.85) + (current_mrr * 0.20)

        conservative_arr = (current_mrr + conservative_monthly_gain) * 12
        target_arr = (current_mrr + target_monthly_gain) * 12
        aggressive_arr = (current_mrr + aggressive_monthly_gain) * 12

        projections = {
            "current_arr": round(current_arr, 2),
            "conservative": {
                "monthly_gain": round(conservative_monthly_gain, 2),
                "projected_arr": round(conservative_arr, 2),
                "percentage_increase": round((conservative_arr - current_arr) / current_arr * 100, 1) if current_arr > 0 else 0,
                "confidence_score": "95% (High Assurance)",
                "timeframe": "90 Days"
            },
            "target": {
                "monthly_gain": round(target_monthly_gain, 2),
                "projected_arr": round(target_arr, 2),
                "percentage_increase": round((target_arr - current_arr) / current_arr * 100, 1) if current_arr > 0 else 0,
                "confidence_score": "85% (Expected Outcome)",
                "timeframe": "120-180 Days"
            },
            "aggressive": {
                "monthly_gain": round(aggressive_monthly_gain, 2),
                "projected_arr": round(aggressive_arr, 2),
                "percentage_increase": round((aggressive_arr - current_arr) / current_arr * 100, 1) if current_arr > 0 else 0,
                "confidence_score": "70% (Full Optimization)",
                "timeframe": "180-240 Days"
            }
        }

        # Revenue Breakdown Levers
        levers = [
            {
                "lever": "Speed-to-Lead & Instant Qualification",
                "monthly_impact": round(current_mrr * 0.12, 2),
                "difficulty": "Low (1-2 days)",
                "description": "Engaging inbound prospects within 2 minutes increases qualification rates by 391% compared to a 30-minute delay."
            },
            {
                "lever": "Pipeline Leak Patching & Automated Follow-up",
                "monthly_impact": round(total_leak_impact * 0.45, 2),
                "difficulty": "Medium (1-2 weeks)",
                "description": "Automating multi-touch email, SMS, and WhatsApp sequences for non-responsive leads and stalled opportunities."
            },
            {
                "lever": "Retention & Churn Reduction Loop",
                "monthly_impact": round(current_mrr * 0.08, 2),
                "difficulty": "Medium (2-3 weeks)",
                "description": "A 5% reduction in customer churn accelerates overall compounding growth rate by 25-40%."
            },
            {
                "lever": "Pricing & Packaging Optimization",
                "monthly_impact": round(current_mrr * 0.10, 2),
                "difficulty": "Low (Immediate)",
                "description": "Introducing tiered feature gates, annual billing discounts, or value-metric pricing to lift AOV by 10-15%."
            }
        ]

        # Phased 30-60-90-180 Action Roadmap
        roadmap = self._generate_roadmap()

        # Tactical Playbooks
        playbooks = self._generate_tactical_playbooks()

        return {
            "projections": projections,
            "revenue_levers": levers,
            "roadmap": roadmap,
            "tactical_playbooks": playbooks
        }

    def simulate(self, conv_lift_pct: float = 0.0, churn_reduction_pct: float = 0.0, price_lift_pct: float = 0.0) -> Dict[str, Any]:
        """Interactively simulates sales increase based on user sliders."""
        current_mrr = self.financials.get("latest_monthly_revenue", 50000)
        current_arr = current_mrr * 12

        # 1. Conversion lift impact
        conv_multiplier = 1.0 + (conv_lift_pct / 100.0)
        # 2. Retention impact (less churn = more compounding base)
        retention_multiplier = 1.0 + (churn_reduction_pct / 100.0 * 0.6)
        # 3. Pricing lift impact
        price_multiplier = 1.0 + (price_lift_pct / 100.0)

        new_mrr = current_mrr * conv_multiplier * retention_multiplier * price_multiplier
        new_arr = new_mrr * 12
        arr_delta = new_arr - current_arr
        total_percentage = ((new_arr - current_arr) / current_arr * 100) if current_arr > 0 else 0

        return {
            "base_mrr": round(current_mrr, 2),
            "base_arr": round(current_arr, 2),
            "simulated_mrr": round(new_mrr, 2),
            "simulated_arr": round(new_arr, 2),
            "net_annual_increase": round(arr_delta, 2),
            "total_percentage_growth": round(total_percentage, 1),
            "inputs": {
                "conversion_lift_pct": conv_lift_pct,
                "churn_reduction_pct": churn_reduction_pct,
                "price_lift_pct": price_lift_pct
            }
        }

    def _generate_roadmap(self) -> List[Dict[str, Any]]:
        """Tailors action steps based on business model and weaknesses."""
        bm = self.business_model

        if bm == "ecommerce_d2c":
            p1_actions = [
                "Implement 3-part automated Abandoned Cart email & SMS flow in Klaviyo (Trigger at 15m, 4h, 24h).",
                "Add 1-click Express Checkout (Shop Pay / Apple Pay) to cut checkout friction.",
                "Deploy an exit-intent popup offering a 10% welcome discount in exchange for phone/email."
            ]
            p2_actions = [
                "Create VIP Tiered Loyalty program to lift repeat order rate from 18% to 28%.",
                "Automate post-purchase replenishment reminders timed to estimated product run-out days.",
                "Install PostHog or Heatmap tracking to analyze drop-offs on mobile product pages."
            ]
            p3_actions = [
                "Integrate AI customer support agent (Intercom Fin or Gorgias AI) to answer pre-purchase questions instantly.",
                "Scale Meta and Google Ads with automated ROAS bidding rules and creative testing."
            ]
        elif bm == "b2b_agency":
            p1_actions = [
                "Transition from static PDF proposals to interactive web proposals (PandaDoc or Qwilr) with click-to-sign.",
                "Enforce a 24-hour turnaround rule from Discovery Call to Proposal delivery.",
                "Send the '9-Word Re-engagement Email' to all inactive proposals from the last 90 days."
            ]
            p2_actions = [
                "Set up Apollo.io cold outbound system targeting verified decision-makers in your niche.",
                "Record Loom video walkthroughs embedded inside every proposal to walk clients through ROI.",
                "Implement a formal Client Referral Incentive (e.g., $1,000 credit or 10% cash bonus on closed referrals)."
            ]
            p3_actions = [
                "Deploy AI Meeting Intelligence (Fireflies.ai) to automatically log notes into CRM.",
                "Productize service offerings into fixed-scope high-margin sprint tiers to shorten sales cycle."
            ]
        else: # B2B SaaS
            p1_actions = [
                "Deploy Speed-to-Lead webhook connecting website forms to Slack + instant calendar booking (Cal.com / Chili Piper).",
                "Enrich inbound signups automatically using Clay or Apollo to flag high-value ICP leads immediately.",
                "Launch an automated 5-step onboarding email drip based on product activation milestones."
            ]
            p2_actions = [
                "Implement AI meeting intelligence (Gong or Fireflies) to analyze sales objections in real time.",
                "Build automated stalled deal alert in CRM for opportunities untouched for >5 business days.",
                "Introduce annual upfront billing discount (save 20%) to pull cash flow forward and slash churn."
            ]
            p3_actions = [
                "Deploy outbound AI SDR agents (Clay + Instantly) targeting lookalike accounts of best customers.",
                "Establish customer health scoring dashboards in CRM to trigger proactive CSM outreach 30 days before renewal."
            ]

        return [
            {
                "phase": "Phase 1: Quick-Win Foundations (Days 1 - 30)",
                "focus": "Plugging Critical Leaks & Speed-to-Lead",
                "expected_impact": "+10% to +18% Immediate Revenue Lift",
                "actions": p1_actions
            },
            {
                "phase": "Phase 2: Systematic Scale (Days 31 - 90)",
                "focus": "Pipeline Velocity & Retention Expansion",
                "expected_impact": "+20% to +35% Cumulative Growth",
                "actions": p2_actions
            },
            {
                "phase": "Phase 3: Autonomous AI Engine (Days 91 - 180)",
                "focus": "AI SDR Outreach & Automated Compounding",
                "expected_impact": "+40% to +65%+ Assured ARR Expansion",
                "actions": p3_actions
            }
        ]

    def _generate_tactical_playbooks(self) -> List[Dict[str, Any]]:
        """Provides ready-to-use tactical copy and scripts."""
        return [
            {
                "name": "The '5-Minute Speed-to-Lead' Inbound Script",
                "trigger": "When an inbound prospect submits a contact/demo request form.",
                "channel": "SMS or Direct Email",
                "template": (
                    "Hi {{first_name}}, Ayush from {{company_name}} here. Noticed you were checking out how to scale {{interest_topic}}. "
                    "I took a quick look at your profile and have 2 specific ideas ready for you. "
                    "Do you have 7 minutes tomorrow at 2:00 PM or 4:30 PM to review them together? (Or grab a time directly here: {{booking_link}})"
                ),
                "why_it_works": "Personalized, acknowledges their inquiry within seconds, provides zero-fluff specific value, and gives two concrete time slots."
            },
            {
                "name": "The '9-Word Re-engagement Email' for Ghosted Deals",
                "trigger": "When a proposal or demo was sent 10+ days ago and the prospect stopped replying.",
                "channel": "Email (Plain text, 1 line)",
                "template": "Hi {{first_name}}, have you given up on {{project_or_goal}}?",
                "why_it_works": "Proven 68% reply rate across thousands of B2B sales cycles. Triggers loss aversion and removes social pressure to respond formally."
            },
            {
                "name": "The Price Objection Pivot ('It's too expensive')",
                "trigger": "When the prospect states budget constraints or compares with cheaper options.",
                "channel": "Live Call / Meeting",
                "template": (
                    "\"I completely understand, {{first_name}}. When people say that, it usually means one of two things: "
                    "either the cash flow isn't available right now, or you're not yet 100% convinced the return will drastically exceed the cost. "
                    "Which one is it in your case?\" ... If return: \"Let's pull up the numbers together and model the exact 90-day payback period.\""
                ),
                "why_it_works": "Separates genuine cash constraints from perceived value doubt without being defensive."
            },
            {
                "name": "Post-Purchase / Onboarding Referral Generator",
                "trigger": "Day 14 after a customer hits their first 'aha' milestone.",
                "channel": "In-app message or personal founder email",
                "template": (
                    "Hi {{first_name}}, thrilled to see you just achieved {{milestone}}! "
                    "Quick question: who is one other founder or leader in your network who is struggling with {{core_pain_point}} right now? "
                    "If you introduce us via email, I'll credit $500 to your next renewal and give them VIP priority onboarding."
                ),
                "why_it_works": "Asks at the peak of satisfaction and clearly defines the exact target persona to introduce."
            }
        ]
