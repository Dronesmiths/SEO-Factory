# TASK: REINFORCE (Weekly Engine)

## Objective
Compounding SEO growth by re-optimizing existing content based on live GSC data.

## Step 1: Data Awareness
1. Load `ANALYTICS/GSC_PULL.json`.
2. Identify "Opportunities" in `OPPORTUNITIES.json`.

## Step 2: Optimization Thresholds
Apply the following deterministic logic:
- **High Impressions + Low CTR (< 2%)**: Rewrite H1 and Meta Description for better clickability.
- **Rising Queries (Position 11-30)**: Expand intro paragraph to include rising semantic keywords.
- **Declining Pages**: Add 1 new Stat Block + Update 2 FAQ questions with fresh intent.
- **Striking Distance (Position 8-15)**: Add a new Data Table + Expand body content by 300 words.

## Step 3: Link Weighting (Feed the Head)
- **Authority Flow**: New pages generated during the daily cycle MUST link to pages flagged as "Top Performers" in `GSC_PULL.json`.
- **Link Score**: Boost internal linking weight for pages in the top 5 ranking positions to protect their lead.

## Step 4: Execution Cycle
1. Run Re-Optimization Prompt.
2. Update `/blog/{slug}/index.html` (Additive changes only).
3. Log changes in `REGISTRY.json` (`last_optimized` field).
4. Commit to `main`.

## Constraints
- Max 4 page re-optimizations per cycle.
- Do NOT delete existing sections.
- Structural changes must respect `THEME.json`.
