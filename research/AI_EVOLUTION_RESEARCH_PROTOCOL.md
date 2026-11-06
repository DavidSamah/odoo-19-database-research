# Evolution of Artificial Intelligence, 1940s–2026 — Historical Research Protocol

**Branch:** research/enterprise-ai-opportunities-2026  
**Checkpoint:** 1.0 — framing and source selection  
**As of:** 2026-11-06  
**Status:** Research design and an initial source-verified orientation. Not a completed literature review, global novelty search, or proof of an integration problem.

## 1. Central question

> How did AI evolve in time—not only in raw capability but in underlying mathematics, knowledge representation, training, compute, datasets, deployment interfaces, human control, and the difficulty of safely integrating the model into existing software?

We will identify transitions in AI's ability to **represent**, **learn**, **infer**, **reason**, **interact**, **act**, and **adapt**, distinguishing these ideas rather than grouping all of them under a broad term such as "intelligence."

The intended final contribution is to identify a persistent or newly emergent *engineering barrier*, then investigate whether a distinct and generalizable way to integrate real AI can remove it. No proposed invention is assumed in advance.

## 2. Chronological coverage and parallel traditions

| Era | Tentative focus | Required correction against primary sources |
|---|---|---|
| Before and through the 1940s | Mathematical logic, computation theory, early neural-network formalizations | Determine actual texts, publication dates, authors, and the difference between foundational theory and operating AI systems |
| 1950–1959 | Turing's evaluation proposal, Dartmouth proposal and 1956 workshop, symbolic problem-solving, early learning machines | Distinguish project proposals, public demonstrations and deployed applications |
| 1960–1979 | Knowledge representation, theorem proving, heuristics, DENDRAL/MYCIN, language interaction, early neural research | Avoid a single story of symbolic AI; identify separate strands |
| 1980–1999 | Expert-system commercialization, limitations, probabilistic/statistical methods, backpropagation, sequence models | Clarify what was genuinely new versus a practical revival; track failures and AI winters |
| 2000–2011 | Statistical ML, feature engineering, data infrastructure, deep neural research | Establish how datasets, GPUs and software frameworks changed practical integration |
| 2012–2016 | Large-scale deep learning, convolutional architectures, representation learning, distributed training | Separate benchmark achievements from production deployment claims |
| 2017–2021 | Transformer, self-supervised pretraining, few-shot prompting, RAG and emerging general model interfaces | What moved from bespoke training to prompting, retrieval and model serving? |
| 2022–2026 | Conversational and multimodal AI, reasoning-oriented systems, tool-use and agents, open weights, deployment ecosystems, governance | Verify dates and benchmarks; separate vendor claims, benchmark success and real-world reliability |

**Important:** Era boundaries overlap; they are organizational conveniences, not exclusive claims that one paradigm replaced another.

## 3. Six analytical lenses for every milestone

1. **Problem pressure:** What could the prior methods not solve? Was it theory, data, compute, cost, integration, correctness or usability?
2. **Technical mechanism:** What mathematical or architectural idea changed? Read the original design, inputs/outputs, learning/inference procedure, claims and explicit limitations.
3. **Enabling conditions:** What hardware, datasets, languages, libraries, funding, networks or organizational arrangements made the transition practical?
4. **Integration contract:** What did an engineer have to build to connect the AI system to a real workflow? Knowledge-base authoring, expert rules, features, inference interface, prompts, retrieval index, tool permissions, transaction boundaries or continuous evaluation?
5. **Evidence of improvement:** What actually changed, by which benchmark or deployment observation? What competing explanations or historical predecessors exist?
6. **Unresolved and inherited barriers:** What was not solved, what failed later, and what survives in 2026? Keep observed data separate from historical inference.

For *time* study use three scales: (i) invention/publication milestone, (ii) subsequent adoption and infrastructure lag, (iii) evolving costs and reliability measured over multiple years. A single timeline is necessary but not sufficient to explain causality.

## 4. Research record for an individual paper or system

- **ID / publication year / actual study period / source type / DOI or stable URL**
- **Research question and selection rationale**
- **Original claim**, without conflating it with secondary interpretations
- **Technical method** (including mathematical model where applicable)
- **Explicit assumptions / data / compute / measurement**
- **Comparison with prior art and independent reproduction**
- **How a software engineer integrated it at the time** (demonstrated vs inferred)
- **What became easier or harder in later periods**
- **Contradictory or negative historical accounts**
- **Relevance to 2026 and to Odoo, if demonstrable**
- **Evidence classification, uncertainty and next single action**

## 5. First source-verified chronological orientation (not full coverage)

These entries are anchored to original papers or authoritative archival records. The *integration implication* in each row is our **research inference**, not a claim made verbatim by the source.

| Date | Primary/authoritative source | Source-supported event | Integration implication to test, NOT a finding |
|---|---|---|---|
| Oct 1950 | Alan Turing, *Computing Machinery and Intelligence*, Mind, DOI 10.1093/mind/LIX.236.433 | Reframed a machine-intelligence question through the imitation game and digital computing | Early emphasis on computational behavior and interactive evaluation; not an enterprise integration interface |
| Aug 1955 / summer 1956 | McCarthy, Minsky, Rochester, Shannon, *Dartmouth Summer Research Project* proposal | Explicit program examining language, abstractions, reasoning, and machine learning | Multi-component AI ambitions preceded modern training or deployment tools |
| 1965 onward | DENDRAL project, recorded in Feigenbaum's 1977 IJCAI paper | Domain-expert rules and scientific hypothesis generation from chemistry data | Hand-authored knowledge and integration to specialized instruments were consequential |
| 9 Oct 1986 | Rumelhart, Hinton, Williams, *Learning representations by back-propagating errors*, Nature | Described weight adjustment of multi-layer networks for learning internal representations | Part of the burden shifts from hand-specified representations to training inputs/optimization |
| 15 Nov 1997 | Hochreiter, Schmidhuber, *Long Short-Term Memory*, Neural Computation | Addressed learning long-time dependencies in recurrent networks | Stateful sequence processing gains importance; how did application interfaces change? |
| 2012 | Krizhevsky, Sutskever, Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NeurIPS | Deep CNN image classification results with GPU-based training | More of the model's learning moves into data/compute infrastructure |
| 12 Jun 2017 | Vaswani and colleagues, *Attention Is All You Need*, arXiv | Proposed transformer sequence model built around attention and training parallelism | Changed practical sequence-model training and later foundation-model deployment |
| 2020 | Brown and colleagues, *Language Models are Few-Shot Learners*, NeurIPS | Demonstrated scaled pretrained model and few-shot task specification through text examples | Some task specialization moves from retraining to contextual instructions; inference and reliability remain open |
| 2020 | Lewis and colleagues, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS | Combined parametric language models with retrievable external knowledge | External context creates integration, provenance and update interfaces |
| 30 Nov 2022 | OpenAI, *Introducing ChatGPT* | Introduced a conversational research-preview model using human feedback training | Conversation becomes an accessible interface, not proof that all software actions are safe |
| 2026 report | Stanford HAI, *AI Index 2026* | Tracks model capabilities, infrastructure, adoption and reliability issues across preceding years | More deployment does not automatically imply solved integration reliability |

**Chronology is incomplete.** Foundational pre-1950, perceptrons, AI winter histories, probabilistic AI, 2000s software and 2023–2026 technical transitions need substantial primary-source examination before Stage 1 is complete.

## 6. Source register — primary or authoritative landing pages

- Turing, 1950 — https://academic.oup.com/mind/article/LIX/236/433/986238
- Dartmouth 1955 proposal, published archival copy and context — https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/1904/0
- Feigenbaum, 1977, historical DENDRAL account — https://ijcai.org/proceedings/1977/231
- Rumelhart/Hinton/Williams, 1986 — https://doi.org/10.1038/323533a0
- Hochreiter/Schmidhuber, 1997 — https://doi.org/10.1162/neco.1997.9.8.1735
- Krizhevsky/Sutskever/Hinton, 2012 — https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
- Vaswani and colleagues, 2017 — https://arxiv.org/abs/1706.03762
- Brown and colleagues, 2020 — https://papers.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html
- Lewis and colleagues, 2020 — https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html
- OpenAI, original ChatGPT launch post, 2022 — https://openai.com/index/chatgpt/
- Stanford HAI, 2026 AI Index — https://hai.stanford.edu/ai-index/2026-ai-index-report

Source selection is currently **orientation-level**, not a full search of scholarship, patent databases, alternative histories or current developer tools. Publication metadata and limitations must be checked for each item during the deep reading phase.

## 7. Safeguards against fictional history and biased conclusions

- Maintain publication dates and dates of developments separately; a 1993 retrospective is not evidence of a 1965 deployment without corroboration.
- Prioritize original peer-reviewed papers and archives, but actively search countervailing accounts and historical precursors.
- Record when published evidence is missing or paywalled, and what metadata is verifiable without reading the full article.
- Do not treat a marketing model launch as rigorous proof of benchmark superiority.
- Do not infer that an increase in models, compute, cost, or adoption **caused** a particular integration outcome without a study.
- Do not claim a new abstraction is globally unique absent rigorous prior-art and prototype comparisons.
- Keep this repository public-safe; do not upload proprietary datasets or private Odoo captures.
- Preserve user approval before moving from research to implementation.

## 8. Current decision

**Verified:** a historical-first study is consistent with the revised scope; this protocol and early source register were constructed from independently retrievable publisher/archival sources.

**Not yet established:** which historical approach caused integration complexity to increase or decrease; whether a common root cause exists; whether a new approach would be novel or useful.

**Next checkpoint:** Stage 1.1 — Early formal, computational and symbolic foundations, leading to 1955/56 Dartmouth. Analyze original texts with exact claims, competing accounts and engineering interfaces of that period. **Stop after the checkpoint for user review.**
