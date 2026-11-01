# Work log (literature pass 2) — status: BLOCKED at download step

## Blocker
arxiv.org and aclanthology.org are denied by the session network policy (curl: CONNECT 403; WebFetch: ENOTFOUND).
No PDF can be saved, so no new paper can be read in full, and no entry may be marked VERIFIED. Nothing was written up.
WebSearch works (returns titles/URLs/snippets only).

## Source file
The "original file" is the PDF Pertubation_articles.pdf (66 pp). Its text was extracted with `pdftotext -layout`.
`original_notes_verbatim_from_pdf.md` = that text with only the chat preamble (first 3 lines + prefix of line 4) removed.
Caveat: the PDF hard-wraps lines (also inside table rows), so the extraction is not byte-identical to the source .md.
Observations for the "Corrections" list (not fixed): scope note says 19/20 papers while the file has 22 entries;
sections 13 and 19 headings are present but the Index/“Additions” tables for 21-22 have no comparison rows;
entries 21-22 and the Relevance/Options sections use a different heading style (no "##").

## Selection criteria (planned)
Priority: MLM pre-training/continued pre-training robustness > WordPiece/subword robustness > Hebrew/Semitic > historical/ancient text >
representation-stability evaluation > source/genre/authorship confounds. Exclude near-duplicates of FreeLB/SMART/RoAST/EDA/TextFooler/BERT-Attack.
Only papers that can be downloaded and read in full become numbered entries.

## Candidate list (UNVERIFIED, from my memory; only ALUM's title/authors confirmed by one web search; no content read)
1. ALUM, Liu et al. 2020 (adversarial MLM pre-training), arXiv 2004.08994 (confirmed by search)
2. CharBERT, Ma et al. 2020 (noisy LM pre-training task)
3. CLEAR, Wu et al. 2020 (contrastive + MLM)
4. MaxMatch-Dropout, Hiraoka et al. 2022 (WordPiece subword regularisation)
5. Adv-BERT / BERT misspellings (Sun et al. 2020) or Kumar et al. 2020
6. Gueta et al. 2022 (Hebrew BERT vocabulary study)
7. BEREL (Lustig et al. 2022, Rabbinic Hebrew)
8. Bollmann 2019 (historical spelling normalisation)
9. Riemenschneider & Frank 2023 (LMs for classical philology)
10. Elazar et al. 2021 (consistency of pretrained LMs)
11. Wegmann et al. 2022 (style vs content representations)
12. ByT5, Xue et al. 2022 (tokenizer-free, noise robustness)
13. Lourie, Ben-Dov & Sharan 2025 (Qumran clustering) — existence/link to be searched
Search queries not yet run beyond the ALUM check; to be run once downloads work.
