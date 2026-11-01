# Robustness to input perturbation in language models: literature notes

## Scope note

This file summarises 19 papers that were downloaded, read and written up from their extracted
text (7 of your 8 seed papers plus 12 additional ones: 5 written in the first pass and 7 more,
previously downloaded but unread, written in a second pass), and records seed 8 (the 2026
legal-NLP paper) as **NOT FOUND**. That makes 20 entries, the maximum allowed. The focus
is BERT-style encoders under input perturbation (typos, word edits, synonym substitution,
embedding-space adversarial perturbation), with some coverage of tagging/slot filling, NLI, QA,
sentence embeddings, seq2seq/MT and decoder-only models, plus benchmarks, a toolkit, a
behavioural-testing framework and a survey. Every number carries a table or section reference;
anything the paper does not state is marked "not specified". Where a paper's section numbers
were unclear in the extraction I cite by heading or table. Statements marked "my reading", "my
inference", "my analysis" or "(derived)" are mine, not claims of the papers. Sections 14–20 were
drafted by a cheaper reader agent and checked with an automatic number check (numbers
must occur in the paper text); sections 1–13 were written and checked earlier by a different
setup. All sources are English-language, none targets Hebrew or morphologically rich scripts,
and none measures the source-vs-genre confound in your thesis. Verification status: VERIFIED
= downloaded and read in full or in all method/result parts; NOT FOUND = could not be located.
No entry is PARTIAL or NOT DOWNLOADED.

## Index table

| # | Paper | Year / venue | Model family | Task type | Perturbation type | Training method | Code
| Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Wei & Zou, EDA | 2019, EMNLP-IJCNLP | word CNN, BiLSTM (no BERT) | text
classification (5 sets) | synonym replace / insert / swap / delete (word level) | offline
augmentation of training set | github.com/jasonwei20/eda_nlp | VERIFIED |
| 2 | Goodfellow et al., FGSM | 2015, ICLR | maxout MLP, images | image classification | L∞
gradient-sign on input | adversarial training, 0.5 clean + 0.5 adversarial loss | none given |
VERIFIED |
| 3 | Madry et al., PGD | 2018, ICLR | CNN / ResNet, images | image classification | L∞
multi-step PGD, random start | min-max adversarial training |
github.com/MadryLab/{mnist,cifar10}_challenge | VERIFIED |
| 4 | Jin et al., TextFooler | 2020, AAAI | WordCNN, WordLSTM, BERT-base, InferSent, ESIM |
classification, NLI | black-box word substitution (counter-fitted synonyms, POS, USE check) |
attack; small adversarial-training experiment | github.com/jind11/TextFooler | VERIFIED |
| 5 | Li et al., BERT-ATTACK | 2020, EMNLP | BERT, LSTM, ESIM | classification, NLI |
MLM-proposed word/sub-word substitution | attack; small adversarial-training experiment |
github.com/LinyangLee/BERT-Attack | VERIFIED |
| 6 | Zhao et al., Noise-BERT | 2024, ICASSP | BERT | noisy slot filling (tagging) | NLPAug
char/word/sentence noise; FGV embedding noise | noise-alignment pre-training + contrastive +
FGV adversarial | none in paper | VERIFIED |
| 7 | Heydari et al., CDAE | 2026, arXiv preprint | frozen BERT-base + MLP autoencoder |
sentence embeddings (SNLI premises) | content-word synonym / dropout / mask | contrastive +
denoising adapter (backbone frozen) | github.com/ComputationIASBS/CDAE | VERIFIED
(description only partly matches, see §7) |
| 8 | 2026 legal-NLP robustness paper ("Robustness-Aware Decoding") | — | — | — | — | — | —
| **NOT FOUND** |
| 9 | Zhu et al., FreeLB | 2020, ICLR | BERT-base, RoBERTa-large, ALBERT | GLUE, QA |
embedding-space PGD, Frobenius ball | K-step adversarial training with accumulated gradients
| github.com/zhuchen03/FreeLB | VERIFIED |
| 10 | Jiang et al., SMART | 2020, ACL | BERT-base, RoBERTa-large | GLUE, SNLI, SciTail,
ANLI | tiny embedding perturbation (ε=1e-5) | smoothness regulariser + Bregman proximal /
EMA | github.com/namisan/mt-dnn | VERIFIED |
| 11 | Kim et al., RoAST | 2023, Findings of EMNLP | RoBERTa-large (+5 encoders, GPT2-large)
| SST-2, MNLI + robustness suite | one-step embedding perturbation; evaluated on TextFooler /
DynaSent / ANLI / AdvGLUE sets | adversarial + consistency + selective gradient masking |
github.com/bbuing9/RoAST | VERIFIED |
| 12 | Moradi & Samwald, input perturbations | 2021, EMNLP | BERT-large, RoBERTa-large,
XLNet-large, ELMo | classification, sentiment, NER, STS, QA | 7 character + 7 word
perturbations, 1–4 per sample | evaluation only | github.com/mmoradiiut/NLP-perturbation |
VERIFIED |
| 13 | Pruthi et al., misspellings | 2019, ACL | BiLSTMs, BERT | sentiment, MRPC | adversarial
char edits (swap/drop/add/key) | word-recognition front end (ScRNN with backoff); DA and adv.
training as baselines | github.com/danishpruthi/adversarial-misspellings | VERIFIED |
| 14 | Cohen et al., SDBN | 2026, Findings of ACL | BERT-base, DeBERTa-v3, LLaMA, Qwen |
classification, NLI, generative QA | embedding ℓ∞ FGSM; char edits; LLM paraphrases |
adversarial training of PEFT (no extra params) | github.com/shaham-lab/SDBN | VERIFIED |
| 15 | Provilkov et al., BPE-Dropout | 2020, ACL | Transformer NMT (no BERT) | machine
translation | stochastic merge dropout; 10% char edits at test | BPE-dropout subword
regularization; standard-BPE inference | none given in paper | VERIFIED |
| 16 | Morris et al., TextAttack | 2020, EMNLP System Demonstrations | LSTM, CNN, BERT and
transformers | classification (GLUE), augmentation | 16 attack recipes (word/char/gradient) |
adversarial training and augmentation utilities | github.com/QData/TextAttack | VERIFIED |
| 17 | Ribeiro et al., CheckList | 2020, ACL | BERT-base/large, RoBERTa, commercial APIs |
sentiment, QQP, QA (behavioural testing) | INV/DIR perturbations; MFT cases | evaluation only
(no training) | github.com/marcotcr/checklist | VERIFIED |
| 18 | Qiang et al., PPCL | 2024, Findings of EACL | LLaMA, GPT-2/3.5; JointBERT baseline |
intent classification, slot filling | oronym / synonym / paraphrase prompt edits | JS-divergence
consistency training | none given in paper | VERIFIED |
| 19 | Wang et al., AdvGLUE | 2021, NeurIPS Datasets and Benchmarks | BERT, RoBERTa,
ELECTRA, T5, ALBERT, DeBERTa | GLUE (5 tasks), robustness evaluation | 14 attacks: word,
sentence, human-crafted | n/a (benchmark); SMART/FreeLB/InfoBERT baselines |
adversarialglue.github.io | VERIFIED |
| 20 | Wang et al., Robustness survey | 2022, NAACL | n/a (survey) | n/a (survey) | taxonomy:
char/word/sentence/embedding perturbations | n/a (survey) | none given in paper | VERIFIED |

Section numbering in this file: entry numbers 1–20 in the table equal the section numbers below.
Files: all 19 read PDFs and `txt/` (layout-mode `pdftotext` output) are in this folder; `work/` holds
cleaned text (`work/clean/`), draft sections 14–20 (`work/sections/`), tools (`work/tools/`), the
number-check script, the digest, the work log and a backup of the previous version.
`download_papers.py`, `papers_manifest.tsv` and `download_report.tsv` are the helper
download files.

---

## 1. EDA — Easy Data Augmentation (seed 1)

**1. Citation and links**
- Wei, J. & Zou, K. (2019). *EDA: Easy Data Augmentation Techniques for Boosting
Performance on Text Classification Tasks.* EMNLP-IJCNLP 2019, pp. 6382–6388 (ACL
Anthology D19-1670, verified at https://aclanthology.org/D19-1670/; arXiv 1901.11196v2 says
"EMNLP-IJCNLP 2019 short paper"). Your source material's "Wang et al., ACL 2019" is wrong:
authors are Wei & Zou, venue is EMNLP-IJCNLP.
- PDF: `Wei2019_EDA.pdf` (arXiv v2). arXiv: https://arxiv.org/abs/1901.11196 . Code:
http://github.com/jasonwei20/eda_nlp (link given in §1 and §9.1 of the paper; repo contents NOT
inspected by me).
- Status: **VERIFIED** (full text read).

**2. Problem and claim**
Small labeled text-classification sets lead to overfitting; NLP lacks cheap, universal
augmentation. EDA proposes four label-preserving token-level edit operations and shows an
average +3.0 points at N_train=500 and +0.8 at full data across 5 datasets with CNN/RNN
(§4.1, Table 2). **It is an augmentation paper, not a robustness paper**: the test sets are always
clean; no perturbed-test accuracy, label agreement, calibration or degradation curve over
perturbation strength is reported.

**3. Perturbations used** (§2)
For a training sentence of length *l*, one of four operations is chosen at random ("randomly
choose and perform one of the following operations"):
1. Synonym Replacement (SR): choose *n* non-stop-word words at random, replace each with
a random WordNet synonym (WordNet cited in §9.1).
2. Random Insertion (RI): pick a random synonym of a random non-stop word, insert it at a
random position; repeat *n* times.
3. Random Swap (RS): pick two random words and swap positions; repeat *n* times.
4. Random Deletion (RD): delete each word independently with probability p.
- Strength parameter α: *n* = α·*l* for SR/RI/RS and p = α for RD (§2). Rounding of α·*l* and the
stop-word list are **not specified** in the paper.
- *n_aug* augmented sentences per original sentence (§2). Recommended settings (Table 3):
N_train=500 → α=0.05, n_aug=16; 2,000 → 0.05, 8; 5,000 → 0.1, 4; larger → 0.1, 4.
- No semantic-similarity filter, no POS constraint, no query budget. Label preservation is
checked only by t-SNE on a trained RNN's last dense layer (§4.3, Fig. 2), which is qualitative.

**4. Method**
1. For every training sentence, generate n_aug augmented copies, each by one randomly
chosen operation with strength α.
2. Train the classifier on the augmented training set. Whether the original sentence is kept
alongside the augmented copies, and whether augmentation is offline or per epoch, is **not
stated in the paper text** (the data size comparison in Fig. 1 implies offline generation; check
the repo).
3. Evaluate on the unmodified test set.
- Loss: standard categorical cross-entropy (§9.1). No consistency loss, no mixing ratio other
than n_aug.
- Not adversarial: no ε, step size, or perturbation in embedding space.

**5. Experimental setup** (§3, §9.1, Table 5)
- Models: word-level CNN (Kim 2014; §9.1: input → Conv1D 128 filters size 5 → global
max-pool → dense 20 ReLU → softmax; random-normal init; Adam; early stopping patience 3)
and bi-LSTM RNN (§9.1: BiLSTM 64 → dropout 0.5 → BiLSTM 32 → dropout 0.5 → dense 20
ReLU → softmax). GloVe 300-d embeddings (§9.1). **No BERT/pretrained transformer.**
- Datasets (Table 5): SST-2 (Ntrain 7,447 / Ntest 1,752), CR (4,082 / 452), SUBJ (9,000 / 1,000),
TREC (5,452 / 500), PC (39,418 / 4,508).
- Training subsets: N_train ∈ {500, 2,000, 5,000, full} (§3.1); fraction sweep {1,5,10,…,100}%
(§4.2).
- Seeds: results averaged over five random seeds (§4). Learning rate, batch size, epochs: **not
specified** (only Adam + early stopping, patience 3).

**6. Results** (Table 2, average accuracy % over 5 datasets, clean test sets)

| Model | N=500 | 2,000 | 5,000 | full |
|---|---|---|---|---|
| RNN | 75.3 | 83.7 | 86.1 | 87.4 |
| RNN + EDA | 79.1 | 84.4 | 87.3 | 88.3 |
| CNN | 78.6 | 85.6 | 87.7 | 88.3 |
| CNN + EDA | 80.7 | 86.4 | 88.3 | 88.8 |
| Average | 76.9 | 84.6 | 86.9 | 87.8 |
| Average + EDA | 79.9 | 85.4 | 87.8 | 88.6 |
- §4.2: EDA with 50% of the training data reaches 88.6% average, above the 88.3% best of
normal training at 100%.
- §4.4 / Fig. 3 (ablation, α ∈ {0.05,0.1,0.2,0.3,0.4,0.5}): SR gains at small α, hurts at high α; RS
gains up to α≤0.2, declines at α≥0.3; RD best at low α and "severely hurt[s]" at high α; RI is
stable across α; α=0.1 a "sweet spot". Exact per-α numbers are only in a figure (not extractable
from the text).
- Agreement, calibration, perturbed-test accuracy: **not reported**. Compute overhead: not
reported (my inference: training data grows by a factor of about n_aug, so training cost grows
similarly).

**7. Reproduction notes**
1. `git clone` eda_nlp, run its augmentation script with α and n_aug from Table 3.
2. For a BERT experiment (your use): augment the training set offline (SR/RI/RS/RD with
α=0.05–0.1, n_aug 4–8), fine-tune normally, then evaluate on *clean and perturbed* test sets
yourself, since the paper does neither.
- Ambiguities: stop-word list, rounding of n, whether originals are kept, CNN/RNN batch
size/epochs/lr, tokenization.
- Pitfalls: for BERT, the word-level edits happen before WordPiece; RS/RD destroy syntax; for
label sets where a single word can decide the label (e.g. layer-specific vocabulary in your
Enneateuch task), SR/RD can silently change the label. EDA's label-preservation check (§4.3)
is qualitative only.

**8. Limitations and caveats**
- The authors themselves say (§6; §10.2 FAQ) that gains are marginal with enough data (<1%
at full data) and that EDA is expected to give negligible improvement with pretrained models
such as BERT/ELMo; they cite Shleifer (2019) for ULMFiT but did **not** test any pretrained
model.
- No robustness evaluation, so it says nothing about how EDA changes behaviour under
perturbed test inputs.
- Evaluation is on short English sentences (average length 7–21 words, Table 5).

---

## 2. Goodfellow et al. — FGSM / adversarial training (seed 2)

**1. Citation and links**
- Goodfellow, I. J., Shlens, J., Szegedy, C. (2015). *Explaining and Harnessing Adversarial
Examples.* ICLR 2015.
- PDF: `Goodfellow2015_FGSM.pdf` (arXiv v3). arXiv: https://arxiv.org/abs/1412.6572 . Code:
none given in the paper (it only points to the pylearn2 `papers/maxout` directory for CIFAR-10
preprocessing code, §1 footnote 2; not inspected).
- Status: **VERIFIED** (full text read). Section numbers below follow the printed headings of the
PDF.
**2. Problem and claim**
Neural nets misclassify inputs perturbed by tiny worst-case perturbations. The authors argue the
cause is *linearity* in high dimensions, not nonlinearity/overfitting (abstract, §3), derive a
one-step gradient-sign attack (FGSM, §4) and use it as an additional training term (§6). **The
paper is about images (MNIST, CIFAR-10, ImageNet); there is no text experiment**, so every
NLP number must come from papers that port it (e.g. FreeLB, SMART, RoAST, Noise-BERT in
this file).

**3. Perturbations used**
- FGSM (§4): x̃ = x + ε · sign(∇ₓ J(θ, x, y)), an L∞-bounded perturbation (‖η‖∞ ≤ ε), optimal for
the linearised cost.
- ε values: 0.007 for GoogLeNet/ImageNet (§4, Fig. 1; "smallest bit of an 8 bit image encoding");
0.25 for shallow softmax and maxout on MNIST, 0.1 for convolutional maxout on preprocessed
CIFAR-10 (§4); ε=0.25 for adversarial training of maxout networks on MNIST (§5). Pixel range
[0,1] for MNIST (footnote in §4).
- Control: random noise ±ε per pixel or U(−ε, ε) per pixel (§6).
- No text-specific constraints exist here; for embeddings, you must define the norm yourself (see
FreeLB/SMART/RoAST).

**4. Method**
1. Compute loss J(θ, x, y) on a minibatch.
2. Compute ∇ₓJ by backprop (one extra backward pass w.r.t. the input).
3. Build x_adv = x + ε·sign(∇ₓJ).
4. Training objective (§6): J ̃(θ,x,y) = α·J(θ,x,y) + (1−α)·J(θ, x + ε·sign(∇ₓJ(θ,x,y))), with **α = 0.5
in all experiments** ("other values may work better … we did not feel the need to explore
more"). The adversarial examples are regenerated every step against the current parameters
(§6: "continually update our supply of adversarial examples").
5. Linear case (§5): for logistic regression the adversarial objective is E ζ(y(ε‖w‖₁ − wᵀx − b)) (ζ
= softplus), similar to but not the same as L1 weight decay.
- Applied at the **input** level (pixels). Gradient of sign() is not propagated: the perturbation is
treated as a constant (§6: "the derivative of the sign function is zero or undefined everywhere",
so the model cannot anticipate the adversary's reaction; the authors also report that
differentiable alternatives, small rotations or scaled-gradient perturbations, gave a weaker
regularizing effect, §6). Also in §6: perturbing hidden layers vs. inputs gave "inconsistent" results
across studies.

**5. Experimental setup** (§6 unless noted)
- Model: maxout network, permutation-invariant MNIST, dropout, 60,000 training examples.
Original maxout net 240 units/layer; adversarial training used a larger net with **1,600 units per
layer** (§6). Optimizer, learning rate, batch size: **not specified** in this paper (inherited from
the maxout paper; not restated).
- Early stopping on the *adversarial* validation error (not clean validation error), then retrained
on all 60,000 examples with the epoch count so chosen (§6).
- Seeds: five runs with different seeds (minibatch order, init, dropout masks) (§6).
- Other experiments: shallow softmax and RBF nets, 12-model maxout ensemble, MP-DBM (§7,
§9, §10).

**6. Results** (MNIST, maxout)

| Quantity | Value | Where |
|---|---|---|
| Clean test error, dropout only | 0.94% | §6 |
| Clean test error, + FGSM training (240 units) | 0.84% | §6 |
| Clean test error, wider net, no adv. training | 1.14% | §6 |
| Clean test error, wider net + adv. training | mean 0.782% (four runs 0.77%, one 0.83%) | §6 |
| Error on FGSM examples, naive maxout, ε=.25 | 89.4% (avg. confidence on mistakes 97.6%) |
§4 |
| Error on FGSM examples after adv. training | 17.9% | §6 |
| Avg. confidence on the remaining mistakes (adv. trained) | 81.4% | §6 |
| Transfer: adv. examples from original model → adv.-trained model | 19.6% error; reverse
direction 40.9% | §6 |
| Random-noise training controls | 86.2% / 90.4% error on FGSM examples (confidence 97.3% /
97.8%) | §6 |
| 12-model ensemble, ε=.25 | 91.1% error on examples against whole ensemble; 87.9% for
single-member examples | §9 |
| Shallow RBF net, ε=.25 | 55.4% error, avg. confidence on mistakes only 1.2% (clean
confidence 60.6%) | §7 |

- Calibration: the paper is one of the early sources showing *high-confidence errors* (§1, §4),
and shows RBF nets are the exception (low confidence when fooled, §7). No ECE is computed.
- Graceful degradation over ε is shown only as a logit-versus-ε plot for one example (§9, Fig. 4,
not a dataset-level curve).
- Compute overhead: one extra forward/backward pass per step (inference from the objective in
§6; the paper does not report wall-clock time).

**7. Reproduction notes**
- For BERT: take the embedding output (word embeddings), compute ∇ of the loss w.r.t. it, step
ε·sign(grad) (or normalised gradient), forward again, and add α·clean + (1−α)·adv loss with
α=0.5. The paper gives **no ε for text**: choose it on a dev set; later work uses ‖δ‖₂ balls (see
FreeLB, SMART).
- Missing/ambiguous: optimizer details, batch size, exact stopping epoch, how validation
adversarial error was computed.
- Pitfalls: (i) the adversarial perturbation must use the *current* model; (ii) report clean accuracy
as well, since α<1 mixes them; (iii) in discrete NLP inputs the embedding perturbation is not a
valid input, so clean-vs-token-perturbed robustness has to be tested separately; (iv) early
stopping on adversarial validation error (as used here) changes the checkpoint you evaluate.

**8. Limitations and caveats**
- Images only; ε-ball in pixel space; no transfer evidence for text from this paper.
- ε is tuned to the "precision of features" argument (§3), which has no direct analogue for token
embeddings.
- Single-step linearisation. Madry et al. (§4 of paper 3 in this file) report that training with FGSM
examples at large ε makes the network overfit to FGSM examples ("label leaking"), i.e.
FGSM-trained models do not gain robustness against PGD; this is not tested in Goodfellow et
al.
- Single dataset adversarial-training result (MNIST); no confidence intervals beyond five seeds.

---

## 3. Madry et al. — PGD adversarial training (seed 3)

**1. Citation and links**
- Madry, A., Makelov, A., Schmidt, L., Tsipras, D., Vladu, A. (2018). *Towards Deep Learning
Models Resistant to Adversarial Attacks.* ICLR 2018 (arXiv v4, Sep 2019).
- PDF: `Madry2018_PGD.pdf`. arXiv: https://arxiv.org/abs/1706.06083 . Code and pre-trained
models (§1 footnote 1): https://github.com/MadryLab/mnist_challenge and
https://github.com/MadryLab/cifar10_challenge (repo contents not inspected by me).
- Status: **VERIFIED** (main text, Tables 1–2 and appendix pointers read; appendix proofs not
read in detail).

**2. Problem and claim**
Frames robustness as a saddle-point (min–max) problem (§2, Eq. 2.1) and argues that PGD is
a "universal" first-order adversary: random-restart PGD reaches loss values that cluster tightly
(§3, Figs. 1–2), so training against PGD yields robustness against all first-order attacks tested
(abstract, §5). Capacity is also shown to matter (§4). Images only (MNIST, CIFAR10).

**3. Perturbations used**
- Allowed set S = L∞ ball of radius ε around x (§2). MNIST ε = 0.3; CIFAR10 ε = 8 (pixel scale
0–255) (§5).
- PGD step: x^{t+1} = Π_{x+S}( x^t + α·sgn(∇ₓ L(θ, x^t, y)) ) (§2), started from a uniformly
random point in the ball (§3, Fig. 1 caption; §5).
- MNIST attack: 40 iterations, step size 0.01 (§5). CIFAR10 attack: 7 steps of size 2 for training;
evaluation adversary 20 steps, same step size (§5).
- Evaluation variants: PGD with 1–20 random restarts and 40/100 steps; Carlini–Wagner-loss
PGD (CW, CW+ with κ=50); black-box transfer attacks from independently trained copy A', from
naturally trained net A_nat, from a different architecture B (§5, Tables 1–2). Additional ε sweep
and L2 PGD (100 steps, step size 2.5·ε/100) (§5, Fig. 6).
- Text constraints: none (images).

**4. Method** (§2, §3.3, §5)
1. Inner maximisation: approximately solve max_{δ∈S} L(θ, x+δ, y) with PGD (random start,
multiple steps, projection onto the ε-ball).
2. Outer minimisation: take the gradient of the loss at the adversarial point x+δ* w.r.t. θ and do
an SGD-type step on θ. Justified via Danskin's theorem (§3.3), which strictly does not hold for
ReLU nets but "consistently reduces the loss of the saddle point problem" empirically (Fig. 5).
3. Training uses **only adversarial examples** (no clean/adversarial mix) in the min–max loss
ρ(θ) = E max_δ L(θ, x+δ, y) (Eq. 2.1). I found no α-mixing term like Goodfellow's; a mixing ratio
is therefore **not applicable / not specified**.
4. No multiple restarts per batch: "a new start will be chosen the next time each example is
encountered" (§5).
- FGSM comparison (§4): FGSM = one-step linearisation; for large ε "the network overfits to
these adversarial examples… label leaking" and does not gain PGD robustness; for small ε
FGSM ≈ PGD.
- Cost: one forward/backward per PGD step, so training cost ≈ (steps + 1)× standard training
(my arithmetic from the algorithm; the paper does not report wall-clock).

**5. Experimental setup** (§4, §5)
- MNIST: CNN with 2 conv layers (32, 64 filters, each followed by 2×2 max-pool) + FC 1024;
natural accuracy 99.2% when trained naturally (§5). Capacity study: start at conv 2 filters/4
filters/FC 64 and double (§4).
- CIFAR10: ResNet with 5 residual units, widened ×10 → (16, 160, 320, 640) filters, 95.2%
accuracy natural training; data augmentation random crops + flips + per-image standardisation
(§4).
- Optimizer, learning rate schedule, batch size, number of epochs, seeds: **not specified** in the
main text (Fig. 5 shows ≈100k training iterations on the x-axis; the lr drops visible in the
CIFAR10 curve are not quantified in text).

**6. Results** (white-box, ε=0.3 MNIST / ε=8 CIFAR10)

| Model | Natural | FGSM | PGD (steps) | Source |
|---|---|---|---|---|
| MNIST, PGD-trained (Table 1) | 98.8% | 95.6% | 93.2% (40 steps, 1 restart); 91.8% (100
steps); 90.4% (40 steps, 20 restarts); 89.3% (100 steps, 20 restarts) | white-box A |
| MNIST, PGD-trained, transfer from copy A' (Table 1) | | 96.8% | 96.0% (40 steps); 95.7% (100
steps, 20 restarts) | A' |
| MNIST, naturally trained net under FGSM (§5) | 99.2% | 6.4% | | |
| CIFAR10, PGD-trained (Table 2) | 87.3% | 56.1% | 50.0% (7 steps); 45.8% (20 steps) |
white-box A |
| CIFAR10, transfer from A' | | 67.0% | 64.2% (7 steps) | A' |

- Clean-accuracy cost: CIFAR10 95.2% natural vs 87.3% PGD-trained (§4, Table 2); MNIST
99.2% vs 98.8% (§5, Table 1). (The two are different CIFAR10 models: the 95.2% number is for
the wide ResNet trained naturally; check Fig. 4 for exact pairing.)
- Degradation vs ε (§5, Fig. 6): at smaller ε than training, accuracy equal or higher; for MNIST
there is a "large drop in robustness for slightly larger ε values" (a cliff, attributed to thresholding
filters tuned to the training ε, Appendix C) while "the decay for … CIFAR10 is smoother."
- L2 MNIST caveat (§5): PGD fails to find adversarial examples even at ε = 4.5, which the
authors say is unlikely to be real robustness (gradient masking; decision-based attack finds the
model "significantly more brittle").
- Calibration, label agreement: not reported.

**7. Reproduction notes**
- Minimal NLP adaptation (not in the paper): treat the (sub)word embedding matrix output as x;
run K PGD steps with step α and projection to an ε-ball (L2 or L∞), update θ with the loss at
x+δ_K. See FreeLB and SMART for text versions.
- Missing: optimizer/lr/batch size/epochs; exact pixel normalisation conventions; whether
BatchNorm is in train or eval mode during attack generation.
- Pitfalls: (i) use random start; (ii) evaluate with a *stronger* attack than the one used in training
(more steps/restarts, CW loss) and report clean accuracy; (iii) a sharp drop just above training ε
(MNIST) means evaluate a range of ε; (iv) gradient masking can make PGD overestimate
robustness (the L2 result).

**8. Limitations and caveats**
- Images; L∞ ε-ball with continuous inputs. Text has discrete inputs, so the guarantee is for
embedding-space perturbations only.
- Low-capacity networks fail to train under PGD (§4: "Weak models may fail to learn non-trivial
classifiers"); capacity requirements are larger than for clean training.
- Robustness is only against the tested first-order attacks; no certified claim.
- Costly: each step multiplies training compute.

---

## 4. Jin et al. — TextFooler, "Is BERT Really Robust?" (seed 4)

**1. Citation and links**
- Jin, D., Jin, Z., Zhou, J. T., Szolovits, P. (2020). *Is BERT Really Robust? A Strong Baseline for
Natural Language Attack on Text Classification and Entailment.* AAAI 2020 (arXiv v6).
- PDF: `Jin2020_TextFooler.pdf`. arXiv: https://arxiv.org/abs/1907.11932 . Code, pre-trained
target models and test samples: https://github.com/jind11/TextFooler (footnote 1; repo not
inspected). Data: http://bit.ly/nlp adv data (footnote 5).
- The AAAI paper has **unnumbered sections**; I cite by heading ("Method", "Experiments", …)
and by table number.
- Status: **VERIFIED** (full text read).

**2. Problem and claim**
Black-box word-substitution attack that keeps meaning, POS and fluency; reduces BERT-base
accuracy to ≈4–20% on five classification and two NLI datasets by changing ≈6–22% of words
(Tables 3–4). A preliminary adversarial-training experiment suggests the generated examples
make models harder to attack (Table 12).
**3. Perturbations used** (Method, "Step 1/Step 2")
- Operation: word replacement only (no insertion/deletion).
- Word importance (Eq. 2): I_w = F_Y(X) − F_Y(X\w) if the predicted label does not change on
deletion; if the label flips to Ȳ: (F_Y(X) − F_Y(X\w)) + (F_Ȳ(X\w) − F_Ȳ(X)). Words ranked by
I_w; **stop words removed** (NLTK + spaCy lists).
- Synonym candidates: top **N = 50** nearest neighbours by cosine similarity in the
counter-fitted embeddings of Mrkšić et al. (2016), with cosine similarity > **δ = 0.7** (Method,
"Synonym Extraction": "empirically setting N to be 50 and δ to be 0.7").
- POS constraint: replacement must have the same POS tag as the original (spaCy tagger).
- Sentence-level constraint: Universal Sentence Encoder (USE) cosine similarity between the
candidate sentence and the current adversarial sentence must exceed a preset threshold ε.
**The numeric value of ε is not stated in the paper** (Algorithm 1 only names it "sentence
similarity threshold ε"); neither is the size of the USE context window. (The value must be read
from the repo; I did not.)
- Perturbation budget: **no explicit cap**; the attack continues until the label flips or words run
out. The reported %-perturbed words is an outcome (Tables 3–4). Query count is also an
outcome (≈2–8× text length, "Results").
- Black-box: needs prediction scores (probabilities) from the target model.

**4. Method** (Algorithm 1)
1. For every word w_i compute importance I_{w_i} by deleting it and re-querying the model (n
queries).
2. Sort words by descending importance, drop stop words.
3. For each word in order: build candidates (top-N synonyms, δ filter, POS filter); substitute each
into the current X_adv; keep candidates with USE-similarity > ε.
4. If any kept candidate flips the prediction, choose the one with the highest sentence similarity
to the original X and return.
5. Otherwise substitute the candidate that minimises the target-label probability and move to the
next word.
6. Return None if all words are processed without flipping the label (Algorithm 1, line 30).
- Adversarial training experiment (Discussion, "Adversarial Training"): adversarial examples
generated on MR and SNLI **training** sets that fooled BERT are added with the original labels
to the training set; BERT is trained "from scratch" (i.e. fine-tuned again) and attacked again.
Mixing ratio, number of added examples, and hyperparameters: **not specified**.

**5. Experimental setup** (Experiments)
- Datasets and sizes (Table 1): AG's News (120K/7.6K train/test, avg. len 43), Fake News
(18.8K/2K, 885), MR (9K/1K, 20), IMDB (25K/25K, 215), Yelp (560K/38K, 152), SNLI (570K/3K,
8), MultiNLI (433K/10K, 11). Attack evaluated on **1,000 random test examples** per dataset
(following Alzantot et al.).
- Target models: WordCNN (windows 3, 4, 5, 100 filters each, dropout 0.3), WordLSTM (1-layer
BiLSTM, 150 hidden units, dropout 0.3), both with 200-d GloVe; BERT-base-uncased (12 layers,
768 hidden, 12 heads, 110M parameters); for NLI: InferSent, ESIM, BERT.
- Fine-tuning hyperparameters of the targets (learning rate, batch size, epochs, seeds): **not
specified**. Standard test accuracies in Table 2 (BERT: AG 94.6, Fake 99.9, MR 85.8, IMDB
92.2, Yelp 96.1, SNLI 90.7, MNLI m/mm 83.9/84.1).
- Human evaluation: 100 examples (MR/WordLSTM and SNLI/BERT), two native-speaker
judges (Experiments, "Setup of Human Evaluation").

**6. Results**

| BERT target (Tables 3–4; 1,000-example subsets) | Original acc. | After-attack acc. | % words
perturbed | USE sim. | Queries |
|---|---|---|---|---|---|
| MR | 86.0 | 11.5 | 16.7 | 0.65 | 166 |
| IMDB | 90.9 | 13.6 | 6.1 | 0.86 | 1134 |
| Yelp | 97.0 | 6.6 | 13.9 | 0.74 | 827 |
| AG | 94.2 | 12.5 | 22.0 | 0.57 | 357 |
| Fake | 97.8 | 19.3 | 11.7 | 0.76 | 4403 |
| SNLI | 89.4 | 4.0 | 18.5 | 0.45 | 60 |
| MultiNLI m/mm | 85.1/82.1 | 9.6/8.3 | 15.2/14.6 | 0.57/0.58 | 78/86 |

- WordCNN/WordLSTM drop to ≈0–4% on MR/IMDB/Yelp/AG and to ≈16% on Fake (Table 3),
e.g. WordLSTM IMDB 89.8 → 0.3 with 5.1% words changed.
- **Internal inconsistency to check**: the Results prose says "from 95.6% to 6.8% for Yelp", but
Table 3 gives 97.0 → 6.6 for BERT/Yelp (the SNLI example 89.4 → 4.0 in the prose does match
Table 4).
- Ablations (Discussion): random word choice instead of importance ranking raises after-attack
accuracy by >45 points (BERT: MR 11.5 → 68.3, AG 12.5 → 80.8, SNLI 4.0 → 59.2; Table 8).
Removing the similarity constraint makes attacks easier but lowers similarity (Table 10).
- Human evaluation: label agreement of human labels on original vs adversarial 92% (MR) and
85% (SNLI); human semantic similarity 0.91 / 0.86; grammaticality original → adversarial 4.22
→ 4.01 (MR), 4.50 → 4.27 (SNLI) on a 1–5 scale (Tables 6–7, "Human Evaluation").
- Adversarial training (Table 12; BERT): MR after-attack accuracy 11.5 → 18.7, % perturbed
16.7 → 21.0; SNLI 4.0 → 8.3, 18.5 → 20.1. **Clean accuracy after adversarial training is not
reported.**
- Transferability (Table 11): moderate; examples from BERT transfer best.
- Calibration/ECE: not reported. Degradation curve over a perturbation budget: not reported (the
attack is unbounded; only final %perturbed given).

**7. Reproduction notes**
1. Use the repo's attack with the counter-fitted vectors, USE, spaCy and NLTK stop words.
2. Reproduce a fine-tuned BERT target and the 1,000-example evaluation subsets.
3. For *robustness scoring on your model*: report after-attack accuracy plus % perturbed words
and query counts. For a *degradation curve*, add an explicit word-budget cap (not in the paper).
- Missing: USE threshold ε, USE window, training hyperparameters of targets,
adversarial-training mix.
- Pitfalls: attack success depends on library versions (spaCy tagger, USE v), on stop-word list,
and on candidate filtering; an unbounded attack almost always drives accuracy near 0, so
after-attack accuracy alone is not comparable across attack budgets; semantic similarity (USE)
is unreliable below ≈10 words (paper's remark in "Results").

**8. Limitations and caveats**
- English only; word-level substitution only; requires access to output probabilities; the attacked
model sees *adversarial* (worst-case) not natural noise, so the numbers are not comparable
with random-typo degradation.
- Only 1,000 test examples per dataset; no confidence intervals; only one adversarial training
experiment, with no clean-accuracy cost reported.
- The authors list failure types in "Error Analysis": word-sense errors ("show" → "testify"),
grammar errors, and task-sensitive content shift (a changed word can change the correct NLI
label), so some "successful" attacks may have changed the true label.

---

## 5. Li et al. — BERT-ATTACK (seed 5)

**1. Citation and links**
- Li, L., Ma, R., Guo, Q., Xue, X., Qiu, X. (2020). *BERT-ATTACK: Adversarial Attack Against
BERT Using BERT.* EMNLP 2020 (arXiv v3).
- PDF: `Li2020_BERTAttack.pdf`. arXiv: https://arxiv.org/abs/2004.09984 . Code:
https://github.com/LinyangLee/BERT-Attack (abstract; repo not inspected). Also re-implemented
in TextAttack (footnote 4 points to https://github.com/QData/TextAttack for GA baseline).
- Status: **VERIFIED** (full text read; Table 1 read in layout mode because the raw extraction
scrambles it).

**2. Problem and claim**
Uses a (pre-trained) BERT masked language model as the substitution generator to attack a
fine-tuned BERT or other models in the black-box setting; claims a higher success rate, lower
perturbation % and 3× lower runtime than TextFooler (§1, §4.3, Table 1, §5.6, Table 9).

**3. Perturbations used** (§3)
- Operation: word (and sub-word-group) substitution proposed by BERT's own MLM head.
Importance score (Eq. 1): I_{w_i} = o_y(S) − o_y(S\w_i), where S\w_i replaces w_i with [MASK]
and o_y is the target model's logit for the correct label.
- Only the top **ε percent** most important words are considered (§3.1: "We only take ε percent
of the most important words"). **ε is not given numerically in the text I extracted.**
- Candidates: top-**K** MLM predictions at each position, K "a hyperparameter" (§3.2.1); effect
of K studied in Fig. 2 with K ∈ {6, 12, 24, 36} (axis values on the plot); value used for the main
results **not specified** in the text. A flexible threshold on candidate probability was also tested
(Table 4); threshold value not specified.
- The chosen word is **not masked** when fed to BERT (§3.2.1: whole original sequence is the
input, "Instead of following the masked language model settings, we do not mask the chosen
word"), so the MLM sees the word and predicts similar words in context.
- Filters: NLTK stop words removed; for sentiment tasks antonyms are filtered using a synonym
dictionary (Mrkšić et al. 2016) (§3.2.1). No POS constraint (stated as an advantage in §3.2).
- Sub-words: if a word is split into BERT sub-words, all K^t sub-word combinations are
generated, converted back to words, and ranked by MLM perplexity; top-K kept (§3.2.1).
- Semantic filter: Universal Sentence Encoder similarity with "a threshold of semantic similarity
score" (§4.2); **threshold value not specified**.
- Query budget: none stated; queries to the target model are reported (Table 1).

**4. Method** (Algorithm 1)
1. Word importance ranking: compute I_w for all words with [MASK] replacement; sort; keep
top-ε% list L.
2. Run BERT once on the sub-word tokenisation H of the *unmasked* sentence to get top-K
predictions P at every position.
3. For each word in L: if single-token, filter candidates (stop words, antonyms), else build
sub-word combinations ranked by perplexity.
4. Try candidates in order; if the target's argmax label changes, return the adversarial sample.
Otherwise keep the candidate that lowers o_y most and continue to the next word in L
(Algorithm 1 lines 18–24).
5. Return None if no sample succeeds.
- Adversarial training experiment (§5.4, Table 5): adversarial samples generated from the
**training set** are added to fine-tuning of the target (BERT, MNLI matched); mixing ratio and
number of added examples **not specified**.
- Cost: the MLM is run once per sentence, so the only repeated cost is querying the target (§3.2,
§5.6).

**5. Experimental setup** (§4)
- Datasets (§4.1): Yelp, IMDB, AG's News, Fake (Kaggle) for classification; SNLI and MNLI
(matched/mismatched) for NLI. **1k random test samples** each, same splits as Alzantot et al. /
TextFooler; GA baseline uses only 50 samples on Fake and IMDB (§4.1).
- Target models: fine-tuned BERT (base, original accuracies 97.8 Fake, 95.6 Yelp, 90.9 IMDB,
94.2 AG, 89.4 SNLI, 85.1 MNLI-m, 82.1 MNLI-mm in Table 1); also Word-LSTM, ESIM,
BERT-large (Table 3). The attacker MLM is BERT-base ("we use BERT-base as the masked
language model for all target models", §5.4). Fine-tuning hyperparameters of targets: **not
specified**.
- NLI attack direction: the MNLI premise or hypothesis is attacked separately (H/P in Table 1).
SNLI/MNLI main numbers target the hypothesis; premises were also attacked "since contextual
replacement would be less reasonable" on very short sequences (§5.2).
- Human evaluation (§4.4): 100 original + 100 adversarial samples each for IMDB and MNLI,
three annotators.

**6. Results** (Table 1; BERT-Attack vs TextFooler, BERT-base target)
| Dataset | Orig. acc | Attacked acc (BA / TF) | Perturb % (BA / TF) | Queries (BA / TF) | USE
sim (BA / TF) |
|---|---|---|---|---|---|
| Fake | 97.8 | 15.5 / 19.3 | 1.1 / 11.7 | 1558 / 4403 | 0.81 / 0.76 |
| Yelp | 95.6 | 5.1 / 6.6 | 4.1 / 12.8 | 273 / 743 | 0.77 / 0.74 |
| IMDB | 90.9 | 11.4 / 13.6 | 4.4 / 6.1 | 454 / 1134 | 0.86 / 0.86 |
| AG | 94.2 | 10.6 / 12.5 | 15.4 / 22.0 | 213 / 357 | 0.63 / 0.57 |
| SNLI (H/P) | 89.4 | 7.4/16.1 / 4.0/20.8 | 12.4/9.3 / 18.5/33.4 | 16/30 / 60/142 | 0.40/0.55 /
0.45/0.54 |
| MNLI-m (H/P) | 85.1 | 7.9/11.9 / 9.6/25.3 | 8.8/7.9 / 15.2/26.5 | 19/44 / 78/152 | 0.55/0.68 /
0.57/0.65 |

(BA = BERT-Attack, TF = TextFooler; the raw PDF extraction scrambles Table 1, so I read it in
layout mode. Where BA is *worse* than TF (SNLI-hypothesis attacked accuracy 7.4 vs 4.0) the
"highest attack success" claim is not uniform.)
- Other targets (Table 3): Word-LSTM IMDB 89.8 → 10.2 (perturb 2.7%); BERT-large IMDB 98.2
→ 12.4; Word-LSTM Yelp 96.0 → 1.1; BERT-large Yelp 97.9 → 8.2; ESIM MNLI-m 76.2 → 9.6
(21.7%); BERT-large MNLI-m 86.4 → 13.2.
- Human evaluation (Table 2): human label accuracy original → adversarial: MNLI 0.90 →
**0.70**, IMDB 0.91 → 0.85; semantic score (1–5) 3.9 → 3.7 (MNLI), 4.1 → 3.9 (IMDB);
grammar 4.0 → 3.6 (MNLI), 3.9 → 3.7 (IMDB). The authors attribute the MNLI drop to short
word-overlapping pairs (§4.4); i.e. up to 20 points of "successful" NLI attacks may be
label-changing.
- Adversarial training (§5.4, Table 5; MNLI matched, BERT): original acc 85.1 → 84.6; attacked
acc 7.9 → 23.1; perturb % 8.8 → 10.5. So clean accuracy cost 0.5 points for a 15.2-point gain in
after-attack accuracy against the same attack.
- Runtime (Table 9, IMDB, seconds/sample): BERT-Attack 16.0 (14.2 without BPE sub-word
handling), TextFooler 42.4, GA 2582.0.
- Ablations: sub-word attack improves success (Table 7); random or least-important ranking
weakens the attack (Table 8: MNLI-m attacked acc 7.9 [importance] vs 20.2 [random] vs 27.2
[least important]).
- Calibration, degradation curves over budgets: not reported.

**7. Reproduction notes**
1. Fine-tune BERT-base on the target task (any recipe). 2. Run the repo (or TextAttack's
`bert-attack` recipe) with the target's logits. 3. Report attacked accuracy, perturbation %,
queries, USE similarity on a fixed 1k subset.
- Missing: ε, K for main table, USE threshold, target hyperparameters, adversarial-training data
size.
- Pitfalls: (i) if you attack the same BERT variant as the generator, results may differ from a
different generator checkpoint; (ii) MLM-proposed words may be antonyms (the authors admit
this in §6), so label-preservation checks (human or NLI-based) are needed for classification
robustness claims; (iii) attacks on very short inputs (<10 tokens) produce semantically poor
samples (§5.2).

**8. Limitations and caveats**
- English; word-level substitutions only; black-box, unconstrained budget (no explicit cap on %
of words), so "attacked accuracy" is not a degradation curve.
- The same attack that is used for adversarial training is used to evaluate it (Table 5), so the
23.1% after-attack figure measures robustness to a known attack, not to other perturbation
types.
- The 1k-sample test sets and single seeds give no confidence intervals.

---

## 6. Noise-BERT (seed 6)

**1. Citation and links**
- Zhao, J., Dong, G., Qiu, Y., Hui, T., Song, X., Guo, D., Xu, W. (2024). *Noise-BERT: A Unified
Perturbation-Robust Framework with Noise Alignment Pre-training for Noisy Slot Filling Task.*
ICASSP 2024 (per arXiv comment "Accepted by ICASSP 2024"; arXiv v3, Mar 2024).
- PDF: `Zhao2024_NoiseBERT.pdf`. arXiv: https://arxiv.org/abs/2402.14494 . **Code: no link in
the paper text** (I grepped for "github"; only nlpaug and a PSSAT-code footnote appear). Not
verified whether a repo exists elsewhere.
- Status: **VERIFIED** (full 4-page paper read). **Short paper: many details are missing** (see
"not specified" below).

**2. Problem and claim**
Targets **noisy slot filling** (a span/entity tagging task in task-oriented dialogue): a BERT-based
slot-filling model degrades under typos, ASR errors, simplification, verbosity and paraphrase.
The claim (abstract, §3.2) is that adding (i) noise-aware pre-training tasks, (ii) a contrastive loss
between original and augmented utterances and (iii) FGV adversarial noise yields better F1 than
PSSAT, W2NER, NAT and Biaffine baselines under every perturbation type, with adversarial
training the most important component (§3.2 ablation).

**3. Perturbations used**
- §2.1 "Multi-level Data Augmentation" with the NLPAug tool: character-level (randomly
add/delete/replace characters in a token), word-level (randomly delete/insert words; replace
words with homophones), sentence-level (replace sentences with synonymous ones).
**Per-token / per-sentence rates, number of augmented copies per utterance, and NLPAug
augmenter names/parameters: not specified.**
- Test perturbations (§3.1): (a) RADDLE diagnostic sets: Typos, Speech (ASR errors),
Simplification, Verbose, Paraphrase; (b) SNIPS perturbed with TextFlint: Typos (character),
Speech (word), AppendIrr (sentence, appends irrelevant text) and combinations ("mixed
perturbation"). TextFlint settings: not specified.
- Adversarial perturbation (§2.3, Eq. 5): v_noise = ε · g/‖g‖ (norm type not stated) with g = ∇ₑ
L_slot ("FGV", Fast Gradient Value, refs [47,48]). **ε is described only as "a small ε"; numeric
value not specified; the layer where e lives (word-embedding output vs. hidden states) is also
not specified** (the text says noise is added "to the input").

**4. Method** (§2.2–2.3, Fig. 2)
Pre-training (on the same data as fine-tuning, §2.2: "the data utilized is identical to the data
employed in the fine-tuning phase"):
1. Slot Masked Prediction (SMP), Eq. 1: randomly replace *k* entities with [MASK] (all tokens of
a multi-token entity) and predict them: L_smp = −Σ_{m=1..M} log P(x_m). *k* not specified.
2. Sentence Noisiness Discrimination (SND), Eq. 2: linear layer on [CLS], binary cross-entropy
for "clean vs noisy" (the label is whether the sentence came from the clean or the
augmented/noisy set): L_snd = −y log ŷ − (1−y) log(1−ŷ).
3. L_pre = α·L_smp + (1−α)·L_snd with **α = 0.6** (Eq. 3).
Fine-tuning (§2.3):
4. Slot head: BERT hidden states → word/relation representations → candidate entity words
classified (a W2NER-style span/relation head is implied; "Biaffine/W2NER" are baselines);
cross-entropy L_slot.
5. Contrastive loss L_cl (Eq. 4): the anchor q is the BERT representation of the original input; its
augmented version is the positive k⁺; other augmented examples in the same batch are
negatives; InfoNCE with temperature τ (value **not specified**).
6. Adversarial attack training: compute g = ∇ₑ L_slot, v_noise = ε·g/‖g‖, second forward pass
on the noised input → L′_slot; L_adv = L_slot + L′_slot (so clean and adversarial loss are
weighted 1:1).
7. Final loss L = β·L_cl + (1−β)·L_adv with **β = 0.3** (Eq. 6).
- Clean/perturbed data mixing ratio, offline vs. online augmentation: **not specified**.
- Compute overhead: one extra forward/backward for FGV plus pre-training stage plus in-batch
contrastive negatives; not quantified in the paper.

**5. Experimental setup** (§3.1)
- Backbone: "BERT" [46]; size (base/large), learning rate, optimizer, batch size, epochs, max
length, seeds: **not specified**. The "±" values in Tables 1–2 are not defined (presumably std
over runs; number of runs not specified).
- Data: RADDLE (single perturbations; the PSSAT evaluation sets) and SNIPS + TextFlint
(mixed perturbations). Train/test sizes: not specified in this paper.
- Baselines: Biaffine, W2NER, NAT (L_aug and L_stabil variants), PSSAT (re-run by the authors
via code obtained from PSSAT's authors, footnote 1).
- Metric: F1 (slot level); "Overall" = average of the five RADDLE perturbation F1s (caption of
Table 1).

**6. Results** (Table 1, RADDLE F1; Table 2 SNIPS mixed)

| Model | Clean | Typos | Speech | Paraphrase | Simplif. | Verbose | Overall (avg of 5) |
|---|---|---|---|---|---|---|---|
| PSSAT | 95.83 | 67.65 | 83.67 | 89.31 | 86.79 | 82.94 | 82.07 |
| Noise-BERT | 96.16 ±0.4 | 71.15 ±1.2 | 84.72 ±1.1 | 90.27 ±0.5 | 88.74 ±0.7 | 84.89 ±0.6 |
83.95 ±0.8 |
| − pre-training | 91.37 | 64.24 | 79.45 | 83.96 | 84.21 | 79.37 | 78.25 |
| − SMP | 92.46 | 64.75 | 80.46 | 85.73 | 84.95 | 80.21 | 79.22 |
| − SND | 92.67 | 65.42 | 79.54 | 84.27 | 84.55 | 79.68 | 78.69 |
| − contrastive | 93.16 | 65.11 | 81.26 | 85.95 | 85.43 | 80.57 | 79.66 |
| − adversarial | 91.52 | 62.96 | 80.37 | 84.19 | 83.74 | 79.26 | 78.10 |

- Clean → perturbed gap for the full model: Overall 96.16 → 83.95 (−12.2 F1); Typos −25.0,
Speech −11.4, Paraphrase −5.9, Simplification −7.4, Verbose −11.3 (my subtraction of Table 1
values). **A character-level gap of 25 points remains even for the proposed robust model.**
- Mixed perturbations (Table 2, SNIPS F1): Typos+Speech 48.86 (PSSAT 44.55, W2NER
41.72); Typos+AppendIrr 59.09 (54.34, 50.17); Speech+AppendIrr 54.42 (51.86, 48.83); all
three 41.41 (36.67, 34.51). No clean SNIPS number is reported in this table.
- Paper's own text: +5.2 over PSSAT on Typos, +2.3 on Verbose (§3.2). Removing adversarial
training hurts most (§3.2 ablation).
- Degradation vs. perturbation strength: not reported (each perturbation type is a single fixed
level). Prediction agreement and calibration: not reported.
- t-SNE of entity representations (Fig. 3) is qualitative only.

**7. Reproduction notes**
- Minimal route (my reading of the paper): (1) build a noisy copy of the training set with NLPAug
(character/word/sentence), mark clean/noisy; (2) continue BERT pre-training with SMP + SND
(α=0.6) on the same data; (3) fine-tune with L = 0.3·L_cl + 0.7·(L_slot + L′_slot), FGV noise on
embeddings.
- Missing: everything numeric except α, β (ε, τ, k, augmentation rates, lr, batch size, epochs,
backbone size, number of seeds, code). Reproduction requires either contacting the authors or
re-tuning; treat any replication as a re-implementation.
- Pitfalls: the pre-training tasks use *task data*, so pre-training and fine-tuning can leak
augmentation artefacts (noisy/clean label is perfectly predictable from the augmenter); PSSAT
baseline numbers were re-run by the authors with code from PSSAT's authors (footnote 1), so
they may not match PSSAT's own publication.

**How it would transfer to other tasks (my analysis, not claims of the paper)**
- Sentence classification (e.g. source-layer classification): SND and the contrastive loss are
task-agnostic; FGV needs only a differentiable loss and embedding access. SMP depends on
*entities*; for classification it would have to be replaced by masking class-salient tokens (e.g.,
high-attribution words) or ordinary MLM on the task corpus (this is a design choice you would
need to validate, not something the paper tests).
- Tagging/NER: direct transfer (same family as slot filling).
- NLI/QA/retrieval: contrastive original-vs-augmented loss transfers (it is SimCSE-like, cf. CDAE
paper in this folder); SMP would mask answer spans/hypothesis keywords.
- Decoder LLMs/seq2seq: SMP/SND are encoder-style objectives; FGV and augmentation
transfer, SND would need a classification head.

**8. Limitations and caveats**
- Short ICASSP paper, single task (slot filling), English dialogue data; no released code (in the
paper); no public hyperparameters.
- The test-time perturbations (RADDLE typo/speech sets and TextFlint) resemble the
augmentation families used in training (§2.1 vs §3.1), so gains partly reflect train/test noise
overlap; the paper's claim of generalisation to "unknown noise" is only tested by the
mixed-perturbation SNIPS set built with another tool.
- The ablation shows clean F1 also drops when components are removed (e.g. −adv: 96.16 →
91.52), which is unusual for adversarial training and suggests pre-training/fine-tuning
interactions or limited tuning; I cannot verify more without code.

---

## 7. CDAE — Contrastive Denoising Autoencoder (seed 7)

**1. Citation and links**
- Heydari, S., Abbasi, A., Hooshmand, M., Ramezani, M. (2026). *CDAE: Enhancing
Perturbation Robustness in Pretrained Language Models with Contrastive Denoising.* arXiv
2607.28236 (v1 30 Jul 2026, v2 16 Oct 2026; cs.AI, "Preprint"; IASBS, Zanjan, Iran). Not
peer-reviewed as far as the paper states.
- PDF: `Heydari2026_CDAE.pdf` (v2). arXiv: https://arxiv.org/abs/2607.28236 . Code:
https://github.com/ComputationIASBS/CDAE (from the abstract; repo not inspected).
- Status: **VERIFIED** (full text read).
- **Seed-description check (you asked me to verify it).** Title, authors and arXiv ID are as you
gave them; it is a 2026 paper. Your description "lexical/contextual perturbations for
robustness-aware training of PLMs" matches only partly:
  - *Lexical perturbations: yes* (WordNet synonym replacement, word dropout, masking of
content words; §3.2.1).
  - *Contextual perturbations: no.* There is no context-aware (MLM/LLM) substitution;
perturbations are random lexical edits on POS-tagged content words.
  - *"Robustness-aware training of PLMs": no, not of the PLM.* The BERT backbone is
**frozen** (§3.2.2); only a small MLP autoencoder on pooled embeddings is trained (§3.2.3). It
improves the **stability of sentence embeddings** (cosine similarity and retrieval of the clean
sentence from its perturbed version), not downstream task accuracy; the authors say
downstream transfer "was not evaluated" (§5).

**2. Problem and claim**
BERT/SimCSE/SBERT sentence embeddings change under content-word perturbations
(abstract, §1). CDAE learns a 128-d perturbation-invariant code on top of a frozen
bert-base-uncased, with a symmetric InfoNCE loss between clean and perturbed views plus a
denoising reconstruction loss. Claim: higher cosine similarity and top-1 retrieval accuracy under
perturbation than BERT, SimCSE and SBERT at moderate/high strengths, with the gap
widening with ρ (abstract, §4.3).

**3. Perturbations used** (§3.2.1)
- Three strategies on **content words** (nouns, verbs, adjectives, adverbs; identified with the
NLTK POS tagger, §4): (a) synonym replacement with a random WordNet synonym; (b) word
dropout (each selected word removed); (c) masking with the tokenizer's mask token.
- Strength ρ ∈ [0,1] = fraction of eligible content words affected. Training: ρ = **0.7**, strategy
chosen at random per sentence (§4, paragraph before 4.1). Evaluation: ρ ∈ {0.1, …, 0.9}
(§4.2).
- No similarity filter or sentence-encoder check; the authors note that at high ρ the meaning may
change, so they measure "representation stability rather than guaranteed semantic equivalence"
(§3.2.1).

**4. Method** (§3.2)
1. Embed sentence s with frozen bert-base-uncased: z = masked mean pooling over the final
hidden layer (Eq. 1), z ∈ R^768. Max length 64 (§3.1).
2. Create a perturbed variant s_p of each training sentence (one strategy, ρ = 0.7), embed it:
z^p; clean: z^o.
3. Encoder MLP: 768 → 512 → 256 → 128, each hidden layer BatchNorm + ReLU + dropout
0.30; final linear layer without activation gives z̄ ∈ R^128 (§3.2.3). Decoder MLP mirrors: 128 →
256 → 512 → 768.
4. Contrastive loss (Eqs. 2–3): ℓ2-normalised z̄^o, z̄^p; logits_ij = (z̄_i^o)ᵀ z̄_j^p / τ; symmetric
InfoNCE with in-batch negatives (no memory bank, no momentum encoder); τ = **0.07**.
5. Reconstruction loss (Eq. 4): L_recon = (1/d)‖ẑ^p − z^o‖² + (1/d)‖ẑ^o − z^o‖² with d = 768
(denoising term + identity term, both against the *clean* embedding).
6. L_total = λ_recon·L_recon + λ_contrast·L_contrast, λ_recon = λ_contrast = **1.0** (Eq. 5).
7. Evaluation representation = the 128-d bottleneck z̄ (§3.2).
- Gradient asymmetry (§3.2.6): contrastive loss updates only the encoder; reconstruction
updates encoder and decoder.
- Mixing with clean data: every pair contains a clean and a perturbed view; the identity term
trains on clean inputs. Perturbations are sampled online (my reading: "During training, input
sentences were perturbed…"; whether the perturbed sentences are regenerated each epoch is
**not specified**).
- Compute: small; one RTX 4060 Laptop GPU (8 GB), 20 epochs (§4). Wall-clock time not
reported.

**5. Experimental setup** (§3.1, §4)
- Data: SNLI premises only, unique sentences (labels discarded); splits 548,820 / 9,840 / 9,824
examples (§4), which sum to the 568,484 (premise, hypothesis, label)-deduplicated examples
stated in §3.1; unique premises are then selected from each split. Mean length 8.8 words,
median 8.
- Training: AdamW, lr 1e-4, weight decay 1e-5, batch 512, 20 epochs, dropout 0.3 (§4). Seeds
{42, 123, 456, 789, 1024, 1234}; CDAE retrained from scratch per seed (§4.3, Table 1 caption).
- Baselines (§4.1): bert-base-uncased mean pooling; "supervised SimCSE checkpoint" (exact
checkpoint not named in the text); Sentence-BERT (checkpoint not named). Baselines are **not
retrained** and are evaluated with the same perturbed sentences.
- Evaluation (§4.2): first N = 3,000 unique test premises; one perturbed counterpart per
sentence per (method, ρ); "a single evaluation sweep" (so the *perturbation sampling* for the
baseline comparison is a single draw).
- Metrics: mean cosine similarity between clean and perturbed embeddings (Eq. 8); top-1
retrieval of the clean sentence among the N clean sentences using the perturbed one as query
(Eq. 10; chance 1/N). Gap Δ = CDAE − baseline (Eq. 9).

**6. Results** (§4.3; CDAE numbers from Table 1 mean over six seeds; baseline numbers only
as quoted in the §4.3 text and Fig. 4, not tabulated)

| ρ | CDAE cosine (drop / mask / synonym) | CDAE top-1 (drop / mask / synonym) |
|---|---|---|
| 0.1 | .974 / .944 / .970 | .997 / .997 / .998 |
| 0.5 | .861 / .893 / .916 | .877 / .968 / .983 |
| 0.9 | .729 / .775 / .848 | .471 / .659 / .908 |

- Quoted baseline values at ρ = 0.9 (§4.3): cosine under masking/dropout: BERT ≈ 0.52/0.53,
SBERT ≈ 0.39/0.26, SimCSE ≈ 0.71/0.67, CDAE 0.78/0.73; under synonym replacement CDAE
0.85 vs BERT 0.79 vs SimCSE 0.81. Top-1 at ρ = 0.9: CDAE ≈ 66% (mask) and 47% (dropout)
vs ≈16% and 13% for SimCSE; synonym ≈ 0.90 vs 0.84 (SimCSE), BERT ≈ 0.46, SBERT ≈
0.67.
- Degradation with strength: smooth and monotone for all three strategies (Table 1; "most
steeply under dropout and least under synonym replacement", §4.3). At low ρ all models are
similar; SimCSE slightly beats CDAE under masking at ρ = 0.1–0.2 (§4.3).
- Seed variability: std across six seeds never exceeds 0.0033 (cosine) and 0.0121 (top-1)
(§4.3). Differences between baselines are not tested with significance tests, and baselines are a
single checkpoint.
- Clean-vs-perturbed *task* performance, label agreement, calibration/ECE: **not reported**
(embedding similarity is the only "agreement"-like measure).

**7. Reproduction notes**
1. Extract bert-base-uncased mean-pooled embeddings (max length 64) for unique SNLI
premises; 2. generate clean/perturbed pairs (ρ = 0.7, random strategy); 3. train the MLP
autoencoder (AdamW 1e-4, batch 512, 20 epochs) with Eq. 3 + Eq. 4; 4. evaluate on the first
3,000 unique test premises with Eqs. 8 and 10.
- For your use: an encoder-side stability metric (cosine/top-1 under ρ-sweeps) is the
transferable piece; the training recipe changes only an adapter, not the PLM. To make it a
*robustness-aware PLM training* method you would have to unfreeze the backbone and add
the same loss in fine-tuning (not done here).
- Ambiguities: which SimCSE/SBERT checkpoints, whether perturbations are resampled per
epoch, split counts, how stop words/POS-tag errors were handled, tokenisation of masked
words.
- Pitfalls: cosine similarity is not comparable across embedding spaces of different
dimension/geometry (the authors acknowledge this and add top-1 retrieval, §4.2); the evaluation
perturbations equal the training perturbations (in-distribution).

**8. Limitations and caveats**
- Authors' own: downstream benefit "was not evaluated … and remains an open question";
ablations of loss terms, alternative backbones (E5) and layer-wise analysis are future work (§5).
- Preprint, no peer review stated; single backbone (bert-base-uncased), single dataset for
training and test (SNLI premises, short sentences of 5–15 words).
- Perturbation families at test time match training time, so generalisation to unseen perturbation
types (typos, paraphrase) is untested.
- Not a classification/tagging robustness result: nothing here shows that a classifier built on
CDAE embeddings keeps its labels.

---

## 8. Seed 8: 2026 legal-NLP robustness paper — **NOT FOUND**

**Verification status: NOT FOUND.** I could not locate, with confidence, a paper matching "a
framework defining a perturbation space constrained by legal structure, adversarial fine-tuning
aligned to deployment noise, and Robustness-Aware Decoding". I did not substitute another
paper and I am not guessing at a title.

What I searched (all in October 2026):
- Web search with the phrase "Robustness-Aware Decoding" together with legal / LLM /
perturbation / adversarial fine-tuning / 2026 (four variants).
- arXiv search (arxiv.org/search) for the exact phrase "robustness-aware decoding" (no results)
and title/abstract searches combining legal with robust, robustness, adversarial, perturbation,
decoding, noise, fine-tuning (about 15 queries). The arXiv title searches returned only unrelated
legal-AI items.
- I read the abstracts (not the full texts) of the five closest-sounding hits and none matches the
three components: 2605.26530 "Which Changes Matter? Towards Trustworthy Legal AI via
Relevance-Sensitive Evaluation and Solver-Grounded Reasoning" (evaluation suite for legally
relevant vs irrelevant perturbations; no adversarial fine-tuning or decoding component stated in
the abstract); 2605.02472 "Accurate Legal Reasoning at Scale…" (neuro-symbolic, not
perturbations); 2608.21409 "Sycophants in the Courtroom…" (diagnostic framework);
2503.18360 "J&H: …Knowledge-Injection Attacks in Legal Domain" (2025); 2308.00165
"Adversarially Robust Neural Legal Judgement Systems" (2023).

Limits of this search: arXiv search is not full-text, and the paper could be on another venue,
under different wording, or not yet indexed. If you can give a title fragment, author or link, I can
verify it. If your source material came from a slide or message, it may also have described a
different paper.

---

---

## 9. Zhu et al. — FreeLB (additional: adversarial training for BERT-style models)

**1. Citation and links**
- Zhu, C., Cheng, Y., Gan, Z., Sun, S., Goldstein, T., Liu, J. (2020). *FreeLB: Enhanced
Adversarial Training for Natural Language Understanding.* ICLR 2020 (arXiv v5).
- PDF: `Zhu2020_FreeLB.pdf`. arXiv: https://arxiv.org/abs/1909.11764 . Code:
https://github.com/zhuchen03/FreeLB (footnote 1; not inspected).
- Status: **VERIFIED** (full text and appendix read).

**2. Problem and claim**
Embedding-space PGD adversarial training of BERT-style encoders to improve **generalisation
(clean accuracy)**, not robustness to perturbed text. FreeLB accumulates parameter gradients
over K PGD ascent steps ("free" large virtual batch of K adversarial embeddings) so it costs
about as much as K-step PGD training. Claims: BERT-base GLUE score 78.3 → 79.4,
RoBERTa-large 88.5 → 88.8 (§1, Table 2); lower loss increase around dev samples in
embedding space (Table 5). **No text-level perturbation (typo, synonym) evaluation is
performed.**

**3. Perturbations used** (§3)
- Perturbation δ added to the **word/sub-word embedding output only** (not segment/position
embeddings; §3, with footnote 2), Frobenius-norm ball ‖δ‖_F ≤ ε (Eq. 1). Applied to the
concatenated embeddings for multi-choice tasks (App. A.1).
- PGD step (Eq. 2): δ_{t+1} = Π_{‖δ‖_F ≤ ε}( δ_t + α · g(δ_t)/‖g(δ_t)‖_F ), g = ∇_δ L(f_θ(X+δ_t),
y).
- Initialisation (Alg. 1, line 4): δ₀ ← (1/√N_δ)·U(−ε, ε); N_δ is not defined in the text I extracted
(presumably the number of perturbed elements; not stated).
- Hyper-parameters per task (App. A.2, Table 7, RoBERTa-large): ε / α / m — MNLI 0.2 / 0.1 / 2;
QNLI 0.15 / 0.1 / 2; QQP 0.45 / 0.15 / 2; RTE 0.15 / 0.03 / 3; SST-2 0.6 / 0.1 / 2; MRPC 0.4 /
0.04 / 3; CoLA 0.2 / 0.025 / 3; STS-B 0.3 / 0.1 / 3; WSC/WNLI ε=0.01, α=0.005, m=2. The PDF
writes them as "2 E -1" etc.; I converted them to decimals. Note that even when mα < ε, the
perturbation can reach ε "due to the random initialization" (App. A.2).
- BERT-base GLUE hyper-parameters: **not specified** beyond "follow Devlin et al. (2019)"
(§4.1).

**4. Method** (Algorithm 1, §3.2–3.3)
1. For each minibatch: δ₀ random init; g₀ ← 0.
2. For t = 1..K: accumulate parameter gradient g_t ← g_{t−1} + (1/K)·E[∇_θ L(f_θ(X+δ_{t−1}),
y)]; compute g_adv = ∇_δ L(f_θ(X+δ_{t−1}), y); δ_t ← Π(δ_{t−1} + α·g_adv/‖g_adv‖_F).
3. After K steps update θ once: θ ← θ − τ·g_K (one optimizer step with the averaged gradient).
- Objective (Eq. 3): min_θ E[(1/K) Σ_{t=0}^{K−1} max_{δ_t ∈ I_t} L(f_θ(X+δ_t), y)] with I_t =
B_{X+δ₀}(αt) ∩ B_X(ε), i.e. equivalent to a K× larger virtual batch of adversarial embeddings.
**Only adversarial points are used in the loss; the clean input is not separately added** except
through δ₀ near X (my reading of Alg. 1; the paper does not state a clean/adv ratio).
- Dropout (§3.3): reuse the **same dropout mask** m in all K ascent steps (Eq. 4). Table 4:
without mask reuse (FreeLB-3*) RTE 87.14 vs 88.13 with it.
- Compute: K forward/backward passes per update (§1/§3.1: "K-PGD requires K
forward-backward passes"); FreeLB has "almost no overhead" relative to K-PGD; relative to
vanilla fine-tuning it is ≈K× the cost (their statement in the Conclusion: adversarial training "still
takes significant overhead compared with vanilla SGD"). No wall-clock number given.

**5. Experimental setup** (§4)
- Models: BERT-base (HuggingFace), RoBERTa-large (fairseq), ALBERT-xxlarge-v2 (Table 6).
Tasks: GLUE (8 tasks + WNLI tricks), ARC-Easy/Challenge, CommonsenseQA.
- Fine-tuning hyper-parameters (lr, batch size, epochs): "same as RoBERTa" (fairseq
`README.glue.md`), MRPC lr 5e-6 (App. A.2); ARC 5 epochs (§4.2). BERT-base values: not
specified.
- Seeds: median ± std over **5 runs** with the same hyper-parameters (Tables 1, 4, 6).
- Robustness measurement (§4.3, Eq. 5): ΔL_max(X, ε) = max_{‖δ‖≤ε} L(f(X+δ), y) − L(f(X), y),
found with 2000-step PGD, step size 5e-3, ε = 0.01‖X‖_F in the convergence check; only
samples correctly classified by all compared models are used (RTE 227, CoLA 850, MRPC 355
samples).

**6. Results**

| RoBERTa-large GLUE dev (median over 5 seeds; Table 4 / Table 1) | RTE | CoLA | MRPC |
|---|---|---|---|
| Vanilla (reimplementation) | 85.61 (1.67) | 67.57 (1.30) | 90.69 (0.54) |
| PGD (m ascent steps) | 87.41 (0.9) | 69.67 (1.2) | 90.93 (0.2) |
| FreeLB (m=3) | 88.13 (1.21) | 71.12 (0.90) | 91.42 (0.72) |

- Leaderboard (Table 2): BERT-base 78.3 → FreeLB-BERT 79.4 overall; RoBERTa 88.5 →
FreeLB-RoBERTa 88.8 (7-model ensemble).
- Table 6: RoBERTa-large 90.2/94.7/92.2/86.6/96.4/90.9/68.0/92.4 vs FreeLB
90.6/95.0/92.6/88.1/96.8/91.4/71.1/92.7 (MNLI/QNLI/QQP/RTE/SST-2/MRPC/CoLA/STS-B);
ALBERT-xxlarge-v2 + FreeLB gains +0.1 to +1.7 points per task (largest: CoLA 71.4 → 73.1;
MRPC 90.9 → 92.4).
- Embedding-space robustness (Table 5, median max loss increase, ×10⁻⁴ for RTE/CoLA, ×10⁻³
for MRPC): RTE vanilla 5.1 / PGD 4.7 / FreeLB 3.0; CoLA 6.1 / 128.2 / 1.4 (PGD trained model
is *worse* than vanilla on CoLA); MRPC 10.2 / 5.7 / 3.6.
- Not reported: accuracy on text-level perturbed inputs, prediction agreement, degradation curve
versus ε, calibration.

**7. Reproduction notes**
1. Clone the repo or implement Alg. 1 around any HuggingFace encoder: hook the
`inputs_embeds` input (word embeddings only), run K=2–3 ascent steps with
normalised-gradient updates (Frobenius norm per example), accumulate parameter gradients
scaled by 1/K, one optimizer step.
2. Keep the same dropout mask across ascent steps (e.g., fix the RNG state or reuse masks).
3. Tune ε, α, m on the dev set per task (Table 7 values are RoBERTa-large specific).
- Missing/ambiguous: N_δ in the init; norm per example vs per batch; BERT-base
hyper-parameters; whether ε scales with sequence length (it is a Frobenius norm over the whole
input matrix, so longer inputs get less per-token budget).
- Pitfalls: the reported GLUE gains are 0.3–1.1 points with seed std of 0.2–1.7 on small tasks
(Tables 1, 4), so single-seed comparisons on RTE/MRPC/CoLA are not meaningful; fine-tuning
RoBERTa can be unstable (Table 1 caption notes unconverged runs).

**8. Limitations and caveats**
- Measures generalisation to clean dev sets and embedding-space invariance, **not robustness
to discrete text perturbations**; an embedding-space adversary "is strictly stronger than a more
conventional text-based adversary" in the authors' words (§3) but there is no evidence here that
this transfers to typos or synonyms (see SMART/RoAST for that).
- ≈K× training cost; limited gains on large tasks; hyper-parameters (ε, α, m) tuned per task on
dev sets.
- English GLUE/QA tasks, sequence-level inputs only.

---

## 10. Jiang et al. — SMART (additional: adversarial/proximal regularisation for BERT-style
fine-tuning)

**1. Citation and links**
- Jiang, H., He, P., Chen, W., Liu, X., Gao, J., Zhao, T. (2020). *SMART: Robust and Efficient
Fine-Tuning for Pre-trained Natural Language Models through Principled Regularized
Optimization.* ACL 2020 (arXiv v5).
- PDF: `Jiang2020_SMART.pdf`. arXiv: https://arxiv.org/abs/1911.03437 . Code:
https://github.com/namisan/mt-dnn (footnote 1 of the paper; not inspected).
- Status: **VERIFIED** (main text and the appendix implementation notes read).

**2. Problem and claim**
Fine-tuning large pre-trained LMs on small target data overfits and updates aggressively.
SMART adds (i) a **smoothness-inducing adversarial regulariser** (outputs should not change
under small embedding perturbations) and (ii) a **Bregman proximal point (trust-region) term
with EMA "mean-teacher" momentum**. Claims state-of-the-art on GLUE, SNLI, SciTail and
ANLI (abstract). **Evaluated on clean benchmark accuracy; "robustness" is tested only through
ANLI and ambiguous-label analyses, not through perturbed text.**

**3. Perturbations used** (§3.1, §4.1, Alg. 1)
- Perturbation of the **first-embedding-layer output** x_i (sub-word embeddings) with ‖x_       ̃ i−
x_i‖_p ≤ ε; the implementation uses **p = ∞** (Alg. 1 caption).
- ε = **1e-5**, initial noise ν ~ N(0, σ²I) with σ = **1e-5**, inner steps T_x̃ = **1**, step size for x̃
η = **1e-3** (§4.1). So the "adversary" is a *very small* single-step L∞ perturbation after a
Gaussian initialisation.
- Perturbation step (Alg. 1, lines 7–10): g̃_i = g_i/‖g_i‖_∞ with g_i = ∇_x̃ ℓ_s(f(x;̃ θ̄_s), f(x; θ̄_s))
averaged over the batch; x_    ̃ i ← Π_{‖x−
                                          ̃ x‖_∞ ≤ ε}(x_̃ i + η g̃_i).
- No text-level perturbations.

**4. Method**
1. Objective (Eq. 1): min_θ F(θ) = L(θ) + λ_s R_s(θ), with R_s(θ) = (1/n) Σ_i max_{‖x_     ̃ i−x_i‖_p ≤
ε} ℓ_s(f(x_
          ̃ i;θ), f(x_i;θ)).
2. ℓ_s = symmetrised KL, D_KL(P‖Q) + D_KL(Q‖P) for classification; squared difference (p−q)²
for regression (§3.1).
3. Proximal/Bregman term (Eq. 2–3): at outer iteration t+1, θ_{t+1} = argmin_θ F(θ) +
μ·D_Breg(θ, θ̃_t), with D_Breg(θ, θ_t) = (1/n) Σ_i ℓ_s(f(x_i;θ), f(x_i;θ_t)).
4. Momentum (Eq. 3): θ̃_t = (1−β)θ_t + β θ̃_{t−1} (EMA teacher; "Mean Teacher").
5. Algorithm 1 per mini-batch: sample batch; init x_ ̃ i = x_i + ν_i; do T_x̃ gradient-ascent steps on
x_̃ i; Adam update of θ on the combined loss; after S inner steps (S = 1) set θ_t = θ̄_S and
update EMA θ̃.
- Hyper-parameters (§4.1): μ = 1, λ_s ∈ {1, 3, 5}, β = 0.99 for the first 10% of updates and
0.999 afterwards (following Tarvainen & Valpola); S = 1, T_x̃ = 1.
- Mixing of clean/adversarial: the cross-entropy L is on **clean** inputs; the adversarial term is a
consistency regulariser between clean and perturbed outputs (no labels used for the perturbed
copy). This differs from Goodfellow/Madry/FreeLB, where the adversarial loss uses labels.
- Compute (Appendix, "implementation notes"): with S = T_x̃ = 1 SMART needs "3 more forward
passes and 3 more backward passes per iteration compared with direct fine-tuning"; "in practice
it takes about 3 times the original training time"; GPU memory approximately doubles.

**5. Experimental setup** (§4.1, §5)
- Models: BERT-base, RoBERTa-large (also MT-DNN-initialised variants). Data: GLUE (8 tasks),
SNLI, SciTail, ANLI.
- Training: Adam / RAdam; lr ∈ {1e-5, 2e-5, 3e-5, 5e-5}; batch ∈ {16, 32, 64}; max 6 epochs;
linear decay with warm-up 0.1; task-layer dropout 0.1 (0.3 MNLI, 0.05 CoLA); gradient clipping
norm 1; max length 512 tokens. Selection of the grid winner per task is not detailed. Seeds:
**single run per table cell not stated as multi-seed**; the paper reports no standard deviations
(not specified).
- Baselines: BERT_ReImp (their re-run), RoBERTa as reported, PGD/FreeAT/FreeLB numbers
copied from the FreeLB paper (Table 1).
**6. Results** (GLUE dev, Table 1; BERT-base ablation Table 3)

| Model | MNLI-m/mm | RTE | QNLI | MRPC (Acc/F1) | CoLA (Mcc) | SST-2 |
|---|---|---|---|---|---|---|
| BERT_ReImp | 84.5/84.4 | 63.5 | 91.1 | 84.1/89.0 | 54.7 | 92.9 |
| SMART_BERT | 85.6/86.0 | 71.2 | 91.7 | 87.7/91.3 | 59.1 | 93.0 |
| RoBERTa-large (reported) | 90.2/– | 86.6 | 94.7 | –/90.9 | 68.0 | 96.4 |
| FreeLB (from FreeLB paper) | 90.6/– | 88.1 | 95.0 | –/91.4 | 71.1 | 96.7 |
| SMART_RoBERTa | 91.1/91.3 | 92.0 | 95.6 | 89.2/92.1 | 70.6 | 96.9 |

- Ablation (Table 3, BERT-base): removing R_s (λ_s=0) lowers RTE 71.2 → 70.8, MRPC 91.3 →
90.8, MNLI 85.6 → 84.8; removing the Bregman term (μ=0) changes little (MNLI 85.4, RTE
71.2). The authors note the effect is larger on small datasets (RTE, MRPC).
- Error analysis (§5.2): on ambiguous MNLI dev samples (annotation agreement 5/0/0 … 3/1/1)
SMART_RoBERTa beats RoBERTa in accuracy and in KL to the annotator distribution, most on
high-ambiguity subsets (Fig. 2).
- ANLI (§5.6, Table 6, "Robustness"): SMART_RoBERTa-large test All 57.1 (combined data) vs
53.7 for RoBERTa-large and 56.9 vs 51.9 (ANLI-only training). This is robustness to
adversarially *collected* examples (human-in-the-loop), not to a perturbation protocol.
- Domain adaptation (§5.4, Table 5): MT-DNN-SMART beats MT-DNN with 0.1% SNLI data
(82.7 vs 82.1) — small gains.
- Not reported: accuracy under typos/synonyms, label agreement under perturbation,
degradation vs ε, calibration, seed variance.

**7. Reproduction notes**
1. Clone MT-DNN/SMART; or implement: forward clean batch → logits P; add noise
ν~N(0,1e-5²) to the embedding output; one ascent step on the symmetric-KL between f(x)̃ and
f(x) (normalise gradient by its L∞ norm, step 1e-3, clamp to ±1e-5); loss = CE(clean) +
λ_s·KL_sym + μ·KL_sym(student, EMA teacher on clean inputs). Update EMA with β as above.
2. Expect ≈3× the fine-tuning time.
- Missing: per-task chosen (lr, batch, λ_s), number of seeds, whether detached clean logits are
used in the KL, the exact EMA initialisation point for the first epoch.
- Pitfalls: with ε = 1e-5 the perturbation is tiny relative to embedding scale (so the regulariser is
closer to a consistency/mean-teacher regulariser than to a worst-case adversary — my
interpretation); gains of ~0.1–1 points are within typical seed variance on small tasks (FreeLB
paper Table 4 shows std up to 1.7); comparisons in Table 1 mix their own runs with numbers
copied from other papers.

**8. Limitations and caveats**
- Generalisation-oriented; no text-perturbation robustness measurement; baselines copied from
other papers with different tuning budgets.
- ≈3× training time and 2× memory; many tuned hyper-parameters (lr, batch, λ_s) per task.
- English classification/regression (GLUE); no evidence for tagging, QA or generation.
---

## 11. Kim et al. — RoAST (additional: adversarial perturbation + selective training; includes
calibration)

**1. Citation and links**
- Kim, J., Mao, Y., Hou, R., Yu, H., Liang, D., Fung, P., Wang, Q., Feng, F., Huang, L., Khabsa,
M. (2023). *RoAST: Robustifying Language Models via Adversarial Perturbation with Selective
Training.* Findings of EMNLP 2023 (arXiv 2312.04032v1).
- PDF: `Kim2023_RoAST.pdf`. arXiv: https://arxiv.org/abs/2312.04032 . Code:
https://github.com/bbuing9/RoAST (footnote 1; not inspected).
- Status: **VERIFIED** (main text, appendix A, C, D and tables read; the 33-page appendix
per-dataset tables were only skimmed).

**2. Problem and claim**
Fine-tuned LMs are fragile along several axes. RoAST fine-tunes with a one-step
embedding-space adversary plus a consistency term, and updates only the (stochastically) most
task-important parameters, to keep pre-trained knowledge. It is evaluated on five axes at once:
in-distribution accuracy, distribution-shift accuracy, adversarial accuracy, **calibration (ECE)**
and anomaly detection (§1, §4.1). Claim: best average relative improvement across 6 LMs, 2
tasks (§4.2, Tables 1–3).

**3. Perturbations used**
- Training perturbation (§3): embedding-level, one gradient-ascent step with step size **δ = 0.1**
under ℓ∞: x̃ := x + δ·(∂L_task/∂x)/‖∂L_task/∂x‖_∞ (single step as in SMART; fixed δ = 0.1 in
§4.1/App. A.3). x = word embeddings of the tokens.
- Evaluation sets (§4.1, App. A.1):
  - *Adversarial (Acc_adv)*: for SST-2, five sets — TextFooler examples generated against
vanilla BERT (TF-B) and against vanilla RoBERTa (TF-R) (following Wang et al. 2021a),
DynaSent R1 and R2 (human-in-the-loop, neutral removed), AdvGLUE (SST-2); for MNLI, nine
sets — TF-B/TF-R × matched/mismatched (4), ANLI R1–R3 (3), AdvGLUE-m/mm (2).
  - *Distribution shift*: SST-2 → Yelp, Amazon, IMDB, cIMDB (counterfactual), Poem; MNLI → 7
entailment sets (Diag, HANS, QNLI, WNLI, NQ-NLI, FEVER-NLI, WANLI), with MNLI treated as
binary entailment vs not-entailment.
  - *Calibration*: average ECE (Guo et al. 2017) over **all** evaluations: 11 datasets for SST-2,
18 for MNLI (App. A.1). **Number of ECE bins: not specified in the text I read.**
  - *Anomaly detection*: max-softmax AUROC against external corpora (WMT16, Multi30K,
etc.).
- The adversarial test sets come from *other* attackers and models (transfer attacks), not from
attacks on the RoAST models themselves.

**4. Method** (§3, Eqs. 1–4, Algorithm 1, App. A.3)
1. Per step, compute x̃ with one gradient step on the embedding output.
2. Loss (Eq. 1): L_train = L_task(x, y) + L_task(x,̃ y) + λ·L_cons(x, x)̃ , where L_cons =
D_KL(f(x)‖f(x)̃ ) + D_KL(f(x)̃ ‖f(x)) (bidirectional KL). Clean and adversarial CE are equally
weighted (1:1). λ ∈ {0.01, 0.1, 0.5}.
3. Importance score (Eq. 2): s(θ) = Σ_{(x,y)} |g(θ)|², g = ∂L_train/∂θ, approximated by gradients
accumulated during the previous epoch's backward passes (no extra cost). The first mask uses
squared gradients of the vanilla cross-entropy loss ("InitGrad").
4. Normalised rank score s(̃ θ) ∈ [0,1]; sampling probability p(θ) = 1 / (1 + exp(2β(s(̃ θ) − α)))
(Eq. 3); mask m(θ) ~ Bernoulli(p(θ)); gradient step θ ← θ − η·(m(θ)/p(θ))⊙g(θ) (Eq. 4; scaling
term 1/p optional, treated as a hyper-parameter). Mask resampled once per epoch (§3). α ∈
{0.95, 0.9, 0.8} for sentiment and {0.6, 0.65, 0.7} for entailment, β ∈ {1, 5, 10} (App. A.3).
- Unbiasedness corollary (App. B, citing Xu et al. 2021): E[g̃] = g under assumptions.
- Compute: one extra forward/backward for the perturbation plus a second forward for L_task(x)̃
per step (my reading of Alg. 1: gradient wrt x then two forward passes); no wall-clock numbers
given. The paper says token-level (VAT-D) perturbation costs "15% more time per iteration" than
embedding-level (App. C.1). Mask computation is "free" (reuses gradients).

**5. Experimental setup** (§4.1, App. A)
- Models: main = RoBERTa-large; also BERT-large, ALBERT-xxlarge, XLNet-large,
ELECTRA-large, DeBERTa-large (Table 3), and GPT2-large with a linear head on the last token
(Table 13, App. D/E).
- Training data: SST-2 train (67k) and MNLI train (393k).
- Optimizer: AdamW (β₁, β₂, ε = 0.9, 0.98, 1e-6), weight decay 0.01, linear decay with warm-up
0.06, **lr 1e-5, batch 16, 10 epochs** (§4.1); A100 GPUs. Hyper-parameters of all methods
tuned from candidate sets on the validation set (App. A.2).
- Seeds: **3 random seeds**, mean ± std (Tables 1–2).
- Baselines (14): Vanilla, WordDrop, R-Drop, HiddenCut, AdvWeight, AdvEmbed (Madry-style),
FreeLB, SMART, RIFT, ChildTuning, R3F, Weight Consolidation, LP-FT.
- Summary metric: Δ_avg = mean over metrics of (s − s_base)/(s_max − s_base) (Eq. 5; s_max
= 100 for accuracies, 0 for ECE, 1 for AUROC) — note this normalises by distance to the best
possible score, so tiny absolute changes at the ceiling (e.g. Acc_in ≈ 96) can be weighed like
large changes elsewhere.

**6. Results** (RoBERTa-large, SST-2, Table 1; mean ± std over 3 seeds)

| Method | Acc_in | Acc_shift | Acc_adv | ECE ↓ | AUROC | Δ_avg |
|---|---|---|---|---|---|---|
| Vanilla | 96.29±0.14 | 91.79±0.13 | 66.30±2.14 | 7.11±0.82 | 86.72±3.60 | 0.00 |
| AdvEmbed | 96.48±0.05 | 91.75±0.32 | 69.90±0.90 | 5.51±0.16 | 90.79±0.35 | 13.70 |
| FreeLB | 96.33±0.34 | 91.94±0.38 | 70.06±0.27 | 6.49±0.51 | 89.82±0.40 | 9.21 |
| SMART | 96.86±0.05 | 91.49±0.33 | 70.09±0.04 | 6.32±0.34 | 90.89±0.44 | 13.10 |
| LP-FT | 96.33±0.25 | 91.85±0.17 | 72.48±0.05 | 4.05±0.20 | 89.46±0.77 | 16.75 |
| **RoAST** | 96.87±0.20 | 92.38±0.12 | 72.57±0.53 | 5.45±0.40 | 90.37±0.65 | 18.39 |
MNLI (Table 2): Vanilla 89.97 / 64.31 / 48.60 / ECE 12.64 / 92.09; AdvEmbed 90.24 / 64.23 /
50.20 / 12.48 / 93.83 (Δ_avg 5.72); SMART 90.74 / 63.27 / 52.27 / 11.41 / 91.42 (2.56); RoAST
90.64 / 63.95 / 51.33 / 11.02 / 93.25 (**7.63**).
- Clean-vs-perturbed: SST-2 clean 96.29 → "adversarial" 66.30 average for vanilla
RoBERTa-large (a 30-point gap on the TextFooler/DynaSent/AdvGLUE mixture), RoAST
narrows it to 96.87 → 72.57 (gap ≈24). MNLI vanilla 89.97 → 48.60 (gap ≈41), RoAST 90.64 →
51.33. So **adversarial test sets still cost 24–39 points after robust fine-tuning**. These sets are
adversarial/human-in-the-loop, not random typos.
- Calibration: average ECE falls from 7.11 → 5.45 (SST-2) and 12.64 → 11.02 (MNLI); LP-FT
has the best SST-2 ECE (4.05). ECE is averaged over in-distribution, shifted and adversarial
sets, so it is **not an ECE under controlled perturbation strength**. Per-dataset ECE is in App.
D (Tables 15, 17, 20), I did not tabulate them.
- Other LMs (Table 3 / 12, relative to vanilla of each LM): MNLI Δ_avg RoAST: BERT-large 25.34
(vs. BERT-large vanilla), RoBERTa 7.63, ALBERT 8.19, XLNet 3.30, ELECTRA 4.39, DeBERTa
11.93; SST-2: 22.76, 18.39, 30.62, 12.74, 8.29, 18.90 (Table 12 values, each vs. its own vanilla).
- Decoder model (Table 13, GPT2-large, SST-2): Vanilla 94.99 / 84.33 / 62.38 / ECE 8.01 /
95.30; RoAST 95.03 / 81.91 / 64.96 / 8.52 / 97.16 (Δ_avg 5.07); Acc_shift and ECE got *worse*,
AdvEmbed is weaker (Δ 2.60). The authors note baselines are less effective on decoder-only
LMs (App. D).
- Ablation (Table 4, SST-2): adversarial perturbation only (a) Δ 13.70; threshold masking only (b)
13.80; both with hard threshold (c) 15.83; full RoAST (with Bernoulli sampling) 18.39.
- Token-level variant (App. C.1, Table 6): RoAST on top of discrete VAT-D perturbation improves
Acc_adv but discrete perturbation lowers clean accuracy unless RoAST mitigates it.

**7. Reproduction notes**
1. Implement x̃ = x + 0.1·g/‖g‖_∞ on the embedding output; L = CE(x) + CE(x)̃ + λ·KL_sym(f(x),
f(x)̃ ).
2. Keep a per-parameter running sum of squared gradients each epoch; at the next epoch
rank-normalise, compute p(θ) with α, β, sample Bernoulli masks per parameter (or per tensor —
**granularity not specified in the text I read**), scale by 1/p optionally.
3. Evaluate with TextFooler-on-vanilla datasets, DynaSent, ANLI, AdvGLUE and ECE with a
fixed bin count (choose and report; the paper's is unspecified).
- Missing: ECE bin count; mask granularity; exact α/β/λ per final run; whether AdvGLUE dev/test
split; code defaults (consult the repo).
- Pitfalls: per-parameter Bernoulli masks of a 355M-parameter model require a mask tensor the
size of the model each epoch; the "Δ_avg" metric is relative to the vanilla of the *same* LM and
not comparable across LMs unless the common baseline is used (as in Table 3); adversarial
sets built against vanilla BERT/RoBERTa could be easier or harder for different architectures.

**8. Limitations and caveats**
- Classification/NLI only (SST-2, MNLI); English; no tagging/QA/retrieval.
- "Adversarial robustness" is measured on fixed sets from other attacks, not on attacks against
the final model, and not under graded perturbation strength; no degradation curve.
- Only 3 seeds; differences of 1–2 points in Acc_adv are within one standard deviation for
several baselines (e.g. SMART 70.09±0.04 vs AdvEmbed 69.90±0.90 vs RoAST 72.57±0.53).
- Decoder-only LM results are limited to GPT2-large on one task and show mixed outcomes
(Table 13).

---

## 12. Moradi & Samwald — Evaluating the Robustness of Neural Language Models to Input
Perturbations (additional: non-adversarial evaluation across tasks)

**1. Citation and links**
- Moradi, M., Samwald, M. (2021). *Evaluating the Robustness of Neural Language Models to
Input Perturbations.* EMNLP 2021 (arXiv 2108.12237v1; "Accepted by EMNLP 2021" per arXiv
comment).
- PDF: `Moradi2021_InputPerturbations.pdf`. arXiv: https://arxiv.org/abs/2108.12237 . Code
(stated in §4): https://github.com/mmoradiiut/NLP-perturbation (not inspected).
- Status: **VERIFIED** (full text read, Tables 3–5 read in layout mode). Section numbers: §1
Introduction, §2 NLP tasks, §3 Language models, §4 Perturbation methods (4.1 character-level,
4.2 word-level), §5 Results (5.1 results/PPS analysis, 5.2 User study), §6 Related work, §7
Conclusion as printed.

**2. Problem and claim**
A **test-time-only** non-adversarial perturbation toolkit (character- and word-level, 14 methods)
applied to fine-tuned BERT-large, RoBERTa-large, XLNet-large and ELMo on five tasks
(classification, sentiment, NER, semantic similarity, QA). Claim: all models are sensitive to small
natural noise; benchmark accuracy overstates robustness (abstract, §7). Models were "neither
pretrained nor fine-tuned on perturbed samples" (§5.1).

**3. Perturbations used** (§4; examples in Table 2)
Character-level (a random word *Word_i* is chosen):
- Insertion: random char inserted at a random position (not first/last) if the word has ≥ 3
characters.
- Deletion: one random char deleted (first and last never deleted; ≥ 3 characters).
- Replacement: one char replaced by an adjacent keyboard key.
- Swapping: one char swapped with its left/right neighbour.
- Repetition: a char (not first/last) duplicated.
- Common misspelled words (CMW): a word that occurs in the Wikipedia list of common
misspellings is replaced by its misspelling.
- Letter-case changing (LCC): case of the first char or of all chars toggled (random choice).
Word-level: Deletion (random word), Repetition (random word copied after itself), Replacement
with synonyms (RWS; WordNet), Negation (verbs negated/de-negated), Singular/plural verbs
(SPV), Verb tense (VT), Word order (WO; M consecutive words reordered; **M not specified**).
- Strength parameter: **Perturbation Per Sample (PPS) = maximum number of perturbations per
sample, PPS ∈ {1, 2, 3, 4}** (§5.1). Tables 3–4 use PPS = 1; Table 5 reports averages for PPS
1–4. Rate per token is not used; length-normalisation is **not applied** (so long inputs get a
lower relative strength).
- Constraints: implemented with NLTK; no similarity encoder. **Manual curation** for
meaning-changing perturbations (Deletion, Negation, RWS): three annotators checked samples
until 200 valid perturbed samples were collected per dataset per PPS, altering labels when
necessary or excluding the sample (~1 minute per sample; counts per PPS in App. B, Tables
10–12). All other perturbations were used automatically and unfiltered.
- Human validation (§5.2): 20 participants; 94% of automatically produced samples (all
character-level + Repetition, SPV, VT; 1–3 perturbations each) judged understandable and
meaning-preserving; for Deletion/RWS/Negation/Word-order only 39% remained meaningful
and label-consistent, 12% meaningful but needing a new label, 49% no longer meaningful.

**4. Method**
Evaluation only (no robust training). Procedure: fine-tune each model on clean data; apply each
perturbation separately to every test sample (for the three curated methods, to a 200-sample
curated subset); report the task metric; report absolute drop per PPS. There is no
label-agreement metric: performance is measured against (possibly corrected) gold labels.

**5. Experimental setup** (§2–3, App. A)
- Datasets (Table 1; train/dev/test): TREC question classification 5,000/452/500 (micro-F1, 50
classes), SST 8,544/1,101/2,210 (accuracy, 5 classes), CoNLL-2003 NER 14,041/3,250/3,453
(F1), STS-B 5,749/1,500/1,379 (Pearson), WikiQA 2,117/296/630 (F1).
- Models: BERT-large cased (340M), RoBERTa-large, XLNet-large, ELMo (2 highway layers,
LSTM 4096, 93.6M parameters; dense 128 + task head).
- Hyper-parameters (App. A, Tables 6–9): BERT: max length 64 (256 for QA), batch 12 (2 for
QA), lr 2e-5 / 1e-5 / 3e-5 / 1e-5 / 2e-5 (TC / SA / QA / NER / SS), epochs 20 / 15 / 10 / 20 / 20;
RoBERTa: same lengths and batches, lr 1e-5 / 1e-5 / 1.5e-5 / 2e-5 / 2e-5, weight decay 0.1
(0.01 for QA and SS), linear decay, warm-up 0.06 (0.05 for NER/SS); XLNet: 6K steps (4K QA),
batch 8, lr 2e-5/2e-5/2e-5/1e-5/1e-5; ELMo: batch 128 (256 QA), dropout 0.2, 20 epochs (10
QA). Optimizer is not stated for the transformers ("default values specified by the original
models").
- Seeds: **five fine-tuning runs**; because a t-test (p = 0.05) found no significant difference
between runs, only the first run is reported (§5.1). Per-run numbers are not reported.

**6. Results** (BERT-large rows; test accuracy/F1 vs perturbed, PPS = 1; Tables 3–5)

| Task (metric) | Clean | Char: insertion | deletion | replacement | swap | repeat | CMW | LCC |
Word: deletion | RWS | word order |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TREC (micro-F1) | 90.4 | 77.4 | 76.2 | 76.1 | 76.5 | 78.8 | 58.4 | 78.3 | 75.1 | 65.7 | 74.5 |
| SST (acc.) | 92.2 | 77.1 | 75.6 | 75.5 | 78.3 | 77.9 | 62.0 | 76.7 | 73.7 | 67.5 | 76.4 |
| CoNLL (F1) | 92.6 | 83.6 | 80.7 | 81.4 | 82.5 | 81.9 | 71.3 | 81.2 | 81.4 | 74.1 | 70.7 |
| STS-B (Pearson) | 82.5 | 72.9 | 71.5 | 73.0 | 74.3 | 74.2 | 68.6 | 73.8 | 72.6 | 69.4 | 72.0 |
| WikiQA (F1) | 91.6 | 82.7 | 80.5 | 81.1 | 81.9 | 79.8 | 68.6 | 80.7 | 78.4 | 71.5 | 76.7 |
- Table 5 (mean absolute decrease over the perturbation methods; BERT): TREC char-level
−15.8 / −17.2 / −18.0 / −18.3 for PPS = 1–4; word-level −8.8 / −10.2 / −13.1 / −13.8. SST char
−17.4 / −18.9 / −20.1 / −21.3; word −11.0 / −13.5 / −15.1 / −16.7. CoNLL char −12.2 → −16.9;
word −10.8 → −14.9. STS char −9.8 → −13.6; word −10.0 → −14.5. WikiQA char −12.2 →
−16.4; word −8.8 → −13.0.
- **Degradation curve**: roughly linear to mildly concave in PPS (e.g. BERT SST char −17.4,
−18.9, −20.1, −21.3; no cliff; the first perturbation does the most damage). Large step from "no
noise" to "one edit" because 1 edit may hit a key word.
- Model differences: RoBERTa best overall but not uniformly; ELMo (character-based) is more
robust to character noise (smaller decreases, e.g. TREC char −8.8 vs BERT −15.8) while XLNet
handles word-order best (TREC WO 83.1 vs BERT 74.5).
- The extremely damaging perturbations are CMW (−32 on TREC for BERT) and RWS (−25 on
TREC), (my interpretation, not a claim of the paper: CMW produces rare surface forms that
fragment into many word-pieces, and RWS can swap in near-synonyms that shift the signal
words).
- Calibration, prediction agreement, perturbation-aware training: **not reported**.

**7. Reproduction notes**
1. `git clone` the repo; fine-tune the models with the App. A hyper-parameters; apply each
perturbation to the test sets with PPS 1–4; for Deletion/Negation/RWS consider your own
curation step (the 200-sample curated subsets are not guaranteed to be in the repo).
2. For a BERT-style classifier of your own: reuse CMW/char edits (cheap), then add agreement
= fraction of examples whose predicted label is unchanged, which is not in this paper but is a
direct by-product.
- Missing: M for word order; the random seed of the perturbation sampler; whether PPS counts
per sample or per word; optimizer for transformers; whether the 200-sample curated subsets are
released.
- Pitfalls: a single perturbed copy per test example (no repetition) means perturbation noise is
part of the reported number; word-level methods that change meaning require label handling;
CMW depends on the Wikipedia misspelling list, which only covers words present in it (coverage
not reported).

**8. Limitations and caveats**
- English; five fixed tasks, short inputs (max length 64 tokens for four of five tasks); test-time
perturbations only, so no information about robust training.
- Single reported fine-tuning run per model (five were run), so seed variance is asserted but not
shown.
- PPS caps the *number* of perturbations, not the fraction of tokens, so degradation curves vs
"5/10/20% of tokens" would need re-implementation.
- Manual curation applied only to three word-level methods and only 200 samples each.

---
## 13. Pruthi et al. — Combating Adversarial Misspellings with Robust Word Recognition
(additional: typo defence in front of BERT)

**1. Citation and links**
- Pruthi, D., Dhingra, B., Lipton, Z. C. (2019). *Combating Adversarial Misspellings with Robust
Word Recognition.* ACL 2019 (long paper; arXiv 1905.11268v2).
- PDF: `Pruthi2019_Misspellings.pdf`. arXiv: https://arxiv.org/abs/1905.11268 . Code (footnote
1): https://github.com/danishpruthi/adversarial-misspellings (not inspected).
- Status: **VERIFIED** (full text read; Table 3 read in layout mode). Sections: §1 Intro, §2
Related work, §3 Robust word recognition (3.1 ScRNN with backoff, 3.2 Model sensitivity, 3.3
Synthesizing adversarial attacks), §4 Experiments (4.1 word error correction, 4.2 robustness to
adversarial attacks, 4.3 sensitivity analysis), §5 Conclusion.

**2. Problem and claim**
Character-level typos chosen adversarially (1–2 edits per sentence) collapse word-level,
char-level and word-piece classifiers, with fine-tuned **BERT** going 90.3 → 45.8 under a
single 1-character "all" attack (abstract, Table 3). Data augmentation and adversarial training
barely help. A modular defence — a semi-character RNN word recogniser placed in front of the
unchanged classifier, with backoff strategies for rare/unseen words — restores BERT to ≈75%
(Table 3). Better word-error-rate alone is not enough: the recogniser should also have low
*sensitivity* (§3.2, §4.3).

**3. Perturbations used** (§3.3 "Allowed perturbations")
- Four character edits, applied only to **internal characters** (first/last char fixed), words of
**length ≥ 4**, **non-stopwords**: Swap (two adjacent internal chars), Drop (remove an internal
char), Keyboard (replace by adjacent QWERTY key), Add (insert an internal char). "All" mixes
them (a random type per word in WER evaluation, §4.1; the worst case over all types in
classifier attacks).
- Attack strength: **1-character** and **2-character** attacks per sentence (one or two edited
words). 1-char: try every allowed perturbation until the prediction flips; 2-char: greedily fix the
least-confident 1-char edit then search the remaining words; complexity O(l) instead of O(l^m)
(footnote 3). The authors note the greedy search makes the robustness score an upper bound
on true robustness.
- Robustness metric (Eq. 2): R_{C,A} = E_s[ min_{s'∈A(s)} 1[C(s') = y] ], i.e. worst-case
accuracy over the allowed perturbation set (so it is a *worst-case* agreement-with-gold
measure, not average-case noise).
- WER evaluation (§4.1): every eligible word in each test review is attacked.

**4. Method** (§3.1; Fig. 1)
1. Train ScRNN word recogniser W: each word is represented by one-hot first char + one-hot
last char + bag-of-chars of the internal characters (order-agnostic); a BiLSTM predicts the
correct word at each step (cross-entropy over the vocabulary), using inputs synthetically
corrupted by one of the four attack types per word. Training on movie-review text of the task
(foreground model, vocabulary capped at 10K) and, for backoff, a background model trained on
IMDB (vocabulary 78,470 words, §4.1).
2. At test time classify C(W(s)). W and C are trained separately (W needs no task labels).
3. Backoff when the ScRNN predicts UNK (§3.1): *pass-through* (keep the possibly misspelled
word), *neutral* (replace by a neutral word such as "a"), *background* (use the large-vocabulary
background recogniser).
4. Baselines (§4.2): After The Deadline (ATD) spell checker; data augmentation (DA: fine-tune
the trained classifier with an equal number of randomly 1-char-attacked training examples);
adversarial training (Adv: iteratively add adversarial examples that fool the current classifier until
dev adversarial accuracy stops improving).
- Sensitivity (Eq. 1): S_{W,V}^A = E_s[ #u(V∘W(s'_1), …, V∘W(s'_n)) / n ], the expected number
of *unique downstream inputs* the attacker can induce per perturbation.
- Compute: inference adds one small BiLSTM pass per sentence; training the recogniser needs
only unlabeled text; no overhead for the BERT classifier itself. Wall-clock numbers: not reported.

**5. Experimental setup** (§4)
- Word recognition: SST (8,544 reviews, vocabulary > 16K); background IMDB (54K reviews,
78K vocabulary). ScRNN: single-layer BiLSTM, hidden dim 50, input dim 198 (= 3 × 66
characters). Learning rate, epochs, optimizer, seed: **not specified**.
- Classifiers: BERT fine-tuned on binary sentence-level SST (word-piece), BiLSTM word-only,
char-only, word+char models (embedding dims 64/32/64+32, hidden 64/64/128; footnote 6) and
BERT on MRPC (200 dev examples, Table 4). BERT fine-tuning hyper-parameters: official
Google BERT code, details **not specified**; BERT version (base vs large): **not specified** in
the text I read.
- Seeds / error bars: **none reported**.

**6. Results**
Word error rate (Table 2, "all"): ATD 11.2, vanilla ScRNN pass-through 10.2 / neutral 10.6 /
background 6.9 (78K-vocabulary ScRNN alone 8.7). The 32% relative reduction in the abstract
is background (6.9) vs pass-through (10.2).

Sentiment, BERT word-piece, accuracy (1-char / 2-char attack; Table 3, no-attack accuracy
first):

| Model | No attack | Swap | Drop | Add | Key | All |
|---|---|---|---|---|---|---|
| BERT | 90.3 | 64.1 / 47.4 | 59.2 / 39.9 | 46.2 / 26.4 | 54.3 / 34.9 | 45.8 / 24.6 |
| BERT + DA | 90.2 | 68.3 / 50.6 | 62.7 / 39.9 | 43.6 / 17.0 | 57.7 / 32.4 | 41.0 / 15.8 |
| BERT + Adv | 89.6 | 69.2 / 52.9 | 63.6 / 40.5 | 50.0 / 22.0 | 60.1 / 36.6 | 47.0 / 20.2 |
| BERT + ATD | 89.0 | 84.5 / 84.5 | 73.0 / 64.0 | 77.0 / 69.5 | 80.0 / 75.0 | 67.0 / 55.0 |
| BERT + pass-through | 89.8 | 85.5 / 83.9 | 78.9 / 75.0 | 70.4 / 64.4 | 75.3 / 70.3 | 68.0 / 58.5 |
| BERT + background | 89.3 | 89.1 / 89.1 | 79.3 / 76.5 | 76.5 / 71.0 | 77.5 / 74.4 | 73.0 / 67.5 |
| BERT + neutral | 88.3 | 88.3 / 88.3 | 81.1 / 79.5 | 78.0 / 74.0 | 78.8 / 76.8 | 75.0 / 68.0 |
- MRPC (Table 4, BERT, "all" attack, 200 dev examples): clean 89.0; 1-char 60.0; 2-char 31.0;
with ATD 75.8 / 61.6; pass-through 84.5 / 81.5; neutral 82.5 / 82.5 (clean 84.0).
- Other models (Table 3): attack on "All" setting drops BiLSTM word-level 79.2 → 58.6 (1-char),
char-only 70.3 → 32.6, word+char 80.5 → 56.6. Robustness order word-only > word+char >
char-only ≈ word-piece; attack strength Add > Key > Drop > Swap (§4.2).
- Sensitivity (Table 5): neutral backoff has the lowest sensitivity (e.g. "All": 11.3 closed-vocab;
11.3 open-vocab neutral vs 30.3 for pass-through; background 14.7).
- **Clean → worst-case-perturbed gap for undefended BERT: 44.5 points for one adversarially
chosen edit (90.3 → 45.8).** Defences recover the "All" 1-char accuracy to 67.0–75.0 at a
clean-accuracy cost of 0.5–2.0 points (89.8 … 88.3 vs 90.3). DA is *worse* than no defence
under Add/All attacks (Table 3).
- Not reported: average-case (random-typo) degradation, calibration, prediction agreement
between clean and perturbed inputs, results on tagging/QA.

**7. Reproduction notes**
1. Fine-tune BERT on SST-2 (sentence-level). 2. Implement the four edits with the constraints
(internal chars, length ≥ 4, no stopwords) and the exhaustive 1-char / greedy 2-char attack;
compute worst-case accuracy. 3. Train ScRNN on the corrupted in-domain corpus and a
background model on a larger corpus; add backoff; evaluate C∘W.
- Missing: ScRNN training hyper-parameters, BERT size/hyper-parameters, stopword list, how
many test sentences were used for SST (full test set assumed, not stated), tokenizer details for
word-piece.
- Pitfalls: the defence assumes the *same* attack family at training (random corruption) and test
time; word-piece BERT sees whatever W returns, so W's UNK fallback must be set per task; the
paper's English-specific "internal characters" trick (first/last letter fixed) may not hold for
morphologically rich or non-Latin scripts — relevant for Hebrew.

**8. Limitations and caveats**
- Worst-case (adversarially chosen) edits, not natural typo rates; English sentiment/paraphrase
only; the tested BERT configuration is not fully specified.
- No random seeds or confidence intervals; MRPC results use only 200 dev examples.
- The pipeline defence changes the input at inference time, so it is a pre-processing defence,
not a robustly-trained encoder; it is language-specific (needs a trained word recogniser).

---

---

## 14. Cohen et al. — SDBN (additional: adversarial training for PEFT in low-resource, noisy
text)

**1. Citation and links**
- Cohen, E., Simai, I., Shaham, U. (2026). *Small Data, Big Noise: Adversarial Training for
Robust Parameter-Efficient Fine-Tuning.* Findings of ACL 2026 (arXiv 2606.10610v1, 9 Jun
2026).
- PDF: `Cohen2026_SDBN.pdf`. arXiv: https://arxiv.org/abs/2606.10610 . Code (footnote 1):
https://github.com/shaham-lab/SDBN (not inspected).
- Status: **full text read** (pdftotext layout used to resolve Tables 1–13). Sections §1–§7
(Methodology = §4.1–4.5) plus Appendices A–D (Algorithms 1–5, §C.1–C.7, §D.1–D.7).

**2. Problem and claim**
Standard PEFT (Adapter, BitFit, LoRA) degrades sharply on noisy text in low-resource regimes:
under word-swapping noise all three drop, "in some cases losing more than 50%" below 1,000
clean Banking77 samples (Fig. 1, §1). Claim: embedding-space **adversarial training is the
robust-optimization layer that PEFT lacks**; SDBN improves accuracy both on clean and on
perturbed inputs, with gains growing as training data shrinks, and it does so "without adding
trainable parameters or extra GPU memory" (§1, abstract). Two variants: **SDBN-h** (discrete
single-character edits selected by gradients, for tokenization-breaking noise) and **SDBN-p**
(LLM-generated semantic variants, for generative tasks) (§1, §4).

**3. Perturbations used**
Training-time uncertainty sets (§4.3–4.5):
- **SDBN**: continuous, embedding-layer FGSM in an ℓ∞ ball, δ = ε·sign(g) (Algorithm 1).
Default **ε = 10⁻⁴**, chosen as best in the norm/ε study (Table 4, §C.7). ℓ1/ℓ2 alternatives in
Algorithms 4–5 (§C.4–C.5).
- **SDBN-h** discrete set: all single-character variants; operations are *delete character, swap
adjacent characters, insert character, double character, Cyrillic substitution, random
capitalization, phonetic replacement* (§C.2 char-type lists); one perturbation type is randomly
selected per input and all single-edit variants under it form S(x) (§C.1).
- **SDBN-p**: k LLM-generated semantic-preserving variants (paraphrases, typos, style) from
GPT-5.2 (§4.5, §C.3); k = 5 for SQuAD, k = 10 for TweetQA (§D.4).
Test-time evaluation noise (Table 6): Slang, Case, Pronoun, Replace-Word, Delete-Word,
Swap-Words, Homophone, Cyrillic, Keyboard-char. Table 1 adds Delete-char, Swap-char,
Double-char; Table 2 uses Swap-Word/Homophone (SQuAD) and Delete-Char/Delete-Word
(TweetQA). Intensity: **variable noise = 1–5 operations per sentence** (Fig. 4); **constant noise
= exactly one operation per sentence** (Appendix D.2, Fig. 7). Evaluation uses the
**TextAttack** library (§D.7); per-type corruption rates are not specified beyond
operations-per-sentence.

**4. Method** (Algorithm 1)
1. e = E(X); Lclean = L(fθ(e), Y); g = ∇e Lclean; δ = ε·sign(g); eadv = e+δ; Ladv = L(fθ(eadv),
Y); update θ (only the PEFT parameters) on Ladv (§4.3).
2. **Adaptive ε** (§C.1): if Ladv falls below Lclean, a line-search reduces ε by a factor of 10 for
up to K iterations until Ladv > Lclean; in practice one iteration suffices with the right ε (§C.1).
3. **Perturbation location**: noise is injected at the **embedding layer only**; encoder-layer
injections collapse accuracy (Table 5). The perturbation is selected from any norm ball; ℓ∞ wins
(§4.3, §C.6).
4. **SDBN-h** (Algorithm 2): each mini-batch is split — one subset gets standard ℓ∞ FGSM, the
rest gets z* = argmax_{z∈C(x)} ⟨g, E(z) − E(x)⟩ (gradient used for *selection*, not creation);
update on L(f(E(z*);θ), y) (§4.4).
5. **SDBN-p** (Algorithm 3): precompute k variants P(x) offline; z* = argmax_{zi∈P(x)}
L(f(E(zi);θ), y); update on Lp (§4.5).
- No additional trainable parameters; adversarial embeddings need one extra forward–backward
pass per mini-batch (§7).

**5. Experimental setup** (§5, §D.7)
- Backbones: **BERT-base** (default for all experiments, §D.7), **DeBERTa-v3**,
**DeBERTa-v3-large** (NLI, Fig. 15), **LLaMA-3.2-1B**, **LLaMA-2-7B**, **Qwen-2.5-7B**
(generative), multilingual BERT-base (Arabic). Parameter counts beyond these names: not
specified.
- Datasets: Banking77, TREC, 20Newsgroups, IMDB, **BLESS** (classification); **SQuAD**,
**TweetQA** (generative); ArSarcasm-v2 (domain shift); NLI cross-genre (§5, §D.2–D.3).
- PEFT methods: **Adapter, BitFit, LoRA, QLoRA** (§5).
- Protocol: **3 warm-up epochs** of standard training then **10–20 epochs** of SDBN or
baseline without perturbations (§5). Generative: SQuAD = 1 warm-up + 10 adversarial epochs,
5 fixed variants; TweetQA = 5 warm-up + 16 adversarial epochs, 10 variants regenerated each
epoch (§D.4).
- Hyper-parameters (§D.7): AdamW, **learning rate 1×10⁻⁴** applied to trainable parameters
only; **LoRA rank 12 (BERT) / 4 (DeBERTa)**; adapter bottleneck 16; **batch size 32**; dropout
0.1.
- Seeds: **5 random seeds** per (dataset–method–size) setting (§D.7, §D.1); §D.2 uses **10
seeds without outliers** (best/worst dropped); NLI uses **20 seeds** (Fig. 15).
- Data scarcity: **5%–100%** of training data; noisy evaluation on a 1,000-sample Banking77
subset with DeBERTa-v3 (§5).
- Baselines: vanilla PEFT, **NEFTune**, **EDA** (αsr=αri=αrs=prd=0.05, num_aug=1,
augmented variant replaces the clean input with probability 0.5, generated once, §D.7);
**FreeLB** and **SMART** appear in the generative tables (Tables 2, 9, 10).

**6. Results**
BLESS, DeBERTa-v3 + LoRA, 1,000 clean samples, accuracy % (Table 1; my
clean-vs-perturbed table):
| Method | Clean | Delete-char | Swap-char | Double-char |
|---|---|---|---|---|
| Vanilla | 89.81 ± 0.29 | 60.67 ± 2.19 | 56.82 ± 2.38 | 68.51 ± 2.75 |
| SDBN | 89.83 ± 0.24 | 60.84 ± 1.85 | 57.22 ± 2.84 | 68.66 ± 2.27 |
| NEFTune | 89.08 ± 0.54 | 61.19 ± 0.89 | 57.22 ± 0.82 | 69.42 ± 1.29 |
| SDBN-h | 89.61 ± 0.30 | **65.14 ± 1.19** | **62.80 ± 1.47** | **72.54 ± 1.05** |
- SDBN-h beats vanilla by +4.47 pp (delete-char) and +5.98 pp (swap-char) (derived) at no
clean-accuracy cost (89.61 vs 89.81), matching the paper's "+4–7%" claim (Table 1, §5);
clean→delete-char drop is −29.14 pp for vanilla and −24.47 pp for SDBN-h (derived).
- Clean data, all PEFT: SDBN improves accuracy at every scale (Table 7), e.g. Banking77 LoRA
91.56±0.18 → 91.77±0.51 (100%), 66.42±1.97 → 72.86±1.24 (10%), 36.29±3.89 → 43.30±2.57
(5%); TREC LoRA 56.04±5.03 → 61.76±1.64 (5%) (Table 7).
- PEFT vs full fine-tuning (Table 3, absolute gains from adding SDBN, Banking77/DeBERTa-v3):
LoRA +23.6 (clean)/+19.6 avg; BitFit +16.0/+12.8; Adapter +13.3/+9.7; **Full FT +1.3/+0.9** —
PEFT gains dwarf full-FT gains.
- Generative (Table 2): SQuAD EM, LLaMA-3.2-1B + LoRA, 200 samples — Vanilla 58.92 /
32.44 (Swap-Word) / 47.28 (Homophone) vs SDBN-p 59.84 / 35.08 / 52.20. TweetQA F1,
LLaMA-2-7B, 200 samples — Vanilla 68.09 / 51.56 (Delete-Char) / 56.06 (Delete-Word) vs
SDBN-p **80.81 / 65.55 / 64.15**.
- ε/norm study (Table 4b, Banking77 1,000 samples): ℓ∞ at ε=10⁻⁴ gives 72.86±1.24, above ℓ∞
10⁻³/10⁻⁵ and all ℓ1/ℓ2 cells.
- Injection point (Table 5, BERT-base + LoRA, 1,000 Banking77): embeddings 57.64±5.04 vs
encoder layers 6.17–6.71±(1.73–2.18).
- Compute overhead (Table 11, NVIDIA H200, batch 32): SDBN ≈ **1.27–1.40×** vanilla
per-batch latency (LoRA 116.21→163.05 ms); SDBN-h adds 5–15% over SDBN; SDBN-p adds
30–39% over SDBN. Peak memory ≤0.15% increase (Table 12, ~68.6 GiB).
- Not reported: calibration/ECE, clean-vs-perturbed label agreement, average-case (natural
typo-rate) degradation.

**7. Reproduction notes**
1. Attach LoRA/Adapter/BitFit to BERT-base or DeBERTa-v3; run 3 warm-up epochs, then
replace the loss with embedding-layer FGSM (ε=10⁻⁴, ℓ∞) for 10–20 epochs (§4.3, §5, §D.7). 2.
Optionally add SDBN-h (split batch, gradient-selected single-char variant) and SDBN-p
(precompute LLM variants, explicit max-loss selection). 3. Evaluate with TextAttack on the Table
6 noise catalogue at 1–5 ops/sentence and 1 op/sentence (Table 6, Fig. 4, D.2).
- Missing / **not specified**: the constant K in the ε line-search (§C.1); the TextAttack attack
configuration and per-type corruption rates; the exact epoch count (only the 10–20 range) for
classification. Warm-up count for classification is 3 (§5); generative schedules are given (§D.4).
- Pitfalls: ε is "sensitive across datasets" (§7) — retune per dataset; embedding-layer injection
only (Table 5); character-level noise needs SDBN-h because case edits stay in-region but
token-breaking edits do not (§4.4, §D.1); SDBN-p needs a GPT-5.2 variant set and more
epochs on generative tasks.

**8. Limitations and caveats**
Stated in §7: the extra forward–backward pass raises per-batch runtime (potential bottleneck at
very large scale) even though GPU memory is unchanged; **ε selection is sensitive across
datasets** and more adaptive/automated tuning is left for future work. My reading: robustness
claims rest on a fixed small-ε ℓ∞ perturbation plus curated noise types, not on a worst-case
attack search; the defence is training-time and unchanged at inference. Not reported:
confidence intervals beyond reported ±std, calibration/ECE, or agreement metrics; several
headline numbers (Figs. 3, 4, 7–15) are figure-only and could not be read as values.

---

## 15. Provilkov et al. — BPE-Dropout (additional: subword/tokenization robustness)

**1. Citation and links**
- Provilkov, I., Emelianenko, D., Voita, E. (2020). *BPE-Dropout: Simple and Effective Subword
Regularization.* ACL 2020 (arXiv 1910.13267v2, 1 May 2020).
- PDF: `Provilkov2020_BPEDropout.pdf`. arXiv: https://arxiv.org/abs/1910.13267 .
- Code: **not specified**; the only repository link is the Moses toolkit (footnote 3:
https://github.com/moses-smt/mosesdecoder; SacreBLEU is footnote 5).
- Status: full cleaned text read. Sections: §1 Intro; §2 Background (BPE, subword
regularization); §3 approach (Algorithm 1); §4 setup (4.1–4.7); §5 experiments (5.1–5.5); §6
analysis (6.1–6.3, incl. 6.3 robustness to misspelled input); §7 related work; §8 conclusions.

**2. Problem and claim**
Standard BPE (Sennrich et al., 2016) is deterministic: each word gets one unique segmentation
(§1, §2.1), so a model sees only one decomposition per word and is not robust to segmentation
errors. Kudo (2018) realised subword regularization only by introducing a *separate*
unigram-LM segmentation needing EM/Viterbi training and forbidding conventional BPE (§2.2).
Claim (§1, §3): BPE itself can produce multiple segmentations, so randomly dropping merges
during the merge procedure (BPE-dropout) yields a simple subword regularization inside
standard BPE. With p = 1 a word splits into characters; p = 0 equals standard BPE (§3).
Training uses p > 0 (usually 0.1); inference uses p = 0, i.e. the original BPE (§3, §6).

**3. Perturbations used** (two distinct ones, kept separate)
- **Training-time (the method itself, §3, Algorithm 1):** during segmentation, at each merge step
*every* possible merge is removed with probability p, then the highest-priority remaining merge
is applied. Repeated occurrences of a merge in a word are dropped independently (footnote 1).
Values used: p = 0.1 for all languages except Chinese and Japanese, where p = 0.6 (§5.3, Table
1).
- **Test-time (robustness evaluation only, §6.3):** the source side of a test set is augmented by
modifying each word with probability **10%**, applying one of (1) removal of one character, (2)
insertion of a random character, (3) substitution of a character by a random one, so perturbed
words are at edit distance 1 (§6.3). This is random natural-noise corruption of the source only,
not adversarial; only one strength (10%) is reported.

**4. Method**
1. Build the normal BPE vocabulary and merge table (§2.1). Of two vocab options, the one
keeping the BPE vocabulary (accepting a few UNKs — 0.00585 / 0.00085 of tokens for
IWSLT15 En-Vi at 32k / 4k) is chosen (§4.2, footnote 2).
2. Segment the training text with BPE-dropout (Algorithm 1, §3) using p > 0, then train the NMT
model.
3. At inference use standard BPE (p = 0); the only difference from BPE is how words are
segmented during training (§3, §6, §8).
- Baselines: standard BPE and Kudo (2018) subword regularization with l = 64, α = 0.1 (§4.1).
- Compute (§5.5, Table 4): relative inference time — 32k vocab: BPE 1.0, BPE-dropout 1.03; 4k
vocab: BPE 1.44, BPE-dropout 1.46 (Table 4; 1000 runs on WMT14 En-Fr, normalised by the
fastest). Segmented input is ~1.25× longer with p = 0.1 (§5.5, footnote 6), but generated
translations stay close to BPE (§5.5, Fig. 4b) because beam search favours frequent tokens
(footnote 8). Wall-clock seconds and training-time overhead: **not specified** (§4.5 gives only
training-batch counts, appendix Tables 6–7).

**5. Experimental setup**
Datasets (Table 1), given as train/dev/test sentences, vocab size, batch size, p (source/target):
IWSLT15 En↔Vi (133k/1553/1268; 4k; 4k; 0.1/0.1); IWSLT15 En↔Zh (209k/887/1261; 4k/16k;
4k; 0.1/0.6); IWSLT17 En↔Fr (232k/890/1210; 4k; 4k; 0.1/0.1); IWSLT17 En↔Ar
(231k/888/1205; 4k; 4k; 0.1/0.1); WMT14 En↔De (4.5M/3000/3003; 32k; 32k; 0.1/0.1); ASPEC
En↔Ja (2M/1700/1812; 16k; 32k; 0.1/0.6). Additional experiments use random WMT14 En-Fr
subsets — 250k, 500k, 1m, 4m, 16m sentence pairs (Table 3, Figs. 2–3). Preprocessing: Moses
tokenizer (footnote 3); Chinese and Japanese are trained almost from unsegmented raw
sentences (§4.3). Main-text models use lowercased data (§4.3).
Model (§4.4): Transformer base — N = 6 layers, h = 8 heads, d_model = 512, d_ff = 2048;
regularization and optimization as in Vaswani et al. (2017). Inference: beam search, beam = 4,
length normalization 0.6 (§4.6). Evaluation: average of the last 5 checkpoints, SacreBLEU
BLEU; `--tok zh` for Chinese and character-based BLEU for Japanese (§4.7, footnote 5). Seeds,
error bars, and explicit learning-rate/warmup/dropout values: **not specified** ("as described in
Vaswani et al. (2017)", §4.4).

**6. Results**
Main results (§5.1, Table 2, 12 datasets): BPE-dropout beats standard BPE by >1.5 BLEU for
En-Vi, Vi-En, En-Zh, Zh-En, Ar-En, De-En and 0.5–1.4 BLEU for the rest; versus Kudo (2018) it
is better on 8 datasets (up to 0.92 BLEU), not significantly different on 3, and worse only on
En-Ja. The abstract reports up to +2.3 BLEU over BPE and +0.9 over Kudo (2018). Best p is
0.1; high p (training near char-level, inferring with BPE) makes models "unable to translate"
(§5.3, Fig. 2). Embedding quality: character 4-gram precision of top-10 neighbours is 0.29
(BPE-dropout) vs 0.18 (BPE) (§6.2). Robustness to misspelled source (§6.3, Table 5) — most
relevant here:

| Dataset (§6.3, Table 5) | BPE clean | BPE misspelled | BPE-dropout clean | BPE-dropout
misspelled | Δ clean | Δ misspelled |
|---|---|---|---|---|---|---|
| En-De | 27.41 | 24.45 | 28.01 | 26.03 | +0.60 | +1.58 |
| De-En | 32.69 | 29.71 | 34.19 | 32.03 | +1.50 | +2.32 |
| En-Fr (4m) | 33.38 | 30.30 | 33.85 | 32.13 | +0.47 | +1.83 |
| En-Fr (16m) | 34.37 | 31.23 | 34.82 | 32.94 | +0.45 | +1.71 |

- Degradation under misspellings (derived) (clean − misspelled BLEU): BPE 2.96 / 2.98 / 3.08 /
3.14 (En-De / De-En / En-Fr 4m / En-Fr 16m); BPE-dropout 1.98 / 2.16 / 1.72 / 1.88 — roughly
halved, at a clean-data cost of only 0.45–1.5 BLEU (§6.3). For En-Fr 16m, BPE-dropout was
used on the source side only (§5.2, Table 5 caption).
- Not reported: accuracy/agreement/calibration metrics, degradation-vs-strength curves,
worst-case attacks, or any non-MT task.

**7. Reproduction notes**
1. Train BPE; keep its merge table and vocabulary (§2.1, §4.2). 2. Change only the training
segmentation: at each step drop each candidate merge with probability p and apply the
highest-priority survivor (Algorithm 1); p = 0.1 (0.6 for zh/ja) (§3, §5.3). 3. Train Transformer
base and infer with p = 0 (§4.4, §4.6). 4. Build the misspelled test set: per source word, 10%
chance of one of delete / insert / substitute a character; report BLEU on clean vs misspelled
source (§6.3).
- Missing: how p was tuned (only "best quality is achieved with p = 0.1", §5.3); learning rate,
warmup, dropout, label smoothing; training length (appendix Tables 6–7 not in the text I read);
seeds; code. Appendix items are **not specified** in the cleaned text.

**8. Limitations and caveats**
- As stated by the paper: BPE-dropout underperforms on En-Ja and is marginal on Ja-En,
En-Zh, Zh-En, so Chinese/Japanese may need language-specific segmentation (§5.1); for large
corpora it should be used on the source side only, since using it on both sides hurts (§5.2.2); its
clean-data benefit shrinks as corpus size grows (§5.4).
- Not stated / not tested: no comparison to WordPiece or BERT; robustness is MT BLEU under
one 10% synthetic word-typo setting, not classification accuracy; no agreement, calibration, or
worst-case adversarial results; only three edit types, source side only; no tagging/QA/parsing;
no seed variance or confidence intervals.
- **my analysis (transfer to a WordPiece BERT encoder):** BPE-dropout is a *training-time
input-segmentation augmentation with standard-BPE inference*, and the paper states the
methods are "not task-specific" (§2), so the *principle* — stochastically re-segmenting training
text so the encoder sees alternative subword decompositions — is architecturally neutral and
could apply to a WordPiece BERT pretraining/finetuning pipeline. However, Algorithm 1 relies on
a BPE merge table with an explicit merge *priority* and independently droppable merge
occurrences (§3, footnote 1); WordPiece selects the longest matching subword greedily, so the
drop rule does not transfer verbatim. The paper never experiments with WordPiece, BERT-style
encoders, classification, or masked-LM objectives, so a clean-vs-misspelled BERT
accuracy/agreement/calibration gain is **not evidenced here** — only a seq2seq BLEU gain
under source-side typos. **my inference:** the roughly halved misspelling degradation of §6.3
(derived above) is suggestive but must be re-established for a BERT encoder; the paper says
nothing about prediction agreement between clean and perturbed inputs, a property separate
from raw BLEU.
---

## 16. Morris et al. — TextAttack (additional: robustness toolkit)

**1. Citation and links**
- Morris, J. X., Lifland, E., Yoo, J. Y., Grigsby, J., Jin, D., Qi, Y. (2020). *TextAttack: A Framework
for Adversarial Attacks, Data Augmentation, and Adversarial Training in NLP.* EMNLP 2020
System Demonstrations (arXiv 2005.05909v4, 5 Oct 2020).
- PDF: `Morris2020_TextAttack.pdf`. arXiv: https://arxiv.org/abs/2005.05909 . Code and tutorials
(abstract): https://github.com/QData/TextAttack (not inspected).
- Status: **VERIFIED** (full text read). Sections: §1 Intro, §2 Framework, §3 Developing NLP
Attacks, §4 Utilizing TextAttack, §5 Under the Hood, §6 Related Work, §7 Conclusion;
Appendices A.1–A.4 (examples, component reference, reproduction results, attack prototypes).
This is a **system/demo paper**: its artefact is the framework and its component taxonomy; the
only experiments are the augmentation curve (Figure 4) and the adversarial-training table (Table
2).

**2. Problem and claim**
Each NLP attack is implemented in its own repository and evaluated on different samples and
victim models, so attacks "cannot be compared directly and fairly" and reimplementing baselines
is error-prone (§1). TextAttack unifies NLP attacks into one Python framework decomposed into
four components — **a goal function, a set of constraints, a transformation, and a search
method** (§1, §2, abstract). It ships implementations of **16** adversarial attacks (abstract,
§3.1, Table 1), **82** pre-trained models (LSTM, CNN, BERT and other transformers, §3.3) and
supports all **nine** GLUE tasks plus summarization and machine translation (§1, §3.3). The
same components are reused for **data augmentation** and **adversarial training** (§1, §4.3,
§4.4), and HuggingFace `transformers`/`nlp` integration lets common tasks run in fewer than
five lines of code (§1 footnote 1, A.1).

**3. Perturbations used**
Transformations (§2, A.2.3) are white-box (uses the model, e.g. HotFlip gradient swap, Ebrahimi
et al. 2017) or black-box. Built-ins: counter-fitted embedding nearest-neighbour swap (Mrkšić et
al. 2016), WordNet synonym swap, masked-LM word swap (BAE, BERT-Attack), gradient-based
word swap, the DeepWordBug character set (deletion, neighbouring-character swap,
random-character insertion/substitution, homoglyph, QWERTY keyboard-neighbour substitution
from Pruthi et al. 2019), word deletion, HowNet POS+sememe swap, and a composite.

Goal functions (§2, A.2.1): untargeted/targeted classification, input reduction, non-overlapping
output, minimum BLEU. Constraints (§2, A.2.2) in four classes: pre-transformation (stopword,
repeat, min word length, max word index, input-column); overlap (max BLEU/chrF/METEOR
difference, max Levenshtein distance, max % words changed); grammaticality (LanguageTool
error cap; POS consistency via flair/SpaCy/NLTK; LM filtering with Google 1-billion-word,
Learning-To-Write, GPT-2); semantics (max embedding distance / min cosine; min
sentence-encoding cosine with Skip-Thought, USE, InferSent, BERT; min BERTScore). Search
methods (§2, A.2.4): Greedy-WIR, beam search ("beam width"), greedy (width 1), genetic
algorithm (Alzantot et al. 2018; Improved GA of Wang et al. 2019), particle-swarm optimisation.

Attack recipes (§3.1, Table 1; prototypes A.4); **all add a stopword-non-replacement
constraint** (Table 1 caption). Stated parameters: **textfooler** — Greedy-WIR, embedding
swap (max candidates 50), min cos sim 0.5, POS, USE angular **0.840845057** (window 15);
**bae** — masked-LM `bert-base-uncased` swap, USE cosine **0.936338023**; **bert-attack**
— max % perturbed **0.4**, USE cosine **0.2**; **alzantot** (faster) — GA pop size **60**,
max iters **20**, temp **0.3**, embedding max MSE **0.5**; **hotflip** — beam width **10**,
max num words **2**, min cos sim **0.8** (white-box); **deepwordbug** — four char
transforms, Levenshtein max **30**; **pruthi** — char transforms incl. QWERTY, max num
words **1**; **textbugger** — char + homoglyph + embedding (max candidates 5), USE angular
**0.8**; **kuleshov** — max % **0.5**, GPT-2 max log-prob diff **2.0**; plus pwws, pso,
seq2sick, morpheus, input-reduction.

**4. Method**
An attack is a combinatorial search for a perturbation satisfying the goal function and all
constraints (§2). Inputs are stored as `AttackedText` objects keeping the original text and
tokenisation, so capitalisation/punctuation survive swaps (§5). Model outputs and constraint
outcomes are cached, speeding up Alzantot's GA by a factor of **5** (§5 footnote 2). *Data
augmentation* (§4.3): the `Augmenter` reuses a transformation plus constraints to make new
samples; `textattack augment` offers standalone recipes; `textattack train --augment` expands
the dataset before training, with user-controlled fraction modified and number of extra versions.
*Adversarial training* (§4.4): `textattack train --attack` trains on the clean set, generates an
adversarial version of each input with a recipe, substitutes it, and periodically regenerates it per
the model's current weaknesses; the model becomes "significantly more robust against the
attack used during training."

**5. Experimental setup**
- Table 2: the default LSTM trained on **3k** sst2 samples; baseline uses early stopping on a
clean set; adversarial training with **deepwordbug** (20 and 75 epochs) and **textfooler** (20
epochs); accuracy under attack reported for deepwordbug, textfooler, pruthi, hotflip and bae.
Table 3 lists example commands.
- Figure 4: built-in **WordCNN** on **rotten tomatoes**, training sets **10²–10⁴** samples,
**95%** confidence intervals over **N = 5** runs.
- Table 4 (attack reproduction): **1000** samples per dataset except IMDB (**100**), since
Genetic/PSO take over **4 days** for 1000 (Table 4 caption); reported vs TextAttack success
rate / % perturbed words for alzantot, bae, deepwordbug, pso, textfooler.
- Seeds, optimiser and random seeds for the LSTM/CNN: not specified in the text read.

**6. Results**
Table 2 (default LSTM on 3k sst2 samples; "accuracy under attack", %). The extraction gives six
percentages per row for five named attack columns; **my inference** is the first column is clean
accuracy, the rest attacks in header order.
| Trained against | clean | deepwordbug | textfooler | pruthi | hotflip | bae |
|---|---|---|---|---|---|---|
| baseline (early stopping) | 77.30 | 23.46 | 2.23 | 59.01 | 64.57 | 25.51 |
| deepwordbug (20 epochs) | 76.38 | 35.07 | 4.78 | 57.08 | 65.06 | 27.63 |
| deepwordbug (75 epochs) | 73.16 | 44.74 | 13.42 | 58.28 | 66.87 | 32.77 |
| textfooler (20 epochs) | 61.85 | 40.09 | 29.63 | 52.60 | 55.75 | 39.36 |

**My reading**: adversarial training raises robustness against the trained attack (deepwordbug
23.46 → 44.74 at 75 epochs) but at a clean-accuracy cost (77.30 → 73.16), and textfooler
training damages clean accuracy most (61.85); since the column mapping is inferred from a
scrambled layout, the cells are provisional. Figure 4: EDA (Wei and Zou 2019) and Embedding
augmentation **immediately improve** WordCNN accuracy on small datasets, "most helpful
when working with very few samples" (§4.3, Figure 4 caption). Table 4 (TextAttack success rates
vs reported numbers) has a pdftotext layout too scrambled to attribute per-cell values.
Systematic differences (§A.3): the GA benchmark uses the faster GA of Jia and Liang (2017)
(**lower** success expected); BAE LSTMs use counter-fitted vs normal GLoVe (**higher**);
PSO uses three concatenated HowNet synonym sets (slightly **more** successful).

**7. Reproduction notes**
1. Install the `textattack` PyPI package or clone https://github.com/QData/TextAttack (abstract,
§3). 2. Reproduce an attack with `textattack attack --model <hf-model> --recipe <recipe>` (A.1,
Table 3); the four-component decomposition and all stated parameters are in A.2/A.4. 3.
Augment with `textattack augment --recipe eda`/`embedding` (§4.3); adversarially train with
`textattack train --attack <recipe> --num-clean-epochs <n>` (§4.4).
- Missing/not specified: random seeds, optimiser and learning-rate schedules for the LSTM/CNN
experiments; the number of eval samples for Table 2; the clean-vs-attack column mapping of
Table 2; a recipe named **CharSwap** is **not mentioned** (only **EDA** and **Embedding**
are named, §4.3, Figure 4). The paper reports no attack on a BERT model *in its own tables*
(BERT appears only as an available pre-trained model, §3.3, and in the Table 4 reproduction
rows).

**8. Limitations and caveats**
- Demo paper: no theorem and no new attack/defence; the contribution is the framework, the
16-recipe taxonomy and the training utilities (§1, §7), demonstrated only by one LSTM on 3k
sst2 samples (Table 2) and a WordCNN augmentation curve on rotten tomatoes (Figure 4) — no
exhaustive BERT robustness benchmark by the authors.
- Reproduction results (Table 4) are not identical to the original papers; the authors name three
systematic sources of divergence (faster GA, embedding type, HowNet synonym union, §A.3),
so "TextAttack" numbers are not interchangeable with published numbers.
- Some attacks are computationally heavy (Genetic/PSO: over 4 days for 1000 samples, Table 4
caption), and some recipes omit parameter values (e.g. MinWordLength, character-insertion
thresholds) — not specified.
- Fidelity caveat for this thesis: the framework makes attacks *runnable and comparable*, but
the paper does not quantify a clean→perturbed gap for any BERT encoder; such numbers must
come from re-running the recipes.

---

## 17. Ribeiro et al. — CheckList (additional: behavioural testing / evaluation)

**1. Citation and links**
- Ribeiro, M. T., Wu, T., Guestrin, C., Singh, S. (2020). *Beyond Accuracy: Behavioral Testing of
NLP Models with CheckList.* ACL 2020, pp. 4902–4912 (arXiv 2005.04118).
- Code (footnote 1; §2.3): https://github.com/marcotcr/checklist . All tests shown are part of the
open-source release and reusable on new models (§3). Not inspected.
- Status: full cleaned text read (references removed); plain-text extraction left Table 1 partly
column-scrambled (see §6). Sections §1–§6; results in Tables 1–4 and Figure 1.

**2. Problem and claim**
Held-out accuracy "often overestimates the performance of NLP models" and hides *where* a
model fails (abstract, §1); prior alternatives target single tasks or capabilities (§1, §5). CheckList
is a task-agnostic behavioural-testing methodology: a matrix of linguistic capabilities (rows) ×
test types (columns), plus a tool for generating many cases (§2; Figure 1). On three tasks it
finds "critical failures in both commercial and state-of-art models"; practitioners with CheckList
"created twice as many tests, and found almost three times as many bugs" as those without
(abstract, §4).

**3. Perturbations used**
Three test types (§2.2); only INV/DIR are perturbation-based:
- **MFT (Minimum Functionality test)**: "a collection of simple examples (and labels) to check a
behavior", like small focused test datasets; detects shortcuts (§2.2; Figure 1A).
- **INV (Invariance test)**: *label-preserving* perturbations where the prediction should stay the
same; "different perturbation functions are needed for different capabilities", e.g. location names
(NER) or typos. Run on unlabeled data (§2.2; Figure 1B).
- **DIR (Directional Expectation test)**: label expected to change in a known direction —
monotonicity or a target label (§2.2; Figure 1C).

Operations (INV/DIR) in §2.3, Tables 1–2: replace neutral words with other neutral words; add
random URLs/handles; swap one character with its neighbour (typo); switch locations; switch
person names; swap adjacent chars in the question (MC typo); add an irrelevant context
sentence; replace words with synonyms (QQP); change the same name in both questions;
symmetry pred(a,b)=pred(b,a); add positive/negative phrases (sentiment DIR). The release also
has "char swaps, contractions, name and location changes" (§2.3). Values come from
templates, a masked-LM (**RoBERTa**, Liu et al. 2019, §2.3/Figure 2), WordNet categories,
and lexicons (verbs/nouns; names, cities, countries; protected-group adjectives) (§2.3).
**Failure-rate definition.** For INV, "models fail whenever their prediction changes and the
probability changes by more than 0.1" (footnote 4). DIR e.g. adding positive phrases "fails if
sent. goes down by > 0.1" (Table 1). Failure rate = share of cases violating the expectation.
Sentiment scores in the [1/3, 2/3] positive-probability range count as neutral (footnote 2).

**4. Method**
1. Treat the model as a black box ("decoupling testing from implementation", §2).
2. Pick capabilities from §2.1: Vocabulary+POS, Taxonomy, Robustness, NER, Fairness,
Temporal, Negation, Coreference, SRL, Logic ("not exhaustive, but a starting point").
3. For each, build MFT and/or INV/DIR cells (§2.2).
4. Generate cases via templates + Cartesian-product lexicons (Figure 1A template "I
{NEGATION} {POS_VERB} the {THING}."), MLM suggestions, and §2.3 perturbations.
5. Compute failure rate per test; save/share reusable suites (§2.3). Compute cost, wall-clock,
seeds: **not specified**.

**5. Experimental setup** (§3)
- Commercial sentiment APIs (11/2019; similar 04/2020): Microsoft Text Analytics (MS), Google
Cloud NL (Google), Amazon Comprehend (Amazon) (footnote 2).
- **BERT-base** and **RoBERTa-base** finetuned on SST-2 (acc 92.7% / 94.8%) and QQP
(acc 91.1% / 91.3%); **BERT-large** finetuned on SQuAD (93.2 F1) for MC (§3). Fine-tuning
hyperparameters: **not specified**.
- Sentiment INV/DIR on unlabeled airline tweets; QQP on its validation set; MC on SQuAD (§3,
§4.2). Model seeds/error bars: **none reported**; user study gives mean ± SE (Table 4).

**6. Results**
Sentiment failure rate (%), Table 1, columns MS / Google / Amazon / BERT / RoB:

| Test | MS | Google | Amazon | BERT | RoB |
|---|---|---|---|---|---|
| MFT neutral adj/nouns | 0.0 | 7.6 | 4.8 | 94.6 | 81.8 |
| MFT sentiment-laden adj | 4.0 | 15.0 | 2.8 | — | — |
| INV replace neutral words | 9.4 | 16.2 | 12.4 | 10.2 | 10.2 |
| INV add URLs/handles | 9.6 | 13.4 | 24.8 | 11.4 | 7.4 |
| INV typo | 5.6 | 10.2 | 10.4 | 5.2 | 3.8 |
| INV switch locations | 7.0 | 20.8 | 14.8 | 7.6 | 6.4 |
| INV switch person names | 2.4 | 15.1 | 9.1 | 6.6 | 2.4 |
| MFT sentiment over time | 41.0 | 36.6 | 42.2 | 18.8 | 11.0 |
| MFT negated negative | 18.8 | 54.2 | 29.4 | 13.2 | — |
| MFT negated neutral | 40.4 | 39.6 | 74.2 | 98.4 | 95.4 |
| MFT negated positive, middle | 98.4 | 100.0 | 100.0 | 74.0 | 30.2 |
| MFT author vs others | 45.4 | 62.4 | 68.0 | 38.8 | 30.0 |
| MFT (question,"no") | 96.8 | 90.8 | 81.6 | 55.4 | 54.8 |
- DIR (Table 1, §3): adding positive phrases drops sentiment for MS 12.6% / Google 12.4%;
adding negative phrases raises it for Google 34.6%. Negation-at-end fails "near 100%" for all
commercial models (§3). Empty cells = values not stated for those models (my analysis of the
scrambled layout).
- QQP (Table 2), BERT/RoBERTa: modifiers change intent 78.4/78.0; synonyms in templates
22.8/39.2; INV real-pair synonyms 13.1/12.7; more X = less antonym 69.4/100.0; INV typo
18.2/12.0; DIR paraphrase-duplicate 69.0/25.0; INV same name both questions 11.8/9.4; DIR
change name in one 35.1/30.1; "is ≠ used to be" 61.8/96.8; "before ≠ after" 98.0/34.4;
"before/after becoming" 100.0/0.0; negation-of-antonym 18.6/0.0; he≠she coref 81.6/88.6;
symmetry INV 4.4/2.2; DIR transitivity 9.7/8.5.
- MC (Table 3, BERT): comparisons 20.0; intensifiers to superlative 91.3; match properties to
categories 82.4; animal vs vehicles 26.2; comparison to antonym 67.3; more/less antonym
100.0; INV typo 11.6; INV add irrelevant context 9.8; before/after last/first 82.9; context negation
67.5; Q negation 100.0; he/she coref 100.0; his/her coref 100.0; former/latter 100.0;
subject/object distinction 60.8; subj/obj with 3 agents 95.7. Bias template "{P1} is not a {PROF},
{P2} is" (doctor; male P1 / female P2): picks the man 89.1%; reversed 3.2%; with secretary
picks the man 4.0% / woman 60.5% (§3).
- BERT/RoBERTa are "fairly accurate (91.5%, 93.9%)" on the SST-2 validation subset
containing negation (18% of instances) yet fail simple negation MFTs (§3).
- User study (Table 4): #tests 5.8±1.1 / 10.2±1.8 / 13.5±3.4 (Unaided / Cap.only / Cap.+templ.);
#cases/test 7.3±5.6 / 5.0±1.2 / 198.0±96; #capabilities 3.2±0.7 / 7.5±1.9 / 7.8±1.1; total severity
10.8±3.8 / 21.7±5.7 / 23.7±4.2; #bugs (sev≥3) 2.2±1.2 / 5.5±1.7 / 6.2±0.9. 18 participants (8
industry, 10 academia, §4.2); §4.1: 5-h session, ~30 tests brainstormed, ~20 implemented.
- Not reported: calibration, clean-vs-perturbed prediction agreement, average-case noise
degradation.

**7. Reproduction notes**
1. Reuse the released test suites (code link; §3) for the three tasks.
2. For tweet INV/DIR: apply the perturbation functions and compute failure rate under the
"prediction changes AND probability moves > 0.1" rule (footnote 4; Table 1).
3. For MFTs: instantiate templates with lexicons; expand fill-ins with RoBERTa MLM suggestions
and WordNet categories (§2.3).
- Missing: fine-tuning hyperparameters, per-cell suite sizes (not specified), seeds/CIs, and the
model-column alignment of some Table 1 cells.
- Pitfalls: many tests need a "neutral" class binary-trained BERT/RoBERTa lack (§3); INV/DIR
need a probability output for the 0.1 threshold.

**8. Limitations and caveats** (as stated by the paper)
- The capability list is "not exhaustive" (§2.1); the tests shown are "a small selection" (§3).
- CheckList "cannot be directly used for non-behavioral issues such as data versioning
problems, labeling errors, annotator biases, worst-case security issues, or lack of
interpretability" (§5).
- INV/DIR test relationships between predictions, not ground truth (§2.2); absence of failure
"does not imply that these models are fair" (§3).
- Some failures are known elsewhere (typos, name sensitivity); most are claimed new (§3).

---

## 18. Qiang et al. — PPCL (additional: consistency training for LLMs)

**1. Citation and links**
- Qiang, Y., Nandi, S., Mehrabi, N., Ver Steeg, G., Kumar, A., Rumshisky, A., Galstyan, A.
(2024). *Prompt Perturbation Consistency Learning for Robust Language Models.* Findings of
EACL 2024, pp. 1357–1370.
- PDF: `Qiang2024_PPCL.pdf`; ACL Anthology: https://aclanthology.org/2024.findings-eacl.91/ .
- Code: **not specified** (no repository link in the text).
- Status: **VERIFIED** (full text incl. appendix). Sections §3–§6, appendix A.1–A.4.

**2. Problem and claim**
Fine-tuned LLMs are made competitive with discriminative IC-SF models — MASSIVE intent
accuracy 89.44 (JointBERT) vs 89.05 (LLaMA-30b+SFT), slot F1 80.43 vs 80.74 (Table 2) —
yet they are brittle to small prompt changes; all model families degrade under oronym, synonym
and paraphrase perturbations (Table 4), most severely in SF under oronyms (§5.3). The claim:
**prompt perturbation consistency learning (PPCL)**, adding a Jensen–Shannon (JS)
divergence term between the output distributions of a clean and a perturbed utterance, recovers
on average **59%** of the IC drop and **69%** of the SF drop (abstract, §5.4), beating data
augmentation with **ten times fewer** augmented samples. The conclusion (§6) gives the
average drop as **13.07%** IC and **22.20%** SF.

**3. Perturbations used** (§3.3, §4.3, Appendix Table 8)
- **Oronym** — words replaced by phonetically similar ones (Table 6); motivated by ASR errors.
- **Synonym** — WordNet synonym replacement ("email to new contact" → "email to novel
contact", Table 8).
- **Paraphrase** — whole-utterance rephrasing (Table 8), produced by "a specific LLM from
Huggingface" pre-trained for paraphrasing (**model not specified**, §4.3).
- Constraints (§4.3): key stop words derived from the domain/intent/slot label sets are **not**
substituted; at most **3 words** perturbed per utterance; perturbations filtered with
**BERTScore ≥ 0.85** against the original.
- Label handling (§4.3): intent labels copied; slot labels copied for oronyms/synonyms
(length/order-preserving) and regenerated for paraphrases.
- The perturbations are *semantically near-equivalent* replacements, not adversarially
optimised worst-case edits (my reading of §4.3).
- Test sets: clean and perturbed sets are one-to-one (§4.2, Eq. 7).

**4. Method** (§3.5, §3.6, Fig. 2)
1. Instruction fine-tune the LLM with sentinel-based prompt formats (Appendix Table 1; §3.2).
2. **PPCL**: feed the clean utterance `x_c` and its perturbed counterpart `x_p` together (Fig. 2);
obtain per-output-token softmax distributions `ŷ_c^j`, `ŷ_p^j`; compute the **JS divergence**
(symmetric KL) between them (Eq. 1), averaged over response length `L` (Eq. 2).
3. For **paraphrases**, where clean/perturbed lengths differ, use the length-averaged
distributions and a single sequence-level JS term (Eq. 3).
4. Objective (§3.6): `L = λ1·L_C + λ2·L_P + λ3·L_JS`, where `L_C` and `L_P` are cross-entropy
of the clean and perturbed outputs against `y` (Eqs. 4–6) and the λ are tuned per dataset.
- Needs paired clean/perturbed data plus semantic-equivalence filtering (§3.6).

**5. Experimental setup** (§4, Appendix A)
- Datasets (Table 7): ATIS 4,478 train / 500 dev / 893 test, 18 intent, 127 slot labels; SNIPS
13,084 / 700 / 700, 7 / 72; MASSIVE 11,514 / 2,033 / 2,974 (en-US only, §A.1), 60 / 56.
- Models: JointBERT and JointBERT+CRF (BERT-base uncased, 12 layers, 768 hidden, 12
heads; max length 50, batch 32, Adam lr 5e-5, dropout 0.1, ≤10 epochs, A.2); GPT-3.5
zero-/few-shot (10 examples, A.2); GPT-2 (124M) and LLaMA 7B / 13B / 30B (A.2).
- SFT (A.2): max length 256, batch 32, Adam lr 3e-4, 100 warm-up steps, 5 epochs. PPCL (A.2):
further 2 epochs, Adam lr 3e-4; λ1/λ2/λ3 tuned per dataset (§5.5) but **values not specified**.
- Metrics (§4.2): IC = accuracy, SF = F1; **PDR = 1 − perf(perturbed)/perf(clean)** (Eq. 7),
smaller is more robust.
- Mitigation runs only on **LLaMA-7b** on MASSIVE (§5.4). Augmentation sizes (Table 5):
PPCL one perturbed sample per clean (**+3k** oronyms, **+5k** synonyms, **+6k**
paraphrases) vs multi-sample **+50k**; PPCL uses ~10% of the augmented data.
- Seeds/error bars and decoding settings: **not specified**.

**6. Results**
LLaMA-7b on MASSIVE; IC clean → perturbed from Table 4, PDR and recovery from Table 5
(baseline and PPCL rows). Drop/recovery in percent; the mean row repeats the paper's own
summary figures (§6, §5.4).

| Perturbation | IC clean → perturbed (T4) | IC-PDR baseline → PPCL (T5) | IC recovery |
SF-PDR baseline → PPCL (T5) | SF recovery |
|---|---|---|---|---|---|
| Oronyms | 89.18 → 74.31 | 16.67 → 8.74 | 47% | 40.75 → 15.41 | 62% |
| Synonyms | 89.23 → 76.79 | 13.94 → 3.74 | 73% | 9.72 → 1.44 | 85% |
| Paraphrases | 82.78 → 80.21 | 8.62 → 3.69 | 57% | 16.14 → 6.36 | 60% |
| Mean | — | 13.07 → — | 59% | 22.20 → — | 69% |

- vs data augmentation (§5.4): one extra perturbed sample with `L_C+L_P` recovers up to 45%
IC / 51% SF for oronyms; multi-sample augmentation (+50k) recovers 58% IC / 59% SF, below
PPCL; PPCL loses only on paraphrase SF (60% vs 74%).
- Ablation (§5.5, Table 5): all three loss terms (L_C, L_P, L_JS) are needed; JS alone recovers
little (5% IC oronyms).
- Other models (Table 4): JointBERT IC-PDR 21.53 / 13.42 / 7.09 and SF-PDR 47.47 / 7.31 /
16.20 (oronym / synonym / paraphrase); GPT-3.5-ZS is stable on IC (1.15% oronym) but
collapses on SF (35.05%). my inference: phonetically corrupted tokens wreck slot boundaries
even for BERT-style taggers.
- Not reported: calibration, clean/perturbed prediction agreement, wall-clock or memory cost,
seeds.

**7. Reproduction notes**
1. Fine-tune JointBERT (baselines) and the LLM (sentinel prompt formats, Table 1). 2. Build the
three generators (WordNet synonyms, NLTK pronouncing corpus for oronyms, a HuggingFace
paraphraser), apply the ≤3-word/stop-word constraints and BERTScore ≥ 0.85 filter (§4.3). 3.
Fine-tune with `L_C+L_P+L_JS` (Eq. 6); evaluate with PDR (Eq. 7).
- Missing: the λ1/λ2/λ3 values, the exact paraphrase model, GPT-2/LLaMA decoding settings,
random seeds, the stop-word list, BERTScore configuration.
- Pitfalls: PPCL assumes the *same* perturbation family at training and test time (§4.3, §5.4); it
needs paired clean/perturbed text and a second forward pass per training step (Fig. 2);
paraphrases need regenerated slot labels (§4.3).
- Cost: no wall-clock/memory overhead reported; the only cost figure is *data* — PPCL uses
one-tenth the augmented samples of multi-sample augmentation (§5.4). Training feeds both
clean and perturbed utterances (Fig. 2), so ~2× the forward pass per step (my inference; the
paper states no factor).

**8. Limitations and caveats**
- Paper's Limitations: small public sets only (MASSIVE, ATIS, SNIPS); gains may not carry to
real-world distributions; robustness shown only for IC-SF.
- The mitigation is demonstrated on **one** model (LLaMA-7b) and **one** dataset (MASSIVE)
(§5.4); ATIS/SNIPS mitigation is said to be in the appendix (§5.4), but the appendix holds only
drop/ablation tables (Tables 9–12).
- No seeds or confidence intervals; per-dataset λ tuning is not fully reported.
- Perturbations are meaning-preserving and BERTScore-filtered, so they are not worst-case
adversarial edits, and robustness is measured with the same generators used for training.
- **my analysis (transfer to an encoder classifier):** PPCL regularises per-output-token
distributions over the whole vocabulary (Eq. 2), fitting a generative decoder. A BERT-style intent
classifier emits a single label distribution per input, so the closest analogue is the
sequence-level JS of Eq. 3 (the paraphrase variant) between clean and perturbed logits; for
token-level slot filling a per-token JS like Eq. 2 would apply. The paper never applies PPCL to its
discriminative JointBERT baseline — the encoder is only the robustness reference (Table 4) —
so encoder transfer is untested here. my inference: a transplant is limited because the JS is
tuned over full vocabularies (an encoder head has few classes, so the signal is coarser and sits
on high-level label logits), and PPCL needs paired meaning-preserving perturbations plus a
second forward pass per step.
- Model families covered: decoder-only LLMs (GPT-2 124M; LLaMA 7B/13B/30B; GPT-3.5 via
API, zero-/few-shot) and BERT-style encoders only as joint IC-SF baselines.

---
## 19. Wang et al. — AdvGLUE (additional: robustness benchmark)

**1. Citation and links**
- Wang, B., Xu, C., Wang, S., Gan, Z., Cheng, Y., Gao, J., Hassan Awadallah, A., Li, B. (2021).
*Adversarial GLUE: A Multi-Task Benchmark for Robustness Evaluation of Language Models.*
NeurIPS 2021 Track on Datasets and Benchmarks (arXiv 2111.02840v2; UIUC, Zhejiang
University, Microsoft, title page).
- PDF: `Wang2021_AdvGLUE.pdf`. arXiv: https://arxiv.org/abs/2111.02840 . Data/leaderboard:
https://adversarialglue.github.io (abstract; §1), CC BY-SA 4.0 (§B.3). The dev set is public; the
test set is hidden and scored through a CodaLab submission API (§3.5; §B.3).
- Status: **VERIFIED** (full text read). §1 Intro, §2 Related Work, §3 Dataset Construction
(3.1–3.5), §4 Diagnostic Report, §5 Conclusion, Appendices §A and §B.

**2. Problem and claim**
This is a benchmark, not a defence paper: robustness results are not comparable because each
method uses its own adversary setup, so a unified benchmark is missing (§1; §B.1). AdvGLUE
applies **14 textual attack methods** to five GLUE tasks and validates the output by humans
(abstract; §5). Findings: (i) around **90%** of generated adversarial examples change the
original meaning or mislead annotators (abstract; §3.4), and only about **10%** reach a 4-vote
consensus among 5 annotators while keeping the original label (§1); (ii) all tested models and
robust-training methods do poorly on AdvGLUE, with ELECTRA (Large) dropping from **93.16**
average GLUE to **41.69** (§1; Table 4).

**3. Perturbations used**
Fourteen attacks across three levels, indexed C1–C11 (abstract; §3.2; Table 1). Twelve distinct
methods; CheckList and StressTest are each counted twice because both supply rule-based
distraction sentences *and* human-crafted templates (footnote 2).
- **Word-level (C1–C5)**: TextFooler (embedding similarity; cosine threshold **0.8** for
sentiment, **0.7** elsewhere, **50** synonyms/word, §A.4); TextBugger (typos; five strategies
— space insert, char delete, keyboard-adjacent and visually-similar replacement, char swap;
first four edit-distance 1, swap ≤2, §A.4); BERT-ATTACK (context-aware masked-LM
replacement; **48** candidates, threshold **0.4**, §A.4); SememePSO (knowledge-guided via
HowNet; inertia **0.8/0.2**, movement probability **0.8/0.2**, population **60**, §A.4);
CompAttack (white-box composition of the other word-level pools, §3.2.1; §A.4).
- **Sentence-level syntactic (C6)**: SCPN (syntax-tree paraphrase; **10** most frequent
ParaNMT-50M templates, CoreNLP **3.7.0**, §3.2.2; §A.4); T3 (perturbs the root context vector;
scaling **1e4**, confidence **0**, up to **100** steps at LR **0.1**, §A.4); AdvFever
(entailment-preserving transforms, all **23** templates, §3.2.2; §A.4).
- **Sentence-level distraction (C7)**: StressTest appends true statements ("and true is true",
"and false is not true") five times to the NLI hypothesis; CheckList adds randomly generated
URLs/handles (§3.2.2). Applied to four tasks excluding QQP (Table 1 caption).
- **Human-crafted (C8–C11)**: CheckList (Temporal, Negation) on SST-2/QQP/QNLI;
StressTest (Numerical Reasoning) on MNLI; ANLI on MNLI; AdvSQuAD (AddSent/AddOneSent)
on QNLI (§3.2.3; Table 1 caption).
**4. Method** (Fig. 1)
1. Sources are the GLUE **dev** sets; **1,000** cases are sampled for QQP, QNLI and
MNLI-m/mm, whole dev sets otherwise; attacks target three surrogates — BERT, RoBERTa,
RoBERTa ensemble (following ANLI, §3.2).
2. **Automatic filtering** (§3.3): keep only examples that fool the other two surrogates
(transferability); drop word-level examples with word modification rate **>15%** and keep the
highest-BERTScore sentence-level ones (fidelity).
3. **Human filtering** (Mechanical Turk, §3.3): a training phase on batches of **20** GLUE dev
examples, requiring **≥85%** accuracy to qualify; then batches of **10** examples from one
attack, each judged by **5** annotators and kept only with **≥4-vote** consensus *and* a
majority label equal to the original.
4. Merging samples distraction and human-crafted data to match the average curated per-attack
size (§3.5). Split: benign data 9:1, adversarial examples from the **90%** benign part become
the hidden test set; human-crafted data split 90/10 (§3.5).
5. Metrics: ASR (Eq. 1), Curated ASR (Eq. 2), Filter Rate = 1 − Curated ASR/ASR, Fleiss Kappa
(0.4–0.6 moderate, 0.6–0.8 substantial), Human Accuracy (§3.4).

**5. Experimental setup**
- Models (§4; Table 4): BERT (Large), ELECTRA (Large), RoBERTa (Large), T5 (Large),
ALBERT (XXLarge), DeBERTa (Large); robust-training baselines: SMART (BERT), SMART
(RoBERTa), FreeLB (RoBERTa), InfoBERT (RoBERTa). Task metrics (macro-averaged): SST-2
acc., QQP acc./F1, QNLI acc., RTE acc., MNLI matched/mismatched acc. (Table 4 caption;
Table 8).
- Fine-tuning (§A.6): BERT 10 epochs on RTE / 4 elsewhere, batch **512** (QNLI) / **256**, LR
**2e-5**; ELECTRA LR **5e-5**, batch **32**, 10 epochs (RTE) / 2, weight decay **0.01**;
RoBERTa and T5 10 epochs, LR **2e-5**, batch **32**/**64**; ALBERT default, batch
**32**/**128**; DeBERTa LR **1e-5**, batch **64**/**32**; SMART grid search, FreeLB all
parameter combinations, InfoBERT batch **32**, LR **2e-5**. Hardware: 8× V100 GPUs, 256
GB (§A.6).
- BERT (Large) and RoBERTa (Large) use *different seeds* from the generation surrogates
(Table 4 caption); the seeds and their number are **not specified**.

**6. Results**
Curation (Table 3; §3.4): Curated ASR is **always below 11%**; filter rates for most methods
exceed **85%**; post-curation Fleiss Kappa is **≈0.6**, and TextBugger shows the highest
Curated ASR and Curated Fleiss Kappa across tasks. Average human accuracy over qualified
annotators is 89.2 / 80.4 / 85.8 / 85.6 / 86.4 for SST-2 / MNLI / RTE / QNLI / QQP (Table 11).
Test set size **4,978** (SST-2 1,420; QQP 422; QNLI 968; RTE 304; MNLI 1,864; Table 1, Table
8).

Macro-average accuracy % (GLUE dev vs AdvGLUE test; Table 4, per-task in Table 9; Δ derived
by me from those columns, matching Table 4's Δ column):
| Model | GLUE | AdvGLUE | Δ (derived) |
|---|---|---|---|
| BERT (Large) | 85.76 | 33.68 | −52.08 |
| ELECTRA (Large) | 93.16 | 41.69 | −51.47 |
| RoBERTa (Large) | 91.44 | 50.21 | −41.23 |
| T5 (Large) | 90.39 | 56.82 | −33.57 |
| ALBERT (XXLarge) | 91.87 | 59.22 | −32.65 |
| DeBERTa (Large) | 92.67 | 60.86 | −31.81 |
| SMART (BERT) | 85.70 | 30.29 | −55.41 |
| SMART (RoBERTa) | 92.62 | 53.71 | −38.91 |
| FreeLB (RoBERTa) | 92.28 | 50.47 | −41.81 |
| InfoBERT (RoBERTa) | 89.06 | 46.04 | −43.02 |

BERT (Large) per task (Table 9): SST-2 93.23 → 33.03; MNLI 85.78/85.57 → 28.72/27.05; RTE
68.95 → 40.46; QNLI 91.91 → 39.77; QQP 90.72/87.38 → 37.91/16.56; it is reported below
random-guess accuracy on every task (§4).

Defence experiments (§4): the largest average gap quoted is **55%** on SMART (BERT);
**SMART (RoBERTa) improves RoBERTa (Large) by over 3.71% on average and also raises
benign accuracy**; InfoBERT (RoBERTa) has both lower benign and lower robust accuracy than
RoBERTa (Large) and was re-run with different hyper-parameters for its best numbers.
DeBERTa (Large) and ALBERT (XXLarge) score highest on AdvGLUE, while ELECTRA (Large)
scores below the surrogate RoBERTa (Large). Diagnostic report (Table 5; §4): models are most
vulnerable to human-crafted examples; for sentence-level perturbations distraction beats
syntactic manipulation; word-level replacement strategies behave similarly, with typo-based and
knowledge-guided attacks most effective.

**7. Reproduction notes**
1. Train on GLUE train data and attack the GLUE dev sets with the 14 attacks using the §A.4
hyper-parameters against the three surrogates. 2. Apply transferability/fidelity filtering (§3.3),
then the MTurk training and filtering stages (§3.3). 3. Merge, split 9:1, evaluate per-task metrics
or submit to CodaLab (§3.5).
- Missing / not specified: the BERTScore cut-off and how many sentence-level samples were
kept per attack; the seeds per model (only that they differ from the surrogates, Table 4 caption);
wall-clock training times; the target Fleiss Kappa value; full annotation templates (external links
only, §A.7). Per-task pay rates: $0.4 / $1.0 / $1.0 / $1.0 / $0.5 (Table 11).
- my reading: reproducing the reported AdvGLUE numbers needs the hidden test set through
CodaLab; only the public dev set — 148 / 78 / 148 / 81 / 283 for SST-2/QQP/QNLI/RTE/MNLI
(derived) from Table 8's label distributions — is reproducible locally.
- Pitfalls: curation discards roughly 90% of raw examples, so an unfiltered re-implementation
reports much higher ASR than the Curated ASR; curation is skipped for distraction and
human-crafted attacks, assumed valid by construction (§3.5).

**8. Limitations and caveats**
- §A.8: compute limits prevent evaluating all existing models; leaderboard submissions are
invited and few-shot robustness is future work. A known concern is that adversarial filtering may
let participants top the leaderboard with *different* errors from the surrogates; the authors argue
curation selects transferable examples exposing shared vulnerabilities.
- §3.3: some grammatical errors and typos remain after curation (intentionally injected by
TextBugger, SCPN, etc.) and are retained because their labels still get high annotator
consensus.
- Coverage: only five GLUE tasks; CoLA (no well-defined automatic attacks) and WNLI
(insufficient data) are excluded (§3.1). It is an evaluation-only diagnostic set used alongside
GLUE; no new defence is proposed (§A.8).
- my inference: the robust-training baselines tested (SMART, FreeLB, InfoBERT) are
embedding-space/virtual-adversarial regularisers, so their weak scores are not evidence about
word- or sentence-level adversarial training, which the paper does not benchmark.
- Not specified: any human-performance comparison on the AdvGLUE test set; error bars or
confidence intervals for model results.

---

## 20. Wang et al. — Robustness survey (additional: survey)

**1. Citation and links**
- Wang, X., Wang, H., Yang, D. (2022). *Measure and Improve Robustness in NLP Models: A
Survey.* NAACL 2022 (arXiv 2112.08313v2 [cs.CL], 9 May 2022).
- PDF: `Wang2022_RobustnessSurvey.pdf`. arXiv: https://arxiv.org/abs/2112.08313 .
- Affiliations: Google Research; Carnegie Mellon University; Georgia Institute of Technology (§
title page). Funding: "in part by a grant from Google" (Acknowledgements).
- Status: full main text read (§1–§7 plus Tables 1–2); references removed from the cleaned text.
Code/artifact repository: **not specified** (no link is given anywhere in the text).
- Structure: §1 Introduction; §2 Definitions of Robustness in NLP (2.1 adversarial attacks, 2.2
distribution shift, 2.3 connections); §3 Robustness in Vision vs. NLP (sub-section "A Common
Theme", printed as 4.1 in the pdftotext); §4 Identify Robustness Failures (4.1 human-prior, 4.2
model-based); §5 Improve Model Robustness (5.1–5.4 data-driven, model/training-based,
inductive-prior, causal intervention; 5.5 connections); §6 Open Questions; §7 Conclusion.

**2. Problem and claim**
The paper argues that robustness research in NLP is scattered across definitions, tasks and
communities, and offers a unifying survey of how to *define, measure and improve* robustness
(§1, abstract). Robustness is unified as robust accuracy over a shifted test distribution D′:
`E_{(x′,y′)∼D′}[f(x′)=y′]` (§2). D′ is constructed either by synthetically perturbing the input (§2.1) or
by a naturally occurring distribution shift (§2.2); the paper's common framing is "synthetic vs.
natural distribution shift" (§2.3). For text classification and sequence labelling the definition
works because y is over a fixed discrete label set; for text generation robustness is "less well
defined" and manifests as positional bias or hallucination, with a lack of reliable metrics to
determine the relationship between f(x′) and the open-ended y′ (§2). §3 lists three vision-vs-NLP
differences: discrete vs. continuous search space (gradient attacks do not transfer directly),
attacks that are perceptible to humans (bounded by not altering sentence meaning) rather than
imperceptible, and support-vs-density differences of the data distributions.

**3. Perturbations used**
The survey's taxonomy of robustness failures / perturbation types:
- **Table 1** ("Perturbation types for identifying robustness failures and improving robustness in
NLP") organizes attacks by *space* (discrete vs. continuous) and *level*: character-level
(HotFlip, DeepWordBug, Synthetic-Noise), word-level (GenAdv, PWWS, SEM, BERT-ATTACK,
TextFooler, SememePSO), sentence-level (AdvSQuAD, SCPNs, CAT-Gen, TAILOR),
mixed-types (CheckList, Polyjuice, MAYA), and embedding-space (AT & VAT, Natural-adversary,
FreeLB, ALUM) (§4, Table 1).
- **Assumption axis** (§2.1): *label-preserving* perturbations (y′=y) — token/character
swapping, paraphrasing, semantically equivalent adversarial rules, adding distractors — versus
*label-changing*/counterfactual perturbations (y′≠y). A separate axis is *semantic-preserving*
vs. *semantic-modifying* (§2.1). The survey cites Wang et al. (2021b) that a significant portion
of ostensibly label-preserving perturbations are not label-preserving, and Morris et al. (2020a)
calling for attention to the *validity* of perturbed examples (§2.1).
- **Natural shifts** (§2.2): grammar errors, dialects, speakers, languages; newly collected
datasets for the same task in a different domain; plus fairness (gendered stereotypes/biases).
- **Failure identification** (§4): human-prior and error-analysis driven (§4.1) vs. model-based
(§4.2: white-box attacks, universal/natural triggers, separately trained bias models,
human-in-the-loop vs. model-in-the-loop).
- **Benchmarks** (Table 2, per task): NLI (Stress-test, HANS, Counterfactual-NLI, ANLI), QA
(AdvSQuAD, Adv-QA, Natural-Perturbed-QA, Natural-shift-QA, SAM), paraphrase (PAWS,
PAWS-X), co-reference (WinoGender, WinoBias), NER (OntoRock, SeqAttack) (Table 2).
- **"Measure" methods**: robust accuracy (§2); stress-test/benchmark datasets organized per
task (Table 2); and, per §2.3 and §6, additional measures such as calibration, stability and
uncertainty estimation under distribution shift, with unified benchmarking tools named as
CheckList, Reliability Testing, Robustness Gym and Dynabench (§6).

**4. Method**
The survey organizes improvement methods into four categories (§5):
- **Data-driven (§5.1)**: data augmentation (Mixup, MixText, CutOut, AugMix, HiddenCut) said
to substantially improve robustness/generalization; counterfactually augmented data via
human-in-the-loop (Kaushik et al. 2019); strategic augmentation of automatically identified
"shortcuts" (Wang et al. 2021d); and reusing challenging/adversarial examples as extra training
data in either discrete input space or embedding space. These are data-level and "often hard to
be interpreted in terms of how and why mitigation works" (§5.1).
- **Model/training-based (§5.2)**: pre-training improves out-of-distribution robustness, attributed
to the self-supervised objective and large, diverse pre-training data; Tu et al. (2020) add that
larger model size, more fine-tuning data and longer fine-tuning also help; better use of minority
examples via group DRO (Sagawa et al. 2020a) and extensions that identify "minority" samples
(Nam et al. 2020, Lahoti et al. 2020, Liu et al. 2021). §5.2 also asks *when* to use data-driven
vs. model-based methods, citing Liu et al. (2019) that failures trace to data blind spots or the
model's intrinsic learning ability, so the two can be combined.
- **Inductive-prior-based (§5.3)**: introduce inductive bias to regularize the hypothesis space;
construct a side component that flags misaligned features, then regularize the main model
(label-associated keywords/fragments, easy-to-learn patterns); ensemble with a bias-only model
(Clark et al. 2019, 2020; Utama et al. 2020a,b), improved by calibrating the bias-only model
(Xiong et al. 2021); regularizers for robust fine-tuning such as mutual-information-based (Wang
et al. 2021a) and smoothness-inducing adversarial regularization (SMART, Jiang et al. 2020);
connected to domain-adversarial training (Ganin et al. 2016) and invariant risk minimization
(IRM) with its extensions (§5.3).
- **Causal intervention (§5.4)**: DRO over an unmeasured variable (Srivastava et al. 2020);
context-aware counterfactuals accounting for confounders (Balashankar et al. 2021);
counterfactual invariant predictors dependent on causal structure (Veitch et al. 2021).
- **§5.5 connections**: three mainstream ideas — leverage large pre-trained data, learn
invariant representations/predictors, and use a prior on the spurious patterns — with solutions
via augmentation, minority reweighting, ensembling, inductive-prior design and causal
intervention; the survey conjectures many mitigations optimize the same robust-generalization
error bound (Wang et al. 2021c).

**5. Experimental setup**
Not applicable: survey. The paper runs no experiments of its own; Tables 1–2 are literature
compilations. The survey reports no original numeric results (no accuracy figures appear in the
main text).

**6. Results**
Not applicable: survey. The only quantitative-flavoured claims the survey itself makes are counts
(e.g., "three" differences between vision and NLP, §3; entries in Tables 1–2) and literature-level
statements such as Taori et al. (2020) finding that robustness to synthetic distribution shift
"might offer little to no robustness improvement under natural distribution shift" (§2.3). No
benchmark numbers are reported or aggregated by the survey.

**7. Reproduction notes**
As a survey there is nothing to reproduce directly; instead it points to the artifacts one would
reproduce from. For evaluation it points to the benchmark datasets named per task in Table 2
and to unified evaluation tools CheckList, Reliability Testing, Robustness Gym and Dynabench
(§6). For attacks it points to the methods in Table 1
(character/word/sentence/embedding-space). For improvement it points to the mitigation
families with their primary citations in §5.1–§5.4 (counterfactually augmented data, group DRO,
bias-only ensembles, SMART, domain-adversarial training, IRM, causal/counterfactual
predictors). Concrete code links or hyper-parameters: **not specified** anywhere in the text.

**8. Limitations and caveats**
The survey states its own gaps/open problems in §6, plus earlier caveats:
- **Identifying unknown robustness failures**: existing identification relies heavily on human
priors/error analyses that pre-define a limited set of patterns, requiring expertise and possibly
carrying subjective bias; proactively discovering "unrobust regions" automatically remains
challenging (§6).
- **Interpreting and mitigating spurious correlations**: mitigation suffers a trade-off between
removing shortcuts and sacrificing performance (Yang et al. 2020; Zhang et al. 2019a); most
strategies are pipeline-based (defining/detecting spurious correlations as prerequisites), risking
error cascades; end-to-end frameworks are needed (§6).
- **Unified framework to evaluate robustness**: a variety of potential spurious patterns makes
quick evaluation hard; the survey calls for more unified benchmarking (§6).
- **User-centred measures and mitigation**, and **connections between human-like linguistic
generalization and NLP generalization**, are named as open (§6).
- Earlier caveats: transferability between synthetic and natural distribution shifts is "relatively
underexplored" (§2.3); the label-preserving assumption often does not hold (§2.1); text
generation lacks robust metrics (§2).
- Scope: my reading — the paper is deliberately conceptual and citation-based, so it supplies no
protocol, no seeds and no numerical comparison of mitigation methods; all empirical claims are
delegated to the cited works (not specified in this text).

---

## Comparison table (all 19 read papers)

| # | Paper | Cost vs plain fine-tuning | Robustness gain reported (metric) | Clean-performance
cost | Ease of reproduction | Model families |
|---|---|---|---|---|---|---|
| 1 | EDA (seed 1) | ~×n_aug training data (my inference; overhead not reported) | n/a —
augmentation paper, clean test sets only | none; +0.8 at full data | high (simple) | CNN/RNN |
| 2 | Goodfellow FGSM (seed 2) | one-step attack + much wider net (1,600 vs 240 units/layer) |
FGSM error 89.4% → 17.9% at ε=.25 | none; clean error 0.94% → 0.782% (improved) | high
(images) | maxout MLP, RBF |
| 3 | Madry PGD (seed 3) | ≈K-step PGD per batch (expensive) | MNIST PGD-trained
89.3–93.2%, FGSM 95.6% vs 6.4% naturally trained | ~none (98.8% vs 99.2% natural) |
medium (capacity caveat) | CNN (MNIST/CIFAR) |
| 4 | TextFooler (seed 4) | n/a — attack, query-heavy (60–4,403 queries) | n/a — attack: BERT
acc. → 4–20% | n/a | medium (needs output probs; 1k subsets) | BERT, WordCNN/WordLSTM |
| 5 | BERT-ATTACK (seed 5) | n/a — attack, 3× faster than TextFooler | n/a — attack: BERT acc.
→ 5–16% | n/a | medium | BERT, Word-LSTM, ESIM |
| 6 | Noise-BERT (seed 6) | noise pre-training + contrastive + FGV adversarial | typos F1 67.65
→ 71.15; overall 82.07 → 83.95 | none; clean 95.83 → 96.16 | low (no code, no
hyper-parameters) | BERT slot filling |
| 7 | CDAE (seed 7) | trains a 128-d head on a frozen BERT (cheap) | top-1 @ρ=0.9 ≈66% vs
SimCSE ≈16% | not reported (embeddings only) | medium (preprint, one backbone) | BERT /
SimCSE / SBERT |
| 9 | FreeLB | ≈K× training cost | embedding-space only; GLUE 78.3 → 79.4 | improves (no cost)
| high (well documented) | BERT / RoBERTa |
| 10 | SMART | ≈3× training time, 2× memory | none on text perturbation (ambiguous/ANLI only)
| improves | medium (many tuned hyper-parameters) | BERT / RoBERTa |
| 11 | RoAST | one-step adversary + consistency term | Acc_adv 66.30 → 72.57; ECE 7.11 →
5.45 (SST-2) | none; Acc_in 96.29 → 96.87 | medium (A100, 3 seeds, tuned) | 6 LMs incl.
GPT2-large |
| 12 | Moradi & Samwald | n/a — test-time evaluation only | n/a — measures degradation (e.g.
SST 92.2 → 75.6 char deletion) | n/a | high (evaluation harness) | BERT/RoBERTa/XLNet/ELMo
|
| 13 | Pruthi — ScRNN | extra recogniser training + inference-time pre-processing | BERT "All"
attack 45.8 → 75.0 (neutral) | small; 90.3 → 88.3 | medium | BERT, BiLSTM/char CNN |
| 14 | SDBN | extra forward–backward pass (runtime, not memory) | delete-char 60.67 → 65.14;
swap-char 56.82 → 62.80 | negligible; 89.81 → 89.61 | medium (ε sensitive across datasets) |
BERT, DeBERTa-v3, LLaMA, Qwen, mBERT |
| 15 | BPE-Dropout | training-time merge dropping, no extra inference | MT misspelled-BLEU
drop roughly halved (e.g. 2.96 → 1.98, En-De) | none; +0.45–1.5 BLEU (gain) | high (simple
BPE change) | Transformer seq2seq (MT) |
| 16 | TextAttack | n/a — toolkit | n/a — adv. training: TextFooler attack 2.23 → 29.63 | large;
77.30 → 61.85 (TextFooler-trained) | high (framework) | LSTM, CNN, BERT |
| 17 | CheckList | n/a — behavioural test suite | n/a — diagnostic failures (e.g. INV typo 5.2) | n/a
| high | BERT/RoBERTa; commercial |
| 18 | PPCL | +2 consistency epochs, ~10× fewer augmented samples | recovers 59% IC / 69%
SF drop (PDR 13.07 → 8.74 oronyms) | not clearly reported | medium (one model/dataset) |
JointBERT, GPT-2, LLaMA, GPT-3.5 |
| 19 | AdvGLUE | n/a — benchmark | n/a — shows −31.81 to −55.41 point drops | n/a | high (test
set) | BERT/ELECTRA/RoBERTa/T5/ALBERT/DeBERTa |
| 20 | Wang survey | n/a — survey | n/a | n/a | n/a | n/a |

Entry 8 is **NOT FOUND** (placeholder with no data); no row is given for it.

## What the literature says about my expectations

### Papers support this

- **(a) a modest ~2–10-point drop under mild-to-moderate perturbation.** For natural word-level
edits the drop lands in this band: Noise-BERT goes clean 96.16 → paraphrase 90.27 (−5.9
(derived)) and simplification 88.74 (−7.4 (derived)) [P6]; the mildest word-order perturbations in
[P12] are also modest. Small drops are likewise seen in the misspelled-BLEU margins [P15]
and at low ρ in the embedding-similarity curves [P7]. **Caveat:** for character-level noise even
the *first* edit often exceeds the band — [P12] reports SST 92.2 → 77.1 under char insertion
and → 75.6 under deletion, and [P13] shows BERT collapsing far past 10 points.
- **(b) large drops exist.** 20–40+ point drops are repeatedly reported: AdvGLUE sends
ELECTRA 93.16 → 41.69 (−51.47) and BERT 85.76 → 33.68 (−52.08) [P19]; BERT 90.3 →
45.8 under the "all" typo attack [P13]; CMW costs −32 on TREC [P12]; typos cost ≈25 F1 on slot
filling [P6]; a vanilla PEFT model loses −29.14 pp (delete-char) [P14]; TextFooler drives BERT to
4–20% [P4,P5].
- **(c) smooth rather than cliff-like degradation.** [P7] reports "smooth and monotone"
degradation for all three perturbation strategies, and [P12] finds curves "roughly linear to mildly
concave … no cliff" (the first perturbation does most damage).
- **Agreement.** [P4] reports human label agreement of 92% (MR) and 85% (SNLI) between
original and adversarial pairs.
- **Calibration.** [P11] is the only paper quantifying ECE, improving SST-2 7.11 → 5.45 and
MNLI 12.64 → 11.02; [P2] is an early source of high-confidence errors (no ECE).
- **Other tasks and families.** Multi-task robustness is measured for classification, sentiment,
NER, similarity and QA [P12]; tagging by [P6]; NLI by [P4,P5]; retrieval/embeddings by [P7]; MT
by [P15]. Decoder-only LLMs are covered by [P11] (GPT2-large), [P18] (GPT-2, LLaMA,
GPT-3.5) and [P14] (LLaMA-3.2-1B, LLaMA-2-7B, Qwen-2.5-7B), and seq2seq by [P15] and T5
in [P19].

### Papers contradict this

- **(b) the "memorization of surface forms" explanation.** [P2] argues explicitly that the cause of
adversarial vulnerability is **linearity in high dimensions, not nonlinearity or overfitting** — a
direct counter to the memorization reading. [P4] and [P5] show that a substantial share of
"successful" attacks change the true label (MNLI human accuracy 0.90 → 0.70 [P5];
task-sensitive label changes in NLI [P4]), and [P19] finds ≈90% of generated adversarial
examples change the original meaning or mislead annotators. So much of a 20–40+ point drop
reflects label noise or meaning change, not surface-form memorization.
- **(c) smoothness.** [P3] reports a "large drop in robustness for slightly larger ε" — a cliff — for
MNIST PGD-trained models (attributed to thresholding filters tuned to the training ε), although it
notes the CIFAR10 decay is smoother.
- **(a)** is implicitly contradicted for character/adversarial noise, where drops routinely exceed
10 points [P12,P13,P6,P14].

### Not tested

- **(a) as a threshold.** No paper states a 2–10-point band as a diagnostic; the numbers are
only ranges I compared across differing perturbation types.
- **(b) directly.** No paper tests surface-form memorization as a mechanism.
- **(c) in most papers.** Degradation *versus strength* is not reported by
[P4,P5,P6,P9,P10,P11,P13,P14,P18]; these report final attacked numbers or single fixed levels.
[P3] shows only one dataset-level plot, and [P2] a single-example ε plot.
- **Agreement (prediction-level).** Clean-vs-perturbed *prediction* agreement is not reported
anywhere in the digest; [P6,P11,P12,P13,P14] all state it as not reported. Only human *label*
agreement is measured [P4].
- **Calibration.** ECE is reported only by [P11]; it is explicitly **not an ECE under controlled
perturbation strength** because it is averaged over in-distribution, shifted and adversarial sets.
All other papers list calibration as not reported, including
[P2,P4,P5,P6,P9,P10,P12,P13,P14,P18].
- **Other tasks.** Retrieval/embedding robustness appears only in [P7] and its downstream
benefit "was not evaluated" [P7]; tagging robustness only in [P6,P18]; QA robustness only
through the test-time toolkit in [P12] (and [P18]'s SLU setting). No paper reports tag/QA/retrieval
robustness together with calibration or agreement.
- **Other model families.** Seq2seq robustness is only MT-BLEU under one synthetic typo
setting [P15]; no seq2seq classification/NLI robustness-to-text-perturbation result is available.

### Bottom line

The literature supports the qualitative shape of my expectations — larger perturbations hurt
more, character/adversarial noise hurts a lot, and at least two papers [P7,P12] find smooth
rather than cliff-like degradation — but it does **not** support exact thresholds like "2–10 points"
or "20–40+ = memorization". The one paper that directly discusses the mechanism [P2] rejects
memorization in favour of linearity, and [P4,P5,P19] show that part of any large drop is label
change rather than memorization. Numbers are **not comparable across perturbation types**:
worst-case adversarial attacks [P4,P5,P19], natural test-time noise [P12], character typos
[P6,P13,P14], augmentation [P1,P15] and embedding-space perturbations [P7,P9] measure
different things at different budgets. Calibration and prediction agreement are almost entirely
untested — only [P11] quantifies ECE, and no paper reports clean-vs-perturbed prediction
agreement — so my calibration and agreement expectations rest on essentially one paper and
remain uncertain.

## Recommended reproduction order (cheapest first)

0. **Evaluation harness (no training).** Stand up the test-time perturbation toolkit of [P12] (14
character/word methods, degradation curves over PPS) plus [P16] TextAttack for
attacks/augmentation/adversarial training and [P17] CheckList for behavioural invariance tests.
[P12] is a pure evaluation artifact; [P16] some recipes are heavy (Genetic/PSO took over 4 days
for 1,000 samples). This step changes no model and is the cheapest.
1. **Augmentation — EDA [P1].** Four label-preserving token edits, simple to implement; cost
grows with the augmentation factor (training data ×n_aug, my inference), and the paper itself
expects negligible gains once pretrained models are used.
2. **Character noise.** Evaluate char perturbations with [P12], then the typo defences: the
modular ScRNN pre-processor [P13] (extra recogniser plus an inference-time pass) and the
character-noise adversarial training of SDBN-h [P14] (one extra forward–backward pass, no
extra GPU memory). Noise-BERT [P6] belongs here too but is hard to reproduce (no code, no
hyper-parameters).
3. **FGSM [P2].** One-step gradient-sign attack and adversarial training; cheap in principle but
[P2] uses a much wider network (1,600 vs 240 units), and [P3] warns FGSM-only training does
not buy PGD robustness.
4. **PGD [P3].** K-step PGD training is the expensive reference defence; the BERT ports cost
roughly K× a clean step for FreeLB [P9], ≈3× time and 2× memory for SMART [P10], and
RoAST [P11] uses a cheaper one-step adversary plus a consistency term. Reproduce in that
cost order, noting [P3]'s capacity requirement.
5. **Others.** CDAE [P7] (representation tests, frozen backbone, cheap), BPE-Dropout [P15]
(simple training-time change for MT-style encoders), PPCL [P18] (extra consistency epochs on
one LLM), and finally the AdvGLUE test set [P19] as an evaluation-only diagnostic, with [P20]
read as a framing reference.

Index Table Additions
| # | Paper | Year / venue | Model family | Task type | Perturbation type | Training method | Code
| Status |
|---|---|---|---|---|---|---|---|---|
| 21 | Li et al., PerturbScore | 2023, arXiv preprint | BERT-base, FreeLB-BERT | text
classification (IMDB, AG's News) | TextFooler, random substitution, PGD embedding noise |
PGD continuous norm search; regression fine-tuning of PerturbScorer |
github.com/renke999/PerturbScore | VERIFIED |
| 22 | Agrawal et al., Perturbed Instructions | 2025, ICLR Workshop | Llama 3 8B Instruct,
Flan-T5 Large | instruction following / classification (CoLA, QNLI, SST-2) | DeepWordBug
(char-level), TextFooler (word-level) on prompts | LoRA instruction unperturbing (SFT-SD);
middle-layer representation alignment | github.com/ary4n99/llm-robustness | VERIFIED |
21. Li et al. — PerturbScore
1. Citation and links
 * Li, L., Ren, K., Shao, Y., Wang, P., Qiu, X. (2023). PerturbScore: Connecting Discrete and
Continuous Perturbations in NLP. arXiv:2310.08889v1 [cs.CL].
 * arXiv: https://arxiv.org/abs/2310.08889. Code: https://github.com/renke999/PerturbScore (§1
footnote 1).
 * Status: VERIFIED (full text read).
2. Problem and claim
Measuring and crafting discrete textual perturbations is challenging due to combinatorial
explosions and subjective distance metrics (§1, §3.2). The authors hypothesize that discrete
token edits can be mapped to equivalent minimum continuous perturbations in embedding
space (§1, §3.3). They propose PerturbScorer, a regression model predicting the continuous
norm bound (\epsilon) directly from perturbed text, outperforming standard metrics like edit
distance and BERTScore (§3.5, §4.4).
3. Perturbations used
 * Discrete (§4.1): TextFooler (word substitutions) and random token replacement using
synonym vocabularies. Edit distances range from 1 to 30 on IMDB and 1 to 15 on AG's News
(§4.2).
 * Continuous (§3.1, §4.1): Embedding-space l_2-norm perturbations generated via multi-step
Projected Gradient Descent (PGD) with T_a = 15 steps and learning rate \alpha = 0.1.
4. Method
 * Quantifying connection: For a discrete perturbation \mathcal{P}(S), search via PGD for the
smallest continuous radius \epsilon satisfying the output-shift equivalence condition
(\vert{}\frac{\Vert{}f_\theta(X+\delta) - f_\theta(X)\Vert{}_2}{\Vert{}f_\theta(X+\delta)\Vert{}_2 \cdot
\Vert{}f_\theta(X)\Vert{}_2} - \Gamma\vert{} < \phi, where \phi = 0.005) (§3.3, §3.4, Algorithm 1).
Discard outliers where shift exceeds bounds.
 * PerturbScorer training: Construct text pairs by concatenating original tokens with
perturbations (e.g., ... recall [reminds] ...) (§3.5). Train a regression head on top of a
Transformer encoder using Mean Squared Error loss on target \epsilon values (§3.5, §4.3).
 * Evaluation: Compute Kendall (\tau) and Spearman (\rho) rank correlation against actual
model shift (§4.2).
5. Experimental setup
 * Models evaluated (f_\theta): Standard fine-tuned BERT-base and FreeLB adversarial
pre-trained BERT (§4.1, Table 2).
 * Datasets: IMDB (binary sentiment, avg. length 220) and AG's News (topic classification, avg.
length 47) (§4.1).
 * Training split: 80% train / 20% test (§4.2). Fine-tuned using Hugging Face Transformers with
learning rate 5e-5, batch sizes 64 (IMDB) and 128 (AG's News) on 4x Nvidia RTX 3090 GPUs
(§4.3).
6. Results
 * Correlation with continuous shift on IMDB under TextFooler (Table 3):
   * Edit Distance: Kendall 0.5153 / Spearman 0.6683 (BERT).
   * BERTScore: Kendall 0.5497 / Spearman 0.7302.
   * USE: Kendall 0.4932 / Spearman 0.6697.
   * PerturbScorer: Kendall 0.7975 / Spearman 0.9342 (BERT); Kendall 0.8173 / Spearman
0.9453 (FreeLB).
 * Generalization (Table 4, Table 5):
   * Cross-dataset (Train IMDB / Test AG's News): Spearman remains 0.6441–0.7150
(outperforming Edit Distance at 0.6278–0.6350).
   * Cross-attack (Train Random / Test TextFooler): Spearman 0.7334–0.7532.
   * Combined Scorer (multi-dataset/perturbation): Achieves Kendall > 0.75 and Spearman >
0.90 across evaluation settings.
7. Reproduction notes
 * Extract discrete-continuous pairs using Algorithm 1 via target model gradients.
 * Ensure proper norm range interval slicing (\Delta\epsilon = 0.01).
 * Format input text using bracketed insertions immediately after target tokens.
8. Limitations and caveats
 * Target-model dependency: \epsilon values are tied to the geometry of specific target models
(f_\theta).
 * Assumes local Lipschitz smoothness, which can degrade under non-smooth loss landscapes.
 * Tested only on short-to-medium sequence classifications; generative tasks and non-Latin
scripts are unexamined.
22. Agrawal et al. — Perturbed Instructions
1. Citation and links
 * Agrawal, A., Alazraki, L., Honarvar, S., Rei, M. (2025). Enhancing LLM Robustness to
Perturbed Instructions: An Empirical Study. ICLR 2025 Workshop on Building Trust in LLMs and
LLM Applications.
 * Code: https://github.com/ary4n99/llm-robustness (§1 footnote 1).
 * Status: VERIFIED (full text read).
2. Problem and claim
While input-data perturbations are widely studied, task instruction perturbations (fixed prompt
templates) severely degrade LLM classification performance (§1). The authors evaluate
mitigation strategies across character- and word-level instruction corruptions, demonstrating that
Iterative Self-Denoising (SDi)—prompting the model to unperturb instructions prior to
execution—substantially outperforms representation alignment, perplexity smoothing, and
ensembling (§1, §3.4).
3. Perturbations used
 * Applied exclusively to prompt instructions (keeping stop words and class labels fixed) (§3.1).
 * Character-level: DeepWordBug (character substitutions, insertions, deletions) (§3.1, Fig. 1b).
 * Word-level: TextFooler (counter-fitted GloVe synonym replacements) (§3.1, Fig. 1c).
 * Generation: Greedy search maximizing performance drop rate (PDR) under query constraints
(§3.1, Algorithm 1).
4. Method
 * Self-Denoising (SD / SDi): Prompt LLM to restore original instruction using in-context
exemplars (from MNLI) and greedy decoding (t=0) (§2.1, Appendix B). SDi runs iteratively up to
5 times until the output stabilizes (§2.1).
 * Supervised Fine-Tuned Denoising (SFT-SDi): LoRA fine-tuning on AdvMix (2,882
perturbed/clean pairs from AdvGLUE and PromptBench) (§2.1, Appendix C).
 * Perplexity Smoothing: GPT-2 computes perplexity; top-10 words ranked by PPL shift are
masked and substituted using DistilRoBERTa-base beam search (B=5) (§2.2, Appendix A.2).
 * Representation Alignment: Siamese LoRA training minimizing cosine distance between clean
and perturbed instruction hidden states at the middle layer (layer 16 in Llama 3 8B; last encoder
layer in Flan-T5) (§2.4, Appendix A.4).
5. Experimental setup
 * Models: Llama 3 8B Instruct and Flan-T5 Large (§3).
 * Datasets: CoLA (1k samples), QNLI (5.5k samples), SST-2 (1.8k samples) (§3.2).
 * Six prompt templates per task (3 task-oriented, 3 role-oriented) (§3.2, Appendix E).
 * Metric: Performance Drop Rate (PDR = 1 -
\frac{\text{Acc}_{\text{perturbed}}}{\text{Acc}_{\text{clean}}}) (§3.3).
 * LoRA config: rank r=64, \alpha=16, dropout 0.1 on Q_{proj}, V_{proj}, learning rate 5e-5,
effective batch size 4, 10 epochs (Table 2).
6. Results (PDR summary, Table 1; lower is better)
| Method | TextFooler PDR | DeepWordBug PDR | Llama 3 PDR | Flan-T5 PDR | Avg. PDR
Improvement (↑) |
|---|---|---|---|---|---|
| Base LLM | 0.174 | 0.077 | 0.192 | 0.059 | — |
| PPL Smoothing | 0.182 | 0.110 | 0.214 | 0.078 | -16.3% |
| Instr. Ensembling | 0.130 | 0.037 | 0.142 | 0.026 | +33.3% |
| Repr. Alignment | 0.113 | 0.053 | 0.125 | 0.041 | +33.8% |
| SD | 0.130 | 0.016 | 0.122 | 0.025 | +41.7% |
| SDi | 0.125 | 0.015 | 0.119 | 0.021 | +44.3% |
| SFT-SDi | 0.072 | 0.030 | 0.082 | 0.021 | +59.2% |
 * Perplexity smoothing degrades performance across all subsets (-16.3% avg. improvement).
 * Clean baseline accuracy remains stable across augmentations (all within 1% of base model
80.1%, Table 3).
 * Negative correlation between instruction semantic similarity (E5-Mistral cosine similarity) and
PDR (r = -0.695 on DeepWordBug; r = -0.547 on TextFooler, Fig. 2).
7. Reproduction notes
 * Few-shot unperturbing meta-prompts require explicit exclusion constraints to avoid altering
label classes or placeholder formatting.
 * Multi-iteration loop terminates early if text is unchanged.
 * Representation alignment requires mean-pooled hidden states from the middle layer before
cosine distance loss.
8. Limitations and caveats
 * Instruction-only focus: Does not address corruption inside the input text instance itself.
 * SFT-SDi inference latency: Incurs multi-call inference overhead during the iterative loop.
 * Benchmarked strictly on binary sentence classification; generation tasks remain unexamined.
Relevance Assessment
 * Top Tier (Most Directly Relevant):
   * Paper 9 (FreeLB) & Paper 10 (SMART): Directly model embedding-space adversarial
perturbations for encoder representations, which seamlessly integrate into pre-training and
MLM-style objectives.
   * Paper 15 (BPE-Dropout): Highly relevant for morphological robustness; injects tokenization
stochasticity without requiring explicit adversarial optimization passes.
   * Paper 21 (PerturbScore): Demonstrates that continuous gradient perturbations reliably
approximate discrete token substitutions, validating the use of continuous embedding
perturbations during encoder training.
 * Secondary Tier (Evaluation & Data Augmentation):
   * Paper 1 (EDA), Paper 4 (TextFooler), Paper 5 (BERT-Attack), Paper 12 (Moradi &
Samwald): Essential for building test suites to benchmark encoder stability.
 * Lowest Tier:
   * Paper 22 (Perturbed Instructions), Paper 18 (PPCL): Focus exclusively on prompt-level /
instruction phrasing for autoregressive LLMs, which does not apply to masked encoder models.
Three Options for Stage 1 (Masked Model Training)
Option A: Subword Regularization via BPE / WordPiece Dropout
 * Mechanism: During the MLM tokenization pipeline, apply stochastic merge dropout
(probability p \in [0.1, 0.2]) to create non-deterministic subword segmentation paths for identical
words.
 * Implementation: Keep standard cross-entropy MLM loss; no adversarial gradient steps are
needed.
 * Advantage: Zero compute overhead during backpropagation; directly handles spelling
variants, prefix/suffix attachments, and morphological irregularities.
Option B: Virtual Adversarial Training on Embeddings (FreeLB / SMART style)
 * Mechanism: For each input batch, compute the gradient w.r.t. input word embeddings, perturb
the continuous vectors within an l_2 Frobenius norm ball (\Vert{}\delta\Vert{}_2 \le \epsilon), and
minimize the symmetric KL divergence / loss between clean and perturbed forward passes.
 * Implementation: Integrate a 2-step gradient ascent loop inside each MLM step, accumulating
gradients over the perturbed representations.
 * Advantage: Directly addresses the continuous-discrete representation gap shown in
PerturbScore, yielding smoother representations and higher out-of-domain generalization
without corrupting syntax.
Option C: Denoising Masked Token Replacement (Hybrid DAE + MLM)
 * Mechanism: Replace standard random masking with a dual perturbation: mask 15% of tokens
for MLM reconstruction, while subjecting an additional 5–10% of unmasked tokens to local
token swaps, deletions, or vocabulary-based random replacements.
 * Implementation: Train the encoder to predict both the masked positions and restore the
perturbed tokens to their original vocabulary indices.
 * Advantage: Teaches the encoder contextual error-correction at the representation level while
maintaining standard pre-training efficiency.
