# Prompt: Daily SEO Content Generation

**Role**: Expert SEO Content Strategist

**Context**: 
Load the following context:
- COMPANY.json
- PILLARS.json
- RULES.md
- STATE.json
- REGISTRY.json

**Objective**: 
Generate content for up to 4 support pages as defined in TASK_DAILY.md.

**Instructions**:
1. Identify the weekly focus pillar and rotation pillars.
2. Select appropriate support page types for each pillar.
3. For each page:
   - Match the brand tone.
   - Follow the layout structure in TEMPLATES/page-template.html.
   - Ensure it's at least 1200 words.
   - Include a 5-question FAQ at the bottom.
   - Link up to the pillar page and 2 sibling pages from REGISTRY.json.
4. Output the raw HTML code for each page.
5. Provide the updated REGISTRY.json entry.
