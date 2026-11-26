# The 3DS Oracle

> **Public disclosure record and standards proposal.** This repository documents
> a pre-authorization response discrepancy vulnerability across browser-mediated
> EMV 3-D Secure (3DS) integrations and the multi-party protocol boundary, along
> with proposed fixes. It contains no attack tooling, real card data, live
> endpoint recipes, reusable tokens, or raw network captures.

- **Research monograph:** [arXiv:2610.32206](https://arxiv.org/abs/2610.32206)
- **Short formal statement:** [PUBLIC_DISCLOSURE.md](PUBLIC_DISCLOSURE.md)
- **Claims and limits:** [CLAIMS.md](CLAIMS.md) | **Corrections:** [CORRECTIONS.md](CORRECTIONS.md)

## Start Here: What Is the Vulnerability? (Plain English)

When you pay online with a card, the merchant often runs a background
authentication check called **EMV 3-D Secure (3DS)** *before* asking your bank to
charge any money ([C-01](CLAIMS.md)). Under EMV 3DS Core v2.3.1.1, messages flow
through this chain:

```text
Buyer / Caller  -->  Merchant & 3DS Server  -->  Card Scheme DS  -->  Issuing Bank (ACS)
  (browser/API)       (checkout integration)      (range routing)      (account handling)
```

Normally, this step decides whether the purchase can complete silently
("frictionless") or needs extra verification such as a one-time passcode
("challenge"), after which payment authorization happens separately
([C-01](CLAIMS.md)).

### Where the Problem Starts

Two facts meet here:

1. **The protocol inspects the card number before payment clearing and without
   universal holder proof (`CWE-696`):** Under EMV 3DS Core v2.3.1.1, the network
   and issuer steps evaluate card-range eligibility (Reqs. 97 and 98) and account
   authentication availability (Req. 105) before any challenge completes and
   before payment authorization ([C-02](CLAIMS.md)). In Core Table A.1, the
   account number (`acctNumber`, 13 to 19 digits) is mandatory (`AReq = R`),
   while expiration date (`cardExpiryDate`) and security code (`cardSecurityCode`)
   are conditional (`AReq = C`, governed by Directory Server rules). Meanwhile,
   the Core specification explicitly leaves how the merchant/gateway ("3DS
   Requestor Environment") admits callers and projects response fields back to
   the browser implementation-defined ([SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)).
2. **A permissive client integration reflects those outcomes to an unverified
   caller (`CWE-204`):** In the browser integration we tested (which allowed a
   public checkout authorization credential to be replayed from a standalone
   client and did not block modified/placeholder CVV2 or expiry values at lookup),
   the client received distinguishable outcomes depending on the card number
   submitted ([C-03](CLAIMS.md)):
   - **Lookup-stage separation (6 of 7 tested cohorts):** Researcher-owned
     issued anchor cards received integration outcomes mapping to *"challenge
     required"*, *"frictionless approved"* (returning non-empty `CAVV` and `ECI`
     fields), *"expired card"* (Reason `05`), or *"not enrolled"* (Reason `13`),
     whereas adjacent same-range comparison candidates returned Reason `08`
     (*"No card record"* / *"No account"*) ([C-03](CLAIMS.md),
     [C-03a](CLAIMS.md)).
   - **Challenge-initiation separation (Cohort G):** One cohort returned a
     uniform *"challenge required"* status (`transStatus = C`) at lookup for every
     tested input. However, when the caller posted the initial challenge request
     (`CReq`) *without entering any OTP*, the issued control returned an
     interactive bank verification page (displaying OTP options and masked
     email/phone hints), whereas adjacent comparison candidates returned an
     HTML auto-submit response carrying `Final CRes` with `transStatus = N`
     ("transaction denied") ([C-04](CLAIMS.md)).

**Important spec caveat ([COR-003](CORRECTIONS.md)):** The Core specification does
**not** require raw lookup responses to be exposed to arbitrary unverified callers,
nor does it establish that every 3DS deployment is exploitable. An observable
oracle requires both the protocol's pre-proof ordering (`C-02`) and reachable,
non-uniform client integration behavior ([THREAT_MODEL.md](THREAT_MODEL.md)).

### Transaction Identifiers as Routing Context

Under EMVCo Core v2.3.1.1:
- **Issuer-generated ID (Req. 104):** When a request reaches an Access Control
  Server (ACS), the ACS generates its own `acsTransID`, so `acsTransID != dsTransID`.
- **DS stand-in ID (Req. 411, browser flow):** When a Directory Server creates the
  `ARes` on the ACS's behalf (for example, returning an Attempt response `transStatus = A`),
  it sets `acsTransID == dsTransID`.

Under black-box testing without backend network traces, matching identifiers in
Cohort E (`authenticate_attempt_successful`) are structurally consistent with a
DS-created response, while distinct identifiers across Cohorts A to D, F, and G
(including Reason `08` comparison inputs routed past DS range checks) are
structurally consistent with ACS processing ([SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)).
Identifier inequality alone is routing-provenance context, not proof that an
account exists or can complete payment.

### Why Probes Can Escape Payment Alerts

- **No payment authorization (`ISO 8583`) is submitted:** Stopping at lookup (or
  at initial `CReq` retrieval without entering an OTP) avoids financial clearing
  attempts, so downstream post-authorization fraud rules do not observe these
  queries as payment declines. *(Because merchant billing records were not
  inspected, we make no claim that upstream 3DS processing itself is free.)*
- **No cardholder alert was observed in bounded tests ([COR-002](CORRECTIONS.md)):**
  EMVCo Core specifies no cardholder SMS or mobile app push notification on
  lookup-only probes or on the Req. 220/221 30-second initial-`CReq` timeout
  (which notifies the DS and Requestor server internally via `RReq` with Reason
  `14` and Cancel Indicator `05`). On researcher-controlled recipient channels,
  no SMS, email, OTP, or push reached test devices during these bounded HTML-text
  observations. Independent bank alert systems and out-of-band PSD2 push flows
  were not instrumented and may differ.

### Why This Matters: Beyond Stolen Card Lists

Where a client-facing checkout leaks lookup or initial-`CReq` distinctions
without holder proof or strict secondary-field checks, an attacker does not rely
solely on already-stolen card dumps. Bounded probing with generated Luhn-valid
candidates can act as a pre-clearing screening channel ([C-05](CLAIMS.md)).
Separately reviewed public tooling confirms automated scripts already parse 3DS
pre-authorization responses ([C-07](CLAIMS.md)).

## What the Bounded Study Proved (And Its Strict Limits)

The primary controlled study evaluated **one** browser-channel checkout
integration (PayPal Braintree and CardinalCommerce on a researcher-controlled
checkout) across **seven** Visa and Mastercard cohorts (`A` to `G`). Seven
researcher-owned issued cards were each paired with three adjacent same-range
Luhn-valid comparison candidates (28 unique inputs, each tested across five
fresh off-context HTTP sessions = **140 lookup observations**, zero payment
authorizations) ([C-03](CLAIMS.md), [EVIDENCE.md](EVIDENCE.md)):

- **Six cohorts (`A` to `F`)** separated the issued control from adjacent
  comparison candidates at the first lookup reply.
- **One cohort (`G`)** returned uniform `transStatus = C` at lookup, then
  separated at the initial `CReq` post (interactive OTP HTML vs. auto-submit
  `Final CRes` `N`) ([C-04](CLAIMS.md)).
- **Selected challenge-free responses** exposed non-empty `CAVV`, `ECI`,
  `paresStatus`, authentication identifiers, and liability indicators before
  authorization ([C-03a](CLAIMS.md)). These client-visible artifacts were not
  independently validated or submitted for clearing and do not prove cryptogram
  validity or payment usability.

**Explicit boundaries:** Adjacent comparison inputs did not have independently
established issuance status, repeated sessions measured within-input stability
rather than population rates, and findings do not establish universal exposure,
component attribution without internal logs, or financial impact
([CLAIMS.md](CLAIMS.md)). Narrower qualitative checks on Stripe and Adyen test
integrations, and a frozen documentation audit covering 24 core 3DS integration
paths (plus a separate 16-path extension), provide cross-ecosystem context and
are not pooled with the primary study ([EVIDENCE.md](EVIDENCE.md)).

## Why Current Controls Leave Gaps

1. **IP throttling faces proxy rotation:** Archived tools include optional
   rotating SOCKS5 routing (`CWE-307`) ([C-07](CLAIMS.md)), and an exploratory A/B
   comparison on our tested device-data path observed fewer single-source blocks
   under distributed residential egress ([SCOPE_AND_ETHICS.md](SCOPE_AND_ETHICS.md)).
   That exploratory check does not establish evasion of every production detector.
2. **Clearing fraud systems operate downstream:** Post-3DS `ISO 8583` scoring
   monitors financial authorizations, whereas pre-authorization lookups sit
   upstream unless governed by dedicated 3DS-tier controls.
3. **Client-visible scheme signals can act as feedback (`US 2026/0134429 A1`):**
   Mastercard's patent application discloses Directory Server scoring for
   "authentication BIN attacks" and network/participant signaling including score
   `998` and Reason `98` ([C-06](CLAIMS.md), [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)).
   Exploratory client log reviews observed Reason `98` during repeated same-range
   Mastercard lookups (without backend traces confirming which component emitted
   it). Reflecting diagnostic codes in browser-readable output (`CWE-209`) lets
   automated callers observe blocks and adjust pacing or proxy rotation
   ([MITIGATIONS.md](MITIGATIONS.md)).
4. **Lookup normalization relocates leaks:** Masking initial lookup status text
   without addressing pre-proof execution order shifts observable distinctions
   into initial `CReq` output (`C-04`), response size, or execution latency
   (`CWE-208`) ([C-08](CLAIMS.md)).

**Multi-party governance context:** Because the 3DS Requestor Environment, gateway,
DS, and ACS sit in different administrative domains and no single component owns
end-to-end query authority, sovereign coordinators (`CISA VINCE-NT CASE#121099`,
`CERT/CC VRF#26-05-CJVGG`) determined (as reported by the researchers) that
multi-party specification architecture falls outside single-vendor CVE
coordination, while our inquiry to EMVCo (`#20260827-17621D`) was processed under
general non-confidential Terms of Use ([TIMELINE.md](TIMELINE.md)). Broader
compliance and security-economics analysis of liability shifting and certification
boundaries is detailed in the companion monograph
([arXiv:2610.32206](https://arxiv.org/abs/2610.32206)).

## Public Operational Evidence

Reviewed third-party archives show that lookup-stage classification has been
implemented in public scripts, though source availability alone does not
establish live operation, accuracy, volume, or prevalence against specific
targets ([C-07](CLAIMS.md), [EVIDENCE.md](EVIDENCE.md)):

- [Archived Telegram Braintree 3DS handler](https://perma.cc/2QL8-9KKR): obtains
  merchant-scoped Braintree authorization from a public checkout, submits card
  credentials, invokes 3DS lookup, classifies returned status, and supports
  SOCKS5 routing.
- [Adyen-labeled Telegram checker](https://perma.cc/Z7E3-KWYT) and
  [`3dali.php`](https://perma.cc/PBA6-AUG5): submits encrypted payment data and
  classifies Saleor `AUTHORIZATION_ACTION_REQUIRED` as `3D Card` (scope limits in
  [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)).
- [BraintreeCHK](https://perma.cc/A25F-XA7V),
  [MeduzaV3](https://perma.cc/KV3L-7ZQG) ([promo](https://perma.cc/9VUB-A9BE)),
  [pubstripe](https://perma.cc/9VSU-SGYN), and a [commercial 3DS Lookup API
  listing](https://perma.cc/G84X-8L43).
- **Practitioner report:** In G+D Netcetera's *Tech Tribe* podcast (Episode
  S11E13, [*"Fraud Alert: Inside a Massive BIN Attack"*](https://youtu.be/IfHsmJHPOcs),
  Nov. 18, 2025), practitioners reported live 3DS-rail velocity bursts exceeding
  10 transactions per second and abuse of pre-authorization responses for
  reconnaissance.
- **Historical precedent:** [CVE-2021-35060](https://nvd.nist.gov/vuln/detail/CVE-2021-35060)
  ([advisory](https://gist.github.com/exviry/9527ce2ccdc0718d3ffd1e3ca62cf304))
  documented an earlier ACS enrollment-endpoint enumeration bug (`CWE-209`). Our
  work examines composed cross-boundary exposure along the specification flow
  rather than one vendor URL.

## How To Fix It

Effective remediation separates tactical containment from long-term architectural
closure ([C-08](CLAIMS.md), [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md)):

1. **Immediate Containment (`AR-01`, `AR-03` to `AR-07`, `AR-14`):** Bind
   checkout context server-side, make transitions single-use, remove internal
   reason codes (`05`, `08`, `13`, `98`), `CAVV`, and `ECI` from browser-visible
   responses (`CWE-209`), return uniform constant-time error responses (`CWE-204`,
   `CWE-208`), and keep anomaly detection flags backend-only (`CWE-307`).
2. **Architectural Closure (`AR-02`, `AR-08`):** Require independently verified
   query authority bound to the exact account and transaction *before* executing
   card-range routing or issuer ledger evaluation (`CWE-696`), or return one
   uniform, state-independent terminal response when authority is absent.

## Repository Structure

| Document | Purpose |
|---|---|
| [PUBLIC_DISCLOSURE.md](PUBLIC_DISCLOSURE.md) | Canonical short formal disclosure statement |
| [CLAIMS.md](CLAIMS.md) | Claim ledger distinguishing proof, bounded data, and proposals |
| [THREAT_MODEL.md](THREAT_MODEL.md) | Channel model, CWE mapping, and security objective |
| [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md) | EMVCo, CVE, Adyen/Saleor, and patent reference limits |
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

All tracker entries and outcomes are researcher-reported and documented in
[TIMELINE.md](TIMELINE.md):
- **CISA CVD / VINCE-NT:** `CASE#121099` (prior `CCASE0209885`)
- **CERT/CC:** `VRF#26-05-CJVGG`, `VRF#26-08-XWHPS`
- **EMVCo:** Inquiry `#20260827-17621D`
- **MITRE CVE Program:** Tracking reference `2026835`
- **Vendor / Scheme Disclosures:** PayPal HackerOne `#3673424`, GitHub
  `GHSA-xjwr-jwm2-wvjr`, Visa HackerOne `#3978615`, American Express HackerOne
  `#3979021`, Mastercard Bugcrowd `8d647a18`, and direct Visa, Mastercard, and
  American Express security contacts.

## Living Record, Ethics, and Citation

This repository contains no enumeration scripts, PAN/BIN fragments, tokens,
CAVVs, transaction IDs, or raw captures ([SCOPE_AND_ETHICS.md](SCOPE_AND_ETHICS.md),
[EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json)). Corrections and technical
feedback are welcomed via GitHub issues citing the relevant Claim ID or
Correction ID ([CORRECTIONS.md](CORRECTIONS.md)). AI tools were used solely for
editorial, drafting, and formatting support ([AI_ASSISTANCE.md](AI_ASSISTANCE.md)).

- **Research study citation:** `arXiv:2610.32206`
- **Disclosure and standards proposal citation:** [CITATION.cff](CITATION.cff)
