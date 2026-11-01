# Scarce-data methods, second set: masking, forgetting, weight averaging, data reuse, memorization, evaluation noise

**Goal:** same as `REPORT.md`: continue pre-training a Hebrew BERT (NeoDictaBERT / DictaBERT) with MLM on a small Ancient-Hebrew corpus (Bible + DSS), then build a classifier. This second set fills the gaps that `REPORT.md` listed (§G) and that the Step 1 assessment found uncovered: masking strategy, weight anchoring, checkpoint averaging, learning-rate re-warming, multi-epoch data reuse, memorization, deduplication and evaluation variance.
**Papers (25 PDFs, none repeated from `REPORT.md`):** `papers2/<arXiv-id>_<ShortName>.pdf`. All are arXiv preprints.

> **How reliable is this?** I read the abstracts of all 25 papers and searched the method sections of the key ones for hyper-parameters (SpanBERT, PMI-Masking, Wettig et al., Cramming, Academic Budget, Data-Constrained Scaling, RecAdam, EWC, L2-SP, Model Soups, Re-warming, MultiBERTs, Dedup). Entries marked ✔ quote details I saw in the PDF. Entries marked ⚠ rely on my recollection, so check the PDF before copying numbers.
> **Almost all of these papers are on English (or vision), with models and data far larger than yours, and many are about from-scratch pre-training or fine-tuning, not continued MLM on a tiny corpus.** Each entry says what transfers and what does not. The only Hebrew-Bible paper in the set (G2) is a Step 3 aid, not a Step 1 method.

---

## 0. Recommended additions to the pipeline (synthesis)

| Stage | What to try | Based on |
|---|---|---|
| Masking | Keep whole-word masking but sweep the rate (e.g. 15/20/30/40%); then test span masking (geometric lengths) or PMI-based n-gram masking as alternatives to uniform whole-word masking. | Should You Mask 15%, SpanBERT, PMI-Masking |
| Objective | Optionally try replaced-token detection as an auxiliary objective to get a loss on every token of a short row. | ELECTRA |
| Anchoring | Add an L2 penalty towards the base weights (L2-SP), or an EWC-style Fisher-weighted penalty, or RecAdam's annealed version. Compare with LoRA. | L2-SP, EWC, RecAdam, LoRA Learns Less |
| LR schedule | Treat the LR schedule as an experiment: warm-up length and peak LR (re-warming), and a final decay to near zero. | Re-warming, Cramming, Academic Budget |
| Averaging | Average weights of several runs (different seeds or hyper-parameters, same init) or along the training trajectory, and interpolate between base and adapted weights. | Model Soups, SWA, WiSE-FT |
| Data | Deduplicate / de-leak near-identical verses (parallel passages) between train and dev; control epochs by the data-constrained results. | Dedup, Data-Constrained Scaling |
| Memorization | Measure verbatim memorization of training verses as a function of epochs and duplicates. | Quantifying Memorization, Emergent Memorization |
| Evaluation | Use several seeds and a bootstrap that resamples both test items and training seeds. | MultiBERTs, Dodge et al. |

---

## A. Masking strategy and pre-training objective

### A1. Should You Mask 15% in Masked Language Modeling? — Wettig et al. 2022 · `2202.08005`
- **What:** a study of the masking rate (and its interaction with the masking strategy).
- **Method ✔:**
  - Pre-train MLMs of several sizes at masking rates from 15% up to 80%, using the efficient 24-hour BERT recipe (Izsak et al.), then evaluate on GLUE, SQuAD and linguistic probing.
  - Compare uniform, span and PMI masking at each rate.
  - Split the masking rate into two factors: the *corruption rate* (how much of the context is corrupted) and the *prediction rate* (how many tokens are predicted).
- **Results ✔:** 15% is not universally optimal; **40% beats 15% for BERT-large**; 80% still keeps 95% of fine-tuning performance; uniform masking needs a higher rate than span or PMI masking, and at their own optimal rates the methods perform similarly. For BERT-base the best rate was lower, near 20% ⚠.
- **Transfer:** English, from-scratch pre-training, downstream GLUE/SQuAD, not continued MLM on rows of ~17 tokens. [my inference] On short rows a high rate removes most of the context, so the best rate is an empirical question; it is a one-line config change.

### A2. SpanBERT — Joshi et al. 2020 · `1907.10529`
- **What:** mask contiguous spans instead of single tokens and predict a whole span from its boundary tokens.
- **Method ✔:**
  - Sample span lengths from a geometric distribution Geo(p = 0.2), clipped at 10 (in words), until 15% of tokens are masked.
  - Replace all tokens of a span with [MASK] (or random tokens) as a unit.
  - **Span Boundary Objective (SBO):** predict each masked token from the two boundary token representations just outside the span plus a position embedding of the target token. Loss = MLM loss + SBO loss.
  - Single contiguous segment per example, no next-sentence prediction.
- **Results ✔:** consistent gains over BERT on span-selection tasks (SQuAD 1.1/2.0 F1 94.6/88.7 for the large model, OntoNotes coreference 79.6 F1) and small gains on GLUE.
- **Transfer:** English, BERT-large, from scratch. Hebrew words are morphologically dense (prefixes, clitics), so a span of 2–3 words is a short phrase; [my inference] this may teach phrase-level and formulaic structure, which could also raise the risk of memorising formulae (see D).

### A3. PMI-Masking — Levine et al. 2021 · `2010.01825`
- **What:** mask n-grams that are strongly collocated, so the model cannot solve the task from shallow local cues.
- **Method ✔:**
  - Define a collocation score for an n-gram as its pointwise mutual information under its *weakest-link* segmentation (the segmentation closest to being separable): high only when every way of splitting it into two parts leaves correlated pieces.
  - Build a vocabulary of the highest-scoring n-grams (up to length 5 ⚠, size ≈800k ⚠) from the corpus.
  - Mask a whole such n-gram when one is chosen, otherwise whole words/tokens as usual.
  - The paper also notes whole-word masking behaves differently as vocabulary size changes (1.08 vs 2.06 tokens per word at 30K vs 2K vocabulary).
- **Results ✔:** reaches the performance of prior masking schemes in **half the training time**, and ends higher.
- **Transfer:** English, large corpora, from scratch. [my inference] A PMI list can be computed from your own corpus, but with a small corpus the PMI estimates are noisy. The biblical text is full of fixed formulae, so PMI masking will select them heavily.

### A4. RoBERTa — Liu et al. 2019 · `1907.11692`
- **What:** a careful BERT replication; the origin of **dynamic masking**, removal of NSP and of long training.
- **Method ✔ (from the abstract):** BERT was significantly undertrained; key design choices (data size, batch size, masking, training length) matter. [general knowledge, not from my reading] dynamic masking means a fresh mask each time a sequence is seen.
- **Use:** your recipe already redraws masks every epoch, so this is mostly confirmation. It is a reference for the claim that training length matters.

### A5. ELECTRA — Clark et al. 2020 · `2003.10555`
- **What:** replaced-token detection (RTD): a small generator replaces some tokens, the main model predicts for **every** token whether it was replaced.
- **Method ✔:** the loss is defined over all input tokens rather than the ~15% masked ones, which is the source of its sample efficiency.
- **Results:** more compute-efficient than MLM at the same size (see the paper's tables).
- **Transfer:** it needs a generator and a discriminator head, so it changes the model and the frozen head policy. [my inference] Low priority for Step 1, but the idea that "every position should produce a learning signal" is the reason very short rows are wasteful under MLM.

---

## B. Keeping the model close to the base: forgetting and anchoring

### B1. L2-SP — Li et al. 2018 · `1802.01483`
- **Method ✔:** add α/2 · ‖w − w₀‖² to the loss, where w₀ are the pre-trained weights, instead of decaying weights to zero. Parts of the network that are new (e.g. a new head) get an ordinary L2 penalty β/2 · ‖w‖².
- **Results ✔:** the authors recommend this simple penalty as the baseline for transfer learning; it beats plain weight decay and fine-tuning alone.
- **Transfer:** convolutional networks and vision. [my inference] Trivially applicable to a Transformer: compute the sum over the trainable weights. The coefficient α has to be tuned on dev loss.

### B2. EWC — Kirkpatrick et al. 2017 · `1612.00796`
- **Method ✔:** L(θ) = L_B(θ) + Σ_i (λ/2) · F_i · (θ_i − θ*_A,i)², where F is the diagonal of the Fisher information computed on the old task A. The penalty acts "like a spring" whose stiffness differs per parameter: stiff for parameters important to the old task.
- **Results:** MNIST permutations and Atari games, sequentially.
- **Transfer:** not NLP, and the Fisher needs data from the old task, which for you would be modern-Hebrew text (a sample is enough). [my inference] For a 461M-parameter model the diagonal Fisher is the size of the model; affordable but not free.

### B3. Recall and Learn / RecAdam — Chen et al. 2020 · `2004.12651`
- **Method ✔:**
  - Treat pre-training and fine-tuning as multi-task learning: Loss = λ·Loss_T + (1−λ)·Loss_S with the source term approximated.
  - **Pretraining Simulation:** since pre-training data is not available, replace the EWC Fisher with a constant, giving the quadratic penalty (γ/2)·Σ(θ_i − θ*_i)² around the pre-trained weights.
  - **Objective Shifting:** anneal λ over time (sigmoid schedule ⚠) from the source term toward the target term. Released as the RecAdam optimizer.
- **Results ✔:** state of the art on GLUE for BERT-base fine-tuning (beating BERT-large with direct fine-tuning).
- **Transfer:** fine-tuning for classification, not continued MLM. The method is only "L2-SP with a schedule", so it is cheap to try after B1.

### B4. LoRA Learns Less and Forgets Less — Biderman et al. 2024 · `2405.09673`
- **Method ✔:** compare LoRA with full fine-tuning on code and math, in instruction fine-tuning (~100K pairs) and **continued pre-training (20B tokens)**.
- **Results ✔:** with standard low ranks LoRA **substantially underperforms** full fine-tuning on the target domain, but it **forgets less** of the base model's abilities; it mitigates forgetting more than weight decay and dropout; full fine-tuning learns perturbations with a rank 10–100× larger than typical LoRA settings.
- **Transfer:** decoder LLMs of billions of parameters, far larger corpora. [my inference] It gives the sign of the trade-off you should expect from LoRA in `REPORT.md` C3: better preservation of the modern-Hebrew base, worse fit to the ancient text.

### B5. Continual Pre-Training of LLMs: How to (re)warm your model? — Gupta et al. 2023 · `2308.04014`
- **Method ✔:** continue pre-training Pythia-410M (trained on the Pile, 300B tokens) on SlimPajama (297B tokens) with linear warm-up and cosine decay; vary warm-up length and maximum learning rate; measure loss on upstream and downstream data.
- **Results ✔:** re-warming first raises the loss on both the old and new data, then improves the new-data performance; a learning rate that is too small learns slowly. See the paper for the effect of warm-up length and peak LR on forgetting.
- **Transfer:** causal LM, hundreds of billions of tokens. [my inference] The point carries over to your peak LR of 2e-5: the peak and warm-up length are knobs worth sweeping, and the early loss rise is expected, not a bug.

---

## C. Weight averaging and interpolation

### C1. Stochastic Weight Averaging (SWA) — Izmailov et al. 2018 · `1803.05407`
- **Method ✔:** average the weights visited along the SGD trajectory using a cyclical or constant learning rate during the last phase of training.
- **Results ✔:** better generalization than conventional SGD on CIFAR and ImageNet networks; flatter solutions; almost no overhead.
- **Transfer:** vision. [my inference] For you it means: save checkpoints from the last epochs and average them; no extra training cost, but BatchNorm is irrelevant for Transformers.

### C2. Model Soups — Wortsman et al. 2022 · `2203.05482`
- **Method ✔:** fine-tune several models from the same pre-trained init with different hyper-parameters, then average their weights. **Uniform soup** averages all; **greedy soup** adds models one at a time, keeping a model only if held-out accuracy does not drop.
- **Results ✔:** the greedy soup of ViT-G models reached 90.94% top-1 on ImageNet, beating the best single model from the sweep (90.78) and a re-evaluated ViT-G (90.47), with no extra inference cost.
- **Transfer:** vision models; models fine-tuned from one initialization lie in a single low-error basin. [my inference] Your runs of E1 (several seeds) could be averaged for free if they start from the same base, and greedy selection uses dev loss, which satisfies Rule R1.

### C3. WiSE-FT — Wortsman et al. 2022 · `2109.01903`
- **Method ✔:** interpolate the weights of the zero-shot (pre-trained) model and the fine-tuned model: θ = (1−α)·θ_0 + α·θ_ft.
- **Results ✔:** large robustness gains under distribution shift (4–6 points on ImageNet shifts) while keeping, even improving, accuracy on the target distribution.
- **Transfer:** CLIP-type vision models. [my inference] This is the cheapest way to answer "how much did we move from the base and what does it cost?": evaluate dev loss on Bible, DSS and modern Hebrew for several α, no retraining needed. It could also serve as a Step 3 control (a less-overfit model).

---

## D. Data reuse, small-data recipes, deduplication and memorization

### D1. Scaling Data-Constrained Language Models — Muennighoff et al. 2023 · `2305.16264`
- **Method ✔:** about 400 training runs, up to 900B tokens and 9B parameters (GPT-2 architecture), varying epochs of repeated data and compute; cosine schedules that decay 10×; no early stopping, so overfitting from repetition is visible.
- **Results ✔:** up to **4 epochs** of repeated data give negligible change in loss compared with unique data; with more repetition the value of added compute decays to zero. Mixing in code gave a 2× increase in effective tokens even on natural-language tasks; relaxing quality filters helps mainly for noisy datasets.
- **Transfer:** causal LM, English, billions of tokens. **Your 15 epochs are well above their 4-epoch regime**; [my inference] that does not mean 15 is wrong for MLM with re-drawn masks (each epoch is a different corruption), but it is the best published warning that returns diminish, and a reason to monitor dev loss per epoch. The "mix in other data" result supports `REPORT.md` A7 / the Rabbinic-mix idea.

### D2. Findings of the BabyLM Challenge — Warstadt et al. 2025 · `2504.08165`
- **What:** a competition on language-model training with a fixed data budget of under 100M words, scored on grammar, downstream tasks and generalization.
- **Method ✔:** participants submit to up to three tracks with different data restrictions; the organizers extract concrete recommendations from over 30 submissions.
- **Results ✔:** the winning submissions used the LTG-BERT architecture (the abstract is truncated in my copy; read the paper for the full list of recommendations).
- **Transfer:** the closest published setting to "small data, MLM encoder", but from scratch, English, and 10–100M words, which is 2–3 orders of magnitude more than the Bible.

### D3. Cramming: Training a Language Model on a Single GPU in One Day — Geiping & Goldstein 2022 · `2212.14034`
- **Method ✔:**
  - Train a BERT-style MLM from scratch for 24 hours on one consumer GPU; re-evaluate nearly every pipeline component.
  - WordPiece vocabulary of 2¹⁵ = 32,768 (smaller vocabularies were worse), data lower-cased and accent-stripped, **single-epoch training** where no data point is revisited, large batch sizes by accumulation, pre-normalization.
  - Learning-rate schedules compared (constant, inverse sqrt, cosine, triangular, one-cycle): the **triangular / one-cycle schedules end with the lowest MLM loss**, probably thanks to quick annealing at the end.
- **Results:** close to BERT on GLUE for the compute used; performance follows scaling laws.
- **Transfer:** from scratch, huge data, single pass. The recipe items that carry over are the LR-schedule ablation (final annealing) and the finding that small vocabularies hurt.

### D4. How to Train BERT with an Academic Budget — Izsak et al. 2021 · `2104.07705`
- **Method ✔:**
  - Recipe for pre-training in 24 hours on 8 12-GB GPUs.
  - Synchronize the warm-up and decay schedules with the time budget; this "greatly improves performance".
  - Use a larger (BERT-large-sized) model, pre-layer normalization, sparse token prediction, no NSP, single-sequence training.
  - **Pre-mask 10 copies of the corpus** instead of dynamic masking, because the benefit of dynamic masking in a low-resource setting is marginal and outweighed by its compute cost.
- **Transfer:** a compute-saving trick. For you compute is not the bottleneck, so dynamic masking (already used) is fine.

### D5. Deduplicating Training Data Makes Language Models Better — Lee et al. 2022 · `2107.06499`
- **Method ✔:**
  - **ExactSubstr:** a suffix array to find repeated substrings above a length threshold (50 tokens ⚠).
  - **NearDup:** MinHash over 5-grams with signatures of 9,000 hashes to estimate Jaccard similarity between documents, then remove near-duplicates.
- **Results ✔:** models trained on deduplicated data emit memorized text ten times less often and need fewer steps for equal or better accuracy; train-test overlap affects over 4% of validation sets of standard datasets.
- **Transfer:** web-scale data. **For you it is a data-leak check:** the Hebrew Bible has many parallel passages (e.g. Samuel/Kings versus Chronicles, repeated laws). [my inference] If a dev verse has a near-identical verse in train, dev loss is optimistic and Rule R1 comparisons are biased. The same applies to DSS biblical scrolls, which are copies of Masoretic verses already in train. A simple 5-gram Jaccard check is enough to measure it.

### D6. Quantifying Memorization Across Neural Language Models — Carlini et al. 2023 · `2202.07646`
- **Method ✔:** prompt the model with a prefix from the training data and test whether it continues with the true suffix.
- **Results ✔:** memorization grows log-linearly with (1) model capacity (larger models memorize 2–5× more), (2) the number of times an example is duplicated, (3) the number of context tokens used to prompt.
- **Transfer:** causal LMs. [my inference] For a masked encoder the analogue is: how well can the model fill in a masked word of a training verse compared to an unseen verse? That gap, per epoch, is a measure for Step 3. A 461M-parameter model repeating a small corpus for 15 epochs is in the risky corner of all three factors.

### D7. Emergent and Predictable Memorization in Large Language Models — Biderman et al. 2023 · `2304.11158`
- **Method ✔:** measure memorization across the Pythia model suite and fit scaling laws that forecast which sequences will be memorized from smaller, cheaper runs.
- **Transfer:** causal LMs, large scale; low priority. [my inference] The idea of using cheap partial runs (shorter or smaller) to forecast the behaviour of the full run is usable for choosing epochs.

---

## E. Evaluation under scarcity (variance, seeds, comparisons)

### E1. The MultiBERTs — Sellam et al. 2022 · `2106.16163`
- **Method ✔:** 25 BERT-base checkpoints that differ only in random initialization and data order; the **Multi-Bootstrap**, a non-parametric bootstrap that resamples both test examples and pre-training seeds, for deciding if an effect is real.
- **Results:** shows that conclusions drawn from one pre-training run can fail to generalize to the procedure.
- **Transfer:** pre-training seeds, not your continued-training seeds, but the logic is identical: resample over test items *and* training runs. [my inference] With 200-item cloze sets, test-item sampling noise is large; the bootstrap is the right way to put an interval on a comparison.

### E2. Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping — Dodge et al. 2020 · `2002.06305`
- **Method ✔:** fine-tune BERT hundreds of times per dataset changing only the random seed; separate the effects of weight initialization (of the new head) and data order.
- **Results ✔:** both factors contribute comparably to the variance of out-of-sample performance; the best-found model improves with the number of trials (so "best of N seeds" must be reported with N); on small datasets many runs can be stopped early.
- **Transfer:** classification fine-tuning (Step 2), not MLM. It matters for the classifier where seed variance will dominate.

---

## F. Tokenization and morphology

### F1. CANINE — Clark et al. 2022 · `2103.06874`
- **Method ✔:** an encoder operating on **characters**, with no fixed vocabulary; downsampling shortens the sequence before a deep Transformer stack; pre-training works on characters or uses subwords as a soft inductive bias.
- **Results ✔:** +2.8 F1 over a comparable mBERT on TyDi QA with fewer parameters.
- **Transfer:** a different architecture, so it cannot be applied to NeoDictaBERT without pre-training from scratch. [my inference] It is relevant as the principled answer to variable spelling (plene/defective, DSS orthography) since a character model does not see spelling variants as different tokens; for your setup the cheaper analogue is the robustness line you already have.

### F2. What's Wrong with Hebrew NLP? And How to Make it Right — Tsarfaty et al. 2019 · `1908.05453`
- **Method ✔:** describes the Onlp suite, a joint morpho-syntactic parsing framework for Modern Hebrew; the point is that in morphologically-rich languages errors in early morphological disambiguation cannot be recovered later in a pipeline, so morphology and syntax are inferred jointly.
- **Transfer:** modern Hebrew parsing. Useful as motivation for evaluating on morphology-sensitive items and for being careful with whole-word versus sub-word evaluation of cloze accuracy.

---

## G. Related to Step 3 (what the classifier could learn)

### G1. (Included above) Memorization and deduplication, D5–D7.
The deduplication and memorization papers are the closest tools for the question "did the classifier learn source rather than memorize text".

### G2. An Information-Theoretic Approach to Identifying Formulaic Clusters in Textual Data — Yoffe, Segev & Sober 2025 · `2503.07303`
- **What:** an **unsupervised** method that finds formulaic clusters (sections with systematic repetition and structural constraints) in text, applied to hypothesized authorial divisions of the **Hebrew Bible**.
- **Method ✔:** a weighted self-information distribution, extended from discrete to continuous differential self-information under multivariate Gaussian assumptions so it also works on neural embeddings; clusters are interpreted from their self-information profiles and characteristic recurring features.
- **Results ✔:** the approach isolates stylistic layers in the Bible and gives a quantitative framework for textual stratification.
- **Use:** directly on topic for the thesis. It shows what a "formulaic-ness" signal looks like in Biblical text, a likely confound: a classifier could separate P from D by formulaic style (genre) rather than source. Worth reading for Step 3 and as a baseline for what a non-neural method can recover.

---

## H. Open gaps (my honest assessment)

1. Almost none of these papers study **continued** MLM on a **tiny** corpus; none study Hebrew. Their claims are about from-scratch pre-training, fine-tuning, or large corpora.
2. I did not read every paper end-to-end; ⚠ numbers need checking in the PDFs.
3. Not covered here: curriculum or data ordering for MLM; learned/adaptive masking; knowledge distillation from the base model as an anchor (the closest in this set is weight-space anchoring B1–B3); ensembling of encoders; byte/character robustness beyond CANINE. My searches for curriculum learning and learned masking returned no relevant arXiv hits that I could verify.
4. No paper found on computational source criticism of the Pentateuch with a neural model; G2 is the only Hebrew Bible text-structure paper in this set.
5. Search was limited to arXiv; some Hebrew-NLP and digital-humanities work lives only on the ACL Anthology.

## Index of files (`papers2/`)

| File | Section |
|---|---|
| 2202.08005_Should_You_Mask_15 | A1 |
| 1907.10529_SpanBERT | A2 |
| 2010.01825_PMI_Masking | A3 |
| 1907.11692_RoBERTa | A4 |
| 2003.10555_ELECTRA | A5 |
| 1802.01483_L2-SP | B1 |
| 1612.00796_EWC | B2 |
| 2004.12651_RecAdam | B3 |
| 2405.09673_LoRA_Learns_Less_Forgets_Less | B4 |
| 2308.04014_Rewarm_Continual_Pretraining | B5 |
| 1803.05407_SWA | C1 |
| 2203.05482_Model_Soups | C2 |
| 2109.01903_WiSE-FT | C3 |
| 2305.16264_Data_Constrained_Scaling | D1 |
| 2504.08165_BabyLM_Findings | D2 |
| 2212.14034_Cramming | D3 |
| 2104.07705_BERT_Academic_Budget | D4 |
| 2107.06499_Deduplication | D5 |
| 2202.07646_Quantifying_Memorization | D6 |
| 2304.11158_Emergent_Memorization | D7 |
| 2106.16163_MultiBERTs | E1 |
| 2002.06305_FT_Init_DataOrder_EarlyStopping | E2 |
| 2103.06874_CANINE | F1 |
| 1908.05453_Whats_Wrong_Hebrew_NLP | F2 |
| 2503.07303_Formulaic_Clusters | G2 |
