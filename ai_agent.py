"""
AuditAI Pro - AI Agent & Growth Copilot
Integrates Gemini 3.8 Flash via the google-genai SDK with an intelligent offline fallback engine.
"""

import os
import json
from typing import Dict, Any, Optional

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AIAuditAdvisor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.client = None
        if HAS_GENAI and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[AIAuditAdvisor] Failed to initialize Gemini Client: {e}")
                self.client = None

    def generate_executive_audit_memo(self, audit_data: Dict[str, Any], growth_data: Dict[str, Any]) -> str:
        """Generates a board-level strategic audit memo."""
        if self.client:
            try:
                prompt = f"""
You are an elite Chief Revenue Officer (CRO) and McKinsey-grade strategic business auditor.
Write an authoritative, highly actionable Executive Audit Memo for the leadership of {audit_data.get('company_name', 'the company')}.

Company Profile:
- Business Model: {audit_data.get('business_model')}
- Audit Score: {audit_data.get('overall_score')}/100 ({audit_data.get('grade')})
- Current ARR: ${audit_data.get('financial_summary', {}).get('annual_run_rate_arr', 0):,.2f}
- LTV:CAC Ratio: {audit_data.get('unit_economics', {}).get('ltv_cac_ratio')}x
- Critical Bottlenecks: {json.dumps([b['title'] for b in audit_data.get('bottlenecks', [])])}
- Projected ARR Potential: ${growth_data.get('projections', {}).get('target', {}).get('projected_arr', 0):,.2f} ({growth_data.get('projections', {}).get('target', {}).get('percentage_increase')}% increase)

Format your response in clean Markdown with:
1. Executive Verdict & Urgency Level
2. Top 3 Revenue Leaks & Financial Bleed Analysis
3. High-Leverage Strategic Turnaround Directive (Immediate, 60-day, and 180-day focus)
4. Recommended Modern Tooling Stack Justification
Keep it sharp, direct, mathematically grounded, and inspiring for a growing company founder.
"""
                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[AIAuditAdvisor] Gemini generation error, falling back to local engine: {e}")

        # High-Fidelity Fallback Memo
        return self._generate_fallback_memo(audit_data, growth_data)

    def ask_copilot(self, user_question: str, audit_data: Dict[str, Any], growth_data: Dict[str, Any], chat_history: Optional[list] = None) -> str:
        """Answers user queries in context of their specific business audit."""
        if self.client:
            try:
                context_summary = f"""
Context:
Company: {audit_data.get('company_name')}
Business Model: {audit_data.get('business_model')}
Audit Score: {audit_data.get('overall_score')}/100 ({audit_data.get('grade')})
Latest Monthly Revenue: ${audit_data.get('financial_summary', {}).get('latest_monthly_revenue', 0):,.2f}
Current ARR: ${audit_data.get('financial_summary', {}).get('annual_run_rate_arr', 0):,.2f}
LTV:CAC: {audit_data.get('unit_economics', {}).get('ltv_cac_ratio')}x
Identified Leaks: {[b['title'] for b in audit_data.get('bottlenecks', [])]}
"""
                prompt = f"""
You are AuditAI Pro, the world's most capable AI Growth Consultant and Revenue Architect.
Answer the founder's question using their audit context.

{context_summary}

User Question: {user_question}

Provide actionable, step-by-step guidance. If asking for scripts, include exact battle-tested copy. If asking for software advice, give concrete implementation tips.
"""
                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[AIAuditAdvisor] Gemini chat error, using fallback: {e}")

        return self._generate_fallback_chat_reply(user_question, audit_data, growth_data)

    def _generate_fallback_memo(self, audit: Dict[str, Any], growth: Dict[str, Any]) -> str:
        comp = audit.get("company_name", "Your Company")
        score = audit.get("overall_score", 70)
        grade = audit.get("grade", "B")
        fin = audit.get("financial_summary", {})
        unit = audit.get("unit_economics", {})
        bottlenecks = audit.get("bottlenecks", [])
        proj = growth.get("projections", {}).get("target", {})

        top_leaks_text = "\n".join([
            f"- **{b.get('title')}**: Impacting ~${b.get('impact_monthly_dollars', 0):,.2f}/mo. *Remedy:* {b.get('ai_recommendation')}"
            for b in bottlenecks[:3]
        ])

        return f"""### 📊 Executive Revenue Audit & Strategic Transformation Memo
**Company:** {comp} | **Audit Health Score:** {score}/100 ({grade})  
**Current ARR:** ${fin.get('annual_run_rate_arr', 0):,.2f} | **Target Projected ARR:** ${proj.get('projected_arr', 0):,.2f} (+{proj.get('percentage_increase', 35)}% Uplift)

---

#### 1. Strategic Verdict
{comp} displays solid commercial validation, but is currently operating with significant friction in its conversion pipeline and unit economics. Our diagnostic audit reveals that your core commercial engine has **{len(bottlenecks)} critical revenue leaks**, costing an estimated **${sum(b.get('impact_monthly_dollars', 0) for b in bottlenecks):,.2f} in lost high-margin revenue each month**.

Your LTV:CAC ratio is currently **{unit.get('ltv_cac_ratio')}x** ({unit.get('ltv_cac_rating')}), indicating that capital efficiency can be substantially multiplied by modernizing your automation infrastructure.

#### 2. Primary Bottlenecks & Value Bleed
{top_leaks_text}

#### 3. Assured Growth Directive (Next 90 to 180 Days)
1. **Immediate (Days 1–30): Speed-to-Lead & Abandonment Patching**
   Reduce response latency to under 2 minutes for inbound inquiries. Companies that respond within 5 minutes are 21x more likely to qualify prospects than those taking 30 minutes.
2. **Expansion (Days 31–90): Pipeline Automation & Retention**
   Deploy multi-channel automated cadences (email, SMS, calendar triggers) for stalled opportunities. Launch automated onboarding retention triggers to protect customer cohorts.
3. **Scale (Days 91–180): Outbound & AI SDR Deployment**
   Scale verified cold outbound using waterfall data providers (Clay + Apollo) to systematically acquire high-value target accounts without ballooning ad spend.

#### 4. Modern Software Stack Priority
Transitioning from fragmented spreadsheets or disconnected point solutions to an integrated modern stack (**Attio/HubSpot CRM + Apollo.io + PostHog Analytics + Stripe Billing**) is estimated to yield an immediate **7.2x to 11.4x ROI** and unlock an additional **${growth.get('projections', {}).get('conservative', {}).get('monthly_gain', 0):,.2f}/month** in guaranteed baseline revenue.
"""

    def _generate_fallback_chat_reply(self, query: str, audit: Dict[str, Any], growth: Dict[str, Any]) -> str:
        q_lower = query.lower()
        comp = audit.get("company_name", "your company")

        if any(w in q_lower for w in ["software", "tool", "crm", "stack", "recommend"]):
            return f"""Based on your audit score ({audit.get('overall_score')}/100) and detected pipeline leaks, here is the high-conviction software stack recommended for {comp}:

1. **Core CRM & Pipeline:** **Attio** or **HubSpot Sales Starter**
   - *Why:* Auto-enriches prospect profiles, tracks deal velocity, and prevents leads from going cold.
2. **Sales Outreach & Contact Intelligence:** **Apollo.io** or **Clay.com**
   - *Why:* Gives you instant access to 275M+ verified decision-makers and automates cold outreach.
3. **AI Support & Inbound Lead Capture:** **Intercom Fin AI** or **Chatbase**
   - *Why:* Captures website leads 24/7 and qualifies inquiries before they bounce.
4. **Product/Funnel Analytics:** **PostHog**
   - *Why:* Identifies the exact moments users abandon your cart or sign-up flow.

Would you like a step-by-step 48-hour implementation blueprint for any of these?"""

        elif any(w in q_lower for w in ["script", "email", "outreach", "template", "cold"]):
            return f"""Here is a battle-tested **Speed-to-Lead Inbound Script** crafted for {comp}:

**Subject:** 2 quick ideas for {{Company}}

**Body:**
> Hi {{First_Name}},
>
> I saw you recently checked out our {audit.get('business_model', 'business')} solutions. 
> 
> I took a look at your current workflow and noticed two immediate opportunities to accelerate your sales cycle and eliminate pipeline drop-off.
>
> Do you have 8 minutes this Tuesday or Thursday for a quick working session? 
> (Alternatively, you can pick a convenient slot directly here: [Your Calendar Link])
>
> Best regards,  
> Ayush | Growth Architect

**Key Rule:** Send this within 120 seconds of form submission for a 390%+ boost in booked calls."""

        elif any(w in q_lower for w in ["churn", "retention", "repeat"]):
            return f"""To curb your churn rate and lift retention for {comp}:

1. **Trigger 'Aha' Milestone Tracking:** Identify the 1 action users take in week 1 that correlates with long-term retention (e.g. inviting a colleague or configuring their first integration).
2. **Automate Pre-Emptive CSM Alerts:** Flag accounts where usage drops by >30% over 7 consecutive days. Reach out with helpful loom video audits before they decide to cancel.
3. **Annual Plan Incentives:** Offer a 20% discount on annual upfront commitments. Annual subscribers experience 65% lower churn than monthly subscribers.
4. **Smart Failed Payment Retries:** Use Stripe Billing Smart Retries to recover involuntarily churned credit cards automatically."""

        else:
            return f"""Regarding your question about **"{query}"** for {comp}:

With your current audit score of **{audit.get('overall_score')}/100** and monthly run-rate of **${audit.get('financial_summary', {}).get('latest_monthly_revenue', 0):,.2f}**, the highest-leverage priority is addressing your primary bottleneck: **{audit.get('bottlenecks', [{}])[0].get('title', 'Pipeline Conversion')}**.

**Action Items:**
1. Focus first on the **Phase 1 Quick Wins** in your Growth Roadmap, which are estimated to generate an immediate **+${growth.get('projections', {}).get('conservative', {}).get('monthly_gain', 0):,.2f}/mo** in added cash flow.
2. Ensure your CRM tracking is fully integrated so zero inbound leads slip through cracks.
3. Align your sales reps around the objection playbooks provided in the Audit Report.

Let me know if you'd like me to draft specific copy, analyze pricing models, or suggest exact tool integrations!"""
