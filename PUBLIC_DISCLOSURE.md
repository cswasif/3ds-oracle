# Public disclosure: browser-mediated EMV 3DS 2.x

## Status

This is a public-interest disclosure and proposed standards response. It omits
operational reproduction instructions and distinguishes protocol structure,
bounded observations, conditional inferences, static third-party review, and
proposals. See [CLAIMS.md](CLAIMS.md).

## Executive statement

An architectural vulnerability in the browser channel (`02-BRW`) of the EMV 3-D Secure (3DS) Core Specification (versions 2.1.0 through 2.3.1.1; Reqs 80, 89, 97–98, 105, 411, 412, 421) allows unauthenticated remote callers at public merchant checkout interfaces to exploit **observable response differences (CWE-203)** as a **pre-authorization account enumeration oracle**.

By submitting candidate 16-digit Primary Account Numbers (PANs) (e.g., Visa, Mastercard) to public checkout endpoints, an attacker can extract live cardholder existence, enrollment status, and account lifecycle states directly from issuing bank mainframes **before any financial authorization or clearing occurs**.

Because this extraction occurs prior to payment clearing:
1. **No CVV or Expiration Date Required (EMVCo Table A.1):** The specification explicitly excludes the Card Verification Value (CVV/CVC) from `AReq` lookup messages, and issuer ACSs do not validate expiration dates at this stage. An attacker only needs candidate 16-digit PANs with arbitrary placeholder dates and CVVs (e.g., `12/99`, `123`) to satisfy frontend form validation.
2. **$0.00 Financial Cost:** No ISO 8583 financial authorization (`0100`/`0200`) is submitted across payment networks (e.g., Visa, Mastercard), incurring zero merchant interchange charges or network fees.
3. **Zero Cardholder Alerts (EMVCo Req 220/221 Silent Timeout):** When an active account triggers a challenge prompt (`transStatus = C`), automated tools extract the confirmation and immediately abandon the HTTP connection without posting a Challenge Request (`CReq`). Under EMVCo Req 220/221, the Access Control Server (ACS) 30-second timer expires silently, transmitting an internal `RReq` (Reason 14, Cancel 05) to the Directory Server (e.g., Visa, Mastercard). **No SMS, push notification, or email alert is ever dispatched to the cardholder.**
4. **Core Ledger Verification via Status Reasons (EMVCo Req 105):** The bank ACS evaluates the PAN against its core ledger under `[Req 105]`, returning observable response signals—such as challenge prompts (`transStatus = C`) vs. Reason 08 (*Card record not found*), Reason 13 (*Not Enrolled*), or Reason 05 (*Expired*)—allowing an attacker to filter out non-existent card numbers and confirm whether an account is live.
5. **Deterministic Routing Oracle (EMVCo Req 411 / UUID Collision Invariant):** When a Directory Server terminates early, EMVCo mandates `acsTransactionID == dsTransactionID`. When a probe successfully reaches an external bank ACS, `acsTransactionID != dsTransactionID`. Exposed in client-facing APIs, this provides a deterministic topological signal confirming whether the candidate reached the bank mainframe.

## Threat Model: Generative Discovery vs. Credential Stuffing

The payment industry has historically treated card testing as a volumetric "credential stuffing" problem—assuming attackers only blast pre-existing stolen card dumps from darknet breaches against checkouts in noisy, high-volume sweeps.

**Our findings establish a more severe threat model: Generative Account Discovery.**
- Attackers do not require stolen card databases.
- By analyzing known or previously breached cards (e.g., Visa, Mastercard) from an issuer, an adversary can reverse-engineer the bank's internal Card Management System (CMS) sub-allocation patterns within an 8-digit Bank Identification Number (BIN).
- Utilizing guided search tree pruning, an attacker may query **50 to 100 surgically targeted candidate numbers** to systematically discover live, active adjacent accounts.
- Routed through rotating residential SOCKS5 proxy pools, these low-volume candidate probes blend invisibly into legitimate checkout traffic, bypassing traditional volumetric rate limiters and Web Application Firewalls (WAFs).

## Historical Precedent & Scope

In 2021, an isolated implementation flaw (**CVE-2021-35060**) established that an OpenWay WAY4 ACS card enrollment endpoint (`/way4acs/enroll`) allowed unauthenticated attackers to discover whether a card existed in the system due to observable error message differences (CWE-209).

**This disclosure demonstrates that the vulnerability is not an isolated vendor implementation bug, but an architectural flaw embedded within the global EMV 3DS Core Specification itself.** The oracle spans the multi-party payment rail:
$$\text{Merchant Checkout} \longrightarrow \text{Payment Gateway} \longrightarrow \text{Scheme Directory Server (e.g., Visa, Mastercard)} \longrightarrow \text{Issuer ACS}$$
The surface is accessible through standard checkout integrations across major gateways (e.g., Braintree, Stripe, Adyen) and multiple ACS hosting platforms.

## Observed Empirical Results

A controlled empirical study examined 28 card inputs (7 researcher-controlled issued cards and 21 adjacent Luhn-valid candidate numbers) across 140 browser-channel sessions (EMV 3DS 2.2.0):
- **Lookup-Stage Differences:** Six cohorts produced immediate observable response differences between active issued cards and adjacent candidate inputs at the lookup stage (`AReq`/`ARes`).
- **Initial-CReq Differences:** One cohort returned uniform lookup classifications (`transStatus = C`) but revealed immediate observable differences upon receiving the first challenge wrapper: adjacent non-issued candidates received an immediate Final `CRes = N`, whereas active issued controls received an interactive credential/OTP challenge interface.
- **Client-Visible Cryptographic Artifacts:** Selected challenge-free responses returned non-empty Cardholder Authentication Verification Values (CAVV/AVV), Electronic Commerce Indicators (ECI), and directory transaction IDs to client-side scripts prior to financial authorization.

## Why Existing Defenses Fail

1. **IP Rate Limiting:** Rotating residential proxy networks assign distinct residential IP addresses to each request, defeating IP-based thresholds.
2. **Clearing-Stage Fraud Detection:** Machine learning fraud models (e.g., FICO Falcon, ACI PRM) evaluate post-authorization ISO 8583 transactions; they have zero visibility into upstream 3DS pre-authorization telemetry.
3. **The In-Band Tripwire Paradox (Mastercard Patent US 2026/0134429 A1):** Payment card schemes (e.g., Mastercard, Visa) deployed Directory Server anomaly detection models that flag suspected enumeration, returning error codes (e.g., Reason 98). Commercial gateways deserialize these error codes into client-visible responses, providing attackers with immediate real-time feedback to tune evasion heuristics.

## Proposed Remediation: Protocol-Level Response Uniformity

Heuristic detection at checkout is structurally insufficient against client-side browser automation. Permanent closure requires **Response Uniformity** within the EMV 3DS Core Specification:
1. **Unadmitted Query:** In the absence of an independently verified authorization proof binding the exact cardholder to the transaction context, the protocol must return an identical, opaque public response regardless of whether the account exists, is inactive, or is blocked.
2. **Admitted Query:** Genuine continuation actions may only be released after the caller's authority over the exact account has been cryptographically established.

The full specification requirements, test suites, and ecosystem action requests are detailed in:
- [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md)
- [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md)
- [ACTION_REQUEST.md](ACTION_REQUEST.md)

## Direct public operational evidence

An [archived membership-gated Telegram-bot Braintree 3DS/VBV handler](https://perma.cc/2QL8-9KKR)
contains a service-oriented card-checking workflow: it obtains merchant-scoped
Braintree authorization from a public checkout, submits caller-provided card
credentials (e.g., Visa, Mastercard), invokes 3DS lookup, classifies returned
status, supports rotating SOCKS5 routing, and gates access through membership
logic. This is direct public evidence that lookup-stage Braintree classification
was implemented as operational code, rather than merely advertised.

The public record also links to an [Adyen-labeled Telegram checker repository](https://perma.cc/Z7E3-KWYT) and its archived [`3dali.php` gateway file](https://perma.cc/PBA6-AUG5), an operational card-checking tool targeting Adyen checkouts that submits encrypted payment data and classifies `AUTHORIZATION_ACTION_REQUIRED` as an active "3D Card".

The record also links to [BraintreeCHK](https://perma.cc/A25F-XA7V),
[MeduzaV3](https://perma.cc/KV3L-7ZQG), its
[promotional video](https://perma.cc/9VUB-A9BE),
[pubstripe's 3DS implementation](https://perma.cc/9VSU-SGYN), and a
[commercial 3DS Lookup API listing](https://perma.cc/G84X-8L43). Together they
provide public evidence of packaging, promotion, cross-family scriptability,
and commercial interest around 3DS/card-checking functionality.

The public record also incorporates critical operational and practitioner disclosures:
- **The "Non-VBV" Checker Duality:** Underground carding syndicates (across Telegram, darknet forums, and video channels) market automated tools as "3DS/VBV BIN Checkers" to discover non-challenging card ranges for fraud. Under the hood, the EMV 3DS protocol transmits the full 16-digit PAN to the Issuer ACS under Req 105, turning what is advertised as a coarse BIN check into an individual live cardholder verification oracle.
- **Industry Incident Telemetry (G+D Netcetera Podcast):** In their *Tech Tribe* podcast (Episode S11E13, [*"Fraud Alert: Inside a Massive BIN Attack"*](https://youtu.be/IfHsmJHPOcs), Nov 18, 2025), leading 3DS provider Netcetera documented live botnets flooding 3DS rails at sustained rates >10 tx/s, doubling bank transaction volumes within seconds and abusing 3DS pre-authorization status codes as a reconnaissance tool to map bank defenses.

This evidence remains bounded. The handler does not implement or demonstrate
public use of the separate initial-CReq differential observed in the controlled
study. Source availability does not alone establish current service operation,
classification accuracy, volume, revenue, use against third parties, or
prevalence. The repository does not host or reproduce the code, live endpoints,
or reusable material.

## Living record, evidence limits, and feedback

The repository is a narrative disclosure and standards proposal. It does not
ship a complete evidence bundle: `evidence/` contains no raw traffic,
row-level observations, account data, tokens, transaction IDs, CAVVs, or live
endpoint details. The release status is recorded in
[EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json).

The linked arXiv monograph will receive corrected and expanded versions as
additional review, source checking, affected-party feedback, and authorized
evidence become available. The authors will preserve the claim classes and
limits recorded in [CLAIMS.md](CLAIMS.md).

Corrections, technical feedback, affected-party statements, and source pointers
are welcome through a repository issue. Please identify the relevant claim,
source, or correction ID. Substantiated feedback will be dated and linked or
incorporated in the public record.

AI assistance was used for writing and editorial support only; see
[AI_ASSISTANCE.md](AI_ASSISTANCE.md).

The correction register is [CORRECTIONS.md](CORRECTIONS.md). It supersedes
older broad wording about universal exposure, notification behavior, and
third-party source review.
