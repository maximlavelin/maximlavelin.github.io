# Work log — literature pass 2 (entries 23–35)

## Source file and handling
- The "original file" is the PDF `Pertubation_articles.pdf` (66 pp), extracted with `pdftotext -layout`. `original_notes_verbatim_from_pdf.md` is that text with only the chat paragraph at the top removed. `robustness_literature_notes_extended.md` contains every one of its 2,828 lines unchanged and in order (checked by a script); everything added is in new blocks (updated scope note at the top; index, entries 23–35 and comparison rows after entry 22; updated relevance/options/gaps/corrections at the end).
- Caveat: the PDF hard-wraps lines (also inside table rows), so it is not byte-identical to the source `.md`.

## Network
First attempt: arxiv.org and aclanthology.org were blocked (proxy 403). After the user allowed them, all downloads worked (arXiv and ACL Anthology only). See `download_report.tsv`.

## Selection criteria (written before reading)
1. Priority: (1) robustness in MLM pre-training/continued pre-training; (2) WordPiece/subword/tokenizer-free robustness; (3) Hebrew/Semitic; (4) historical/ancient text; (5) stability/agreement evaluation; (6) source/genre/authorship confounds.
2. Prefer MLM-stage and spelling-variation relevance over generic adversarial NLP; exclude near-duplicates of FreeLB, SMART, RoAST, EDA, TextFooler, BERT-Attack.
3. Only papers that could be downloaded and read become numbered entries; maximum 13.

## How candidates were found (honest account)
- Web searches actually run (WebSearch, standard mode): (a) "ALUM Adversarial Training for Large Neural Language Models arXiv 2004.08994"; (b) "Lourie Ben-Dov Sharan 2025 Qumran Dead Sea Scrolls clustering Ancient Language Processing Workshop"; (c) "Dead Sea Scrolls Hebrew orthography plene defective spelling variation language model BERT normalization" (no computational result; only non-computational orthography literature); (d) "NeoDictaBERT DictaBERT robustness spelling variation Hebrew pretrained model" (no robustness paper; gave arXiv 2510.20386); (e) the title of the Agrawal et al. paper (to find its arXiv id 2504.02733).
- **Most of the 13 candidates were chosen from my prior knowledge of the literature, not discovered by broad search**; each was verified by downloading the PDF and checking its title/authors in the extracted text. Consequently the search coverage is narrower than a systematic search: no query was run for e.g. Arabic orthographic variation, Akkadian/Latin LMs, OCR/HTR-noise robustness of encoders, or tokenisation-robustness benchmarks beyond those named. This is a limitation of this pass.

## Included (13)
23 ALUM, 24 CharBERT, 25 CLEAR, 26 MaxMatch-Dropout, 27 ByT5, 28 NeoDictaBERT, 29 AlephBERTGimmel (Gueta et al.), 30 BEREL, 31 Bollmann 2019, 32 Riemenschneider & Frank 2023, 33 Elazar et al. 2021, 34 Wegmann et al. 2022, 35 Lourie et al. 2025.

## Rejected / not numbered
- Sun et al. 2020, Adv-BERT (arXiv 2003.04985): downloaded and title-checked; dropped because the cap of 13 was reached and it is closest to generic adversarial NLP (shows BERT's misspelling brittleness, overlaps the existing entries 12–13 and CharBERT). File `papers/Sun2020_AdvBERT.pdf` kept.
- DictaBERT (arXiv 2308.16687), AlephBERT (2104.04052): seen as references; not downloaded.
- Not searched: Akkadian/Latin/Greek pre-training beyond entry 32; Arabic orthography.
- Found but not downloaded: none (no failed download after access was opened).

## Reading depth and status decisions
- VERIFIED: 23, 24, 25, 26, 28, 29, 30. PARTIAL: 27 (ByT5: §6 noise section and design read, not all per-task tables), 31 (Bollmann: Tables 3 and 5, §2 survey and §5.1 skimmed), 32 (Riemenschneider: Latin tables and probing appendix not read), 33 (Elazar: §7 representation analysis not read), 34 (Wegmann: Tables 4–7 and error analysis skimmed), 35 (Lourie: the main comparison is in a figure I could not extract).
- BEREL (30): the experiments page is an embedded image with no text layer (no OCR available); I read it from a rendered PNG at 220 dpi. Its table numbers are therefore transcribed by eye and are **not covered by the automatic number check**.

## Quality checks run (script `check.py`, kept outside the repo)
- Every decimal / percentage / thousands-separated number in the paper-claim parts of entries 23–35 (lines not marked as my analysis, derived, or citation metadata) was looked up in the paper's extracted text (raw and layout mode). Result: all found except: the arXiv number in entry 29's citation (not in the paper), two Table 3/5 values of entry 29 that the extraction prints with a space instead of a decimal point ("87 13", "97 27"; present and equal), and the 19 numbers of entry 30 (image page, see above). One real error was found and fixed: a derived difference in entry 26 had been written as +0.03 and is +0.01 (82.18 → 82.19). Integers (e.g. "10 days") and values written without a leading digit were not machine-checked except the Wegmann table values, which were grepped by hand.
- Format: entries 23–35 each have the eight parts, a status, and a "Transfer to my setting (my analysis)" line. The index additions and the comparison additions contain the same entries 23–35 (the comparison additions also give rows for the previously missing 21 and 22).
- PDFs: all 31 PDF names that the file mentions exist in `papers/`. The original text names no PDF for entries 17, 21, 22; I saved them as `Ribeiro2020_CheckList.pdf`, `Li2023_PerturbScore.pdf`, `Agrawal2025_PerturbedInstructions.pdf`. Entry 8 has none (NOT FOUND). Titles of all 20 re-downloaded old PDFs were checked against their entries' titles on page 1; I did not re-verify the old entries' contents.

## Items I could not verify
- Venues not printed in the PDFs (24 COLING?, 26 COLING?, 27 TACL volume, 29, 30, 31 NAACL?, 32 ACL?, 33 TACL?, 34 RepL4NLP?) — marked "not verified" in each entry. Repository names cut by line breaks (26, 32, 34) and the BEREL bit.ly link were not opened.
