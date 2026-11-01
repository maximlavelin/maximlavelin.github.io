# Suggestions for Step 1 (continued MLM of NeoDictaBERT on Ancient Hebrew)

Condensed from `scarce_data_methods_assessment.md`; paper references point to `REPORT.md`.

## Do first (minutes to hours)

1. **Measure tokenizer fragmentation.** Mean sub-words per word on Bible rows, DSS rows and a modern-Hebrew sample, separately. Also inspect how the tokenizer treats maqaf, sof pasuq and any DSS damage/reconstruction marks (BEREL, A1). This decides whether vocabulary work is needed; expect that it is not for the Bible.
2. **Score the untouched base model** on the dev loss with the same fixed masks, so the gain of the shipped recipe over NeoDictaBERT itself is known (A3 found an unadapted Hebrew BERT already carries Biblical signal).
3. **Confirm the optimiser settings:** bias-corrected AdamW, warm-up (E1, E2). Probably already true; costs nothing to check.

## Experiments, in order of value per cost

### E1. Seed noise + epoch sweep
- Shipped recipe, 3–5 seeds, continue to 40–60 epochs, log dev loss and train loss every epoch.
- Gives the across-seed std of dev loss at epoch 15 (the noise floor for all later comparisons) and the best-epoch per seed.
- Success: best-epoch dev loss beats the epoch-15 mean by more than 2× the seed std, with no sharp widening of the train/dev gap.
- Source: B1 (TAPT, 100 re-masked epochs), E2 (longer training), §0 row 6 (≥5 seeds).
- Watch: memorisation of verse text (Step 3 tests this).

### E2. Mix in related text at matched size
- Add Rabbinic Hebrew rows (Sefaria / Dicta Library, A1) at 1:1 with the Bible+DSS rows, Biblical passages removed from the added set. Keep the number of ancient-row exposures equal to the shipped recipe. Alternative: a modern-Hebrew replay mix (§0 stage 1).
- Dev loss computed on ancient dev rows only.
- Success: improvement beyond 2× seed std from E1.
- Source: A1, A7 (match the size of the mixed-in text), §0 stage 1.
- Needs: corpus size in words to set the mix.

### E3. Anchored update (control for forgetting / memorisation)
- LoRA r=8 and r=16 on attention (C3), epochs from E1. Optional arm: Mixout p≈0.9 (E3, value ⚠ in the report). Optional: gradual unfreezing (B5) folded in.
- Success: dev loss within noise of the shipped recipe with a smaller train/dev gap, or better.
- If it is clearly worse, that bounds how much of the full-update gain is memorisation.
- Run separately from E2.

## Hold back

- **Vocabulary extension** (B2 Extend, B3 WECHSEL, B4 FOCUS): only if step 1 shows heavy DSS fragmentation. Conflicts with the frozen LM head, and new tokens for DSS spellings would encode orthography, which Step 3 must rule out.
- **EDA-style perturbation (F1) and further orthographic normalisation (A6):** belong to the robustness line already in progress.

## Not for Step 1

- UDA (F2), PET/SetFit (D1, D2), top-layer re-initialisation (E1): Step 2.
- Teacher distillation via Bible↔English pairs (A8), Wasserstein separation metric (A2, A3): Step 2/3.
- Chunking, packing, longer contexts: settled by the pilot.

## Rules for all runs

- Decide on dev loss only; cloze test sets are evaluated once, at the end.
- 200-item cloze sets have a binomial standard error of about 3.5 points near 50% accuracy, so test-set differences under ~7 points are not interpretable.
- Report mean ± std over seeds.

## Missing inputs

- Corpus size in words (Bible rows, DSS rows).
- Whether NeoDictaBERT ties input and output embeddings.
- Dev set size, and whether a dev-only cloze subset is possible.
