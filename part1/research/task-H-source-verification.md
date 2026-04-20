# Task H: Source Verification Report

Date: 2026-04-19

This report verifies the accessibility and currency of sources cited in two project reports:
- `learning_unlearning.md`
- `research-harness-engineering.md`

---

## H-1: Key URL and Version Verification

### Priority Sources Status Table

| Source | URL Tested | HTTP Status | Last Updated | Notes |
|---|---|---|---|---|
| OpenAI Practical Guide for Building Agents | `openai.com/index/practical-guide-to-building-agents/` | **403 Forbidden** | Unknown | All tested OpenAI URL variants (blog, index, platform docs, cdn PDF) return 403 or 404. The page exists but OpenAI blocks automated/non-browser access. The guide was originally published in early 2025. Manual browser verification required. Consider linking directly to the OpenAI Agents SDK docs or the PDF if a stable URL can be confirmed. |
| Anthropic Building Effective Agents | `anthropic.com/engineering/building-effective-agents` | **200 OK** | April 13, 2026 | Accessible and actively maintained. Originally published December 19, 2024; most recently updated April 13, 2026. Still current and authoritative. |
| NIST AI RMF GenAI Profile (NIST.AI.600-1) | `airc.nist.gov/Docs/1` and related paths | **404 Not Found** | Unknown | The document identifier NIST.AI.600-1 is confirmed via the NIST AI Resource Center homepage (airc.nist.gov), which lists it as "Generative AI Profile." However, direct document links return 404 -- the URL structure appears to have changed. The NIST AI Resource Center confirms the AI RMF 1.0 is currently being revised. The PDF URL `nist.gov/system/files/documents/2024/07/26/NIST.AI.600-1.pdf` also returns 404. Recommend navigating from `airc.nist.gov/Home` to locate the current download link. |
| NIST Agent Hijacking Technical Blog | `nist.gov/artificial-intelligence/agent-hijacking-critical-threat-ai-agent-systems` | **404 Not Found** | N/A | The original cited URL is broken. However, a closely related post was found at `nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition`, published **March 23, 2026**. This post covers agent hijacking (indirect prompt injection) and reports on a red-teaming competition with 250,000+ attack attempts against 13 frontier models. **Recommended replacement URL.** |
| OWASP LLM Top 10 | `genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/` | **200 OK** | April 28, 2025 | Accessible. This is the **2025 version**, published November 18, 2024, last updated April 28, 2025. Current and authoritative. |
| Martin Fowler / Harness Engineering | `martinfowler.com/articles/harness-engineering.html` | **200 OK** | April 2, 2026 | Accessible. Authored by Birgitta Bockeler. Published April 2, 2026 (updated from February 2026 memo). Current and authoritative. |

### Additional Sources from `research-harness-engineering.md`

| Source | URL | HTTP Status | Last Updated | Notes |
|---|---|---|---|---|
| arXiv 2604.12311 (Vibe Coding study) | `arxiv.org/abs/2604.12311` | **200 OK** | April 14, 2026 | Accessible. Paper by S M Jamil Uddin. Current. |
| Stanford CS146S Bulletin | `bulletin.stanford.edu/courses/2274401` | **200 OK** (content not rendered) | Unknown | Page loads but content is JavaScript-rendered; course listing confirmed to exist. |
| GitHub Vibe Coding Tutorial | `docs.github.com/en/copilot/tutorials/vibe-coding` | **200 OK** | Current (references Claude Sonnet 4.5) | Accessible and current. |
| GitHub Cloud Agent Docs | `docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent` | **200 OK** | Current (expiry 2026-04-21) | Accessible and current. |
| arXiv 2603.05344 (OPENDEV) | `arxiv.org/abs/2603.05344` | **200 OK** | March 13, 2026 | Accessible. Marked as work in progress. |
| Simon Willison vibe coding post | `simonwillison.net/2025/Mar/19/vibe-coding/` | **200 OK** | March 19, 2025 | Accessible and current. |
| arXiv 2512.14012 (Developers Don't Vibe) | `arxiv.org/abs/2512.14012` | **200 OK** | December 16, 2025 | Accessible and current. |
| Stack Overflow 2025 Survey (AI) | `survey.stackoverflow.co/2025/ai` | **200 OK** | 2025 | Accessible. Trust findings confirmed: 46% distrust AI accuracy, only 33% trust it. |
| GitClear Research Page | `gitclear.com/recent_ai_developer_productivity_code_quality_research` | **403 Forbidden** | Unknown | Blocked for automated access. Manual verification required. |

### Summary for H-1

- **Accessible and current (no action needed):** Anthropic guide, OWASP LLM Top 10 (2025), Martin Fowler article, arXiv papers (3), GitHub docs (2), Simon Willison, Stack Overflow survey
- **Accessible but blocked for automated fetch (manual check recommended):** OpenAI guide, GitClear
- **URL broken -- replacement found:** NIST agent hijacking blog (use CAISI research blog URL from March 2026)
- **URL broken -- needs manual navigation:** NIST AI RMF GenAI Profile (NIST.AI.600-1) -- navigate from `airc.nist.gov/Home`

---

## H-2: Harness Documentation Currency

### Documentation Status Table

| Document | URL Tested | Status | Notes |
|---|---|---|---|
| Harness Agents Documentation | `developer.harness.io/docs/category/agents` | **Accessible (redirected)** -- but content is **GitOps Agents**, not AI Agents | The "agents" category at developer.harness.io covers **GitOps Agents** (ArgoCD-based infrastructure agents), not AI-powered coding or DevOps agents. This is a different product from what is discussed in the reports. Topics include agent installation, OpenShift operator, disaster recovery, and ArgoCD upgrades. |
| Harness AIDA Documentation | Multiple paths tested (`/platform/harness-aida/`, `/category/harness-aida`, `/aida-overview`) | **All return 404** | AIDA documentation appears to have been **removed or restructured**. The Harness developer docs homepage (25+ categories) shows no dedicated AIDA section. The product page (`harness.io/products/aida`) also returns 404. **AIDA may have been rebranded.** |
| Harness AI Product Page | `harness.io/products/aida` vs `harness.io/ai` | `/products/aida` returns **404**; the current page is the **Harness AI** product page | Harness appears to have **rebranded from "AIDA" to "Harness AI"**. The current product page describes an "AI-native software delivery platform" with specialized agents, agentic flows, and a "Software Delivery Knowledge Graph." AIDA is not mentioned. Current references (Citi, United Airlines) and 2026 dating confirm this is the active product. |
| Harness Effective Prompting Guide | `developer.harness.io/docs/infra-as-code-management/devops-agent/effective-prompting` | **404 Not Found** | URL structure suggests it was under IaCM/DevOps Agent, but the entire path is broken. The developer docs sitemap shows no `devops-agent` or `effective-prompting` entries. **Likely removed or restructured.** |
| Harness Skills Operating Model | `developer.harness.io/docs/infra-as-code-management/devops-agent/devops-agent-skills` | **404 Not Found** | Same situation as Effective Prompting. No sitemap entry found. **Likely removed or restructured.** |
| Harness Privacy/Data Handling | `developer.harness.io/docs/platform/harness-aida/aida-security-faqs` | **404 Not Found** | AIDA-specific security/privacy FAQ is gone. Privacy information may now be under the broader Harness AI or platform security documentation. **Needs manual investigation.** |
| Harness Training / University | `university.harness.io` -> `developer.harness.io/university` | **200 OK (redirected)** | Accessible. Offers 15+ self-paced courses across product modules, plus instructor-led training and certifications. Last updated March 1, 2024. Still active. Note: `university.harness.io` now redirects to `developer.harness.io/university`. |

### Key Finding: AIDA Rebranding

The most significant finding is that **Harness appears to have rebranded AIDA to "Harness AI"**. Evidence:
1. All AIDA-specific documentation URLs return 404
2. The AIDA product page (`harness.io/products/aida`) returns 404
3. The current Harness AI page describes agentic capabilities without mentioning "AIDA"
4. The developer docs homepage lists no AIDA category
5. The sitemap contains no AIDA-related URLs
6. The DevOps Agent documentation (which included Effective Prompting and Skills) appears entirely removed

**Recommendation:** All Harness AIDA references in the reports should be updated to reflect the current "Harness AI" branding and documentation structure. The specific cited documents (Effective Prompting, Skills, privacy/data handling) need to be re-located under the new product architecture, or noted as no longer publicly available.

### Summary for H-2

| Document | Status | Action Required |
|---|---|---|
| Harness Agents docs | **Current but different product** (GitOps, not AI agents) | Clarify which "agents" product is referenced |
| Harness AIDA overview | **Deprecated / Rebranded** to Harness AI | Update all references |
| Harness Effective Prompting | **Not found** (404) | Locate replacement or mark as unavailable |
| Harness Skills operating model | **Not found** (404) | Locate replacement or mark as unavailable |
| Harness privacy/data handling | **Not found** (404) | Locate replacement under Harness AI |
| Harness Training / University | **Current** | Update URL to `developer.harness.io/university` |

---

## H-3: Korean Regulatory Document Currency

### Verification Approach

Korean government websites (goe.go.kr, kcc.go.kr, nia.or.kr) use heavy JavaScript rendering and redirect chains that prevent automated content extraction. All three sites loaded only redirect scripts. The following assessment is based on organizational web presence verification and known publication timelines.

### Document Status Table

| Document | Issuing Organization | Website Accessible | Known Version | Status | Notes |
|---|---|---|---|---|---|
| 생성형 인공지능 활용교육 교사용 가이드라인 | 경기도교육청 (Gyeonggi Provincial Office of Education) | `goe.go.kr` -- **Accessible** (JS redirect) | 2024 version cited in report | **Likely current but unverifiable via automated fetch** | The website is operational (redirects to `/goe/main.do`). The guideline was issued as part of the 2024 education policy cycle. Korean education AI guidelines are typically updated annually. A 2025 or 2026 revision may exist. **Manual verification required** by searching the 경기도교육청 site or the Korean education policy portal. |
| 생성형 인공지능 서비스 이용자 보호 가이드라인 | 방송통신위원회 (Korea Communications Commission, KCC) | `kcc.go.kr` -> `kmcc.go.kr` -- **Redirected** | 2024 version cited in report | **Organization restructured; URL changed** | KCC website now redirects from `kcc.go.kr` to `kmcc.go.kr` (한국방송통신위원회). This redirect (302) suggests an organizational or domain restructuring. The guideline may still be valid but the issuing body's web presence has changed. **Manual verification required** at the new domain. |
| 생성형 AI 윤리 가이드북 | 한국지능정보사회진흥원 (NIA, National Information Society Agency) | `nia.or.kr` -- **Accessible** | 2024 version cited in report | **Organization site active; document not found on homepage** | The NIA website is confirmed operational. The guide was not found in the main navigation or homepage content. It may be hosted in a sub-portal (e.g., AI Ethics Center) or a publication archive. **Manual verification required** by searching the NIA knowledge base or AI ethics portal. |

### Key Observations for Korean Documents

1. **JS-heavy government sites**: All three Korean government websites use JavaScript-based rendering and redirect chains, making automated verification impossible. Manual browser-based checks are required.

2. **KCC domain change**: The Korea Communications Commission has changed its primary domain from `kcc.go.kr` to `kmcc.go.kr`. This is a significant change that should be reflected in citations.

3. **Annual update cycles**: Korean government AI guidelines typically follow annual policy cycles. The 2024 versions cited in the reports may have been superseded by 2025 or 2026 editions. Key search terms for manual verification:
   - "경기도교육청 생성형 AI 가이드 2025" or "2026"
   - "방송통신위원회 생성형 AI 가이드라인 최신"
   - "한국지능정보사회진흥원 AI 윤리 가이드북 개정"

4. **Potential policy evolution**: Korea's AI regulatory landscape has been actively evolving. The 「인공지능 기본법」 (AI Framework Act) and related regulations may have introduced new or updated guidelines that supersede the cited documents.

### Recommended Actions for Korean Documents

| Document | Action |
|---|---|
| 경기도교육청 가이드라인 | Manually search `goe.go.kr` for the latest version. Check if a 2025/2026 edition exists. |
| 방송통신위원회 가이드라인 | Update domain reference from `kcc.go.kr` to `kmcc.go.kr`. Manually verify document currency at new domain. |
| NIA 윤리 가이드북 | Search NIA's publication archive or AI Ethics Center portal for the latest edition. |

---

## Overall Recommendations

### Sources Requiring Immediate Attention

1. **Harness AIDA documentation (all references)**: Product appears rebranded to "Harness AI." All AIDA-specific doc URLs are broken. This is the highest-priority update needed across both reports.

2. **NIST Agent Hijacking blog**: Original URL is broken. Replace with the CAISI Research Blog post (March 2026): `https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition`

3. **NIST AI RMF GenAI Profile (NIST.AI.600-1)**: Direct links are broken. Note that AI RMF 1.0 is currently being revised. Navigate from `airc.nist.gov/Home` to find the current download link.

4. **KCC domain change**: Update `kcc.go.kr` references to `kmcc.go.kr`.

### Sources Confirmed Current (No Action Needed)

- Anthropic Building Effective Agents (updated April 2026)
- OWASP LLM Top 10 2025 edition
- Martin Fowler / Harness Engineering article
- All arXiv papers (2604.12311, 2603.05344, 2512.14012)
- GitHub documentation (vibe coding tutorial, cloud agent)
- Simon Willison blog posts
- Stack Overflow 2025 Survey
- Harness University/Training (with URL update to `developer.harness.io/university`)

### Sources Requiring Manual Browser Verification

- OpenAI Practical Guide for Building Agents (blocks automated access)
- GitClear research page (blocks automated access)
- All three Korean regulatory documents (JS-rendered government sites)
