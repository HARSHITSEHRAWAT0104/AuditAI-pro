"""
AuditAI Pro - Software Stack Recommender for New & Growing Companies
Provides curated, data-driven software stack recommendations tailored to audit weaknesses and company stage.
"""

from typing import List, Dict, Any

SOFTWARE_CATALOG = [
    # 1. CRMs & Pipeline Management
    {
        "id": "hubspot_starter",
        "name": "HubSpot Sales & CRM",
        "category": "CRM & Pipeline Management",
        "badge": "Industry Standard All-In-One",
        "tagline": "Centralized customer database with deal pipelines, email tracking, and meeting scheduling.",
        "ideal_for": ["b2b_saas", "b2b_agency"],
        "startup_pricing": "Free plan available; Starter Suite starts at $20/user/mo (Startup Program offers up to 75% off)",
        "setup_time": "1-3 Days",
        "roi_multiplier": "7.2x",
        "solves_bottlenecks": ["leak_manual_stack", "leak_mql_sql", "leak_agency_proposals"],
        "key_features": [
            "Visual drag-and-drop deal pipeline",
            "Automatic email & call logging with Gmail/Outlook",
            "Meeting scheduler links with custom qualification forms",
            "Speed-to-lead automated notifications"
        ],
        "pros": ["Massive ecosystem & integrations", "Generous startup discounts", "Extremely reliable"],
        "cons": ["Enterprise tiers get expensive as contact lists balloon"],
        "website": "https://www.hubspot.com"
    },
    {
        "id": "attio_crm",
        "name": "Attio (AI-Native CRM)",
        "category": "CRM & Pipeline Management",
        "badge": "Top Choice for Modern Tech Startups",
        "tagline": "The next-generation, ultra-flexible CRM built for modern tech teams with real-time AI enrichment.",
        "ideal_for": ["b2b_saas", "b2b_agency"],
        "startup_pricing": "Free up to 3 users; Plus tier is $29/user/mo",
        "setup_time": "1 Day",
        "roi_multiplier": "8.8x",
        "solves_bottlenecks": ["leak_manual_stack", "leak_mql_sql"],
        "key_features": [
            "Automatic contact & company data enrichment without manual research",
            "Notion-style flexible table and kanban views",
            "Granular relationship scoring based on email velocity",
            "AI prompt-based workflow automations"
        ],
        "pros": ["Lightning fast modern UI", "Auto-enrichment saves 5+ hours/rep/week", "Effortless setup"],
        "cons": ["Less legacy third-party plugins than 15-year-old CRMs"],
        "website": "https://attio.com"
    },
    {
        "id": "pipedrive",
        "name": "Pipedrive",
        "category": "CRM & Pipeline Management",
        "badge": "Best for Pure Deal Closing Velocity",
        "tagline": "Activity-based sales CRM designed to keep sales reps focused on taking action and closing deals.",
        "ideal_for": ["b2b_agency", "b2b_saas"],
        "startup_pricing": "Starts at $14/user/mo with 14-day free trial",
        "setup_time": "2 Days",
        "roi_multiplier": "6.5x",
        "solves_bottlenecks": ["leak_deal_close", "leak_agency_proposals"],
        "key_features": [
            "Visual pipeline with activity reminders",
            "AI Sales Assistant offering next-best-action tips",
            "Revenue forecasting and goal tracking",
            "Smart contact data autofill"
        ],
        "pros": ["Very intuitive for non-technical sales reps", "Affordable transparent pricing"],
        "cons": ["Limited built-in marketing email automation"],
        "website": "https://www.pipedrive.com"
    },

    # 2. Sales Outreach & Lead Gen Intelligence
    {
        "id": "apollo_io",
        "name": "Apollo.io",
        "category": "Sales Intelligence & Outbound",
        "badge": "Best All-In-One B2B Prospecting",
        "tagline": "Database of 275M+ verified B2B contacts paired with automated multi-channel cold email and calling sequences.",
        "ideal_for": ["b2b_saas", "b2b_agency"],
        "startup_pricing": "Free tier with 60 credits/mo; Basic plan at $49/user/mo",
        "setup_time": "2 Days",
        "roi_multiplier": "11.4x",
        "solves_bottlenecks": ["leak_ltv_cac", "leak_mql_sql"],
        "key_features": [
            "275M+ B2B decision-maker database with verified emails and direct dials",
            "Automated cold email sequence builder with A/B testing",
            "Built-in cloud phone dialer with call recording",
            "Buying intent signals and tech stack tracking"
        ],
        "pros": ["Replaces 3-4 separate point tools (ZoomInfo, Outreach, Hunter)", "Huge contact coverage"],
        "cons": ["Deliverability requires proper domain warmup settings"],
        "website": "https://www.apollo.io"
    },
    {
        "id": "clay_com",
        "name": "Clay.com",
        "category": "Sales Intelligence & Outbound",
        "badge": "Ultimate AI Data Waterfall & Personalization",
        "tagline": "Scale 1-to-1 personalized outbound using 50+ data providers and AI research agents in a single spreadsheet.",
        "ideal_for": ["b2b_saas", "b2b_agency"],
        "startup_pricing": "Free starter tier; Starter tier at $149/mo (includes thousands of credits)",
        "setup_time": "3 Days",
        "roi_multiplier": "14.2x",
        "solves_bottlenecks": ["leak_mql_sql", "leak_ltv_cac"],
        "key_features": [
            "Waterfall enrichment across 50+ providers to maximize email match rates to 85%+",
            "AI web scraping agents that visit company websites to extract specific value propositions",
            "Hyper-personalized first lines written automatically by AI",
            "1-click export to Smartlead, Instantly, or HubSpot"
        ],
        "pros": ["Unmatched outbound reply rates (often 8-15%)", "Superpowers 1 SDR to do the work of 5"],
        "cons": ["Learning curve requires understanding formula columns"],
        "website": "https://clay.com"
    },
    {
        "id": "instantly_ai",
        "name": "Instantly.ai",
        "category": "Sales Intelligence & Outbound",
        "badge": "Best for Cold Email Deliverability",
        "tagline": "Send thousands of cold emails without landing in spam thanks to unlimited automated account warmups.",
        "ideal_for": ["b2b_saas", "b2b_agency"],
        "startup_pricing": "Growth plan at $37/mo with unlimited email accounts",
        "setup_time": "1-2 Days",
        "roi_multiplier": "9.5x",
        "solves_bottlenecks": ["leak_ltv_cac"],
        "key_features": [
            "Unlimited email account connections and automated mailbox warmups",
            "AI-powered sequence generator and reply sentiment classification",
            "Unified Unibox to manage all replies across 20+ domains in one screen",
            "Automated bounce protection"
        ],
        "pros": ["Priced by emails sent, not per seat", "Keeps primary business domain safe"],
        "cons": ["Requires purchasing secondary sending domains (.co, .io)"],
        "website": "https://instantly.ai"
    },

    # 3. AI Customer Support & Inbound Sales Agents
    {
        "id": "intercom_fin",
        "name": "Intercom + Fin AI Agent",
        "category": "AI Customer Support & Inbound Agents",
        "badge": "Top AI Inbound Conversion Agent",
        "tagline": "AI agent that resolves 50%+ of inbound inquiries instantly and captures high-intent sales leads 24/7.",
        "ideal_for": ["b2b_saas", "ecommerce_d2c"],
        "startup_pricing": "Startup program offers 100% off for 6 months (then $0.99 per successful resolution)",
        "setup_time": "1 Day",
        "roi_multiplier": "8.1x",
        "solves_bottlenecks": ["leak_cart_abandonment", "leak_mql_sql", "leak_churn"],
        "key_features": [
            "Grounding on company help docs, website, and FAQs with zero hallucination guarantee",
            "Instantly routes hot sales leads directly to rep calendars",
            "24/7 coverage across global timezones",
            "Multilingual instant translation in 45+ languages"
        ],
        "pros": ["Incredible startup program (100% free for 6 months)", "High resolution accuracy"],
        "cons": ["Pay-per-resolution cost scales with massive support volume"],
        "website": "https://www.intercom.com"
    },
    {
        "id": "chatbase",
        "name": "Chatbase / Voiceflow",
        "category": "AI Customer Support & Inbound Agents",
        "badge": "Budget-Friendly Custom AI Chatbot",
        "tagline": "Create a custom ChatGPT-style sales bot trained on your website data in under 5 minutes.",
        "ideal_for": ["b2b_agency", "ecommerce_d2c", "b2b_saas"],
        "startup_pricing": "Free tier; Hobby at $19/mo, Standard at $99/mo",
        "setup_time": "15 Minutes",
        "roi_multiplier": "6.8x",
        "solves_bottlenecks": ["leak_cart_abandonment", "leak_mql_sql"],
        "key_features": [
            "Instant web crawler training",
            "Lead capture forms embedded inside chat widget",
            "Custom branding with embed code for any website",
            "Zapier & Webhook integration to push leads to CRM"
        ],
        "pros": ["Can be live in 15 minutes", "Very low price point"],
        "cons": ["Fewer complex enterprise routing rules than Intercom"],
        "website": "https://www.chatbase.co"
    },

    # 4. Analytics, Attribution & Revenue Intelligence
    {
        "id": "posthog",
        "name": "PostHog",
        "category": "Analytics & Revenue Intelligence",
        "badge": "All-in-One Product & Growth Analytics",
        "tagline": "The open-source product analytics platform with session replay, feature flags, A/B testing, and funnels.",
        "ideal_for": ["b2b_saas", "ecommerce_d2c"],
        "startup_pricing": "Generous free tier (1M events + 5k session replays/mo free) + $50k startup credits",
        "setup_time": "1-2 Days",
        "roi_multiplier": "10.1x",
        "solves_bottlenecks": ["leak_cart_abandonment", "leak_churn", "leak_deal_close"],
        "key_features": [
            "Full conversion funnel leak visualization",
            "Session replay videos to watch exactly where users drop off",
            "Feature flags & experimentation to test pricing and copy changes",
            "Customer cohorts and churn prediction telemetry"
        ],
        "pros": ["Replaces Mixpanel, Hotjar, LaunchDarkly, and Google Analytics in one tool", "Huge free tier"],
        "cons": ["Event tracking naming requires thoughtful schema design"],
        "website": "https://posthog.com"
    },
    {
        "id": "fireflies_ai",
        "name": "Fireflies.ai / Gong",
        "category": "Analytics & Revenue Intelligence",
        "badge": "Best AI Sales Meeting Intelligence",
        "tagline": "Automatically joins sales calls, transcribes conversations, identifies objections, and syncs summaries to CRM.",
        "ideal_for": ["b2b_agency", "b2b_saas"],
        "startup_pricing": "Free tier available; Pro tier at $10/user/mo",
        "setup_time": "10 Minutes",
        "roi_multiplier": "7.5x",
        "solves_bottlenecks": ["leak_deal_close", "leak_agency_proposals", "leak_manual_stack"],
        "key_features": [
            "Automatic Zoom, Google Meet, and Teams call recording",
            "AI sentiment, question, and objection detection",
            "Automated action items and deal summaries written to CRM notes",
            "Competitor mention tracking across sales team"
        ],
        "pros": ["Saves sales reps 45 mins of manual CRM data entry per day", "Affordable compared to Gong ($1,200+/seat)"],
        "cons": ["Requires calendar invite access"],
        "website": "https://fireflies.ai"
    },

    # 5. Marketing, Lifecycle & Retention Automation
    {
        "id": "klaviyo",
        "name": "Klaviyo",
        "category": "Marketing & Retention Automation",
        "badge": "Gold Standard for E-Commerce Retention",
        "tagline": "Intelligent marketing automation platform for SMS and email driving repeat purchases and lifetime value.",
        "ideal_for": ["ecommerce_d2c"],
        "startup_pricing": "Free tier up to 250 contacts; Starts at $20/mo",
        "setup_time": "1-2 Days",
        "roi_multiplier": "12.8x",
        "solves_bottlenecks": ["leak_cart_abandonment", "leak_repeat_ltv"],
        "key_features": [
            "Pre-built automated flows: Abandoned Cart, Welcome Series, Back in Stock, Win-Back",
            "Predictive analytics: Next Order Date, Customer Lifetime Value (CLV), Churn Risk",
            "Precision segmentation based on purchase frequency and browse behavior",
            "Native 1-click Shopify and WooCommerce integration"
        ],
        "pros": ["Direct revenue attribution shows exact dollars earned per email sent", "Highest converting templates"],
        "cons": ["Price scales as subscriber count grows past 20,000"],
        "website": "https://www.klaviyo.com"
    },
    {
        "id": "customer_io",
        "name": "Customer.io",
        "category": "Marketing & Retention Automation",
        "badge": "Best for Event-Driven SaaS Retention",
        "tagline": "Automate personalized customer journeys based on real product usage events and actions.",
        "ideal_for": ["b2b_saas"],
        "startup_pricing": "Essentials plan starts at $100/mo (Startup discount available)",
        "setup_time": "2-3 Days",
        "roi_multiplier": "8.9x",
        "solves_bottlenecks": ["leak_churn", "leak_mql_sql"],
        "key_features": [
            "Event-driven workflow canvas triggering emails when users take (or fail to take) product actions",
            "Multi-channel support across email, push notifications, in-app messages, and webhooks",
            "Cohort retention tracking",
            "Visual branching logic based on user data attributes"
        ],
        "pros": ["Incredible flexibility for SaaS product-led growth", "Reliable event pipeline"],
        "cons": ["Requires developer to send custom user events"],
        "website": "https://customer.io"
    },

    # 6. Billing, Payments & Proposals
    {
        "id": "stripe_billing",
        "name": "Stripe Billing & Invoicing",
        "category": "Billing, Payments & Invoicing",
        "badge": "Essential Infrastructure for Global Revenue",
        "tagline": "Recurring billing, automated smart payment retries, customer portal, and tax compliance.",
        "ideal_for": ["b2b_saas", "b2b_agency", "ecommerce_d2c"],
        "startup_pricing": "Pay-as-you-go (0.5% - 0.8% on recurring volume)",
        "setup_time": "1-2 Days",
        "roi_multiplier": "9.0x",
        "solves_bottlenecks": ["leak_churn", "leak_manual_stack"],
        "key_features": [
            "Smart Retries using machine learning to recover failed credit card payments (recovers 38% of churn)",
            "Self-serve customer portal for plan upgrades and billing updates",
            "Automated prorated upgrades and downgrades",
            "Automated invoicing with ACH and wire support"
        ],
        "pros": ["Recovers lost revenue automatically", "Industry standard security & reliability"],
        "cons": ["Custom webhook integrations need backend developer"],
        "website": "https://stripe.com/billing"
    },
    {
        "id": "pandadoc",
        "name": "PandaDoc / Qwilr",
        "category": "Billing, Payments & Invoicing",
        "badge": "Best for High-Ticket Proposal Close Rates",
        "tagline": "Interactive proposals with embedded videos, pricing tables, and legal electronic signatures.",
        "ideal_for": ["b2b_agency"],
        "startup_pricing": "Essentials starts at $19/user/mo",
        "setup_time": "1 Day",
        "roi_multiplier": "7.8x",
        "solves_bottlenecks": ["leak_agency_proposals", "leak_deal_close"],
        "key_features": [
            "Real-time analytics showing when clients open proposals and how many seconds they spent on pricing",
            "Interactive pricing tables where clients can select add-ons",
            "Legally binding e-signatures with Stripe payment integration upon signature",
            "CRM pipeline sync"
        ],
        "pros": ["Increases proposal close rate by 34%", "Shortens signing turnaround from 7 days to 24 hours"],
        "cons": ["Monthly per-seat model"],
        "website": "https://www.pandadoc.com"
    }
]

class SoftwareRecommender:
    def __init__(self, audit_result: Dict[str, Any]):
        self.audit = audit_result
        self.business_model = audit_result.get("business_model", "b2b_saas")
        self.bottlenecks = audit_result.get("bottlenecks", [])
        self.bottleneck_ids = {b.get("id") for b in self.bottlenecks}
        self.current_stack = [s.lower() for s in audit_result.get("current_stack", [])]

    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Calculates personalized match scores and returns sorted recommendations."""
        recommended = []

        for sw in SOFTWARE_CATALOG:
            item = dict(sw)
            # Calculate match score based on business model and detected leaks
            score = 60 # baseline score

            # Match model
            if self.business_model in item.get("ideal_for", []):
                score += 20
            else:
                score -= 15

            # Solves bottlenecks
            solves = item.get("solves_bottlenecks", [])
            overlap = set(solves).intersection(self.bottleneck_ids)
            if overlap:
                score += min(20, len(overlap) * 10)

            # Check if already in stack
            sw_name_lower = item["name"].lower()
            if any(term in sw_name_lower for term in self.current_stack):
                item["already_in_use"] = True
                score = max(50, score - 20)
            else:
                item["already_in_use"] = False

            score = min(99, max(45, score))
            item["fit_score"] = score

            # Reason why recommended
            reasons = []
            if overlap:
                reasons.append(f"Directly resolves {len(overlap)} of your critical audit bottlenecks")
            if self.business_model in item.get("ideal_for", []):
                reasons.append(f"Tailored specifically for {self.business_model.replace('_', ' ').title()} stage companies")
            reasons.append(f"Fast {item['setup_time']} deployment with {item['roi_multiplier']} expected ROI")

            item["recommendation_reason"] = " • ".join(reasons)
            recommended.append(item)

        # Sort by fit score descending
        recommended.sort(key=lambda x: x["fit_score"], reverse=True)
        return recommended
