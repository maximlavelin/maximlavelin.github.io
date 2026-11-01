# Scarce-data methods for adapting a Modern-Hebrew BERT to Ancient Hebrew (Torah / DSS)

**Goal:** continue pre-training a modern Hebrew BERT (AlephBERT / DictaBERT) on small amounts of ancient Hebrew, then fine-tune a classifier on very little labelled data.
**Papers (25 PDFs):** `papers/<arXiv-id>_<ShortName>.pdf`. All are arXiv preprints.

> **How reliable is this?** I read the abstracts of all 25 papers and the relevant method sections of the key ones (Don't Stop Pretraining, Extending mBERT, BEREL, MiqraBERT, the Ancient-Greek sentence-embedding paper, the Classical-Philology paper). Entries marked ✔ quote hyper-parameters I saw in the PDF. Entries marked ⚠ rely on my recollection of well-known papers, so check the exact numbers in the PDF before you copy them.
> **No paper covers DSS or Biblical Hebrew continued pre-training with a BERT directly.** The closest work is Latin/Greek/Rabbinic-Hebrew models and Biblical-Hebrew embedding studies. The rest is general low-resource technique.

---

## 0. Recommended pipeline (synthesis)

| Stage | What to do | Based on |
|---|---|---|
| 0. Tokenizer check | Measure how many sub-words per word the modern tokenizer produces on Torah/DSS. Niqqud/cantillation, plene/defective spelling and Aramaic prefixes fragment badly. **Strip or normalise niqqud and te'amim first.** If fragmentation is severe, add tokens (see §B). | BEREL, Extending mBERT, FOCUS |
| 1. Continued pre-training (MLM) | Run it on your corpus plus a **replay mix** of modern Hebrew to limit forgetting. Use a small LR (1e-5 to 5e-5), many epochs with re-masked data (TAPT used 100 epochs), dynamic masking at 15%. Optionally add Rabbinic text from Sefaria as an intermediate step, since it sits between modern and Biblical Hebrew. | Don't Stop Pretraining, BEREL, Latin BERT |
| 2. If memory or forgetting is a problem | Use LoRA or adapters for the MLM stage, or a language adapter with a task adapter. | MAD-X, LoRA, Adapters |
| 3. Classifier, fine-tuning | Use bias-corrected AdamW, LR ~2e-5, warm-up, **more epochs than the default 3**, and several seeds. Re-initialise the top layers. Try Mixout. Use layer-wise LR decay (ULMFiT). | Zhang et al., Mosbach et al., Mixout, ULMFiT |
| 4. If under ~100 labels | Try SetFit (contrastive sentence-transformer fine-tuning) or PET (cloze reformulation). | SetFit, PET |
| 5. Augmentation | Use token-level EDA and back-translation (modern Hebrew ↔ English) on the labelled data. Use consistency training (UDA) on the unlabelled data. | EDA, UDA, survey |
| 6. Evaluation | Report mean ± std over ≥5 seeds, because variance dominates at this data size. | Zhang et al., Mosbach et al. |

---

## A. Closest to your domain (Hebrew, ancient and historical languages)

### A1. BEREL: BERT Embeddings for Rabbinic-Encoded Language — Shmidman et al. 2022 · `2208.01875`
- **What:** a BERT for Rabbinic Hebrew and Aramaic, motivated by modern Hebrew models failing on it. It is the best precedent for "modern Hebrew model is wrong for old Hebrew".
- **Method ✔:**
  - Trained from scratch with the original BERT script and the BERT-base config.
  - Corpus is ~220M words (Sefaria 200M plus Dicta Library 20M).
  - Vocabulary is 128,000 word pieces.
  - The WordPiece script was changed so that an apostrophe or double-quote that belongs to a Rabbinic abbreviation (for example acronyms and apocopated forms) stays inside the token instead of being split off. Such abbreviations are about 1 in 5–10 words.
- **Results:** it beats AlephBERT and HeBERT on a homograph-disambiguation challenge set built from Rabbinic texts.
- **Take-away:** corpus-specific tokenization matters. Check how your tokenizer treats geresh, maqaf, sof-pasuq and the like.
- **Caveat:** 220M words is far more than the Torah (~300k words) and DSS. Their recipe is not a scarce-data recipe.

### A2. MiqraBERT: Sentence-BERT fine-tuning for Biblical Hebrew parallels — Smiley 2026 · `2606.19638`
- **What:** AlephBERT fine-tuned with a Siamese (Sentence-BERT) setup for verse-level similarity in Biblical Hebrew, using only **1,650 labelled pairs**. It is the only paper I found that adapts a modern Hebrew BERT to Biblical text with scarce data.
- **Method ✔:**
  - Two verses go through a shared AlephBERT encoder, and mean pooling gives 768-d embeddings.
  - Cosine similarity is regressed onto the label (parallel = 1, non-parallel = 0).
  - Data is 825 true parallels (Chronicles synoptic material plus poetic parallelism studies) and 825 random negatives.
  - Split is 70/15/15, trained for **2 epochs** (validation plateaued, then overfit), ~36 s on a T4.
  - Evaluated with the Wasserstein distance between the parallel and non-parallel cosine distributions.
- **Results:** better separation than the off-the-shelf encoders (see paper tables). This is a small, new preprint, so treat the numbers cautiously.
- **Recreate:** `sentence-transformers` with AlephBERT plus a mean-pooling layer, `CosineSimilarityLoss`, 2 epochs.

### A3. Intertextual Parallel Detection in Biblical Hebrew: A Transformer-Based Benchmark — Smiley 2025 · `2506.24117`
- **What:** a benchmark of E5, AlephBERT, MPNet and LaBSE for finding Samuel/Kings ↔ Chronicles parallels, zero-shot.
- **Method ✔:** per-verse embeddings, cosine similarity, and Wasserstein distance between the parallel and non-parallel score distributions. Code is at github.com/dmsmiley/detect-bh.
- **Results:** E5 is best at detecting parallels, AlephBERT is best at rejecting non-parallels.
- **Use:** a ready evaluation protocol, and evidence that an unadapted AlephBERT already carries signal on Biblical text.

### A4. AlephBERT — Seker et al. 2021 · `2104.04052`
- **What:** the standard Modern-Hebrew BERT-base. It is trained from scratch on a larger corpus and vocabulary than earlier Hebrew PLMs (OSCAR, Wikipedia and tweets ⚠, vocabulary ≈52k ⚠).
- **Method:** standard MLM (the paper reports no NSP), with whole-word-aware vocabulary choices and a new benchmark suite (segmentation, POS, morphology, NER, sentiment).
- **Use:** a base model candidate. Its evaluation suite is useful for checking that continued pre-training does not destroy modern-Hebrew ability.

### A5. DictaBERT — Shmidman et al. 2023 · `2308.16687`
- **What:** a newer, stronger Modern-Hebrew BERT-base, with released fine-tuned heads for prefix segmentation, morphological tagging and QA.
- **Method:** BERT-base pre-training on a large Hebrew corpus. Details are in the paper.
- **Use:** probably the best starting checkpoint. It comes from the same group (DICTA) as BEREL, so ancient-text issues are known to them.

### A6. Latin BERT — Bamman & Burns 2020 · `2009.10053`
- **What:** BERT for Latin, 642.7M words from Classical to modern.
- **Method:** BERT-base, subword vocabulary tailored to Latin, and heavy pre-processing/normalisation of orthography (for example u/v and i/j). Evaluated on POS tagging (new SOTA on all three UD Latin sets), restoring missing text, word-sense disambiguation (new dataset) and contextual nearest-neighbour search.
- **Use:** shows the downstream uses scholars care about, and the value of orthographic normalisation. This is the "template" paper for a historical-language BERT.

### A7. Exploring Large Language Models for Classical Philology (GreBERTa / GreTA / PhilBERTa / PhilTa) — Riemenschneider & Frank 2023 · `2305.13698`
- **What:** RoBERTa and T5 for Ancient Greek, in monolingual and multilingual (Greek + Latin + English) variants.
- **Method ✔:**
  - They collected Ancient Greek with a retrieve-and-filter pipeline: text-quality filtering, removal of Latin/English/German passages, and de-duplication.
  - They chose RoBERTa over BERT because dynamic masking uses the data better.
  - For the multilingual models they added English translations of ancient texts, matched in size to the ancient data, to avoid the English overwhelming it.
  - Evaluation is on two UD treebanks (dependency parsing, lemmatization, UPoS/XPoS) and probing tasks. One probing task is **few-shot**: the MLM head is fine-tuned on 10–50 synonym/antonym examples.
- **Results:** the models beat prior Ancient Greek BERTs. The multilingual variants help on some tasks, and T5's decoder helps lemmatization.
- **Use:** a data-curation checklist, and a worked example of mixing a related high-resource language into ancient pre-training (for you: modern Hebrew, Rabbinic Hebrew, or English translations of Torah/DSS).

### A8. Sentence Embedding Models for Ancient Greek via Multilingual Knowledge Distillation — Krahn et al. 2023 · `2308.13116`
- **What:** sentence embeddings for Ancient Greek from a small parallel corpus. A strong scarce-data idea: **distil a good English/multilingual teacher into your ancient-language student**.
- **Method ✔:**
  - Build a parallel Ancient-Greek ↔ English sentence dataset by aligning documents with their translations, using sentence-embedding alignment.
  - Teacher M (mpnet or st5) embeds the English side. The student embeds both sides and is trained with MSE so that M̂(s) ≈ M(t) and M̂(t) ≈ M(t) (the Reimers & Gurevych 2020 recipe).
  - Student is a BERT-like model. 15 epochs with mpnet, 30 with st5. Batch size 128, max length 128, 2,000 warm-up steps, LR 2e-5.
  - Evaluate every 500 steps on 5k held-out pairs (STS and translation search) and keep the best checkpoint.
- **Results:** new Ancient Greek STS, translation-search and retrieval benchmarks, and large gains over the baselines (see paper).
- **Recreate for Hebrew:** this needs aligned Torah ↔ English (or modern Hebrew) pairs, which exist (Sefaria). The `sentence-transformers` multilingual distillation training script does this.

## B. Continued pre-training and adapting to a new language or domain

### B1. Don't Stop Pretraining (DAPT / TAPT) — Gururangan et al. 2020 · `2004.10964` ⭐
- **What:** a second phase of MLM pre-training on domain text (DAPT) or on the task's own unlabeled text (TAPT) improves classification, including in low-resource settings.
- **Method ✔:**
  - Continue RoBERTa's MLM objective. DAPT: 12.5k steps (a single pass) over the domain corpus.
  - TAPT: **100 epochs** on the task's training data, with the data **randomly re-masked** each time (15% masking) as artificial augmentation.
  - Optional extra step: select additional task-relevant unlabeled text by nearest-neighbour search (kNN-TAPT).
  - Combine them: DAPT then TAPT, then fine-tune.
- **Results:** across 4 domains and 8 tasks, DAPT beats the base model, TAPT adds on top of DAPT, and DAPT+TAPT is best. Gains are largest where the domain is far from the original pre-training distribution.
- **Use:** this is your main recipe. Your domain (ancient Hebrew) is far from Modern Hebrew, so DAPT-style gains are plausible. TAPT on your labelled classifier texts is nearly free.

### B2. Extending Multilingual BERT to Low-Resource Languages — Wang et al. 2020 · `2004.13640`
- **What:** the "Extend" method: add the missing vocabulary of a new language to M-BERT and continue pre-training. It is directly relevant if the Hebrew tokenizer fragments Biblical Hebrew.
- **Method ✔:**
  - Train a new WordPiece vocabulary on target text, and add new pieces not in the original.
  - Enlarge the embedding matrix from V_mbert×d to (V_mbert+V_new)×d. M-BERT ties encoder and decoder weights, so the output layer grows too. New rows are initialised with BERT's usual random init.
  - Continue MLM pre-training on target text. Batch 32, LR 2e-5, **500k iterations** (versus 1e-4 and 2M for a from-scratch monolingual model).
- **Results:** better NER than M-BERT and comparable or better than a from-scratch monolingual model in several languages, even without extra data (using Wikipedia only).
- **Caveat:** 500k steps needs a lot of text. Scale it down for a Torah/DSS-size corpus.

### B3. WECHSEL — Minixhofer et al. 2022 · `2112.06598`
- **What:** swap the tokenizer for a target-language one and **initialise the new embeddings from the source model's embeddings** using multilingual static word vectors and a bilingual dictionary. It is a smarter alternative to random initialisation of added tokens.
- **Method:** (1) train a new tokenizer; (2) train or fetch static embeddings for the source and target languages; (3) align them with a bilingual dictionary (Procrustes); (4) each new token embedding becomes a similarity-weighted average of the source token embeddings nearest to it; (5) continue training on target text.
- **Results:** substantial savings of compute and data over training from scratch.
- **Recreate:** needs a source↔target dictionary. For Ancient ↔ Modern Hebrew you could build one from lemma overlap or a Strong's-style lexicon.

### B4. FOCUS — Dobler & de Melo 2023 · `2305.14481`
- **What:** a dictionary-free alternative to WECHSEL. Each new token is a sparsemax-weighted combination of the *overlapping* tokens (those shared by the old and new vocabularies), chosen by similarity in an auxiliary static embedding space trained on the target corpus.
- **Use:** since Ancient and Modern Hebrew share much vocabulary, the overlap is large, which is exactly where FOCUS works well. It also needs only a small target corpus to train the auxiliary fastText-style embeddings.

### B5. ULMFiT — Howard & Ruder 2018 · `1801.06146`
- **What:** the original recipe for fine-tuning a language model with little labelled data.
- **Method (from the paper ⚠ check values):**
  - Discriminative fine-tuning: a different LR for each layer, dropping by about 2.6× per layer going down.
  - Slanted triangular learning-rate schedule.
  - Gradual unfreezing: unfreeze the top layer first, then one more layer per epoch.
  - Three stages: general LM, target-domain LM fine-tuning, classifier.
- **Results:** error cut by 18–24% on most datasets, and with 100 labelled examples it matches training from scratch on 100× more data.
- **Use:** the three-stage logic (general → ancient-domain LM → classifier) is exactly your plan. The discriminative LR and gradual unfreezing tricks work with BERT.

### B6. When Do You Need Billions of Words of Pretraining Data? — Zhang et al. 2021 · `2011.04946`
- **What:** learning curves for MiniBERTas pre-trained on 1M, 10M, 100M and 1B words.
- **Results:** models need only ~10M–100M words to learn most syntactic and semantic features that probes can detect. Commonsense and many NLU tasks need much more.
- **Use:** an expectation-setter. A few million words of ancient Hebrew teach a lot of surface and syntactic structure but cannot teach world knowledge, so lean on the modern Hebrew base for the rest.

---

## C. Parameter-efficient adaptation (less overfitting, less forgetting)

### C1. Adapters — Houlsby et al. 2019 · `1902.00751`
- **Method:** insert two small bottleneck modules (down-project → non-linearity → up-project, with a residual connection) in each Transformer layer. Freeze the BERT weights and train only the adapters plus layer norms.
- **Results:** within 0.4% of full fine-tuning on GLUE while training ~3.6% of the parameters per task ⚠.

### C2. MAD-X — Pfeiffer et al. 2020 · `2005.00052`
- **Method:** (1) train a **language adapter** with MLM on target-language text (adding an invertible adapter at the embedding layer); (2) train a **task adapter** on source-language labelled data; (3) at test time, swap in the target language adapter.
- **Use:** the language-adapter-plus-task-adapter split fits "ancient Hebrew MLM, then classifier" exactly. It also lets you train the classifier on modern Hebrew labelled data and swap in the ancient-language adapter, if such data exists.

### C3. LoRA — Hu et al. 2022 · `2106.09685`
- **Method:** freeze the weights and add trainable low-rank updates ΔW = BA (rank r, typically 4–16) to the attention projections (Q and V). Scale by α/r. The updates can be merged into the weights after training.
- **Use:** simple, works for both the MLM stage and the classifier. Use the `peft` library.

---

## D. Few-shot classification

### D1. PET — Schick & Schütze 2021 · `2001.07676` and "Small Language Models Are Also Few-Shot Learners" `2009.07118`
- **Method:** turn each input into a cloze sentence, for example "ביקורת: <text> . סך הכל זה [MASK]", and map the label to a verbalizer word. (1) Fine-tune one model per pattern on the few labelled examples. (2) Use the ensemble to soft-label unlabelled data. (3) Train a normal classifier on the soft labels. iPET repeats this iteratively.
- **Results:** beats standard fine-tuning by a large margin with tens of examples. The second paper shows an ALBERT-size model matches GPT-3 on SuperGLUE few-shot.
- **Caveat:** it relies on the MLM head, so the model must be good at masked prediction in your language. That favours doing the continued-MLM step first. It also needs natural-language patterns in Hebrew.

### D2. SetFit — Tunstall et al. 2022 · `2209.11055`
- **Method:** (1) generate positive and negative pairs from the few labelled examples; (2) fine-tune a sentence-transformer contrastively; (3) fit a logistic-regression head on the embeddings.
- **Results:** competitive with much larger models using about 8 examples per class. No prompts are needed.
- **Use:** pair it with the MiqraBERT-style Sentence-BERT model from A2, or the distilled embeddings from A8.

---

## E. Fine-tuning stability with small datasets

### E1. Revisiting Few-sample BERT Fine-tuning — Zhang et al. 2021 · `2006.05987`
- **Findings:** (1) use BERTAdam *with* bias correction (omitting it, as the original BERT code did, causes instability); (2) re-initialise the top few layers (try the top 3–6) before fine-tuning; (3) train for more iterations than 3 epochs. With these, many "fix" methods give much smaller gains.

### E2. On the Stability of Fine-tuning BERT — Mosbach et al. 2021 · `2006.04884`
- **Findings:** instability comes from optimisation (vanishing gradients early in training), not from catastrophic forgetting or small data. Remedy: bias-corrected Adam, a small LR with warm-up, and **longer training (e.g. 20 epochs)**.

### E3. Mixout — Lee et al. 2020 · `1909.11299`
- **Method:** during fine-tuning, with probability p replace each parameter by its pre-trained value, as in dropout but toward the original weights. A typical p is ~0.9 ⚠.
- **Use:** keeps the fine-tuned model close to the pre-trained one. Zhang et al. found it adds little once the optimiser issues are fixed, so try it last.

## F. Data augmentation

### F1. EDA — Wei & Zou 2019 · `1901.11196`
- **Method:** four operations: synonym replacement, random insertion, random swap, random deletion. The recommended α is ~0.05–0.1 (the fraction of words changed) with 4–16 augmented sentences per original, more for smaller datasets ⚠.
- **Results:** training with EDA on 50% of the data matches training on 100% without it (average over five datasets).
- **Hebrew note:** synonym replacement needs a Hebrew thesaurus or WordNet. Use random deletion/swap, or nearest neighbours from the model's own embeddings, if you have none.

### F2. UDA — Xie et al. 2020 · `1904.12848`
- **Method:** for unlabelled data, add a consistency loss (KL divergence) between predictions on the original text and on an augmented copy (back-translation or TF-IDF word replacement), together with the usual supervised loss.
- **Results:** with 20 labelled IMDb examples it reached an error rate of about 4% (the paper's headline; see the PDF).
- **Use:** your unlabelled ancient text becomes useful in the classifier stage. Back-translation needs a Hebrew↔English MT model and will be noisy on Biblical Hebrew.

## G. Open gaps (my honest assessment)

1. I found **no paper that continues pre-training a Modern-Hebrew BERT on Biblical or DSS text**. Doing so (with proper ablations) would itself be a contribution.
2. Search coverage was limited to arXiv (it works from this environment). ACL Anthology papers on Hebrew NLP (for example work on Biblical Hebrew morphology or Dicta's other tools) may exist and are not covered here.
3. For the DSS in particular, the computational work I found is on images (manuscript dating, writer identification), so I dropped it as irrelevant to a text BERT.
4. Numbers marked ⚠ should be checked in the PDFs before you cite them.

## Index of files

| File | Section |
|---|---|
| 2208.01875_BEREL_Rabbinic_Hebrew | A1 |
| 2606.19638_MiqraBERT | A2 |
| 2506.24117_Biblical_Hebrew_Parallel_Detection | A3 |
| 2104.04052_AlephBERT | A4 |
| 2308.16687_DictaBERT | A5 |
| 2009.10053_Latin_BERT | A6 |
| 2305.13698_Classical_Philology_LMs | A7 |
| 2308.13116_Ancient_Greek_Sentence_Embeddings | A8 |
| 2004.10964_Dont_Stop_Pretraining | B1 |
| 2004.13640_Extending_mBERT_Low_Resource | B2 |
| 2112.06598_WECHSEL | B3 |
| 2305.14481_FOCUS | B4 |
| 1801.06146_ULMFiT | B5 |
| 2011.04946_Billions_of_Words_Pretraining | B6 |
| 1902.00751_Adapters_Houlsby, 2005.00052_MAD-X, 2106.09685_LoRA | C1–C3 |
| 2001.07676_PET, 2009.07118_Small_LMs_Few_Shot, 2209.11055_SetFit | D |
| 2006.05987_Revisiting_Few_Sample_BERT_FT, 2006.04884_Stability_of_FT_BERT, 1909.11299_Mixout | E |
| 1901.11196_EDA, 1904.12848_UDA | F |
