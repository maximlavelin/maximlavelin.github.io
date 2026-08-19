#!/usr/bin/env python3
"""Builds the portfolio site: homepage + 5 project pages, sharing one stylesheet."""
import os, math, random

OUT = os.path.dirname(os.path.abspath(__file__))
EMAIL = "maxim.lavelin@live.biu.ac.il"

def fig(src, cap):
    return (f'<figure class="fig"><img src="../assets/fig/{src}" alt="{cap}">'
            f'<figcaption>{cap}</figcaption></figure>')
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
        "dl":[("Full report (PDF)","../assets/NYC_TAXI_Lavelin.pdf"),("Open notebook in Colab","https://colab.research.google.com/drive/1mwuHis2RWH6t1U_sNqK2xu5CrjNilP5D")],
        "sections":[
            ("Problem","<p>NYC taxi demand swings from near zero to over 12,000 rides per hour within a single day. Under-forecasting means long passenger waits and lost revenue; over-forecasting means wasted idle mileage and fuel. I framed this as a supervised regression problem — predict total citywide pickups for a given hour — using a year of NYC TLC trip records merged with JFK weather observations.</p>"),
            ("Data","<ul><li><b>8,616 hourly observations</b> across 2024, aggregated from NYC TLC Yellow Taxi trip records.</li><li>Demand is highly volatile: mean 4,708 rides/hour, standard deviation 2,712, ranging from 0 to 12,757.</li><li>Weather from JFK Airport (NOAA/NCEI), reduced from roughly 125 raw meteorological fields to the two that carried operational signal: continuous temperature and a <b>binary rain indicator</b>. Precipitation intensity did not matter; presence of rain did.</li></ul>"),
            ("Approach","<p>Two models, evaluated identically, so the case for non-linearity is made rather than assumed:</p><ul><li><b>Linear regression baseline</b> — an interpretable additive combination of temporal, weather, and lagged demand features. It captures broad seasonality but structurally cannot model regime-dependent spikes.</li><li><b>XGBoost</b> — gradient-boosted trees, able to learn conditional interactions such as demand responding to weather differently depending on hour of day or recent history.</li></ul><p>Features: hour of day, day of week, weekend flag, temperature, rain flag, and <b>lagged demand</b> (24-hour and 168-hour lags plus rolling means). The lag features turned out to dominate.</p>"),
            ("Evaluation","<p>I used a <b>strict chronological split</b> — train on January–September 2024, validate on October, test on November–December — rather than random k-fold. This mirrors how the model would actually be deployed, predicting the future from only the past, and avoids the leakage a random split would silently introduce.</p><p>MAE was the primary metric because it is directly interpretable as rides per hour. RMSE is reported alongside it to surface large errors, which are disproportionately costly during peaks.</p>"),
            ('Results', '<table class="metrics"><tr><th>Model</th><th>MAE (rides/hr)</th><th>RMSE</th></tr><tr><td>Linear regression</td><td class="num">728.43</td><td class="num">993.47</td></tr><tr class="best"><td>XGBoost</td><td class="num">546.19</td><td class="num">810.55</td></tr></table><p>The linear model systematically <b>underestimates peak demand</b> &mdash; and, as the plot below shows, it does something worse at the troughs: it predicts <b>negative ride counts</b>, which is physically impossible and a clear signal that the additive structure has been pushed past where it applies. XGBoost tracks both the magnitude and the timing of the swings.</p>' + fig('taxi-actual-vs-pred.png', 'Actual demand vs. linear baseline and XGBoost, November 2024. Note the linear model dipping below zero.') + '<p>Feature importance shows the <b>168-hour (weekly) lag</b> dominating predictive power, followed by the 24-hour lag and hour of day. Weather contributes only secondary, contextual signal &mdash; which means better representations of demand history would buy more accuracy than adding external variables.</p>' + fig('taxi-importance.png', 'XGBoost feature importance. The weekly lag dominates.')),
            ("Limitations","<p>Weather from a single airport station is a coarse proxy for citywide conditions, and city-level aggregation hides neighbourhood variation — a zone-level model (Manhattan separately from the outer boroughs) would likely outperform this one. I would also fold in event data such as concerts and games to catch non-seasonal demand shocks, currently the hardest cases for the model.</p>"),
        ],
    },
    {
        'slug':'vehicle-safety', 'fig':'Fig. 02',
        'domain':'Deep learning · NLP',
        'title':'Vehicle Safety Intelligence',
        'long':'Vehicle Safety Intelligence: Text-Only Severity Prediction from NHTSA Complaints',
        'stack':'TF-IDF · CNN · BiLSTM · Isotonic calibration · Bootstrap CIs',
        'chart': fig_roc, 'cap':'ROC curves, held-out test set',
        'result':'Predicts whether a complaint describes a <b>serious</b> safety failure from its text alone. The regularised CNN reached <b>0.9513 ROC-AUC</b> on a 6.61% positive rate — and isotonic calibration cut the Brier score from 0.0291 to <b>0.0232</b>.',
        'meta':['Deep Learning · Course 35374','NHTSA FLAT_CMPL','300,000 complaints'],
        'callout':'Three neural architectures compared under an identical split and evaluation pipeline, predicting serious safety failures (crash, fire, injury or death) from complaint text only. The <b>regularised CNN won at 0.9513 ROC-AUC / 0.7318 F1</b>. The more useful finding is what the bootstrap intervals say about whether that win is real — and it is not real against every competitor.',
        'tags':['Python','TensorFlow / Keras','TF-IDF','1D CNN','BiLSTM','Isotonic regression','Bootstrap CIs','Class weighting'],
        'dl':[('Full report (PDF)','../assets/Vehicle_Safety_Intelligence.pdf'),('Open notebook in Colab','https://colab.research.google.com/drive/1YZrvtE-PIvSMx_LksFaMc-UzAokp6bV1')],
        'sections':[
            ('Problem', '<p>NHTSA receives hundreds of thousands of owner complaints in free text. Triaging them by hand does not scale, but the ones describing a crash, fire, injury or death are exactly the ones a reviewer needs to see first. The task: given only the complaint narrative, predict whether it describes a serious safety failure.</p><p>The framing matters as much as the modelling. This is a <b>triage signal for a human reviewer</b>, not an autonomous verdict on whether a vehicle is safe — which is why the evaluation focuses on ranking quality and calibrated probabilities rather than a single accuracy figure.</p>'),
            ('Target and leakage control', '<p>The label is constructed from four source fields: a complaint is serious if <span class="mono">CRASH</span> or <span class="mono">FIRE</span> is flagged, or if injuries or deaths are greater than zero. Those four fields build the gold label and are then <b>withheld entirely from the models</b>, which see only the <span class="mono">CDESCR</span> narrative — no make, model, manufacturer, state, component, or incident flag.</p><p>The split is the part I would defend hardest. One incident can appear across multiple rows because different components attach to the same complaint, so splitting by row would put near-duplicate text in both train and test. Instead the data is partitioned <b>by ODINO</b>, the unique complaint identifier, roughly 70/15/15 — so no complaint can straddle the split.</p><p>Component category is derived too, but strictly for post-hoc subgroup analysis. It never enters training, which is what makes the per-component results below diagnostically meaningful rather than circular.</p>'),
            ('Imbalance', '<p>In the held-out test set, <b>1,495 of 22,605</b> complaints are positive — a <b>6.61%</b> serious-failure rate. A model that answered &ldquo;not serious&rdquo; every single time would score 93.4% accuracy while being worthless, so accuracy was never the headline metric.</p><p>All three models train with <b>class weights</b>, the positive class weighted by the negative-to-positive ratio, so rare serious complaints contribute proportionally more loss and the networks cannot minimise error by simply favouring the majority.</p>'),
            ('The three models', '<ul><li><b>Model 1 — TF-IDF + MLP.</b> 3,000 features, unigrams and bigrams, into Dense(128) → Dense(64) → sigmoid. It deliberately ignores word order, which makes it a clean test of how much severity signal lives in vocabulary alone.</li><li><b>Model 2 — regularised 1D CNN.</b> 20k-token vocabulary, 64-dim learned embedding, Conv1D(64, kernel 5) with global max pooling, dropout 0.3 and L2 1e-4. Learns local phrase patterns and keeps the strongest detected pattern in the complaint.</li><li><b>Model 3 — BiLSTM.</b> 48 units per direction with spatial dropout, able in principle to model dependencies across the whole narrative.</li></ul>'),
            ('Results', '<table class="metrics"><tr><th>Model</th><th>ROC-AUC</th><th>95% bootstrap CI</th><th>F1</th><th>Brier</th></tr><tr><td>TF-IDF + MLP</td><td class="num">0.9428</td><td class="num">[0.9349, 0.9500]</td><td class="num">0.6338</td><td class="num">0.0459</td></tr><tr class="best"><td>CNN (regularised)</td><td class="num">0.9513</td><td class="num">[0.9443, 0.9578]</td><td class="num">0.7318</td><td class="num">0.0291</td></tr><tr><td>BiLSTM</td><td class="num">0.9337</td><td class="num">[0.9255, 0.9414]</td><td class="num">0.6797</td><td class="num">0.0398</td></tr></table>' + fig('veh-roc.png', 'ROC curves for all three models on the held-out test set.') + '<p>The CNN leads on every metric. But the bootstrap intervals are what make the comparison honest: the CNN&rsquo;s [0.9443, 0.9578] sits clear of the BiLSTM&rsquo;s [0.9255, 0.9414], so <b>that gap is real</b>. Against the TF-IDF MLP&rsquo;s [0.9349, 0.9500] the intervals <b>overlap</b> — the CNN&rsquo;s 0.0085 edge over a bag-of-words baseline is not cleanly separable at this sample size.</p><p>That shapes the recommendation rather than undermining it. The CNN is the better model and worth deploying, but Model 1 remains a legitimate operational choice if inference cost or interpretability matters more than a fraction of a point of AUC. The BiLSTM is the clear loser: most expensive to train, lowest AUC. <b>The signal in these narratives is lexical and local</b> — explicit words and short phrases — not long-range syntax, which is exactly why the convolution beats the recurrence.</p>'),
            ('Calibration', '<p>AUC only says the model ranks serious complaints above non-serious ones. For triage you need more: a score of 0.70 should mean roughly a 70% chance. Those are different properties and the raw sigmoid outputs did not have the second one.</p><p>Fitting <b>isotonic regression</b> on validation predictions and applying it to the test set improved the Brier score from <b>0.0291 to 0.0232</b>.</p>' + fig('veh-calibration.png', 'Reliability diagram for the CNN: raw sigmoid outputs against isotonic-calibrated probabilities.') + '<p>Calibration also reframes the threshold decision. At a fixed 0.5 cut-off the calibrated model gives precision 0.8712 and recall 0.6829 — but in safety triage a <b>false negative is far more costly than a false positive</b>, since a missed serious complaint is a review that never happens. The right operating point is lower than 0.5, and it should be set from an explicit cost function rather than inherited from a default.</p>'),
            ('Where it fails', '<p>Because component labels were never used in training, breaking performance down by component is a genuine diagnostic rather than a restatement of an input.</p>' + fig('veh-component.png', 'Calibrated ROC-AUC by component category, strongest to weakest.') + '<p>Performance varies materially: <b>Service Brakes, Hydraulic reaches 0.997</b> and Air Bags 0.975, while <b>Suspension sits at 0.854</b> and Exterior Lighting at 0.888. That pattern is interpretable — a hydraulic brake failure or an airbag event tends to be described in vivid, unambiguous language, whereas a suspension complaint often reads the same whether or not it ended in a crash. Some of these groups carry few positives, so the subgroup figures deserve caution.</p>'),
            ('Limitations', '<p>The dataset carries <b>selection bias</b> by construction: it describes complaints that people chose to submit to NHTSA, not the safety of all vehicles on the road, and results depend on how fluently each complainant wrote in English. A high score is a prioritisation signal, not evidence that an event occurred.</p><p>Given that the BiLSTM underperformed a bag-of-words baseline, I would expect smaller gains from a pretrained transformer than the usual assumption suggests, though it is still the obvious next test. More valuable would be temporal validation — training on earlier complaints and testing on later ones — to check whether both discrimination and calibration hold as vocabulary drifts.</p>'),
        ],
    },
    {
        "slug":"retail-consultant", "fig":"Fig. 03",
        "domain":"Unsupervised learning · Customer analytics",
        "title":"Retail Consultant",
        "long":"Retail Consultant: An End-to-End Customer Analytics Pipeline",
        "stack":"PCA · K-Means vs. HAC · Apriori · STL · LOF · SVD",
        "chart": fig_clusters, "cap":"PCA projection, 86.1% of variance",
        "result":"HAC beat K-Means on silhouette <b>0.604 vs. 0.321</b>, splitting 5,878 customers into 5,871 retail and just <b>7 wholesale buyers</b> — who turned out to be every single anomaly the outlier detector flagged in that segment.",
        "meta":["Unsupervised Learning","March 2026","Online Retail II · 805,549 rows"],
        "callout":"An end-to-end pipeline on <b>805,549</b> cleaned transactions: PCA and clustering split <b>5,878 customers</b> into two behavioural groups, Apriori found cross-sell rules with lift up to <b>28.0</b>, STL exposed weekly demand seasonality, and LOF flagged <b>59 customers</b> for business review — including all 7 wholesale buyers.",
        "tags":["Python","pandas","scikit-learn","mlxtend","surprise","PCA","HAC","Apriori","STL","LOF","SVD"],
        "dl":[("Full report (PDF)","../assets/Unsupervised_Project_Lavelin.pdf"),("Open notebook in Colab","https://colab.research.google.com/drive/1S9-2OCXeCSv8kpkbf1XCduK9ZwnrN9It")],
        "sections":[
            ("Problem","<p>Framed as a consulting engagement: a mid-sized online retailer holds extensive transactional data but cannot identify its most valuable customers, does not know which products sell together for which customer types, and is concerned about unusual or potentially fraudulent purchasing. The pipeline turns raw invoice lines into an answer for each of those.</p>"),
            ("Data engineering","<p>Cleaning the Online Retail II data meant dropping rows with no Customer ID, excluding credit notes and returns (invoices prefixed <span class=\"mono\">C</span>), and removing non-positive quantities and prices — leaving <b>805,549 rows</b>, aggregated to <b>5,878 customers</b>.</p><p>Beyond standard RFM I added two features that turned out to matter more than the mandatory ones: <b>AvgOrderValue</b> (separates high-spend-per-visit from frequent low-value customers) and <b>AvgQuantityPerInvoice</b> (captures bulk buying). The median customer buys 3 times, spends &pound;899, and orders 158 units per invoice — that last number already hints at a wholesale group hiding in the data.</p>"),
            ('Segmentation', '<p>Both a log transform and StandardScaler were applied before clustering, because spending data is heavily right-skewed and every algorithm used here is distance-based.</p><p>PCA reduced six features to two components capturing <b>86.1%</b> of variance (PC1 64.7%, PC2 21.4%), producing a distinctly fan-shaped distribution. PC1 is dominated by AvgQuantityPerInvoice and Monetary, so distance along it is essentially a wholesale-versus-retail axis.</p>' + fig('retail-pca.png', 'PCA projection of all customers. The fan shape is what breaks K-Means and favours average-linkage HAC.') + '<p>K-Means silhouette peaked at k=2 (0.321) and fell monotonically after. But <b>HAC with average linkage scored 0.604</b> &mdash; nearly double &mdash; and was selected programmatically. The reason is visible in the plot above: K-Means assumes spherical, equally sized clusters, and this data is neither. DBSCAN was also tested and rejected outright, classifying <b>83% of customers as noise</b>.</p>' + fig('retail-silhouette.png', 'K-Means silhouette scores, k = 2 to 8. Strictly decreasing after k = 2.') + '<table class="metrics"><tr><th>Median feature</th><th>Regular buyers</th><th>Wholesale buyers</th></tr><tr><td>Customers</td><td class="num">5,871</td><td class="num">7</td></tr><tr class="best"><td>Monetary</td><td class="num">&pound;896.60</td><td class="num">&pound;12,393.70</td></tr><tr><td>Avg. order value</td><td class="num">&pound;284.87</td><td class="num">&pound;10,877.18</td></tr><tr><td>Avg. qty / invoice</td><td class="num">157.5</td><td class="num">17,766</td></tr><tr><td>Variety (unique SKUs)</td><td class="num">45</td><td class="num">9</td></tr></table><p>Seven customers generate roughly 14&times; the revenue per head while buying just 9 product types in enormous volumes. The two groups need entirely different commercial treatment: loyalty and cross-sell for retail, account management and volume pricing for wholesale.</p>'),
            ("Market basket analysis","<p>Apriori was run separately per segment. Among regular buyers (31,212 invoices, 165 items), the strongest rule pairs the pink and green Regency teacups at <b>lift 28.0, confidence 0.838</b> — a customer buying one is 28 times more likely than chance to buy the other. That is textbook set-completion behaviour and maps directly to a &ldquo;complete the collection&rdquo; campaign.</p><p>The wholesale segment was <b>correctly skipped</b> by the size threshold (7 customers, 16 invoices). Wholesale purchasing is driven by volume and margin, not product affinity, so the absence of basket rules there is the right finding rather than a gap.</p>"),
            ("Seasonality and anomalies","<p>STL decomposition (period=7, robust) of the top-selling item showed a <b>consistent weekly seasonal cycle</b> plus a non-monotonic trend, meaning inventory planning on year-over-year averages alone would mislead.</p><p>LOF (n_neighbors=20, contamination=0.01) flagged <b>59 anomalous customers</b> — and notably, <b>all 7 wholesale buyers</b> were among them, confirming each has a distinctive individual profile. The top case placed 2 invoices worth &pound;168,472, including a single line of 80,995 units, which is a data-integrity and fraud-review priority rather than a segmentation insight.</p>"),
            ("Recommender","<p>An SVD collaborative filter on implicit ratings tuned to <b>n_factors = 1</b> (CV RMSE 1.1041), beating a BaselineOnly model (1.1230) by <b>1.7%</b>.</p><p>That the optimum is a single latent factor is itself the finding: the preference structure is genuinely low-dimensional, which aligns with the two-segment clustering result. Training separate models per segment is the obvious next iteration.</p>"),
            ("Limitations","<p>The wholesale segment contains only 7 customers, so every conclusion about it is anecdotal rather than statistical. I would also validate segments against downstream outcomes such as repeat purchase and churn, rather than silhouette alone — a well-separated cluster is not automatically a commercially useful one.</p>"),
        ],
    },
    {
        "slug":"transit-accessibility", "fig":"Fig. 04",
        "domain":"GIS · Spatial data science",
        "title":"Public Transport Accessibility",
        "long":"Gaps Between Public Transport Need and Accessibility in Urban Israel",
        "stack":"GeoPandas · GTFS · CBS Census 2022 · Getis-Ord Gi* · ArcGIS Pro",
        "chart": fig_hotspot, "cap":"Gi* hot spots vs. cold spots",
        "result":"Across <b>2,179 statistical areas</b>, stop coverage was already ~94% — so the real gap is <b>frequency, not distance</b>. Found <b>168 high-need / low-access</b> areas, with 75% of Tel Aviv&ndash;Yafo flagged as hot spots.",
        "meta":["GIS & AI · Dr. Asnat Mangel","2025–2026","CBS Census 2022 + GTFS"],
        "callout":"Combined CBS Census 2022 with national GTFS feeds across <b>2,179 urban statistical areas in 142 localities</b>, building separate need and supply indices and measuring the gap. The headline finding inverts the intuitive assumption: physical stop coverage is near-universal, so <b>service frequency</b> is what actually separates well-served areas from underserved ones.",
        "tags":["Python (Colab)","GeoPandas","GTFS","Spatial joins","400m buffers","Getis-Ord Gi*","ArcGIS Pro","ArcGIS Online"],
        "dl":[("Full report (PDF)","../assets/Transit_Gap_Maxim_Eng.pdf"),("Open notebook in Colab","https://colab.research.google.com/drive/1qendT_WFNsLzhzkZg-2t7rmnnRbtTMks"),("Interactive map (ArcGIS Online)","https://infoi.maps.arcgis.com/apps/mapviewer/index.html?webmap=3f7b8a254d78433e8053a5c3381434a7")],
        "sections":[
            ("Problem","<p>Transit planning needs a defensible definition of &ldquo;underserved&rdquo; rather than a visual impression of a sparse map. Following Currie&rsquo;s (2010) methodology, this project calculates need and supply separately and then measures the gap between them, so that the areas identified are those where high dependence on public transport coincides with low actual service.</p>"),
            ("Data and method","<p>Three sources: the CBS 2022 statistical-area layer, the 2022 population census, and nationwide GTFS feeds from Israel&rsquo;s Ministry of Transport.</p><ul><li><b>Need index</b> built from share of households without a car, share of residents aged 65+, population density, and median income — the variables that capture dependence on public transport rather than mere population size.</li><li><b>Supply index</b> from <b>400-metre buffers</b> around stops combined with departures per capita on a representative weekday, so frequency counts rather than just proximity.</li><li><b>Getis-Ord Gi*</b> hot-spot analysis to separate statistically significant clusters from incidental variation, run in Python and then independently re-run in ArcGIS Pro as a validation step.</li><li>Three GeoJSON layers exported to ArcGIS Pro for cartography, then published to ArcGIS Online as an interactive map.</li></ul>"),
            ('Findings', '<p>The analysis covered <b>2,179 urban statistical areas across 142 localities</b>. The most useful result was not the one I expected: median stop coverage is approximately <b>100%</b> and mean coverage about <b>94%</b>, meaning physical access to a stop is essentially solved in urban Israel. <b>What separates areas is service frequency</b> &mdash; how many departures actually serve that stop.</p><p><b>168 statistical areas</b> were classified as high need / low accessibility. The strongest spatial concentration is in Tel Aviv&ndash;Yafo, where <b>121 of 161 areas (about 75%)</b> are hot spots, with further clusters in Jerusalem and in northern and southern urban areas. Cold spots &mdash; a better match between need and supply &mdash; appear in Netanya, Bnei Brak, and several Arab localities including Umm al-Fahm, Tayibe, Tamra, Sakhnin and Tira.</p>' + fig('transit-hotspots.png', 'Statistically significant gap clusters (Getis-Ord Gi*). Red indicates hot spots at 99% confidence.') + '<p>Because dense central areas show substantial gaps alongside peripheral ones, the pattern <b>cannot be reduced to a centre-versus-periphery divide</b> &mdash; which is the finding most directly relevant to how service improvements would be prioritised.</p>' + fig('transit-mean-gap.png', 'Mean need&ndash;supply gap aggregated by locality, for comparison between local authorities.')),
            ("Limitations","<p>The analysis uses scheduled GTFS data rather than observed performance, so a route that is timetabled but chronically late counts as served. It also assumes a uniform 400-metre walking distance regardless of terrain or road network, and the demographic inputs are 2022 figures that do not reflect later changes to either population or the transport network.</p>"),
        ],
    },
    {
        "slug":"web-tracking", "fig":"Fig. 05",
        "domain":"Data ethics · Unsupervised learning",
        "title":"Web Tracking & AI Profiling",
        "long":"From Tracking Infrastructure to AI Profiling",
        "stack":"Feature engineering · K-Means · DBSCAN · Chi-square testing",
        "chart": fig_dbscan, "cap":"DBSCAN core vs. 634 outliers",
        "result":"Google trackers on <b>99.2%</b> of 10,000 sites; news sites carry <b>10.85</b> trackers against a 6.25 mean. The ethical point: the two &ldquo;tracking regimes&rdquo; <b>did not exist in the data</b> — the algorithm created them.",
        "meta":["AI Ethics seminar","WhoTracks.me, March 2025","10,000 websites"],
        "callout":"Measured tracking across <b>10,000 websites</b> and used K-Means to identify two tracking regimes (silhouette 0.467). The central argument is methodological: those regime labels were <b>absent from the source data</b> and were manufactured by the clustering choices — the same computational move that turns behavioural traces into inferred profiles of people.",
        "tags":["Python","pandas","scikit-learn","K-Means","DBSCAN","Chi-square","PCA","Data ethics"],
        "dl":[("Full report (PDF)","../assets/Web_Tracking_Final_Report.pdf"),("Open notebook in Colab","https://colab.research.google.com/drive/1S5Uoo9C8lWHC3WEYo55xK7jb4rjSKR8F")],
        "sections":[
            ("Question","<p>How do online tracking practices enable AI-driven profiling, and what ethical concerns emerge from algorithmic inference? The empirical half measures tracking across 10,000 sites. The conceptual half uses that exercise to demonstrate something about inference itself — that the categories a model outputs are made, not found.</p>"),
            ("Data and features","<p>Built a site-level dataset of <b>10,000 rows</b> from the WhoTracks.me March 2025 release. Features cover tracker volume, company diversity, cookie activity, query-string tracking, referer leakage, third-party cookies and overall tracking prevalence, plus Facebook presence and one-hot site categories.</p><p>One deliberate exclusion is worth noting: <b>Google presence was dropped from the clustering</b> despite being retained descriptively, because at <b>99.2% prevalence</b> it has almost no discriminative power. A feature that is true of nearly everything cannot separate anything.</p>"),
            ('Findings', '<p>Across the 10,000 sites the mean tracker count was <b>6.25</b> (median 5.2). Google-affiliated trackers appeared on <b>99.2%</b> of sites and Facebook/Meta on <b>48.9%</b> &mdash; concentration consistent with Englehardt and Narayanan (2016).</p><p>Tracking varies sharply by sector: <b>News and Portals average 10.85</b> trackers per site, against <b>3.82 for Banking</b> and <b>3.06 for Government</b>.</p>' + fig('web-categories.png', 'Average trackers per site by website category.') + '<p>K-Means at K=2 (silhouette <b>0.467</b>) split sites into High and Lower Tracking Intensity regimes. The high-intensity group carries more than twice the trackers (12.05 vs. 4.87) and companies (9.14 vs. 3.61), with triple the referer leakage.</p>' + fig('web-clusters.png', 'Mean tracking characteristics of the two K-Means regimes.') + '<p>The category&ndash;cluster association is significant at <b>p &lt; .001</b>, with News and Portals strongly overrepresented in the high-intensity regime (standardised residual <b>+23.7</b>) while Government, Banking and Adult sites are underrepresented. DBSCAN separately identified <b>634 outliers</b>, the most extreme carrying 26&ndash;35 trackers.</p>' + fig('web-residuals.png', 'Standardised residuals for the category&ndash;regime association (red = overrepresented).')),
            ("The actual argument","<p>A silhouette of 0.467 indicates meaningful but overlapping structure — a <b>continuum, not two natural kinds</b> of website. The two regimes are an artefact of choosing K=2, of which features were selected, and of how they were scaled. Change those decisions and the categories change.</p><p>That is precisely the ethical problem. The labels did not exist in the source data; the algorithm produced them. Applied to behavioural data about people rather than sites, the identical procedure generates inferred interests, risk scores and predictive profiles — categories that a person never disclosed, could not anticipate at the moment of consent, and cannot easily contest. The privacy harm sits in the <b>inference step</b>, not only in collection.</p><p>Working on this changed how I treat cluster labels in my other projects. Naming a group is an analytical act with consequences, not a neutral description of something that was already there.</p>"),
            ("Limitations","<p>This is a single monthly snapshot and it classifies websites, not users. WhoTracks.me measurements come from consenting Ghostery and Cliqz users, who likely differ from the general population in privacy awareness, geography and browser choice; the direction of that sampling bias cannot be determined from the data. Several tracking indicators are also strongly correlated, reducing the number of genuinely independent signals driving the clusters.</p>"),
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
