# PewDiePie: The Road to 100 Million

A YouTube / influencer analytics case study of how Felix Kjellberg's channel (PewDiePie) grew to 100 million subscribers.

> **Fact check:** PewDiePie was the first *individual* creator to reach 100M subscribers (Aug 25, 2019) and the fastest channel to get there. The first *channel* overall was T-Series (May 29, 2019).

## Deliverables

| File | What it is |
|---|---|
| `pewdiepie_research_paper.pdf` | Research paper with three quantitative models, six figures and a conceptual growth-loop diagram |
| `pewdiepie_growth_dataset.xlsx` | Dataset with live formulas (Milestones, Phases, Doubling, Counterfactual, Rivalry_Events, Sources) |
| Dashboard (published page) | Interactive-style one-page dashboard in PewDiePie red/black/white |
| `analysis.py` | Python script that recomputes the models and regenerates the paper's figures |

## Key findings

- Doubling time lengthened from about 6 months (2013-14) to about 33 months, then stayed constant for 25M-50M (32.8 mo) and 50M-100M (32.5 mo).
- Growth was roughly linear at 0.8-1.0M subscribers/month from 2014 to 2018.
- The last 25M (Dec 2018 to Aug 2019) came at about 2.9M/month, about 2.8x the prior phase.
- Extrapolating earlier trends gives 100M in Dec 2020 (Trend B) to Jun 2021 (Trend A), so the actual date was about 15-22 months earlier.

## Method

1. **Phase velocity:** net gain / months between milestones (months = days / 30.4375).
2. **Doubling time:** months to double the subscriber base.
3. **Counterfactual:** Trend A is an OLS line through the 25M, 50M and 75M milestones; Trend B extends the 2017-18 pace from 75M.

## Dataset notes

- Seven milestones: 1M, 10M, 20M, 25M, 50M, 75M, 100M.
- Blue cells are hardcoded inputs, black cells are formulas, green cells are cross-sheet links.
- Each milestone has a source and confidence rating. The 1M, 25M and 75M dates rely on a single secondary source (BloggersPassion), so they are rated Medium.
- The dashboard merges 10M-25M into one phase (about 1.8M/month); the paper and workbook split it into 10M-20M and 20M-25M.

## Limitations

- Only seven observations, with averaged velocities between them.
- Causal claims about the T-Series rivalry are interpretive; milestone data cannot isolate causes.
- Trend A uses three points, so its R-squared (0.992) is descriptive only.

## Reproduce

```bash
pip install matplotlib numpy
mkdir -p figs
python analysis.py   # prints model results, writes figs/f1.png ... f6.png
```

Open the Excel file and edit the blue input cells on `Milestones` to see all models update.

## Sources

1. Social Blade, "PewDiePie becomes first YouTuber to reach 50 million subscribers"
2. Wikipedia, "List of most-subscribed YouTube channels"
3. VidIQ, "PewDiePie: The Moment He Hit 100,000,000 YouTube Subscribers"
4. Mein-MMO, "YouTube: PewDiePie is the 1st person with 100 million subs"
5. BloggersPassion, "PewDiePie net worth"
6. Business Insider India, career profile of PewDiePie
