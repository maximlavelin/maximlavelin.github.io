#!/usr/bin/env python3
"""Builds the portfolio site: homepage + 5 project pages, sharing one stylesheet."""
import os, math, random

OUT = os.path.dirname(os.path.abspath(__file__))
EMAIL = "maxim.lavelin@live.biu.ac.il"
GH = "https://github.com/maxim-lavelin"

W, H = 210.0, 62.0          # mini-figure viewBox
PAD_L, PAD_R, PAD_T, PAD_B = 4, 4, 6, 8

def _sx(i, n):
    return PAD_L + (W - PAD_L - PAD_R) * (i / max(n - 1, 1))

def _sy(v, lo, hi):
    if hi == lo: hi = lo + 1
    return H - PAD_B - (H - PAD_T - PAD_B) * ((v - lo) / (hi - lo))

def path_from(vals):
    lo, hi = min(vals), max(vals)
    pts = [(_sx(i, len(vals)), _sy(v, lo, hi)) for i, v in enumerate(vals)]
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts), pts

def svg_wrap(inner):
    return (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-hidden="true" fill="none">{inner}</svg>')

def baseline():
    return (f'<line x1="{PAD_L}" y1="{H-PAD_B:.0f}" x2="{W-PAD_R:.0f}" y2="{H-PAD_B:.0f}" '
            f'stroke="#DCE1E8" stroke-width="1"/>')

# ---- Fig 1: NYC taxi diurnal demand curve (real shape from the report) ----
def fig_taxi():
    demand = [3250,2100,1300,820,700,760,1600,3120,4300,4620,5000,5400,
              5760,6000,6220,6800,6860,7000,8100,7120,6500,6460,6060,4700]
    d, pts = path_from(demand)
    area = d + f" L {pts[-1][0]:.1f},{H-PAD_B} L {pts[0][0]:.1f},{H-PAD_B} Z"
    peak = max(range(len(demand)), key=lambda i: demand[i])
    px, py = pts[peak]
    return svg_wrap(
        baseline() +
        f'<path d="{area}" fill="#1F77B4" fill-opacity=".10"/>'
        f'<path d="{d}" stroke="#1F77B4" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="#FF7F0E"/>'
    )

# ---- Fig 2: ROC curve ----
def fig_roc():
    fpr = [i/40 for i in range(41)]
    tpr = [1 - math.exp(-7.5*f) for f in fpr]
    pts = [(PAD_L + (W-PAD_L-PAD_R)*f, H-PAD_B - (H-PAD_T-PAD_B)*t) for f, t in zip(fpr, tpr)]
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = d + f" L {W-PAD_R},{H-PAD_B} L {PAD_L},{H-PAD_B} Z"
    return svg_wrap(
        baseline() +
        f'<line x1="{PAD_L}" y1="{H-PAD_B}" x2="{W-PAD_R}" y2="{PAD_T}" '
        f'stroke="#C6CDD6" stroke-width="1" stroke-dasharray="3 3"/>'
        f'<path d="{area}" fill="#1F77B4" fill-opacity=".10"/>'
        f'<path d="{d}" stroke="#1F77B4" stroke-width="1.7"/>'
    )

# ---- Fig 3: RFM cluster scatter ----
def fig_clusters():
    random.seed(7)
    cents = [(55,20,"#1F77B4"), (105,38,"#FF7F0E"), (160,16,"#2CA02C")]
    dots = []
    for cx, cy, col in cents:
        for _ in range(16):
            x = cx + random.gauss(0, 15); y = cy + random.gauss(0, 7)
            x = max(PAD_L+2, min(W-PAD_R-2, x)); y = max(PAD_T, min(H-PAD_B-2, y))
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{col}" fill-opacity=".65"/>')
        dots.append(f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="none" stroke="{col}" stroke-width="1.3"/>')
    return svg_wrap(baseline() + "".join(dots))

# ---- Fig 4: spatial hot-spot grid (Getis-Ord style) ----
def fig_hotspot():
    random.seed(3)
    cells, cw, ch = [], 13.5, 11.5
    cols, rows = 15, 4
    ox = PAD_L + 2
    oy = PAD_T
    for r in range(rows):
        for c in range(cols):
            # cold cluster left, hot cluster right-centre
            d_hot = math.hypot(c-10, r-1.6); d_cold = math.hypot(c-3, r-2.4)
            z = 2.4/(1+d_hot*0.8) - 1.9/(1+d_cold*0.8) + random.gauss(0,.18)
            if z > .45:   fill, op = "#FF7F0E", min(.85, .35+z*.6)
            elif z < -.35: fill, op = "#1F77B4", min(.8, .3+abs(z)*.6)
            else:          fill, op = "#B9C2CD", .28
            cells.append(f'<rect x="{ox+c*cw:.1f}" y="{oy+r*ch:.1f}" width="{cw-1.6:.1f}" '
                         f'height="{ch-1.6:.1f}" fill="{fill}" fill-opacity="{op:.2f}"/>')
    return svg_wrap("".join(cells))

# ---- Fig 5: DBSCAN — dense core + flagged outliers ----
def fig_dbscan():
    random.seed(11)
    dots = []
    for _ in range(46):
        x = random.gauss(78, 26); y = random.gauss(34, 9)
        x = max(PAD_L+2, min(W-PAD_R-2, x)); y = max(PAD_T, min(H-PAD_B-2, y))
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="#1F77B4" fill-opacity=".55"/>')
    for x, y in [(168,14),(182,40),(158,44),(192,22),(174,52)]:
        dots.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="none" stroke="#FF7F0E" stroke-width="1.4"/>')
    return svg_wrap(baseline() + "".join(dots))

# ============================================================
PROJECTS = [
    {
        "slug":"nyc-taxi", "fig":"Fig. 01",
        "domain":"Time-series forecasting · Independent project",
        "title":"NYC Taxi Fleet Optimizer",
        "long":"NYC Taxi Fleet Optimizer: Predicting Hourly Urban Demand with Weather Integration",
        "stack":"Linear Regression · XGBoost · Lag features · Chronological validation",
        "chart": fig_taxi, "cap":"Mean demand by hour, 2024",
        "result":"XGBoost cut mean absolute error <b>~25%</b> below the linear baseline (728 → 546 rides/hr) on a strict chronological hold-out.",
        "meta":["Bar-Ilan University","2024 TLC + NOAA data","Individual project"],
        "callout":"XGBoost reduced Mean Absolute Error by <b>~25%</b> over a linear baseline (728.43 → 546.19 rides per hour) on a strictly chronological hold-out — with the largest gains during peak-hour demand, exactly when accurate forecasting matters most operationally.",
        "tags":["Python","pandas","scikit-learn","XGBoost","Time-series feature engineering","Chronological validation"],
        "dl":[("Full report (PDF)","../assets/NYC_TAXI_Lavelin.pdf"),("Notebook (.ipynb)","../assets/NYC_CODE_LAVELIN.ipynb")],
        "sections":[
            ("Problem","<p>NYC taxi demand swings from near zero to over 12,000 rides per hour within a single day. Under-forecasting means long passenger waits and lost revenue; over-forecasting means wasted idle mileage and fuel. I framed this as a supervised regression problem — predict total citywide pickups for a given hour — using a year of NYC TLC trip records merged with JFK weather observations.</p>"),
            ("Data","<ul><li><b>8,616 hourly observations</b> across 2024, aggregated from NYC TLC Yellow Taxi trip records.</li><li>Demand is highly volatile: mean 4,708 rides/hour, standard deviation 2,712, ranging from 0 to 12,757.</li><li>Weather from JFK Airport (NOAA/NCEI), reduced from roughly 125 raw meteorological fields to the two that carried operational signal: continuous temperature and a <b>binary rain indicator</b>. Precipitation intensity did not matter; presence of rain did.</li></ul>"),
            ("Approach","<p>Two models, evaluated identically, so the case for non-linearity is made rather than assumed:</p><ul><li><b>Linear regression baseline</b> — an interpretable additive combination of temporal, weather, and lagged demand features. It captures broad seasonality but structurally cannot model regime-dependent spikes.</li><li><b>XGBoost</b> — gradient-boosted trees, able to learn conditional interactions such as demand responding to weather differently depending on hour of day or recent history.</li></ul><p>Features: hour of day, day of week, weekend flag, temperature, rain flag, and <b>lagged demand</b> (24-hour and 168-hour lags plus rolling means). The lag features turned out to dominate.</p>"),
            ("Evaluation","<p>I used a <b>strict chronological split</b> — train on January–September 2024, validate on October, test on November–December — rather than random k-fold. This mirrors how the model would actually be deployed, predicting the future from only the past, and avoids the leakage a random split would silently introduce.</p><p>MAE was the primary metric because it is directly interpretable as rides per hour. RMSE is reported alongside it to surface large errors, which are disproportionately costly during peaks.</p>"),
            ("Results","<table class=\"metrics\"><tr><th>Model</th><th>MAE (rides/hr)</th><th>RMSE</th></tr><tr><td>Linear regression</td><td class=\"num\">728.43</td><td class=\"num\">993.47</td></tr><tr class=\"best\"><td>XGBoost</td><td class=\"num\">546.19</td><td class=\"num\">810.55</td></tr></table><p>The linear model systematically <b>underestimates peak demand</b> — its additive structure cannot capture the sharp transitions of rush hour. XGBoost tracks both the magnitude and the timing of those swings. Feature importance shows the <b>168-hour (weekly) lag</b> dominating predictive power, followed by the 24-hour lag and hour of day; weather contributes only secondary, contextual signal.</p><!-- FIGURE SLOT: export Figure 5 from the notebook and uncomment\n<figure class=\"fig\"><img src=\"../assets/taxi-actual-vs-predicted.png\" alt=\"Actual vs predicted hourly demand, November 2024\"><figcaption>Actual demand vs. linear and XGBoost projections, November 2024.</figcaption></figure>\n-->"),
            ("Limitations","<p>Weather from a single airport station is a coarse proxy for citywide conditions, and city-level aggregation hides neighbourhood variation — a zone-level model (Manhattan separately from the outer boroughs) would likely outperform this one. I would also fold in event data such as concerts and games to catch non-seasonal demand shocks, currently the hardest cases for the model.</p>"),
        ],
    },
    {
        "slug":"vehicle-safety", "fig":"Fig. 02",
        "domain":"Deep learning · NLP",
        "title":"Vehicle Safety Intelligence",
        "long":"Vehicle Safety Intelligence: Classifying NHTSA Complaints at Scale",
        "stack":"TF-IDF · MLP / CNN / BiLSTM · ROC & PR · Calibration · Bootstrap CIs",
        "chart": fig_roc, "cap":"ROC curve, held-out test set",
        "result":"Classified <b>~300,000</b> NHTSA complaints, comparing MLP, CNN and BiLSTM with calibration and bootstrap confidence intervals rather than a single accuracy number.",
        "meta":["Deep Learning (35374)","May 2026","Final project"],
        "callout":"Trained and compared MLP, CNN and BiLSTM architectures on <b>~300,000</b> NHTSA vehicle safety complaints, reporting ROC and precision-recall curves, calibration, and bootstrap confidence intervals for every metric — not a single point estimate.",
        "tags":["Python","TF-IDF","PyTorch / TensorFlow","MLP","CNN","BiLSTM","Calibration","Bootstrap CIs"],
        "dl":[("Full report (PDF)","#"),("Notebook (.ipynb)","#")],
        "sections":[
            ("Problem","<p>NHTSA receives hundreds of thousands of free-text vehicle safety complaints. Triaging them by hand does not scale. This project builds a text classification pipeline to categorise complaints automatically, comparing progressively more expressive architectures under an evaluation protocol designed to be statistically honest rather than flattering.</p>"),
            ("Data","<ul><li><b>~300,000</b> free-text NHTSA complaint records.</li><li>Text cleaning, tokenisation, and <b>TF-IDF</b> vectorisation as the classical baseline representation.</li><li>[Add: target variable definition — severity class, defect category, or injury flag.]</li></ul>"),
            ("Approach","<p>Three architectures of increasing capacity, to test whether deep sequence models actually earn their cost over a simpler baseline on this task:</p><ul><li><b>MLP</b> on TF-IDF features — fast and interpretable, the bar the others have to clear.</li><li><b>CNN</b> — captures local n-gram-like patterns in complaint text.</li><li><b>BiLSTM</b> — models sequential context across the full complaint narrative.</li></ul>"),
            ("Evaluation","<p>Evaluation deliberately went beyond headline accuracy:</p><ul><li><b>ROC and precision-recall curves</b> — PR matters here because complaint classes are imbalanced, and ROC-AUC alone can look strong on an imbalanced problem.</li><li><b>Calibration analysis</b> — checking whether predicted probabilities are trustworthy, not merely whether the top class is right. A model used for triage needs to be believable when it says 90%.</li><li><b>Bootstrap confidence intervals</b> — quantifying how much each metric would move on a different sample, rather than trusting one split.</li></ul>"),
            ("Results","<table class=\"metrics\"><tr><th>Model</th><th>ROC-AUC</th><th>PR-AUC / F1</th><th>95% CI</th></tr><tr><td>MLP (TF-IDF)</td><td class=\"num\">[value]</td><td class=\"num\">[value]</td><td class=\"num\">[value]</td></tr><tr><td>CNN</td><td class=\"num\">[value]</td><td class=\"num\">[value]</td><td class=\"num\">[value]</td></tr><tr class=\"best\"><td>BiLSTM</td><td class=\"num\">[value]</td><td class=\"num\">[value]</td><td class=\"num\">[value]</td></tr></table><p>[Summarise which model won and why — for example, whether the BiLSTM's gain over the CNN was larger than the bootstrap interval, which is the question that actually decides if the extra complexity is justified.]</p>"),
            ("Limitations","<p>[For example: with more compute I would fine-tune a pretrained transformer as a stronger baseline than TF-IDF + MLP, and test whether it meaningfully beats the BiLSTM given the added inference cost.]</p>"),
        ],
    },
    {
        "slug":"retail-consultant", "fig":"Fig. 03",
        "domain":"Unsupervised learning · Customer analytics",
        "title":"Retail Consultant",
        "long":"Retail Consultant: An End-to-End Customer Analytics Pipeline",
        "stack":"RFM · K-Means / HAC · Apriori · LOF · SVD recommender",
        "chart": fig_clusters, "cap":"Segments in RFM space",
        "result":"One pipeline covering segmentation, cross-sell rules, anomaly detection and recommendations on ~1M Online Retail II transactions.",
        "meta":["Unsupervised Learning","March 2026","Online Retail II"],
        "callout":"Segmented customers into [N] actionable groups using RFM features and clustering, mined association rules for cross-sell, flagged anomalous accounts, and built an SVD recommender — a single pipeline covering segmentation, merchandising and retention.",
        "tags":["Python","pandas","scikit-learn","mlxtend","RFM","K-Means","HAC","Apriori","LOF","SVD"],
        "dl":[("Full report (PDF)","#"),("Notebook (.ipynb)","#")],
        "sections":[
            ("Problem","<p>Retailers sitting on raw transaction logs often cannot answer four basic questions: who are our best customers, what should we cross-sell, which accounts look anomalous, and what should we recommend next. This project builds one pipeline that answers all four, on the Online Retail II dataset from a UK online retailer.</p>"),
            ("Approach","<ul><li><b>RFM feature engineering</b> — recency, frequency and monetary value per customer, the standard basis for customer value segmentation.</li><li><b>Clustering</b> — K-Means compared against hierarchical agglomerative clustering, selecting on both silhouette score and whether the resulting groups were actually interpretable as customer types.</li><li><b>Apriori association rules</b> — surfaced product bundles frequently bought together, directly usable for merchandising decisions.</li><li><b>Time-series decomposition</b> — separated sales into trend, seasonality and residual to distinguish real demand shifts from noise.</li><li><b>Local Outlier Factor</b> — flagged customers and transactions with unusual behaviour, relevant as fraud or churn-risk signals.</li><li><b>SVD recommender</b> — matrix factorisation over the customer-product interaction matrix for personalised recommendations.</li></ul>"),
            ("Results","<table class=\"metrics\"><tr><th>Metric</th><th>Value</th><th>Interpretation</th></tr><tr><td>Silhouette score</td><td class=\"num\">[X.XX]</td><td>Cluster separation quality</td></tr><tr class=\"best\"><td>Top segment revenue share</td><td class=\"num\">[XX%]</td><td>Where retention spend should go</td></tr><tr><td>Recommender RMSE</td><td class=\"num\">[X.XX]</td><td>Accuracy on held-out interactions</td></tr></table><p>[Describe the segments in business language — for example: high-value loyalists, at-risk high spenders, one-time bargain buyers — since the segment names are what a stakeholder would actually act on.]</p>"),
            ("Limitations","<p>With more time I would validate the segments against downstream outcomes such as repeat purchase rate and churn, rather than clustering metrics alone, and test DBSCAN as a density-based alternative for customer groups that are not cleanly spherical.</p>"),
        ],
    },
    {
        "slug":"transit-accessibility", "fig":"Fig. 04",
        "domain":"GIS · Spatial data science",
        "title":"Public Transport Accessibility",
        "long":"Transit Gap: A Spatial Accessibility Index for Public Transport",
        "stack":"GeoPandas · GTFS · Census 2022 · 400m buffers · Getis-Ord Gi*",
        "chart": fig_hotspot, "cap":"Gi* hot spots vs. cold spots",
        "result":"Combined census and transit-schedule data into an accessibility index, using Getis-Ord Gi* to flag statistically significant transit deserts — exported ready for ArcGIS.",
        "meta":["GIS & AI","Python (Colab)","CBS Census 2022 + GTFS"],
        "callout":"Built a 400-metre accessibility and need index combining CBS Census 2022 with GTFS transit data, using Getis-Ord Gi* to identify statistically significant transit deserts — exported as GeoJSON and CSV ready for direct use in ArcGIS.",
        "tags":["Python","GeoPandas","Shapely","GTFS","Spatial joins","Getis-Ord Gi*","GeoJSON"],
        "dl":[("Full report (PDF)","#"),("Notebook (.ipynb)","#")],
        "sections":[
            ("Problem","<p>Transit planning needs a precise, defensible definition of &ldquo;underserved&rdquo; rather than a visual impression of a sparse map. This project builds a quantitative accessibility index from population data and real transit stop locations, then tests which gaps are statistically significant rather than incidental.</p>"),
            ("Data","<ul><li><b>CBS Census 2022</b> — population and demographic data at statistical-area level.</li><li><b>GTFS</b> feeds — actual transit stop locations and service schedules.</li></ul>"),
            ("Approach","<ul><li>Built <b>400-metre walking buffers</b> around every transit stop using GeoPandas geometry operations.</li><li><b>Spatial joins</b> between population polygons and buffer coverage, to compute what share of each area's population has walkable access.</li><li>Constructed an <b>accessibility and need index</b> combining coverage with population density and [demographic factors, e.g. age or car-ownership].</li><li>Applied <b>Getis-Ord Gi*</b> hot-spot analysis, which identifies clusters of high or low accessibility unlikely to arise by chance — the step that turns a map into a finding.</li><li>Exported <b>GeoJSON and CSV</b> structured for direct import into ArcGIS, so a planner can use the output without touching the code.</li></ul>"),
            ("Results","<p>[Summarise: identified [N] statistically significant transit-desert clusters, concentrated in [region type], covering roughly [X]% of the study area's population.]</p><!-- FIGURE SLOT: export your Gi* map and uncomment\n<figure class=\"fig\"><img src=\"../assets/transit-hotspots.png\" alt=\"Getis-Ord Gi* hot spot map\"><figcaption>Gi* hot-spot analysis of transit accessibility.</figcaption></figure>\n-->"),
            ("Limitations","<p>[For example: the index treats stop presence as binary, but a stop served once an hour is not meaningfully accessible — incorporating service frequency and wait time would sharpen it, as would validating against reported commute times.]</p>"),
        ],
    },
    {
        "slug":"web-tracking", "fig":"Fig. 05",
        "domain":"Data ethics · Unsupervised learning",
        "title":"Web Tracking & AI Profiling",
        "long":"Web Tracking, Privacy and AI Profiling",
        "stack":"StandardScaler · K-Means · DBSCAN · Statistical testing",
        "chart": fig_dbscan, "cap":"DBSCAN core vs. outliers",
        "result":"Clustered ~10,000 websites by tracking behaviour, turning a familiar claim about surveillance into measured, testable structure.",
        "meta":["Ethics, Data & AI seminar","WhoTracks.me","~10,000 websites"],
        "callout":"Clustered roughly <b>10,000 websites</b> by tracking behaviour using K-Means and DBSCAN, identifying [N] distinct tracker profiles and testing statistically whether site categories differ — turning a familiar claim about web surveillance into measured structure.",
        "tags":["Python","pandas","StandardScaler","K-Means","DBSCAN","Hypothesis testing","Data ethics"],
        "dl":[("Full report (PDF)","#"),("Notebook (.ipynb)","#")],
        "sections":[
            ("Problem","<p>&ldquo;Websites track you&rdquo; is repeated often and measured rarely. This project asks whether tracking behaviour across the web has quantifiable structure, and whether the resulting picture supports or complicates common assumptions about surveillance and AI-driven profiling.</p>"),
            ("Approach","<ul><li>WhoTracks.me data covering tracking behaviour across <b>~10,000 websites</b>.</li><li>Cleaning and feature engineering on tracker counts, categories and behaviours per site.</li><li><b>StandardScaler</b> normalisation ahead of distance-based clustering, since raw tracker counts and rates are on very different scales.</li><li><b>K-Means</b> for a fixed set of interpretable tracking profiles, and <b>DBSCAN</b> to check whether density-based structure reveals outlier sites — unusually aggressive or unusually clean — that K-Means would average away.</li><li>Statistical testing of whether differences between site categories are significant rather than merely visible in a plot.</li></ul>"),
            ("Results","<p>[Summarise the profiles found — for example: [N] clusters ranging from minimal-tracking sites to profiles carrying [X]+ third-party trackers per page, with [category] sites significantly more likely to fall in the heaviest cluster (p &lt; 0.05).]</p>"),
            ("Why it matters","<p>The clustering here is evidence for a policy question, not an exercise for its own sake. Deciding which features encode &ldquo;tracking intensity&rdquo;, and being careful about what the clusters do and do not license you to claim, is the same judgement needed when building any system that touches personal data. That combination — technical work plus a clear view of its downstream effect — is the part of this project I would want to bring to a team.</p>"),
            ("Limitations","<p>[For example: this is a snapshot. Tracking behaviour likely shifted across regulatory waves such as GDPR enforcement, so a longitudinal version would show whether these clusters are stable or whether sites migrate between them.]</p>"),
        ],
    },
]

CSS = open(os.path.join(OUT, "assets", "style.css")).read()

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light only">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
<style>{inline_css}</style>
</head>
<body>
<nav class="nav">
  <div class="wrap">
    <a href="{home}" class="brand">Maxim Lavelin<em>.</em></a>
    <div class="nav-links">
      <a href="{home}#projects">Projects</a>
      <a href="{home}#methods" class="hide-sm">Methods</a>
      <a href="{home}#about" class="hide-sm">About</a>
      <a href="{cv}">CV</a>
      <a href="mailto:{email}" class="nav-cta">Contact</a>
    </div>
  </div>
</nav>
"""

FOOT = """<footer>
    <span>Maxim Lavelin · Bar-Ilan University · 2026</span>
    <span><a href="{gh}">GitHub</a> &nbsp;·&nbsp; <a href="#">LinkedIn</a> &nbsp;·&nbsp; <a href="mailto:{email}">{email}</a></span>
  </footer>
</div>
</body>
</html>
"""

def build_home():
    rows = []
    for p in PROJECTS:
        rows.append(f"""
    <a class="row" href="projects/{p['slug']}.html">
      <div class="r-fig">{p['fig']}</div>
      <div class="r-chart">
        {p['chart']()}
        <div class="cap">{p['cap']}</div>
      </div>
      <div class="r-body">
        <div class="r-domain">{p['domain']}</div>
        <h3 class="r-title">{p['title']}</h3>
        <div class="r-stack">{p['stack']}</div>
        <div class="r-result">{p['result']}</div>
        <div class="r-go">Read the write-up &nbsp;→</div>
      </div>
    </a>""")

    html = HEAD.format(
        title="Maxim Lavelin — Data Science & Machine Learning Portfolio",
        desc="Five end-to-end data science projects: demand forecasting, deep learning on text, customer analytics, spatial analysis, and data ethics.",
        css="assets/style.css", home="index.html", cv="assets/Maxim_Lavelin_CV.pdf", email=EMAIL, inline_css=CSS)

    html += f"""
<div class="wrap">

  <header class="hero">
    <div class="status">Available for data science / ML roles</div>
    <h1>Five projects taken from raw data to a <span class="thin">decision someone could act on.</span></h1>

    <div class="byline">
      <span><b>Maxim Lavelin</b></span>
      <span>Information Technologies, Bar-Ilan University</span>
      <span>Mechanical engineering background</span>
    </div>

    <div class="abstract">
      <div class="label">Abstract</div>
      <div>
        <p>I build the whole pipeline: sourcing and cleaning the data, choosing a model that fits the
        constraint rather than the trend, and evaluating it in a way that would survive contact with
        production. Each project below is written up the way I would hand it to a colleague — what the
        problem was, what I chose and why, what the numbers came out as, and where it falls short.</p>
        <p>The work spans supervised forecasting, deep learning on unstructured text, unsupervised
        segmentation, geospatial statistics, and the ethics of systems that profile people. Full reports
        and notebooks are linked from every write-up.</p>
      </div>
    </div>
  </header>

  <section class="section" id="projects">
    <div class="section-head">
      <h2>Selected work</h2>
      <span class="count">5 projects · 2026</span>
    </div>
    <div class="rows">{''.join(rows)}
    </div>
  </section>

  <section class="section" id="methods">
    <div class="section-head">
      <h2>Methods &amp; tools</h2>
      <span class="count">applied across the five projects</span>
    </div>
    <div class="methods">
      <div class="method">
        <h4>Modelling</h4>
        <ul><li>XGBoost / GBMs</li><li>Linear &amp; logistic regression</li><li>MLP · CNN · BiLSTM</li><li>K-Means · HAC · DBSCAN</li><li>SVD / matrix factorisation</li></ul>
      </div>
      <div class="method">
        <h4>Evaluation</h4>
        <ul><li>Chronological validation</li><li>ROC &amp; precision-recall</li><li>Probability calibration</li><li>Bootstrap confidence intervals</li><li>Silhouette · Getis-Ord Gi*</li></ul>
      </div>
      <div class="method">
        <h4>Engineering</h4>
        <ul><li>Python · pandas · NumPy</li><li>scikit-learn · XGBoost</li><li>PyTorch / TensorFlow</li><li>GeoPandas · Shapely</li><li>Git · Colab</li></ul>
      </div>
      <div class="method">
        <h4>Data work</h4>
        <ul><li>Feature engineering</li><li>Lag &amp; rolling features</li><li>TF-IDF / text pipelines</li><li>Spatial joins · GTFS</li><li>GeoJSON · ArcGIS export</li></ul>
      </div>
    </div>
  </section>

  <section class="section" id="about">
    <div class="section-head"><h2>About</h2></div>
    <div class="about">
      <div class="label">Author note</div>
      <div>
        <p>I trained as a <strong>mechanical engineer</strong> before moving into information technologies
        and data science. That background is the reason I care less about squeezing a leaderboard metric
        and more about whether a result holds under real constraints — which is why the taxi model is
        validated chronologically rather than by random split, and why the complaint classifier reports
        confidence intervals instead of a single number.</p>
        <p>I am currently looking for a data science, machine learning or analytics role where I can own
        problems end to end. The fastest way to judge whether that fits is to read one write-up and the
        report behind it — <a href="projects/nyc-taxi.html">the taxi forecaster</a> is the most complete.</p>
      </div>
    </div>
  </section>
"""
    html += FOOT.format(gh=GH, email=EMAIL)
    open(os.path.join(OUT, "index.html"), "w").write(html)

def build_project(i, p):
    prev_p = PROJECTS[i-1] if i > 0 else None
    next_p = PROJECTS[i+1] if i < len(PROJECTS)-1 else None

    html = HEAD.format(
        title=f"{p['title']} — Maxim Lavelin",
        desc=p['result'].replace("<b>","").replace("</b>",""),
        css="../assets/style.css", home="../index.html",
        cv="../assets/Maxim_Lavelin_CV.pdf", email=EMAIL, inline_css=CSS)

    tags = "".join(f'<span class="tag">{t}</span>' for t in p['tags'])
    dl = "".join(f'<a href="{u}">{n}</a>' for n, u in p['dl'])
    meta = "".join(f"<span>{m}</span>" for m in p['meta'])
    secs = "".join(
        f'<div class="doc"><h2>{h}</h2><div class="doc-body">{b}</div></div>'
        for h, b in p['sections'])

    prev_link = (f'<a href="{prev_p["slug"]}.html">← {prev_p["title"]}</a>'
                 if prev_p else '<a href="../index.html">← All projects</a>')
    next_link = (f'<a href="{next_p["slug"]}.html">{next_p["title"]} →</a>'
                 if next_p else '<a href="../index.html">All projects →</a>')

    html += f"""
<div class="wrap">
  <div class="crumb"><a href="../index.html">← All projects</a> &nbsp;/&nbsp; <span class="mono">{p['fig']}</span></div>

  <header class="p-hero">
    <div class="r-domain">{p['domain']}</div>
    <h1>{p['long']}</h1>
    <div class="p-meta">{meta}</div>
    <div class="callout">{p['callout']}</div>
    <div class="tags">{tags}</div>
    <div class="dl">{dl}</div>
  </header>

  {secs}

  <div class="pager">{prev_link}{next_link}</div>
"""
    html += FOOT.format(gh=GH, email=EMAIL)
    open(os.path.join(OUT, "projects", f"{p['slug']}.html"), "w").write(html)

if __name__ == "__main__":
    build_home()
    for i, p in enumerate(PROJECTS):
        build_project(i, p)
    print("built:", os.listdir(OUT), os.listdir(os.path.join(OUT, "projects")))
