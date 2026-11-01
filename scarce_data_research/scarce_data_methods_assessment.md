# Scarce-data techniques for Step 1 (continued MLM of NeoDictaBERT on Ancient Hebrew)

Source: `REPORT.md` in this folder (25 papers). Sections and paper ids below refer to that report. Nothing here comes from an online search. Claims from my own knowledge are tagged **[general knowledge]**; reasoning that goes beyond the report is tagged **[my inference]**.

## 1. Summary

1. Most worth trying first: a **seed-noise baseline plus a longer epoch sweep with dev-based early stopping** (B1 TAPT trained 100 epochs; E2 recommends ~20 epochs). It is cheap, it is the precondition for judging every other change under Rule R1, and the shipped 15 epochs may be short for a corpus this small.
2. Second: **mix in related text at matched size** (Rabbinic Hebrew per A1, or modern-Hebrew replay per report §0; A7 shows the size-matching rule). It attacks the scarcity directly rather than squeezing the same rows harder.
3. Third: a **regularised-towards-base variant** (LoRA C3, or Mixout E3 applied to MLM) as a control for forgetting and memorisation, which matters for Step 3.
4. Run the **tokenizer-fragmentation diagnostic** (report §0 stage 0, A1, B2–B4) before anything else; it costs minutes and decides whether vocabulary work is needed at all. Note that vocabulary extension conflicts with the frozen LM head.
5. The report does **not** cover span/salience masking, curriculum, checkpoint averaging, EWC, ensembling or batch-size effects; those are gaps, not negative results.

## 2. All techniques considered

| Technique | Source in report | Status | Fit for Step 1 | Cost | Risk | Priority |
|---|---|---|---|---|---|---|
| Dynamic re-masking across epochs | B1 (TAPT, 100 epochs, re-masked) | **possibly covered** (20% whole-word, redrawn every epoch) | high | none | – | – (done) |
| Many more epochs than 15, with dev early stopping | B1 (100 epochs), E2 (20 epochs) | not implemented (15 epochs fixed) | high | low (compute only) | memorisation; Step 3 | **1** |
| Seed-variance estimate (≥5 seeds, mean ± std) | §0 row 6, E1, E2 | not implemented (not stated in context) | high (needed for R1) | low–medium | none | **1** |
| Mix in Rabbinic Hebrew (Sefaria/Dicta) | A1 (corpus), §0 stage 1 | not implemented | high | medium (data prep) | dilution of Biblical signal | **2** |
| Replay of modern Hebrew to limit forgetting | §0 stage 1 (report synthesis, no paper result) | not implemented | medium | medium | dilution | 2 (same run family) |
| Match size of mixed-in text to the ancient data | A7 | not implemented | high (rule for the above) | none | – | with 2 |
| kNN selection of related unlabeled text | B1 (kNN-TAPT) | not implemented | medium | medium | needs a bigger pool | 4 |
| LoRA for the MLM stage | C3 | not implemented (full model trained) | medium | low | under-adaptation | **3** |
| Adapters (bottleneck) | C1 | not implemented | medium | low | under-adaptation | 3 (alt.) |
| MAD-X language adapter + invertible embedding adapter | C2 | not implemented | medium for Step 1, high for Step 2 | medium | same | 3 (alt.) |
| Mixout (stochastic reset toward base weights) | E3 | not implemented | medium | low | E1 says gains shrink once optimiser is fixed | 3 (alt.) |
| Gradual unfreezing (top layer first) | B5 | not implemented | medium | low | interacts with lr decay | 5 |
| Discriminative / layer-wise learning rates | B5 | **possibly covered** (xi 0.95 decay) | – | – | – | – (done) |
| Slanted-triangular / warm-up schedule | B5, E2 | **possibly covered** (schedule not stated in context) | medium | none | – | check |
| Bias-corrected AdamW | E1, E2 | **possibly covered** (standard in modern trainers) | high | none | – | check |
| Tokenizer-fragmentation diagnostic | §0 stage 0, A1, B2 | not implemented (not stated) | high (diagnostic) | minutes | none | **0** |
| Add vocabulary + random init (Extend) | B2 | not implemented | conditional on diagnostic | high | **conflicts with frozen LM head**; orthography encoding (Step 3) | 6 |
| Add vocabulary + informed init (WECHSEL / FOCUS) | B3, B4 | not implemented | conditional on diagnostic | high | as above | 6 |
| Tokenizer handling of punctuation / abbreviation marks | A1 | not implemented (not stated) | medium (DSS damage marks, maqaf, sof pasuq) | low | – | with 0 |
| Strip niqqud / orthographic normalisation | §0 stage 0, A6 | **possibly covered** (`train_no_pointed.csv`); further normalisation overlaps robustness line | – | – | Step 3 spelling confound | – |
| EDA-style token perturbation on rows | F1 | not implemented; **overlaps robustness line** | low–medium | low | corrupts syntax of 17-token rows | 7 |
| Back-translation / consistency (UDA) | F2 | not implemented | low (classifier method) | high | noisy on Biblical Hebrew | reject for Step 1 |
| Distil a teacher via Bible↔English pairs | A8 | not implemented | low for MLM; Step 2 candidate | high | – | reject for Step 1 |
| Re-initialise top layers | E1 | not applicable to Step 1 | – | – | – | Step 2 |
| PET / SetFit | D1, D2 | not applicable | – | – | – | Step 2 |
| Wasserstein evaluation of embedding separation | A2, A3 | not applicable to Step 1 | – | – | – | Step 2/3 |
| Expectation from data volume (10M–100M words) | B6 | – | context | – | – | needs corpus size |

## 3. Top candidates

### 3.1 Longer training with dev early stopping, and a seed-noise baseline (priority 1)
**What / source.** B1: TAPT ran **100 epochs** over the task's own small text with re-masking each epoch, and this stacked on top of DAPT. E2: fine-tuning instability is an optimisation problem and the remedy includes **longer training (e.g. 20 epochs)** with small lr and warm-up. §0 row 6 and E1/E2: report **mean ± std over ≥5 seeds** because variance dominates at small data sizes.
**Status.** The dynamic re-masking part is already in the recipe. The epoch count (15, fixed) and the seed estimate are not.
**Why it could help here.** With single 17-token rows and 20% masking, each epoch exposes only a fifth of the tokens as targets; B1's 100-epoch TAPT is the one result in the report that is about exactly this regime (small fixed text, re-masked). [my inference] 15 epochs may be well short of the dev-loss minimum for a 461M model on a small corpus, or it may already be past it; the current context does not say whether 15 was chosen by a curve or fixed in advance.
**Cost / risk.** Compute only. Risk: later epochs memorise verse text, which is exactly what Step 3 tests. Monitor the train-loss / dev-loss gap per epoch.
**What does not transfer.** B1 used RoBERTa-base, English, and classification as the end metric; the 100-epoch figure is not a recommendation for a 461M model. E2 is about fine-tuning, not MLM. The evidence supports "sweep it", not a specific number.
**Test under R1.** Run the shipped recipe with 3–5 seeds, continuing to e.g. 40–60 epochs, saving dev loss (fixed masks) per epoch. Output: (a) std of dev loss across seeds at epoch 15, which is the noise floor for all later comparisons; (b) the epoch of minimum dev loss per seed. Success: a mean dev-loss improvement at the best epoch larger than 2× the across-seed std at epoch 15 [my inference; the report gives no threshold]. The test cloze sets stay untouched.

### 3.2 Mixing in related text at matched size (priority 2)
**What / source.** A1: Rabbinic Hebrew (Sefaria ~200M words, Dicta Library ~20M) sits between modern and Biblical Hebrew and was enough to train BEREL from scratch. §0 stage 1 (the report's own synthesis, not a paper result): a replay mix of modern Hebrew to limit forgetting, optionally Rabbinic text as an intermediate step. A7: when mixing a high-resource language into ancient pre-training, they **matched its size to the ancient data** so it would not swamp it. B1 kNN-TAPT: select related unlabeled text by nearest-neighbour search.
**Status.** Not implemented.
**Why it could help here.** It is the only family in the report that adds information rather than regularising. Rabbinic text shares the consonantal script, much vocabulary and plene/defective variation [my inference]. [general knowledge] Sefaria also contains the Bible itself; the Biblical portion must be removed or the dev set is contaminated.
**Cost / risk.** Data preparation, longer epochs. Risk: dilutes the Biblical/DSS signal; mismatched orthography; dev loss on Bible/DSS may rise even if representations improve. Rabbinic text is not needed for Step 2 and could pull the model toward Rabbinic style.
**What does not transfer.** A1 trained from scratch at 220M words; A7 is Ancient Greek with RoBERTa and judged on UD tagging; neither measured the effect of mixing on a *small* target corpus. kNN-TAPT needs a candidate pool, which you do not have without Rabbinic data.
**Test under R1.** Arm A: shipped recipe. Arm B: same, with Rabbinic rows added at 1:1 size to the Bible+DSS rows (A7's rule), Biblical passages removed, same number of ancient-row exposures. Dev loss is computed on the ancient dev rows only. Needs the corpus size in words to set the mix; not given in the context.
**Step 2/3 link.** Lower memorisation pressure on verse text (more varied input) [my inference]. No obvious orthography confound, but DSS-vs-Masoretic spelling differences are not addressed by this.

### 3.3 Regularise towards the base model: LoRA, adapters or Mixout (priority 3)
**What / source.** C3 LoRA: freeze weights, train low-rank updates on Q and V, rank 4–16, merge after training. C1 adapters: bottleneck modules, train only those and layer norms. C2 MAD-X: a language adapter trained with MLM plus an invertible adapter at the embedding layer, later paired with a task adapter. E3 Mixout: during training, with probability p reset each parameter to its pre-trained value; E1 found its gain small once the optimiser is fixed.
**Status.** Not implemented (full model minus head and norm is updated).
**Why it could help here.** Full updates of 461M parameters on a small corpus are the classic memorisation setting [my inference]. These methods cap how far the model can move, which is also protection for Step 3. MAD-X's language-adapter/task-adapter split maps one-to-one onto Step 1/Step 2.
**Cost / risk.** Low compute; adapters train faster. Risk: under-adaptation, i.e. worse dev loss than full training. If so, that is useful information: it bounds how much of the current gain is "real" adaptation versus memorisation [my inference].
**What does not transfer.** C1–C3 are all evaluated on English classification or generation after fine-tuning, not on MLM continued pre-training; C2 trained language adapters with MLM but on Wikipedia-scale text. E3 is a fine-tuning regulariser.
**Test under R1.** Arm A: shipped recipe. Arm B: LoRA (r=8 and r=16) on attention, with the same epoch count found in 3.1. Arm C (optional): Mixout p≈0.9 (⚠ value from the report's recollection). Metric: dev loss, plus the train/dev gap as a memorisation indicator. Success: dev loss within noise of Arm A with a smaller train/dev gap, or better.

### 3.4 Tokenizer diagnostic, then (only if needed) vocabulary work (priority 0 as diagnostic, 6 as intervention)
**What / source.** §0 stage 0: count sub-words per word on Torah/DSS. A1: BEREL changed WordPiece so abbreviation marks stay inside tokens. B2: add new WordPiece units, enlarge the embedding and output matrices, continue MLM (500k steps there). B3/B4: initialise new rows from existing embeddings (WECHSEL needs a dictionary; FOCUS uses vocabulary overlap, which should be large between modern and ancient Hebrew).
**Status.** Not implemented. The diagnostic costs minutes.
**Why it may matter here.** NeoDictaBERT's 128k vocabulary is modern. [my inference] The diagnostic question is the DSS: reconstruction brackets, damage markers and non-standard spelling may fragment badly. The Bible (unpointed) probably fragments less. The number needed: mean sub-words per word on Bible rows and DSS rows separately, versus modern text.
**Conflict.** The LM head is frozen. Adding rows requires training new output rows; and B2 relies on tied input/output embeddings, which may or may not hold for NeoDictaBERT (not specified in the context). Either way this changes the shipped recipe's freezing policy.
**Risk for Step 3.** New tokens for DSS spellings would let the model encode orthography directly, which is precisely the confound Step 3 tests. Treat as a last resort.
**What does not transfer.** B2 added an entire new language to M-BERT with 500k steps; B3/B4 replace the whole tokenizer for cross-lingual transfer. Your case is a vocabulary that mostly already fits.

### 3.5 Cheap checks of the recipe (not experiments)
- Bias-corrected AdamW with warm-up (E1, E2): possibly covered; confirm.
- Gradual unfreezing (B5): not implemented; low cost; could be added to 3.3's arms rather than tested alone.
- Baseline before training: evaluate the untouched NeoDictaBERT on the dev loss with the same fixed masks. A3 found that an unadapted AlephBERT already carries signal on Biblical text; the size of the gain over the base model is a needed reference [my inference].

## 4. Rejected or deferred

| Technique | Reason |
|---|---|
| Chunking, packing, longer contexts | Settled by the pilot (context §3.2). Nothing in the report argues against single rows; A8 used max length 128 but for sentence embeddings. No report technique *requires* long contexts. |
| UDA consistency training (F2) | A classifier-stage semi-supervised method; needs back-translation, which the report itself says will be noisy on Biblical Hebrew. Keep for Step 2. |
| PET / SetFit (D1, D2), top-layer re-init (E1) | Step 2 methods. PET's caveat (needs a good MLM head) is an argument *for* Step 1, not a technique for it. |
| Teacher distillation via parallel data (A8) | Produces sentence embeddings, not an MLM; could become a Step 2 auxiliary signal if Bible↔translation pairs are used. |
| EDA on rows (F1) | Evidence is from English classification; random swap/deletion on 17-token Hebrew rows is as likely to teach bad syntax as to regularise. Overlaps the robustness line in progress; evaluate it there, not here. |
| Orthographic normalisation beyond stripping niqqud (A6) | Overlaps the robustness line and can mask the DSS-vs-Masoretic spelling signal that Step 3 must test. |
| Wasserstein separation metric (A2, A3) | An evaluation tool for embeddings, relevant to Steps 2–3 only. |

## 5. Experimental plan (max three)

| # | Experiment | Arms | Dev metric | Success criterion | Combine? |
|---|---|---|---|---|---|
| E1 | Seed noise + epoch sweep | shipped recipe × 3–5 seeds, up to 40–60 epochs, dev loss per epoch | dev loss (fixed masks); train/dev gap | best-epoch mean dev loss better than epoch-15 mean by > 2× seed std [my inference]; gap not widening sharply | Prerequisite for E2 and E3; run first |
| E2 | Mixed-in related text | shipped vs. +Rabbinic at 1:1 (Bible removed from Sefaria), same ancient-row exposures, best epoch from E1 | dev loss on ancient dev rows | improvement > 2× seed std | Separate from E3 (confounded otherwise) |
| E3 | Anchored update | shipped vs. LoRA r=8/16 (optional Mixout), epochs from E1 | dev loss; train/dev gap | within noise of shipped with a smaller gap, or better | Separate from E2; gradual unfreezing may be folded in |

Order by value per cost: E1 (cheap, unlocks the rest), E3 (cheap, informative about memorisation for Step 3), E2 (most expensive, most upside). If only two can run: E1 then E2.

Seed noise on the cloze test sets: each has 200 items, so the binomial standard error at ~50% accuracy is about 3.5 points [general knowledge]; differences smaller than roughly 7 points on those sets are not interpretable even once, which is another reason to decide on dev loss. The dev set size is not given in the context; if it is a few hundred rows, consider a dev-only cloze subset so that early stopping is not driven solely by loss [my inference].

## 6. Provenance

**Supported by the report.** B1's 100-epoch re-masked TAPT and its gain on top of domain pre-training; E2's recommendation for longer training; the ≥5-seed reporting rule (§0, E1, E2); A1's Rabbinic corpus and tokenizer change; A7's size-matching of mixed-in text; C1–C3 method descriptions; E3's mechanism and E1's finding that its gain is small; B2–B4's vocabulary extension and initialisation methods; A3's observation that an unadapted Hebrew BERT already carries Biblical signal.

**My inference.** That 15 epochs may be short for this regime; the 2× seed-std criterion; that mixed text reduces memorisation pressure; that LoRA's shortfall, if any, bounds the memorisation share; the DSS fragmentation guess; that Sefaria contains the Bible and must be filtered; the dev-only cloze suggestion.

**General knowledge, not from the report.** The binomial standard-error figure for 200-item test sets; that Sefaria includes the Biblical text.

**Uncertain.** Whether NeoDictaBERT ties input and output embeddings (affects §3.4); whether the shipped schedule uses warm-up and bias-corrected Adam; the Mixout p and EDA α values are ⚠ in the report; what the corpus size is in words, which §3.2 and B6 both need.

**Not covered by the report.** Span, salience-based or learned masking; curriculum or data ordering; checkpoint averaging or model merging; ensembling; EWC-style weight anchoring (Mixout is the closest); batch-size effects; early-stopping policy; any work on DSS text (the only DSS papers found were image-based and were dropped); any paper continuing pre-training of a modern-Hebrew BERT on Biblical text.
