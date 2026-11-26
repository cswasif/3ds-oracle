# Disclosure timeline

Last updated: Nov. 26, 2026.

This is a concise, researcher-reported chronology matching the companion
monograph ([arXiv:2610.32206](https://arxiv.org/abs/2610.32206), Appendix
disclosure table). A tracker documents contact; it does not independently
validate a technical claim or prove the presence or absence of a patch. See
[CORRECTIONS.md](CORRECTIONS.md).

| Date | Party | Channel and reference | Researcher-reported outcome |
|---|---|---|---|
| Since 2018 | Independent research | Prior empirical testbed & threat modeling | Initiated independent payment-security measurement framework. |
| 2020 to 2025 | Longitudinal audit | Passive EMVCo spec & public CaaS observation | Audited EMVCo v2.1 to v2.3 specs and passive public threat artifacts with zero financial purchases or illicit interaction. |
| Apr. 14 to 15, 2026 | PayPal / Braintree | HackerOne `#3673424` | Closed as Informative (component-scope standard integration behavior); technical appeal submitted. |
| Apr. 16 to Aug. 31, 2026 | MITRE CVE Program | CVE request `2026835` | Formal intake acknowledged; full technical dossier submitted; closed without CVE assignment on Aug. 31, 2026. |
| May 16 to 18, 2026 | CERT/CC | `VRF#26-05-CJVGG` | Coordination declined; recommended setting target disclosure date and proceeding publicly. |
| Jun. 1 to 11, 2026 | VulnCheck CNA | Alternate CNA review | Declined under intended-behavior reasoning; deferred to CERT/CC on Jun. 11, 2026. |
| Jun. 9, 2026 | Braintree maintainers | GitHub private report `GHSA-xjwr-jwm2-wvjr` | Submitted for maintainer review (`braintree-web`); finder credit recorded Jun. 11; no written patch notice received. |
| Aug. 6 to 10, 2026 | CERT/CC & CISA | `VRF#26-08-XWHPS` / `CCASE0209885` | CERT/CC reiterated public disclosure recommendation; parallel CISA case issued automated acknowledgment. |
| Aug. 27 to Sep. 3, 2026 | EMVCo | Inquiry `#20260827-17621D` | Submitted for specification review; processed under general non-confidential Terms of Use. |
| Aug. 29, 2026 | Visa | HackerOne `#3978615` | Closed as Informative (endpoint designed to route authentication challenges within component scope). |
| Aug. 30, 2026 | American Express | HackerOne `#3979021` | Accepted into active triage review. |
| Aug. 29 to Sep. 9, 2026 | Mastercard | Bugcrowd `8d647a18` | Closed as Not Applicable (cross-party architectural scope outside isolated bounty program). |
| Sep. 1 to Oct. 15, 2026 | Visa, Mastercard, Amex | Direct scheme security contacts | Protocol memoranda, Reason 98 comparison notes, and patent `US 2026/0134429 A1` addenda routed internally for technical review. |
| Oct. 24, 2026 | EMVCo | Inquiry `#20260827-17621D` | Submitted preprint draft for non-confidential technical review. |
| Oct. 27, 2026 | Public | Monograph `arXiv:2610.32206` and LinkedIn article | Public disclosure after more than 180 days of coordinated outreach. |
| Nov. 9, 2026 | Public record | Repository release | Added `CReq`-stage correction, scope limits, and proposed consortium response (`COR-001`, `COR-002`). |
| Nov. 11, 2026 | Public record | Living-record & AI notice | Added AI-writing disclosure, living-record commitment, and claim precision rules (`COR-003` to `COR-005`). |
| Nov. 14 to 17, 2026 | CISA CVD / VINCE-NT | `CASE#121099` (prior `CCASE0209885`) | Submitted multi-party dossier; CISA confirmed on Nov. 17 that multi-party protocol specifications fall outside CVE/sovereign coordination thresholds and advised direct vendor engagement; authors documented EMVCo's lack of public VDP intake. |
| Nov. 22, 2026 | EMVCo | Inquiry `#20260827-17621D` | Updated inquiry with published arXiv link, living repository, Anti-Oracle Profile, and Conformance Framework. |
| Nov. 24, 2026 | Public record | Repository taxonomy update | Aligned disclosure canonically to MITRE CWE v5.0 and eliminated Unicode em-dashes (`COR-006`). |
| Nov. 26, 2026 | Public record | Clarity & consistency audit | Rewrote `README.md` and `PUBLIC_DISCLOSURE.md` in plain English for broader technical/policy readability and synchronized `SCOPE_AND_ETHICS.md`, `CLAIMS.md`, and `TIMELINE.md` (`COR-007`). |

## Correction record

Earlier public wording described one cohort only as uniformly challenge-required.
The corrected statement is that it was uniform at lookup (`transStatus = C`) but
distinguishable after the initial `CReq` (`COR-001`). Earlier categorical
language about cardholder alerts was narrowed to the notification behavior
observed on researcher-controlled channels (`COR-002`).

Older wording also elevated third-party source snapshots without defining what
the source did and did not establish. The corrected record links reviewed
archives and records their implemented workflow evidence, while retaining strict
limits on execution, current operation, accuracy, use, and prevalence (`COR-004`).

Update this file only with dated, sourced corrections, responses, closure
artifacts, or changes to a declared action request.
