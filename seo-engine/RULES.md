# SEO Engine Rules (Universal)

## Daily limits
- Max new pages/day: 4

## Where pages go
- Create new pages at: /blog/{slug}/index.html

## Content rules
- Minimum 1200 words
- 1 H1, then H2/H3 structure
- Include a 5-question FAQ at bottom
- Avoid duplicate topics already in REGISTRY.json
- Avoid cannibalizing pillar URLs

## Internal linking rules
- Every new page must link:
  - Up to its pillar page (1 exact match anchor)
  - To 2 sibling support pages already in registry

## Site updates required
- Update sitemap.xml with new URLs
- Append new URLs to REGISTRY.json

## Commit rules
- Commit directly to main
- Commit message format:
  "SEO: add {N} support pages for {pillar_slug}"
