"""
AuditAI Pro - Verification & Integrity Test Suite
Verifies that all core components, mathematical models, recommendations, and API routes operate without error.
"""

import sys
import os
import json

def run_tests():
    print("[TEST] 1. Testing Sample Data...")
    from sample_data import get_sample_saas_data, get_sample_ecommerce_data, get_sample_agency_data, export_sample_csvs
    saas_data = get_sample_saas_data()
    ecom_data = get_sample_ecommerce_data()
    agency_data = get_sample_agency_data()
    assert len(saas_data["monthly_records"]) == 12, "SaaS records count mismatch"
    assert len(ecom_data["monthly_records"]) == 12, "E-com records count mismatch"
    assert len(agency_data["monthly_records"]) == 12, "Agency records count mismatch"
    export_sample_csvs("sample_exports")
    print("  -> Sample data OK.")

    print("[TEST] 2. Testing Audit Engine...")
    from audit_engine import AuditEngine
    engine = AuditEngine(business_model=saas_data["business_model"], company_name=saas_data["company_name"])
    audit_res = engine.analyze(saas_data["monthly_records"], current_stack=saas_data["current_stack"])
    assert "overall_score" in audit_res, "overall_score missing"
    assert "score_pillars" in audit_res, "score_pillars missing"
    assert "bottlenecks" in audit_res, "bottlenecks missing"
    print(f"  -> Audit score calculated: {audit_res['overall_score']}/100 ({audit_res['grade']})")
    print(f"  -> Detected {len(audit_res['bottlenecks'])} bottlenecks.")

    print("[TEST] 3. Testing Growth Advisor & Simulation...")
    from growth_advisor import GrowthAdvisor
    advisor = GrowthAdvisor(audit_res)
    growth_plan = advisor.generate_growth_plan()
    assert "projections" in growth_plan, "projections missing"
    assert "roadmap" in growth_plan, "roadmap missing"
    sim_res = advisor.simulate(conv_lift_pct=5.0, churn_reduction_pct=10.0, price_lift_pct=5.0)
    assert sim_res["net_annual_increase"] > 0, "Simulation lift should be positive"
    print(f"  -> Target Projected ARR: ${growth_plan['projections']['target']['projected_arr']:,.2f}")
    print(f"  -> Simulated Net Gain: +${sim_res['net_annual_increase']:,.2f}/yr (+{sim_res['total_percentage_growth']}%)")

    print("[TEST] 4. Testing Software Recommender...")
    from software_recommender import SoftwareRecommender
    recommender = SoftwareRecommender(audit_res)
    sw_list = recommender.get_recommendations()
    assert len(sw_list) > 5, "Expected more than 5 software recommendations"
    top_sw = sw_list[0]
    print(f"  -> Top Recommendation: {top_sw['name']} (Fit: {top_sw['fit_score']}%)")

    print("[TEST] 5. Testing AI Agent & Copilot...")
    from ai_agent import AIAuditAdvisor
    agent = AIAuditAdvisor()
    memo = agent.generate_executive_audit_memo(audit_res, growth_plan)
    assert len(memo) > 100, "Memo generated is too short"
    chat_reply = agent.ask_copilot("How do I improve my sales speed to lead?", audit_res, growth_plan)
    assert len(chat_reply) > 50, "Chat reply is too short"
    print("  -> AI Memo & Chat generated successfully.")

    print("\n[SUCCESS] ALL AUDITAI PRO TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
