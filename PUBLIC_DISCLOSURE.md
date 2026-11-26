# Public disclosure: browser-mediated EMV 3DS 2.x

## Status

This is the canonical short disclosure statement and standards reform summary.
It omits operational reproduction instructions and strictly separates protocol
structure, bounded observations, conditional inferences, third-party source
reviews, and proposals under [CLAIMS.md](CLAIMS.md).

## Plain-language summary

Before an online merchant charges a payment card, browser-mediated **EMV 3-D
Secure (3DS)** routes a card-verification check from the merchant checkout and
payment gateway ("3DS Requestor Environment" / 3DS Server), through a card
scheme **Directory Server (DS)**, to the issuing bank's **Access Control Server
(ACS)** ([C-01](CLAIMS.md)).

Where a client integration allows unverified queries to reach this path and
surfaces branch or reason outputs back to the caller, the composed flow exhibits
an ordering and boundary weakness (`CWE-696: Incorrect Behavior Order` leading to
`CWE-204: Observable Response Discrepancy`):

1. **Pre-authorization evaluation using the card number:** Under EMVCo Core
   v2.3.1.1, the protocol performs range routing (Reqs. 97 and 98) and issuer
   ACS authentication-availability evaluation (Req. 105) prior to challenge
   completion and prior to `ISO 8583` payment clearing ([C-02](CLAIMS.md)). In
   Core Table A.1, `acctNumber` (13 to 19 digits) is required (`AReq = R`), while
   `cardExpiryDate` and `cardSecurityCode` are conditional (`AReq = C`,
   governed by DS rules). At the same time, Core leaves Requestor-Environment
   caller admission and client response projection implementation-defined
   ([SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)).
2. **Account- and range-dependent outcomes reach the caller:** In the tested
   browser integration (which accepted replayed checkout tokens and modified/dummy
   CVV2 and expiry values at lookup), unverified probes returned distinguishable
   status classes, reason codes, challenge indicators, or initial challenge HTML
   ([C-03](CLAIMS.md), [C-04](CLAIMS.md)).
3. **Why alerts and clearing systems can miss probes:** Because probing stops at
   lookup or immediately after fetching the initial challenge form (`CReq`)
   without submitting an OTP, no `ISO 8583` payment authorization reaches
   clearing. *(Because billing records were not inspected, we make no claim
   that upstream 3DS processing is cost-free.)* EMVCo Core defines no
   cardholder SMS or push alert on lookup probes or on the Req. 220/221
   initial-`CReq` 30-second timeout (which sends `RReq` with Reason `14` and
   Cancel Indicator `05` to the DS and notifies the Requestor server at Step 18).
   On researcher-controlled test channels, no SMS, email, OTP, or push was
   observed ([COR-002](CORRECTIONS.md)); independent issuer notification systems
   and out-of-band PSD2 push flows were not instrumented.

## Canonical weakness taxonomy (MITRE CWE v5.0)

| Weakness | Protocol stage and manifestation |
|---|---|
| `CWE-696` Incorrect Behavior Order | Range routing and issuer ledger evaluation occur before verified authority for the queried account and transaction ([C-02](CLAIMS.md), [C-08](CLAIMS.md)). |
| `CWE-204` Observable Response Discrepancy | Unverified callers observe distinct response classes at lookup (`AReq`/`ARes`) or initial challenge retrieval (`CReq`/`CRes`) ([C-03](CLAIMS.md), [C-04](CLAIMS.md)). |
| `CWE-209` Information Exposure Through an Error Message | Client JSON exposes diagnostic reason codes (`05`, `08`, `13`, `98`), statuses, and pre-authorization artifacts (`CAVV`, `ECI`) ([C-03a](CLAIMS.md)). |
| `CWE-208` Observable Timing Discrepancy | Non-constant-time early drops versus remote backend queries create measurable latency separation even when text is normalized ([THREAT_MODEL.md](THREAT_MODEL.md)). |
| `CWE-602` Client-Side Enforcement of Server-Side Security | Checkout flows trust browser tokens, client telemetry, or JavaScript callbacks without cryptographic session binding ([THREAT_MODEL.md](THREAT_MODEL.md)). |
| `CWE-307` Improper Restriction of Excessive Authentication Attempts | Volumetric IP limits are challenged by rotating residential proxies and missing cross-requestor anomaly controls ([C-05](CLAIMS.md)). |

## Bounded empirical observations

A controlled study evaluated **one** browser-channel integration (PayPal
Braintree and CardinalCommerce on a researcher-controlled checkout) across seven
EMV 3DS 2.2.0 Visa and Mastercard cohorts (`A` to `G`). Seven researcher-owned
issued cards were paired with three adjacent same-range Luhn-valid comparison
inputs each, observed over five fresh off-context HTTP sessions per input (28
inputs, **140 lookup observations**, zero payment authorizations)
([C-03](CLAIMS.md), [EVIDENCE.md](EVIDENCE.md)):

- **Lookup-stage separation (`C-03`):** Six cohorts (`A` to `F`) produced
  repeatable response-class differences between the issued control and adjacent
  comparison candidates at the first lookup reply (including Reason `05`, `13`,
  `challenge_required`, frictionless `authenticate_successful`, and scheme
  attempt `authenticate_attempt_successful` vs. Reason `08`).
- **Initial-`CReq` separation (`C-04`):** One cohort (`G`) returned a uniform
  `transStatus = C` at lookup, then separated when the caller posted the initial
  `CReq` without submitting an OTP: comparison inputs returned an auto-submit
  HTML form carrying `Final CRes` with `transStatus = N`, whereas the issued
  control returned an interactive challenge/OTP interface containing masked
  contact metadata.
- **Identifier provenance (`SOURCE_CROSSWALK.md`):** Under black-box evaluation
  without internal logs, equal identifiers (`acsTransID == dsTransID`) in Cohort E
  (`authenticate_attempt_successful`) are structurally consistent with a
  DS-created response under browser Req. 411, whereas distinct identifiers
  (`acsTransID != dsTransID`) across Cohorts A to D, F, and G (including Reason
  `08` comparison inputs within participating bank ranges) are structurally
  consistent with ACS-routed processing under Req. 104. Identifier inequality
  is routing provenance, not proof of active account issuance.
- **Pre-authorization cryptographic artifacts (`C-03a`):** Selected
  challenge-free responses exposed non-empty `CAVV`, `ECI`, `paresStatus`,
  identifiers, and liability indicators to the client caller before financial
  authorization. These artifacts were not independently validated or tested for
  clearing and do not prove usability or account validity.

**Evidentiary boundaries:** Comparison-input issuance status was not
independently established. These results establish repeatable input-correlated
response separation (`CWE-204`) in the tested integration; they do not establish
account validity, payment usability, universal exposure across deployments, or
internal component attribution without backend logs ([CLAIMS.md](CLAIMS.md)).
Separate qualitative checks on Stripe and Adyen test integrations, and a 24-path
(+ 16-path extension) documentation audit, are reported separately and not
pooled with the cohort study ([EVIDENCE.md](EVIDENCE.md)).

## Threat escalation and defense gaps

1. **Generative candidate probing (`C-05`):** Where an integration exposes
   pre-authorization lookups without verified holder authority or strict
   secondary-credential validation, attackers need not rely solely on stolen
   card lists; bounded adjacent-range probing can screen candidates within a
   target BIN/IIN range.
2. **Limits of network anomaly detection (`C-06`):** Published Mastercard Patent
   Application `US 2026/0134429 A1` describes DS-tier feature scoring, trained
   models, and Reason `98` / score `998` signaling (`Authentication BIN Attack`).
   Exploratory logs observed Reason `98` during same-range Mastercard probing
   (consistent with that signal pattern, without backend proof of detector
   origin). Surfacing attack-detection codes in public JSON (`CWE-209`) lets
   adaptive callers detect blocks and adjust pacing; routing the tested
   device-data path through distributed SOCKS5 egress removed observed
   single-source blocks in an exploratory comparison
   ([SCOPE_AND_ETHICS.md](SCOPE_AND_ETHICS.md)).
3. **Superficial patches relocate signals (`C-08`):** Suppressing error text
   alone shifts leaks to initial `CReq` behavior, payload sizes, or latency
   (`CWE-208`).

## Historical precedent and public operational evidence

Unlike vendor-specific implementation bugs such as
[CVE-2021-35060](https://nvd.nist.gov/vuln/detail/CVE-2021-35060)
([advisory](https://gist.github.com/exviry/9527ce2ccdc0718d3ffd1e3ca62cf304)),
this exposure stems from pre-proof behavior ordering across the multi-party EMV
3DS protocol boundary ([C-02](CLAIMS.md), [C-08](CLAIMS.md)).

Reviewed public third-party archives establish that automated lookup-stage
card-checking code exists outside academia ([C-07](CLAIMS.md),
[EVIDENCE.md](EVIDENCE.md)):
- [Telegram Braintree 3DS/VBV handler](https://perma.cc/2QL8-9KKR) (lookup
  classification with optional SOCKS5 proxy support and membership gating);
- [Adyen-labeled Telegram checker](https://perma.cc/Z7E3-KWYT) and
  [`3dali.php`](https://perma.cc/PBA6-AUG5) (Saleor/Adyen
  `AUTHORIZATION_ACTION_REQUIRED` workflow);
- [BraintreeCHK](https://perma.cc/A25F-XA7V),
  [MeduzaV3](https://perma.cc/KV3L-7ZQG) ([video](https://perma.cc/9VUB-A9BE)),
  [pubstripe](https://perma.cc/9VSU-SGYN), and a [commercial 3DS Lookup API
  listing](https://perma.cc/G84X-8L43); and
- **Practitioner telemetry:** G+D Netcetera's *Tech Tribe* podcast (Episode
  S11E13, [*"Fraud Alert: Inside a Massive BIN Attack"*](https://youtu.be/IfHsmJHPOcs),
  Nov. 18, 2025) reported live botnets flooding 3DS rails above 10 tx/s and
  abusing pre-authorization responses for reconnaissance.

These archives establish implemented lookup-stage workflow logic and industry
incident reporting; they do not show public exploitation of the separate
initial-`CReq` differential, current live availability, accuracy, or prevalence.

## Proposed remediation: containment and architectural closure

1. **Current-version containment (`AR-01`, `AR-03` to `AR-07`, `AR-14`):** Bind
   server-side transaction context, make transitions one-use, enforce strict
   allowlists suppressing diagnostic reasons (`05`, `08`, `13`, `98`) and
   client-side `CAVV`/`ECI` outputs, return uniform constant-time reject profiles,
   and confine anomaly detection signals to authenticated backend channels
   ([MITIGATIONS.md](MITIGATIONS.md)).
2. **Future architectural closure (`AR-02`, `AR-08`):** Eliminate `CWE-696` by
   verifying independent caller authority for the exact account and operation
   before triggering card-range routing or ledger queries, returning one uniform
   state-independent response when authority is absent
   ([CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md), [P-01](CLAIMS.md),
   [P-02](CLAIMS.md)).

## Living record and corrections

The companion monograph ([arXiv:2610.32206](https://arxiv.org/abs/2610.32206))
and this repository are living records. Corrections, technical feedback, and
affected-party statements are tracked in [CORRECTIONS.md](CORRECTIONS.md). AI
tools were used strictly for editorial and formatting support
([AI_ASSISTANCE.md](AI_ASSISTANCE.md)).
