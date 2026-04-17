import streamlit as st
from orchestrator import run_agent_loop

# ── API KEYS — replace with your actual keys ──────────────────────────────────
OPENAI_API_KEY      = ""      
FOURSQUARE_API_KEY  = ""           # Your Foursquare API key (from developer.foursquare.com)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Planner India",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Full CSS — warm, vibrant, light theme ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#fff8f0 0%,#fef3e8 50%,#fff5f0 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg,#ff6b35 0%,#ff9a5c 60%,#ffb347 100%);
    border-radius: 24px; padding: 48px 56px;
    margin-bottom: 28px; position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(255,107,53,0.28);
}
.hero::before {
    content:"✈"; position:absolute; right:56px; top:16px;
    font-size:130px; opacity:0.11; transform:rotate(-18deg);
}
.hero h1 {
    font-family:'Playfair Display',serif !important;
    font-size:2.8rem !important; font-weight:900 !important;
    color:#fff !important; margin:0 0 6px 0 !important;
    text-shadow:0 2px 14px rgba(0,0,0,0.18); line-height:1.1 !important;
}
.hero p { color:rgba(255,255,255,0.9) !important; font-size:1.05rem !important; margin:0 !important; }
.badge {
    display:inline-block; background:rgba(255,255,255,0.22);
    color:#fff; border-radius:20px; padding:4px 14px;
    font-size:0.8rem; font-weight:700; margin:12px 6px 0 0;
    border:1px solid rgba(255,255,255,0.38); letter-spacing:0.04em;
}

/* ── Input card ── */
.input-card {
    background:#fff; border-radius:20px; padding:28px 32px;
    box-shadow:0 4px 24px rgba(255,107,53,0.09);
    border:1px solid rgba(255,107,53,0.12); margin-bottom:20px;
}
.input-card h3 {
    font-family:'Playfair Display',serif !important;
    color:#2d1b0e !important; font-size:1.3rem !important;
    margin:0 0 18px 0 !important;
}

/* Streamlit widget overrides */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border:2px solid #ffe0cc !important; border-radius:12px !important;
    padding:10px 16px !important; font-family:'DM Sans',sans-serif !important;
    background:#fffaf7 !important; color:#2d1b0e !important;
    transition:border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color:#ff6b35 !important;
    box-shadow:0 0 0 3px rgba(255,107,53,0.13) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label {
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
    color:#5c3317 !important; font-size:0.88rem !important;
    text-transform:uppercase; letter-spacing:0.06em;
}

/* Button */
[data-testid="stButton"] > button {
    background:linear-gradient(135deg,#ff6b35,#e8420a) !important;
    color:#fff !important; border:none !important; border-radius:14px !important;
    padding:14px 32px !important; font-family:'DM Sans',sans-serif !important;
    font-size:1.05rem !important; font-weight:700 !important;
    box-shadow:0 8px 28px rgba(255,107,53,0.38) !important;
    width:100% !important; transition:all 0.2s !important;
}
[data-testid="stButton"] > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 12px 36px rgba(255,107,53,0.48) !important;
}

/* Section heading */
.sec-head {
    font-family:'Playfair Display',serif; font-size:1.7rem;
    font-weight:800; color:#2d1b0e; margin:32px 0 14px;
    padding-bottom:8px; border-bottom:3px solid #ff6b35;
    display:inline-block;
}

/* Stats row */
.stats-row { display:flex; gap:14px; margin-bottom:24px; flex-wrap:wrap; }
.stat-chip {
    background:#fff; border-radius:14px; padding:14px 20px;
    border:1px solid #ffe0cc; font-family:'DM Sans',sans-serif;
    text-align:center; flex:1; min-width:110px;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
}
.stat-chip .sv { font-size:1.35rem; font-weight:700; color:#ff6b35; display:block; }
.stat-chip .sl { font-size:0.75rem; color:#7a5c46; font-weight:600;
                  text-transform:uppercase; letter-spacing:0.05em; }

/* Plan cards */
.pc {
    background:#fff; border-radius:18px; padding:22px 26px;
    margin-bottom:14px; box-shadow:0 3px 18px rgba(0,0,0,0.07);
    border:1px solid #ffe8d6; transition:transform 0.2s;
}
.pc:hover { transform:translateY(-2px); }
.pc-title {
    font-family:'Playfair Display',serif; font-size:1.05rem;
    font-weight:700; color:#ff6b35; margin:0 0 10px;
}
.pc-main { font-size:1.05rem; font-weight:600; color:#2d1b0e; margin-bottom:5px; }
.pc-sub  { font-size:0.88rem; color:#7a5c46; margin:3px 0; }
.pc-highlight { color:#ff6b35; font-weight:700; font-size:1.08rem; }
.pill {
    display:inline-block; background:#fff0e8; color:#c2410c;
    border-radius:20px; padding:2px 11px; font-size:0.8rem;
    font-weight:600; margin:3px 3px 0 0;
}

/* Place items */
.place-row {
    display:flex; align-items:center; gap:10px; padding:7px 0;
    border-bottom:1px dashed #ffe8d6; font-size:0.93rem; color:#3d2010;
}
.place-row:last-child { border-bottom:none; }
.pdot { width:7px; height:7px; border-radius:50%; background:#ff6b35; flex-shrink:0; }

/* Budget card */
.bc {
    background:linear-gradient(135deg,#fff8f0,#fff);
    border-radius:18px; padding:22px 26px;
    box-shadow:0 4px 20px rgba(255,107,53,0.1);
    border:2px solid #ffd4b8; margin-bottom:14px;
}
.br {
    display:flex; justify-content:space-between; padding:8px 0;
    border-bottom:1px solid #fff0e8; font-size:0.93rem; color:#3d2010;
}
.br:last-child { border-bottom:none; }
.br.tr {
    font-weight:700; font-size:1.08rem; color:#2d1b0e;
    padding-top:12px; border-top:2px solid #ff6b35; border-bottom:none;
}
.ba { font-weight:600; color:#c2410c; }

/* Status */
.s-ok {
    background:linear-gradient(135deg,#dcfce7,#bbf7d0);
    border-radius:13px; padding:15px 18px; border-left:5px solid #16a34a;
    font-weight:700; font-size:1.05rem; color:#14532d; margin-top:10px;
}
.s-over {
    background:linear-gradient(135deg,#fef3c7,#fde68a);
    border-radius:13px; padding:15px 18px; border-left:5px solid #d97706;
    font-weight:700; font-size:1.05rem; color:#78350f; margin-top:10px;
}

/* Log steps */
.ls {
    display:flex; align-items:flex-start; gap:10px; padding:8px 0;
    border-bottom:1px solid #fff0e8; font-size:0.9rem; color:#3d2010; line-height:1.5;
}
.ls:last-child { border-bottom:none; }
.lb {
    display:inline-block; border-radius:6px; padding:2px 9px;
    font-size:0.73rem; font-weight:700; letter-spacing:0.07em;
    white-space:nowrap; min-width:76px; text-align:center; flex-shrink:0;
}
.lt { background:#dbeafe; color:#1d4ed8; }
.la { background:#fed7aa; color:#c2410c; }
.lo { background:#dcfce7; color:#15803d; }
.lr { background:#fce7f3; color:#be185d; }

/* Expander */
[data-testid="stExpander"] {
    border:1px solid #ffe0cc !important; border-radius:14px !important;
    background:#fff !important; margin-bottom:8px !important;
}

/* Places source badge */
.src-badge {
    display:inline-block; border-radius:10px; padding:2px 10px;
    font-size:0.73rem; font-weight:700; margin-left:8px;
}
.src-foursquare { background:#e0f2fe; color:#0369a1; }
.src-curated    { background:#f0fdf4; color:#15803d; }
.src-generic    { background:#fef9c3; color:#854d0e; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Agentic AI Travel Planner — India</h1>
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────

c1, c2 = st.columns(2)
with c1:
    source = st.text_input(" From City", placeholder="e.g. Hyderabad, Pune, Delhi")
with c2:
    destination = st.text_input("To City", placeholder="e.g. Manali, Goa, Jaipur")

c3, c4 = st.columns(2)
with c3:
    budget = st.number_input("Total Budget (₹)", min_value=2000,
                              max_value=200000, value=15000, step=500)
with c4:
    days = st.slider(" Number of Days", min_value=1, max_value=30, value=5)

st.markdown("</div>", unsafe_allow_html=True)

go = st.button("Plan My Trip !", use_container_width=True)

# ── Run ───────────────────────────────────────────────────────────────────────
if go:
    if not source.strip():
        st.error("Please enter a source city."); st.stop()
    if not destination.strip():
        st.error("Please enter a destination city."); st.stop()
    if source.strip().lower() == destination.strip().lower():
        st.error("Source and destination must be different."); st.stop()

    with st.spinner("Agents are working... (20–40 seconds)"):
        try:
            final_plan, logs = run_agent_loop(
                source.strip(), destination.strip(),
                budget, days, OPENAI_API_KEY, FOURSQUARE_API_KEY
            )
        except Exception as e:
            st.error(f"Error: {e}"); st.exception(e); st.stop()

    st.success("Trip planned!")

    # Pull data
    validation  = final_plan.get("validation", {})
    transport   = final_plan.get("transport") or {}
    hotel_data  = final_plan.get("hotel") or {}
    hotel_rec   = hotel_data.get("recommended", hotel_data) if isinstance(hotel_data, dict) else {}
    places      = final_plan.get("places") or []
    breakdown   = final_plan.get("budget_breakdown") or {}
    total_cost  = validation.get("total_cost", 0)
    within_b    = validation.get("within_budget", False)
    diff        = validation.get("difference", 0)
    t_mode      = transport.get("mode", "N/A").title()
    t_dur       = transport.get("duration_hours", 0)
    t_cost      = transport.get("cost", 0)
    num_iters   = len(set(l.get("iteration", 0) for l in logs))
    places_src  = final_plan.get("places_source", "generic")

    # ── Stats strip ──────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="stats-row">
  <div class="stat-chip"><span class="sv">₹{total_cost:,}</span><span class="sl">Total Cost</span></div>
  <div class="stat-chip"><span class="sv">{t_mode}</span><span class="sl">Transport</span></div>
  <div class="stat-chip"><span class="sv">{t_dur}h</span><span class="sl">Travel Time</span></div>
  <div class="stat-chip"><span class="sv">{len(places)}</span><span class="sl">Places Found</span></div>
  <div class="stat-chip"><span class="sv">{num_iters}</span><span class="sl">Iterations</span></div>
  <div class="stat-chip"><span class="sv">{'✅' if within_b else '⚠️'}</span><span class="sl">{'In Budget' if within_b else 'Over Budget'}</span></div>
</div>
""", unsafe_allow_html=True)

    # ── Agent Reasoning ───────────────────────────────────────────────────────
    st.markdown('<div class="sec-head"> Agent Reasoning</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-family:DM Sans,sans-serif;color:#7a5c46;margin-bottom:14px;font-size:0.93rem'>Each iteration shows how GPT thinks, which agent it calls, what it observes, and how it replans</p>", unsafe_allow_html=True)

    iters = {}
    for lg in logs:
        k = lg.get("iteration", 0)
        iters.setdefault(k, []).append(lg)

    badge_cfg = {
        "THINK":   ("THINK",   "lt"),
        "ACT":     ("ACT",     "la"),
        "OBSERVE": ("OBSERVE", "lo"),
        "REPLAN":  ("REPLAN",  "lr"),
    }

    for it_n in sorted(iters.keys()):
        lbl = "🔰 Start" if it_n == 0 else f" Iteration {it_n}"
        with st.expander(lbl, expanded=(it_n <= 1)):
            rows = ""
            for lg in iters[it_n]:
                step    = lg.get("step","")
                content = lg.get("content","")
                btxt, bcls = badge_cfg.get(step, (step, "lt"))
                rows += f'<div class="ls"><span class="lb {bcls}">{btxt}</span><span>{content}</span></div>'
            st.markdown(rows, unsafe_allow_html=True)

    # ── Final Plan ────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">📋 Your Travel Plan</div>', unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        # Transport
        if transport:
            icon = {"train":"🚂","flight":"✈️","bus":"🚌"}.get(transport.get("mode",""),"🚗")
            st.markdown(f"""
<div class="pc">
  <div class="pc-title">{icon} Transport</div>
  <div class="pc-main">{t_mode} &nbsp;·&nbsp; {source.title()} → {destination.title()}</div>
  <p class="pc-sub"> Duration: <b>{t_dur} hours</b></p>
  <p class="pc-sub"> Cost: <span class="pc-highlight">₹{t_cost:,}</span></p>
</div>
""", unsafe_allow_html=True)

        # Hotel
        if hotel_rec and hotel_rec.get("name"):
            stars   = "⭐" * hotel_rec.get("stars", 0)
            price   = hotel_rec.get("price_per_night", 0)
            amenity_pills = "".join([f'<span class="pill">{a}</span>' for a in hotel_rec.get("amenities",[])])
            stretch = ' <span style="color:#d97706;font-size:0.8rem">⚠️ Budget stretch</span>' if hotel_data.get("budget_stretch") else ""
            st.markdown(f"""
<div class="pc">
  <div class="pc-title">🏨 Hotel{stretch}</div>
  <div class="pc-main">{hotel_rec.get("name","N/A")} {stars}</div>
  <p class="pc-sub">₹{price:,}/night × {days} nights = <span class="pc-highlight">₹{price*days:,}</span></p>
  <div style="margin-top:10px">{amenity_pills}</div>
</div>
""", unsafe_allow_html=True)

        # Places — with source badge
        if places:
            src_map = {
                "foursquare": ("🌐 Foursquare Live", "src-foursquare"),
                "curated":    ("📝 Curated List",    "src-curated"),
                "generic":    ("📋 Generic List",    "src-generic"),
            }
            src_lbl, src_cls = src_map.get(places_src, ("📋 Generic List", "src-generic"))
            rows = "".join([f'<div class="place-row"><div class="pdot"></div>{p}</div>' for p in places])
            st.markdown(f"""
<div class="pc">
  <div class="pc-title">📍 Places to Visit <span class="src-badge {src_cls}">{src_lbl}</span></div>
  {rows}
</div>
""", unsafe_allow_html=True)

    with right:
        # Budget card
        food_c = breakdown.get("food_budget", 0)
        act_c  = breakdown.get("activities_budget", 0)
        t_icon = {"train":"🚂","flight":"✈️","bus":"🚌"}.get(transport.get("mode",""),"🚗")

        st.markdown(f"""
<div class="bc">
  <div class="pc-title" style="margin-bottom:14px">💰 Budget Breakdown</div>
  <div class="br"><span>{t_icon} Transport</span><span class="ba">₹{validation.get('transport_cost',0):,}</span></div>
  <div class="br"><span>🏨 Hotel ({days} nights)</span><span class="ba">₹{validation.get('hotel_cost',0):,}</span></div>
  <div class="br"><span>🍽️ Food (≈₹{food_c//days if days else 0:,}/day)</span><span class="ba">₹{food_c:,}</span></div>
  <div class="br"><span>🎯 Activities</span><span class="ba">₹{act_c:,}</span></div>
  <div class="br tr"><span>Total</span><span>₹{total_cost:,}</span></div>
  <div class="br" style="border:none;opacity:0.65"><span>Your Budget</span><span>₹{budget:,}</span></div>
</div>
""", unsafe_allow_html=True)

        if within_b:
            st.markdown(f'<div class="s-ok">✅ Within Budget!<br><span style="font-weight:500;font-size:0.9rem">You save ₹{diff:,} 🎉</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="s-over">⚠️ Over Budget<br><span style="font-weight:500;font-size:0.9rem">Over by ₹{diff:,}</span></div>', unsafe_allow_html=True)

        realloc = breakdown.get("reallocation_log", [])
        if realloc:
            with st.expander("📝 Reallocation Notes"):
                for note in realloc:
                    st.markdown(f'<div style="font-family:DM Sans,sans-serif;font-size:0.87rem;color:#5c3317;padding:5px 0;border-bottom:1px solid #ffe8d6">🔄 {note}</div>', unsafe_allow_html=True)

    st.markdown("""
<div style="text-align:center;margin-top:40px;padding:20px;
font-family:DM Sans,sans-serif;color:#b08060;font-size:0.83rem">
</div>
""", unsafe_allow_html=True)