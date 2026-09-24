/**
 * AuditAI Pro - Frontend Application Engine
 * Handles live analytics, Chart.js visualizations, AI chat, interactive growth simulation, and uploads.
 */

let currentAuditData = null;
let currentGrowthData = null;
let currentSoftwareData = [];
let revenueChartInstance = null;
let radarChartInstance = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchCurrentAudit();
});

// Fetch current active audit session
async function fetchCurrentAudit() {
    try {
        const res = await fetch('/api/current-audit');
        const data = await res.json();
        currentAuditData = data.audit;
        currentGrowthData = data.growth;
        currentSoftwareData = data.software;
        renderAll(data);
    } catch (err) {
        console.error("Failed to load audit data:", err);
    }
}

// Render all tabs and UI components
function renderAll(data) {
    const audit = data.audit;
    const growth = data.growth;
    const software = data.software;
    const memo = data.memo;

    renderBanner(audit);
    renderKPIs(audit, growth);
    renderCharts(audit);
    renderPillars(audit);
    renderFunnel(audit);
    renderBottlenecks(audit);
    renderGrowthProjections(growth);
    renderRoadmap(growth);
    renderPlaybooks(growth);
    renderSoftware(software);
    renderMemo(memo);

    if (window.lucide) {
        lucide.createIcons();
    }
}

// 1. Render Top Banner & Big Score
function renderBanner(audit) {
    document.getElementById('banner-company-name').textContent = audit.company_name || 'Venture';
    const modelTag = document.getElementById('banner-model-tag');
    modelTag.textContent = (audit.business_model || 'B2B SaaS').replace('_', ' ').toUpperCase();

    // Score badge
    const scoreVal = audit.overall_score || 75.0;
    document.getElementById('score-number').textContent = scoreVal.toFixed(1);
    document.getElementById('score-grade').textContent = audit.grade || 'A-';
    document.getElementById('score-status').textContent = audit.health_status || 'Healthy';

    // SVG Circle animation
    const circle = document.getElementById('score-circle');
    const circumference = 213.6; // 2 * pi * 34
    const offset = circumference - (scoreVal / 100) * circumference;
    circle.style.strokeDashoffset = offset;

    // Color based on status
    if (scoreVal >= 80) {
        circle.setAttribute('class', 'text-emerald-500 transition-all duration-1000 ease-out');
        document.getElementById('score-grade').className = 'text-base font-bold text-emerald-400';
    } else if (scoreVal >= 65) {
        circle.setAttribute('class', 'text-indigo-400 transition-all duration-1000 ease-out');
        document.getElementById('score-grade').className = 'text-base font-bold text-indigo-400';
    } else {
        circle.setAttribute('class', 'text-amber-500 transition-all duration-1000 ease-out');
        document.getElementById('score-grade').className = 'text-base font-bold text-amber-400';
    }
}

// 2. Render Top KPI Cards
function renderKPIs(audit, growth) {
    const fin = audit.financial_summary || {};
    const unit = audit.unit_economics || {};
    const proj = (growth.projections && growth.projections.target) || {};

    document.getElementById('kpi-arr').textContent = '$' + Number(fin.annual_run_rate_arr || 0).toLocaleString();
    document.getElementById('kpi-growth').textContent = `+${fin.period_growth_pct || 0}% growth`;
    document.getElementById('kpi-target-arr').textContent = '$' + Number(proj.projected_arr || 0).toLocaleString();
    document.getElementById('kpi-uplift-pct').textContent = `+${proj.percentage_increase || 0}% Assured Lift`;

    document.getElementById('kpi-ltv-cac').textContent = (unit.ltv_cac_ratio || 0).toFixed(2) + 'x';
    document.getElementById('kpi-ltv').textContent = '$' + Number(unit.ltv || 0).toLocaleString();
    document.getElementById('kpi-cac').textContent = '$' + Number(unit.cac || 0).toLocaleString();

    document.getElementById('kpi-cycle-days').textContent = (unit.sales_cycle_days || 45) + ' Days';
    document.getElementById('kpi-churn').textContent = (unit.avg_churn_pct || unit.avg_repeat_pct || 0).toFixed(1) + '%';
}

// 3. Render Chart.js Visualizations
function renderCharts(audit) {
    const records = audit.monthly_history || [];
    const labels = records.map(r => r.month);
    const revenues = records.map(r => r.revenue);
    const adSpends = records.map(r => r.ad_spend || 0);

    // Revenue Trajectory Chart
    const revCtx = document.getElementById('revenueChart').getContext('2d');
    if (revenueChartInstance) {
        revenueChartInstance.destroy();
    }

    revenueChartInstance = new Chart(revCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Monthly Revenue ($)',
                    data: revenues,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#818cf8',
                    pointRadius: 4
                },
                {
                    label: 'Ad & Acquisition Spend ($)',
                    data: adSpends,
                    borderColor: '#f43f5e',
                    borderDash: [5, 5],
                    borderWidth: 2,
                    fill: false,
                    tension: 0.2,
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { size: 11 } }
                },
                tooltip: {
                    backgroundColor: '#0f172a',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: '#1e293b' },
                    ticks: { color: '#64748b', font: { size: 10 } }
                },
                y: {
                    grid: { color: '#1e293b' },
                    ticks: {
                        color: '#64748b',
                        font: { size: 10 },
                        callback: val => '$' + Number(val).toLocaleString()
                    }
                }
            }
        }
    });

    // 6-Pillar Radar Chart
    const pillars = audit.score_pillars || {};
    const radarLabels = [
        'Revenue Health',
        'Funnel Conversion',
        'Unit Economics',
        'Retention Health',
        'Acquisition ROI',
        'Tech Stack'
    ];
    const radarValues = [
        pillars.revenue_health || 70,
        pillars.funnel_conversion || 70,
        pillars.unit_economics || 70,
        pillars.retention_health || 70,
        pillars.acquisition_efficiency || 70,
        pillars.tech_stack_maturity || 70
    ];

    const radarCtx = document.getElementById('radarChart').getContext('2d');
    if (radarChartInstance) {
        radarChartInstance.destroy();
    }

    radarChartInstance = new Chart(radarCtx, {
        type: 'radar',
        data: {
            labels: radarLabels,
            datasets: [{
                label: 'Audit Score',
                data: radarValues,
                backgroundColor: 'rgba(99, 102, 241, 0.25)',
                borderColor: '#6366f1',
                pointBackgroundColor: '#818cf8',
                borderWidth: 2,
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: { display: false, stepSize: 25 },
                    grid: { color: '#1e293b' },
                    angleLines: { color: '#1e293b' },
                    pointLabels: {
                        color: '#94a3b8',
                        font: { size: 9, weight: '500' }
                    }
                }
            }
        }
    });
}

// 4. Render Pillars Breakdown
function renderPillars(audit) {
    const p = audit.score_pillars || {};
    const container = document.getElementById('pillars-container');
    container.innerHTML = '';

    const list = [
        { name: "Revenue Health & Trajectory", score: p.revenue_health, desc: "Evaluates historical revenue velocity, predictability, and stability." },
        { name: "Funnel Conversion & Leak Control", score: p.funnel_conversion, desc: "Stage-to-stage transition rates and drop-off leak friction." },
        { name: "Unit Economics (LTV:CAC)", score: p.unit_economics, desc: "Margin durability, payback speed, and acquisition efficiency." },
        { name: "Customer Retention & Churn Defense", score: p.retention_health, desc: "Churn prevention, repeat purchase loops, and cohort decay." },
        { name: "Acquisition & Channel ROAS", score: p.acquisition_efficiency, desc: "Paid vs organic balance, customer acquisition cost containment." },
        { name: "Tech Stack & Automation Maturity", score: p.tech_stack_maturity, desc: "Modern CRM, AI SDR tooling, and pipeline integration." }
    ];

    list.forEach(item => {
        const sc = item.score || 70;
        let colorClass = "text-emerald-400";
        let barClass = "bg-emerald-500";
        if (sc < 60) {
            colorClass = "text-rose-400";
            barClass = "bg-rose-500";
        } else if (sc < 75) {
            colorClass = "text-amber-400";
            barClass = "bg-amber-500";
        }

        const card = document.createElement('div');
        card.className = "bg-slate-950/60 border border-slate-800/80 p-3.5 rounded-xl space-y-2";
        card.innerHTML = `
            <div class="flex justify-between items-center text-xs">
                <span class="font-semibold text-slate-200">${item.name}</span>
                <span class="font-bold ${colorClass}">${sc.toFixed(1)}/100</span>
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="${barClass} h-full rounded-full transition-all duration-700" style="width: ${sc}%"></div>
            </div>
            <p class="text-[11px] text-slate-400">${item.desc}</p>
        `;
        container.appendChild(card);
    });
}

// 5. Render Funnel
function renderFunnel(audit) {
    const funnel = audit.funnel_metrics || {};
    const stages = funnel.stages || [];
    const container = document.getElementById('funnel-container');
    container.innerHTML = '';

    stages.forEach((st, idx) => {
        const card = document.createElement('div');
        card.className = "bg-slate-950/60 border border-slate-800 p-4 rounded-xl space-y-2 relative";
        
        let convInfo = "";
        if (idx > 0) {
            convInfo = `<div class="text-[11px] text-indigo-300 font-semibold bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded inline-block">
                ${st.conversion_from_prev}% from prev stage
            </div>`;
        } else {
            convInfo = `<div class="text-[11px] text-slate-400 font-medium">Top of Funnel (100%)</div>`;
        }

        card.innerHTML = `
            <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                <span>Stage ${idx + 1}</span>
                <span class="text-slate-500">Step ${idx + 1}/4</span>
            </div>
            <div class="text-sm font-bold text-white">${st.name}</div>
            <div class="text-2xl font-black text-indigo-400 font-mono">${Number(st.count).toLocaleString()}</div>
            ${convInfo}
        `;
        container.appendChild(card);
    });
}

// 6. Render Bottlenecks & Leaks
function renderBottlenecks(audit) {
    const bottlenecks = audit.bottlenecks || [];
    const list = document.getElementById('bottlenecks-list');
    list.innerHTML = '';

    document.getElementById('tab-leak-count').textContent = bottlenecks.length;

    let totalBleed = 0;
    bottlenecks.forEach(b => totalBleed += (b.impact_monthly_dollars || 0));

    document.getElementById('total-bleed-amount').textContent = `-$${totalBleed.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}/mo`;
    document.getElementById('total-bleed-annual').textContent = `-$${(totalBleed * 12).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}/yr`;

    if (bottlenecks.length === 0) {
        list.innerHTML = `<div class="p-8 text-center text-xs text-slate-400">No critical leaks detected! Pipeline operating at peak efficiency.</div>`;
        return;
    }

    bottlenecks.forEach(b => {
        const item = document.createElement('div');
        item.className = "bg-slate-900/80 border border-slate-800 p-5 rounded-xl space-y-3 relative overflow-hidden";
        
        let sevBadge = b.severity === 'CRITICAL' 
            ? '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">CRITICAL LEAK</span>'
            : '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">OPTIMIZATION GAP</span>';

        item.innerHTML = `
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div class="flex items-center space-x-2">
                    ${sevBadge}
                    <h3 class="text-sm font-bold text-white">${b.title}</h3>
                </div>
                <div class="text-xs font-mono font-bold text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded border border-rose-500/20">
                    Bleed: -$${Number(b.impact_monthly_dollars || 0).toLocaleString()}/mo
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-1">
                <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80">
                    <strong class="text-slate-300 block mb-1">🔍 Diagnostic Root Cause:</strong>
                    <span class="text-slate-400 leading-relaxed">${b.diagnosis}</span>
                </div>
                <div class="bg-indigo-950/30 p-3 rounded-lg border border-indigo-900/40">
                    <strong class="text-indigo-300 block mb-1">⚡ Prescribed AI Intervention:</strong>
                    <span class="text-indigo-200/90 leading-relaxed">${b.ai_recommendation}</span>
                </div>
            </div>
        `;
        list.appendChild(item);
    });
}

// 7. Render Assured Growth Plan
function renderGrowthProjections(growth) {
    const proj = growth.projections || {};
    const cons = proj.conservative || {};
    const target = proj.target || {};
    const agg = proj.aggressive || {};

    document.getElementById('proj-cons-arr').textContent = '$' + Number(cons.projected_arr || 0).toLocaleString();
    document.getElementById('proj-cons-gain').textContent = `+$${Number(cons.monthly_gain || 0).toLocaleString()}/mo (+${cons.percentage_increase || 0}% ARR)`;

    document.getElementById('proj-target-arr').textContent = '$' + Number(target.projected_arr || 0).toLocaleString();
    document.getElementById('proj-target-gain').textContent = `+$${Number(target.monthly_gain || 0).toLocaleString()}/mo (+${target.percentage_increase || 0}% ARR)`;

    document.getElementById('proj-agg-arr').textContent = '$' + Number(agg.projected_arr || 0).toLocaleString();
    document.getElementById('proj-agg-gain').textContent = `+$${Number(agg.monthly_gain || 0).toLocaleString()}/mo (+${agg.percentage_increase || 0}% ARR)`;

    // Revenue Levers
    const levers = growth.revenue_levers || [];
    const levContainer = document.getElementById('levers-container');
    levContainer.innerHTML = '';
    levers.forEach(l => {
        const card = document.createElement('div');
        card.className = "bg-slate-950/60 border border-slate-800 p-4 rounded-xl space-y-1.5";
        card.innerHTML = `
            <div class="flex justify-between items-center text-xs">
                <span class="font-bold text-slate-200">${l.lever}</span>
                <span class="text-emerald-400 font-mono font-bold">+$${Number(l.monthly_impact).toLocaleString()}/mo</span>
            </div>
            <div class="text-[11px] text-slate-400">${l.description}</div>
            <div class="text-[10px] text-slate-500 pt-1">Implementation Effort: <strong class="text-slate-300">${l.difficulty}</strong></div>
        `;
        levContainer.appendChild(card);
    });
}

// 8. Render Phased Action Roadmap
function renderRoadmap(growth) {
    const roadmap = growth.roadmap || [];
    const container = document.getElementById('roadmap-container');
    container.innerHTML = '';

    roadmap.forEach(phase => {
        const pCard = document.createElement('div');
        pCard.className = "bg-slate-950/60 border border-slate-800 p-4 rounded-xl space-y-3";
        
        const actionsHtml = phase.actions.map(act => `
            <li class="flex items-start space-x-2 text-xs text-slate-300">
                <span class="text-indigo-400 mt-0.5">•</span>
                <span>${act}</span>
            </li>
        `).join('');

        pCard.innerHTML = `
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-800/80 pb-2">
                <span class="text-xs font-bold text-white">${phase.phase}</span>
                <span class="text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">${phase.expected_impact}</span>
            </div>
            <div class="text-xs text-slate-400 font-medium">Core Objective: <span class="text-indigo-300">${phase.focus}</span></div>
            <ul class="space-y-1.5 pl-1">
                ${actionsHtml}
            </ul>
        `;
        container.appendChild(pCard);
    });
}

// 9. Render Tactical Playbooks & Scripts
function renderPlaybooks(growth) {
    const playbooks = growth.tactical_playbooks || [];
    const container = document.getElementById('playbooks-container');
    container.innerHTML = '';

    playbooks.forEach(pb => {
        const card = document.createElement('div');
        card.className = "bg-slate-950/70 border border-slate-800 p-4 rounded-xl space-y-2.5 flex flex-col justify-between";
        card.innerHTML = `
            <div class="space-y-1.5">
                <div class="flex items-center justify-between text-xs">
                    <span class="font-bold text-slate-200">${pb.name}</span>
                    <span class="text-[10px] text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded font-mono">${pb.channel}</span>
                </div>
                <div class="text-[11px] text-slate-400">Trigger: ${pb.trigger}</div>
                <div class="bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs font-mono text-slate-200 whitespace-pre-wrap selection:bg-indigo-600">
${pb.template}
                </div>
            </div>
            <div class="text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
                💡 <strong class="text-slate-300">Why it works:</strong> ${pb.why_it_works}
            </div>
        `;
        container.appendChild(card);
    });
}

// 10. Render Software Recommendations
function renderSoftware(softwareList) {
    const grid = document.getElementById('software-grid');
    grid.innerHTML = '';

    softwareList.forEach(sw => {
        const card = document.createElement('div');
        card.className = "glow-card bg-slate-900/80 border border-slate-800 rounded-xl p-5 flex flex-col justify-between space-y-4";
        card.setAttribute('data-category', sw.category);

        const featuresHtml = sw.key_features.slice(0, 3).map(f => `
            <li class="flex items-start space-x-1.5 text-[11px] text-slate-300">
                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0"></i>
                <span>${f}</span>
            </li>
        `).join('');

        card.innerHTML = `
            <div class="space-y-3">
                <div class="flex justify-between items-start">
                    <div>
                        <span class="text-[10px] uppercase font-bold text-indigo-400 tracking-wider">${sw.category}</span>
                        <h4 class="text-base font-bold text-white flex items-center space-x-2">
                            <span>${sw.name}</span>
                            ${sw.already_in_use ? '<span class="text-[10px] font-medium bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">In Current Stack</span>' : ''}
                        </h4>
                    </div>
                    <div class="text-right">
                        <span class="text-xs font-black text-indigo-300 bg-indigo-500/20 border border-indigo-500/30 px-2 py-0.5 rounded-full font-mono">
                            ${sw.fit_score}% Fit
                        </span>
                    </div>
                </div>

                <p class="text-xs text-slate-300 leading-relaxed">${sw.tagline}</p>

                <div class="p-2.5 rounded-lg bg-indigo-950/30 border border-indigo-900/30 text-[11px] text-indigo-200">
                    🎯 <strong>Why Recommended:</strong> ${sw.recommendation_reason}
                </div>

                <div class="space-y-1.5 pt-1">
                    <span class="text-[11px] font-semibold text-slate-400 block">Core Capabilities:</span>
                    <ul class="space-y-1">
                        ${featuresHtml}
                    </ul>
                </div>
            </div>

            <div class="pt-3 border-t border-slate-800/80 space-y-2">
                <div class="flex justify-between items-center text-[11px] text-slate-400">
                    <span>Pricing: <strong class="text-slate-200">${sw.startup_pricing.split(';')[0]}</strong></span>
                    <span>ROI: <strong class="text-emerald-400">${sw.roi_multiplier}</strong></span>
                </div>
                <div class="flex justify-between items-center text-[11px] text-slate-400">
                    <span>Setup: <strong class="text-slate-300">${sw.setup_time}</strong></span>
                    <a href="${sw.website}" target="_blank" class="text-indigo-400 hover:text-indigo-300 flex items-center space-x-1 font-medium">
                        <span>Visit Tool</span>
                        <i data-lucide="external-link" class="w-3 h-3"></i>
                    </a>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    if (window.lucide) {
        lucide.createIcons();
    }
}

// 11. Render Markdown Memo
function renderMemo(memoText) {
    const memoContainer = document.getElementById('memo-content');
    // Simple markdown conversion for bold, headers, and bullet points
    let html = memoText
        .replace(/^### (.*$)/gim, '<h3 class="text-base font-bold text-white mt-3 mb-1">$1</h3>')
        .replace(/^#### (.*$)/gim, '<h4 class="text-sm font-semibold text-indigo-300 mt-2 mb-1">$1</h4>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em class="text-slate-300">$1</em>')
        .replace(/^\s*\-\s(.*$)/gim, '<li class="ml-4 list-disc text-slate-300 my-0.5">$1</li>')
        .replace(/^\s*\d\.\s(.*$)/gim, '<li class="ml-4 list-decimal text-slate-300 my-0.5">$1</li>')
        .replace(/\n\n/g, '<p class="my-2 text-slate-300 leading-relaxed"></p>');
    memoContainer.innerHTML = html;
}

// Tab Switching
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    const targetTab = document.getElementById(`tab-${tabId}`);
    if (targetTab) {
        targetTab.classList.remove('hidden');
        targetTab.classList.add('animate-fade-in');
    }

    event.currentTarget.classList.add('active');
}

// Software Category Filter
function filterSoftware(category) {
    document.querySelectorAll('.sw-filter-btn').forEach(btn => {
        btn.classList.remove('bg-indigo-600', 'text-white', 'active');
        btn.classList.add('bg-slate-900', 'text-slate-300');
    });
    event.currentTarget.classList.add('bg-indigo-600', 'text-white', 'active');
    event.currentTarget.classList.remove('bg-slate-900', 'text-slate-300');

    const cards = document.querySelectorAll('#software-grid .glow-card');
    cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

// Interactive Simulation Updates
async function updateSimulation() {
    const convLift = parseFloat(document.getElementById('slider-conv').value);
    const churnRed = parseFloat(document.getElementById('slider-churn').value);
    const priceLift = parseFloat(document.getElementById('slider-price').value);

    document.getElementById('val-conv').textContent = `+${convLift}%`;
    document.getElementById('val-churn').textContent = `+${churnRed}%`;
    document.getElementById('val-price').textContent = `+${priceLift}%`;

    try {
        const res = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversion_lift_pct: convLift,
                churn_reduction_pct: churnRed,
                price_lift_pct: priceLift
            })
        });
        const sim = await res.json();

        document.getElementById('sim-arr-val').textContent = '$' + Number(sim.simulated_arr).toLocaleString();
        document.getElementById('sim-net-annual').textContent = `+$${Number(sim.net_annual_increase).toLocaleString()}/yr (+${sim.total_percentage_growth}%)`;
        document.getElementById('sim-monthly-val').textContent = '$' + Number(sim.simulated_mrr).toLocaleString() + '/mo';
    } catch (err) {
        console.error("Simulation error:", err);
    }
}

function resetSimulation() {
    document.getElementById('slider-conv').value = 0;
    document.getElementById('slider-churn').value = 0;
    document.getElementById('slider-price').value = 0;
    updateSimulation();
}

// Sample Dataset Loader
async function loadSampleDataset(datasetId) {
    document.querySelectorAll('#btn-saas, #btn-ecommerce, #btn-agency').forEach(b => {
        b.className = 'px-2.5 py-1 rounded font-medium transition text-slate-400 hover:text-white';
    });
    const activeBtn = document.getElementById(`btn-${datasetId}`);
    if (activeBtn) {
        activeBtn.className = 'px-2.5 py-1 rounded font-medium transition bg-indigo-600 text-white';
    }

    try {
        const res = await fetch(`/api/audit/load-sample/${datasetId}`, { method: 'POST' });
        const data = await res.json();
        currentAuditData = data.audit;
        currentGrowthData = data.growth;
        currentSoftwareData = data.software;
        renderAll(data);
    } catch (err) {
        console.error("Failed to load sample dataset:", err);
    }
}

// Interactive Chat with AI Copilot
async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';
    const messages = document.getElementById('chat-messages');

    // Add user bubble
    const userBubble = document.createElement('div');
    userBubble.className = "flex items-start justify-end space-x-2";
    userBubble.innerHTML = `
        <div class="bg-indigo-600 text-white p-3 rounded-lg max-w-[85%] leading-relaxed">${msg}</div>
        <div class="w-6 h-6 rounded-md bg-slate-700 flex-shrink-0 flex items-center justify-center text-[10px] font-bold">You</div>
    `;
    messages.appendChild(userBubble);
    messages.scrollTop = messages.scrollHeight;

    // Loading indicator
    const loadingBubble = document.createElement('div');
    loadingBubble.id = 'chat-loading';
    loadingBubble.className = "flex items-start space-x-2";
    loadingBubble.innerHTML = `
        <div class="w-6 h-6 rounded-md bg-indigo-600 flex-shrink-0 flex items-center justify-center text-[10px] font-bold">AI</div>
        <div class="bg-slate-800 p-3 rounded-lg text-slate-400 max-w-[85%] flex items-center space-x-1.5">
            <span class="animate-pulse">Analyzing audit telemetry & drafting strategic response...</span>
        </div>
    `;
    messages.appendChild(loadingBubble);
    messages.scrollTop = messages.scrollHeight;

    try {
        const res = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();

        const loadEl = document.getElementById('chat-loading');
        if (loadEl) loadEl.remove();

        const aiBubble = document.createElement('div');
        aiBubble.className = "flex items-start space-x-2";
        
        let formattedReply = data.reply
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');

        aiBubble.innerHTML = `
            <div class="w-6 h-6 rounded-md bg-indigo-600 flex-shrink-0 flex items-center justify-center text-[10px] font-bold">AI</div>
            <div class="bg-slate-800/90 p-3 rounded-lg text-slate-200 border border-slate-700 max-w-[85%] leading-relaxed">${formattedReply}</div>
        `;
        messages.appendChild(aiBubble);
        messages.scrollTop = messages.scrollHeight;
    } catch (err) {
        console.error("Chat error:", err);
    }
}

function handleChatKey(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

// Upload Modal Logic
function openUploadModal() {
    document.getElementById('upload-modal').classList.remove('hidden');
}
function closeUploadModal() {
    document.getElementById('upload-modal').classList.add('hidden');
}
function updateFileName(input) {
    if (input.files && input.files[0]) {
        document.getElementById('file-label').textContent = input.files[0].name;
    }
}

async function handleUploadSubmit(event) {
    event.preventDefault();
    const form = document.getElementById('upload-form');
    const formData = new FormData(form);
    const btn = document.getElementById('upload-btn');
    btn.disabled = true;
    btn.innerHTML = '<span>Running AI Audit Engine...</span>';

    try {
        const res = await fetch('/api/audit/upload', {
            method: 'POST',
            body: formData
        });
        if (!res.ok) {
            const err = await res.json();
            alert(`Audit error: ${err.detail || 'Could not parse sales report'}`);
            btn.disabled = false;
            btn.innerHTML = '<span>Run Full AI Audit</span>';
            return;
        }

        const data = await res.json();
        currentAuditData = data.audit;
        currentGrowthData = data.growth;
        currentSoftwareData = data.software;
        renderAll(data);
        closeUploadModal();
        switchTab('overview');
    } catch (err) {
        alert("Upload failed: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>Run Full AI Audit</span>';
    }
}

// Pricing & Subscription Modal Logic
function openPricingModal() {
    document.getElementById('pricing-modal').classList.remove('hidden');
    fetchBillingStatus();
}
function closePricingModal() {
    document.getElementById('pricing-modal').classList.add('hidden');
}

async function fetchBillingStatus() {
    try {
        const res = await fetch('/api/billing/plans');
        const data = await res.json();
        const tier = data.active_tier || 'growth_pro';
        const label = document.getElementById('header-tier-label');
        if (label) {
            label.textContent = tier === 'growth_pro' ? 'Growth Pro' : (tier === 'agency_whitelabel' ? 'Agency White-Label' : 'Free Plan');
        }
    } catch (e) {
        console.error("Billing fetch error:", e);
    }
}

async function upgradePlan(planId) {
    try {
        const res = await fetch('/api/billing/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plan_id: planId })
        });
        const data = await res.json();
        if (data.mode === 'stripe' && data.checkout_url) {
            window.location.href = data.checkout_url;
        } else {
            alert(`🎉 ${data.message || 'Subscription updated to ' + planId}`);
            fetchBillingStatus();
            closePricingModal();
        }
    } catch (e) {
        alert("Billing error: " + e.message);
    }
}

async function saveWhiteLabelConfig() {
    const agencyName = document.getElementById('agency-name-input').value.trim();
    const logoUrl = document.getElementById('agency-logo-input').value.trim();
    try {
        await fetch('/api/billing/whitelabel-config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ agency_name: agencyName, agency_logo_url: logoUrl })
        });
        alert(`✅ Agency branding saved! Reports will now be branded under "${agencyName}".`);
    } catch (e) {
        alert("Failed to save branding: " + e.message);
    }
}

