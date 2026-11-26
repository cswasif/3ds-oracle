# The 3DS Oracle

> **Public disclosure record and standards proposal.** This repository explains
> an architectural flaw in browser-based EMV 3-D Secure (3DS) and proposes
> technical fixes. It contains no attack tooling, real card data, live endpoint
> recipes, reusable tokens, or raw network captures.

- **Research monograph:** [arXiv:2610.32206](https://arxiv.org/abs/2610.32206)
- **Short formal statement:** [PUBLIC_DISCLOSURE.md](PUBLIC_DISCLOSURE.md)
- **Quick navigation:** [Repository Map](#repository-structure) | [Claims Ledger](CLAIMS.md) | [Corrections](CORRECTIONS.md)

## Start Here: What Is This Vulnerability? (Plain English)

When you pay online with a card, the merchant often runs a background check called
**EMV 3-D Secure (3DS)** *before* asking your bank to charge any money. That
check passes through three organizations:

```text
Caller / Checkout  -->  Payment Gateway  -->  Card Network (DS)  -->  Issuing Bank (ACS)
   (unauthenticated)      (forwards query)     (checks card range)    (checks card account)
```

In a normal payment, this step decides whether the purchase can go through silently
("frictionless") or needs an extra verification step such as a one-time passcode
("challenge") ([C-01](CLAIMS.md)).

### The Core Mistake

Because this check happens **before any financial charge** and **without proof
that the caller holds the card** (`CWE-696: Incorrect Behavior Order`), an automated
script at a public checkout can grab a normal public checkout token, enter any
16-digit card number with dummy expiration dates and CVVs (the 3DS lookup message
does not require CVV validation, under EMVCo Core Table A.1 and Req. 105), and
read how the payment system reacts ([C-02](CLAIMS.md)).

Instead of returning one uniform response to an unverified caller, the system can
return **different client-visible answers depending on the card number tested**
(`CWE-204: Observable Response Discrepancy`) ([C-03](CLAIMS.md)):

1. **Separated at the first lookup reply (6 of 7 tested cohorts):**
   In six tested bank/network cohorts, a known real card triggered outcomes such
   as *"challenge required"*, *"frictionless approved"* (even returning
   cryptographic authentication fields such as `CAVV` and `ECI`), *"expired card"*
   (Reason `05`), or *"not enrolled"* (Reason `13`), whereas adjacent test
   numbers sharing the same bank prefix returned *"no card record"* (Reason `08`)
   ([C-03](CLAIMS.md), [C-03a](CLAIMS.md)).
2. **Separated at the next step even when lookup looked identical (Cohort G):**
   One cohort tried to mask the lookup reply by answering *"challenge required"*
   (`transStatus = C`) for every tested card number. However, when the script
   posted the very first challenge-screen request (`CReq`) *without entering any
   OTP*, the real card returned an interactive bank verification webpage (which
   even displayed masked email and phone hints), while every adjacent candidate
   returned a hidden auto-submitting denial (`transStatus = N`)
   ([C-04](CLAIMS.md)).

### Why Transaction IDs Also Reveal Routing

Under EMVCo protocol rules (Req. 104 and Req. 411):
- When the **card network Directory Server** answers on the bank's behalf (such as
  blocking an unassigned card range with Reasons `80` or `87`, dropping a
  suspected sweep with Reason `98`, or issuing an attempted stand-in response as
  seen in Cohort E), the Directory Server sets the two transaction identifiers
  equal (`acsTransID == dsTransID`).
- When the request passes the range check and is routed onward to an **issuing
  bank's Access Control Server** (which happened for both real cards and Reason
  `08` "no card record" candidates inside a bank's participating BIN range in our
  study), the two identifiers are distinct (`acsTransID != dsTransID`).

Combined with status and reason codes, these fields help an outside caller infer
whether a query stopped at the card network or reached an issuing bank
([SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)), though identifier inequality alone
is routing-provenance evidence rather than a guarantee of active issuance.

### Why Alerts and Fraud Systems Often Miss It

- **No payment charge occurs:** Because the probe stops at 3DS lookup (or after
  loading the initial challenge HTML without selecting an OTP method), no
  clearing-stage financial authorization (`ISO 8583`) reaches the bank. Merchant
  processing fees do not trigger, and bank post-authorization fraud engines are
  blind to upstream lookup probes.
- **Lookup timeouts are internal to the network:** EMVCo rules do not specify an
  SMS or push alert to the cardholder on a lookup-only request or on the
  30-second initial challenge timeout (Req. 220 and 221 specify an internal
  `RReq` timeout report from the bank ACS to the Directory Server). On our
  monitored test channels, no SMS, email, OTP, or push notification was observed
  during these bounded probes ([COR-002](CORRECTIONS.md)); independent bank alert
  systems and out-of-band PSD2 push flows were not instrumented and can behave
  differently.

### Why This Matters: Beyond Stolen Card Dumps

The payment industry has often assumed attackers only test already-stolen card
lists purchased after data breaches. Because pre-authorization 3DS lookup accepts
candidate 16-digit numbers without real CVVs or payments, attackers can also use
these responses to screen algorithmically generated candidates within a target
bank prefix (BIN) ([C-05](CLAIMS.md)). Separate public carding tools show
automated scripts already parsing 3DS pre-authorization statuses at checkout
([C-07](CLAIMS.md)).

## What the Bounded Study Proved (And Its Strict Limits)

To keep testing safe and verifiable, the primary controlled evaluation tested
**one** browser-channel checkout integration (PayPal Braintree and
CardinalCommerce on a researcher-controlled checkout) across **seven** Visa and
Mastercard bank/card-range cohorts (`A` to `G`). Each of 7 researcher-owned
issued cards was paired with 3 adjacent Luhn-valid comparison numbers from the
same range (28 inputs total, each tested across 5 fresh sessions = **140 lookup
observations**, with zero payment authorizations) ([C-03](CLAIMS.md),
[EVIDENCE.md](EVIDENCE.md)).

- **Six cohorts (`A` to `F`)** separated the real card from adjacent candidates at
  the first lookup reply.
- **One cohort (`G`)** returned uniform `transStatus = C` at lookup, then
  separated immediately at the first `CReq` step (`interactive OTP HTML` vs.
  auto-submit `CRes` with `transStatus = N`) ([C-04](CLAIMS.md)).
- **Selected frictionless and attempted responses** exposed non-empty `CAVV`,
  `ECI`, `paresStatus`, and liability indicators in client-visible output before
  any payment clearing ([C-03a](CLAIMS.md)).

**Important scope limits:** The adjacent comparison candidates did not have
independently verified issuance status, repetitions measured within-input
stability rather than population rate, and the study does not estimate universal
prevalence, internal component attribution without backend logs, or downstream
payment usability ([CLAIMS.md](CLAIMS.md)). Separately reported qualitative
checks on Stripe and Adyen test integrations, and a frozen documentation audit
covering 24 core 3DS integration paths (plus a 16-path extension), provide
cross-ecosystem context and are not pooled with the 7-cohort study
([EVIDENCE.md](EVIDENCE.md)).

## Why Existing Defenses Fall Short (And Why It Remains Unfixed)

1. **IP rate limiting is bypassed:** Archived carding tools pair lookup probes with
   rotating residential SOCKS5 proxies, spreading queries across ordinary home IP
   addresses (`CWE-307`) ([C-07](CLAIMS.md)).
2. **Bank fraud scoring watches the wrong stage:** Clearing-stage fraud engines
   monitor financial authorizations, not pre-authorization 3DS lookups.
3. **In-band attack signals help bots tune evasion (`US 2026/0134429 A1`):**
   Mastercard's published patent application describes Directory Server scoring to
   flag an "authentication BIN attack" and communicate risk codes such as Reason
   `98` ([C-06](CLAIMS.md)). Exploratory log reviews observed Reason `98` during
   repeated same-range Mastercard lookups (without backend traces proving which
   component generated it). When gateways copy diagnostic reason codes directly
   into readable client JSON (`CWE-209`), callers see immediately when a rule
   triggered and can adjust proxy rotation ([MITIGATIONS.md](MITIGATIONS.md)).
4. **Superficial patches relocate the oracle:** Hiding lookup errors without fixing
   pre-proof execution order moves the leak to the initial `CReq`, payload size,
   or network response timing (`CWE-208`) ([C-08](CLAIMS.md)).

**The ecosystem trap:** Merchants rely on PCI DSS SAQ A iframe outsourcing, which
leaves gateway-hosted 3DS lookup endpoints outside merchant audits; PCI 3DS Data
Matrix v1.3 omits PANs, `transStatusReason`, transaction IDs, and removed
`CAVV` from protected 3DS elements; EMVCo certification tests syntax using
non-Luhn test ranges; and sovereign vulnerability coordinators (`CISA VINCE-NT
CASE#121099`, `CERT/CC VRF#26-05-CJVGG`) determined multi-party protocol specs
fall outside single-vendor CVE scope while EMVCo has no public VDP
([TIMELINE.md](TIMELINE.md)). Consequently, gateways and networks process lookup
volume while issuing banks and cardholders bear downstream reissuance and fraud
exposure.

## Public Operational Evidence

Reviewed third-party archives confirm that automated lookup-stage classification
has been built into public tooling, though these snapshots establish available
code workflows rather than prevalence, accuracy, or live operational volume
([C-07](CLAIMS.md), [EVIDENCE.md](EVIDENCE.md)):

- [Archived Telegram Braintree 3DS handler](https://perma.cc/2QL8-9KKR): obtains
  merchant-scoped Braintree authorization from a public checkout, submits card
  data, invokes 3DS lookup, classifies returned status, and routes via SOCKS5.
- [Adyen-labeled Telegram checker](https://perma.cc/Z7E3-KWYT) and
  [`3dali.php`](https://perma.cc/PBA6-AUG5): submits encrypted checkout data
  and classifies Saleor `AUTHORIZATION_ACTION_REQUIRED` as an active "3D Card"
  (limits documented in [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)).
- [BraintreeCHK](https://perma.cc/A25F-XA7V),
  [MeduzaV3](https://perma.cc/KV3L-7ZQG) ([promo](https://perma.cc/9VUB-A9BE)),
  [pubstripe](https://perma.cc/9VSU-SGYN), and a [commercial 3DS Lookup API
  listing](https://perma.cc/G84X-8L43).
- **Industry report:** In G+D Netcetera's *Tech Tribe* podcast (Episode S11E13,
  [*"Fraud Alert: Inside a Massive BIN Attack"*](https://youtu.be/IfHsmJHPOcs),
  Nov 18, 2025), practitioners described live botnets probing 3DS rails above 10
  transactions per second and abusing pre-authorization responses for bank
  reconnaissance.
- **Historical precedent:** [CVE-2021-35060](https://nvd.nist.gov/vuln/detail/CVE-2021-35060)
  ([advisory](https://gist.github.com/exviry/9527ce2ccdc0718d3ffd1e3ca62cf304))
  showed an earlier enrollment-endpoint enumeration oracle in one vendor's ACS
  software (`CWE-209`). Our work shows that protocol-boundary leakage spans the
  multi-party specification flow, not just one vendor URL.

## How To Fix It

Permanent remediation requires separating immediate risk reduction from true
architectural closure ([C-08](CLAIMS.md), [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md)):

1. **Immediate Containment (`AR-01`, `AR-03` to `AR-07`, `AR-14`):** Lock checkout
   context server-side, enforce single-use state transitions, strip internal
   reason codes (`08`, `98`), `CAVV`, and `ECI` from browser/API outputs
   (`CWE-209`), normalize unadmitted responses with constant-time handling
   (`CWE-204`, `CWE-208`), and keep ML anomaly flags backend-only (`CWE-307`).
2. **Architectural Closure (`AR-02`, `AR-08`):** Require verified query authority
   bound to the exact account and transaction *before* triggering card-range
   routing or issuer ledger lookups (`CWE-696`), or return one identical,
   state-independent response when authority is absent.

## Repository Structure

| Document | Purpose |
|---|---|
| [PUBLIC_DISCLOSURE.md](PUBLIC_DISCLOSURE.md) | Canonical short formal disclosure statement |
| [CLAIMS.md](CLAIMS.md) | Claim ledger distinguishing proof, bounded data, and proposals |
| [THREAT_MODEL.md](THREAT_MODEL.md) | Channel model, CWE mapping, and security objective |
| [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md) | EMVCo, PCI, CVE, and patent reference limits |
| [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md) | Proposed Anti-Oracle Requirements (`AR-01` to `AR-08`, `AR-14`) |
| [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md) | Synthetic-account test matrix for verification |
| [ACTION_REQUEST.md](ACTION_REQUEST.md) | Concrete deliverables requested from ecosystem actors |
| [MITIGATIONS.md](MITIGATIONS.md) | Implementation guidance for gateways, schemes, and issuers |
| [SELF_ASSESSMENT.md](SELF_ASSESSMENT.md) | Safe testing procedure for authorized operators |
| [EVIDENCE.md](EVIDENCE.md) | Evidence ledger, third-party archives, and release status |
| [TIMELINE.md](TIMELINE.md) | Dated, researcher-reported coordination chronology |
| [CORRECTIONS.md](CORRECTIONS.md) | Supersession log preserving accuracy across updates |
| [AI_ASSISTANCE.md](AI_ASSISTANCE.md) | Editorial AI disclosure |
| [SCOPE_AND_ETHICS.md](SCOPE_AND_ETHICS.md) | Harm minimization and dual-use publication boundaries |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Pre-release verification checklist |

## Coordinated Disclosure

All tracker outcomes are researcher-reported and documented in [TIMELINE.md](TIMELINE.md):
- **CISA CVD / VINCE-NT:** `CASE#121099` (prior `CCASE0209885`)
- **CERT/CC:** `VRF#26-05-CJVGG`, `VRF#26-08-XWHPS`
- **EMVCo:** Inquiry `#20260827-17621D`
- **MITRE CVE Program:** Tracking reference `2026835`
- **Vendor / Scheme Disclosures:** PayPal HackerOne `#3673424`, GitHub `GHSA-xjwr-jwm2-wvjr`, Visa HackerOne `#3978615`, American Express HackerOne `#3979021`, Mastercard Bugcrowd `8d647a18`, and direct Visa/Mastercard/Amex security team submissions.

## Living Record, Ethics, and Citation

This repository contains no enumeration scripts, PAN/BIN fragments, tokens,
CAVVs, transaction IDs, or raw captures ([SCOPE_AND_ETHICS.md](SCOPE_AND_ETHICS.md),
[EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json)). Corrections and technical
feedback are welcomed via GitHub issues citing the relevant Claim ID or
Correction ID ([CORRECTIONS.md](CORRECTIONS.md)). AI tools were used solely for
editorial, drafting, and formatting support ([AI_ASSISTANCE.md](AI_ASSISTANCE.md)).

- **Research study citation:** `arXiv:2610.32206`
- **Disclosure and standards proposal citation:** [CITATION.cff](CITATION.cff)
