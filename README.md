# The 3DS Oracle

> **Public disclosure record and standards proposal.** This repository contains
> no attack tooling, card data, live endpoint recipes, reusable transaction
> material, or row-level traffic. It is a narrative disclosure and reform
> proposal, not a complete public evidence bundle.

- Research monograph: https://arxiv.org/abs/2610.32206
- Canonical short statement: [PUBLIC_DISCLOSURE.md](PUBLIC_DISCLOSURE.md)
- Claims and limits: [CLAIMS.md](CLAIMS.md)
- Threat model: [THREAT_MODEL.md](THREAT_MODEL.md)
- Standards and patent crosswalk: [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)
- Proposed consortium profile: [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md)
- Proposed conformance-test framework: [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md)
- Requested owner actions: [ACTION_REQUEST.md](ACTION_REQUEST.md)
- Defender guidance: [MITIGATIONS.md](MITIGATIONS.md)
- Authorized self-assessment: [SELF_ASSESSMENT.md](SELF_ASSESSMENT.md)
- Evidence index and release status: [EVIDENCE.md](EVIDENCE.md)
- AI-writing disclosure: [AI_ASSISTANCE.md](AI_ASSISTANCE.md)
- Corrections: [CORRECTIONS.md](CORRECTIONS.md)
- Disclosure timeline: [TIMELINE.md](TIMELINE.md)
- Release checklist: [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)

## Vulnerability Overview

An architectural flaw in the browser channel (`02-BRW`) of the EMV 3-D Secure (3DS) Core Specification (versions 2.1.0 through 2.3.1.1; Reqs 80, 89, 97–98, 105, 411, 412, 421) allows unauthenticated remote callers at public merchant checkouts to exploit **observable response differences (CWE-203 / CWE-204)** as a **pre-authorization account enumeration oracle**.

By submitting candidate 16-digit Primary Account Numbers (PANs) (e.g., Visa, Mastercard) to public merchant checkout endpoints, an attacker can extract internal account states directly from issuing bank mainframes (e.g., whether an account exists, is active, or expired) **before any financial authorization occurs**.

Because this check happens prior to payment clearing:
1. **No CVV or Expiration Date Required (EMVCo Table A.1):** The specification explicitly excludes the Card Verification Value (CVV/CVC) from `AReq` lookup messages, and issuer ACSs do not validate expiration dates at this stage. An attacker only needs candidate 16-digit PANs with arbitrary placeholder dates and CVVs (e.g., `12/99`, `123`) to satisfy frontend form validation.
2. **$0.00 Financial Cost:** No financial transaction (`0100` ISO 8583 message) is generated across payment networks (e.g., Visa, Mastercard), incurring zero network clearing fees or merchant processing charges.
3. **Zero Cardholder Alerts (Req 220/221 Silent Timeout):** When an active card triggers a challenge (`transStatus = C`), the automated script extracts the classification and immediately drops the connection without posting a challenge request (`CReq`). Under **EMVCo Req 220/221**, the ACS 30-second timer expires silently, sending an internal `RReq` with Reason 14 and Cancel 05 to the Directory Server (e.g., Visa, Mastercard). **No SMS, email, or mobile push notification is ever dispatched to the cardholder.**
4. **Core Ledger Verification via Status Reasons (EMVCo Req 105):** The bank Access Control Server (ACS) evaluates the PAN against its live cardholder database, returning observable status reasons (such as challenge prompts `transStatus = C` vs. Reason 08 *Card record not found*, Reason 13 *Not Enrolled*, or Reason 05 *Expired*), allowing an attacker to filter unallocated numbers from live, enrolled accounts.
5. **Deterministic Routing Oracle (EMVCo Req 411 / UUID Collision Invariant):** When a Directory Server terminates early, EMVCo mandates `acsTransactionID == dsTransactionID`. When a probe successfully reaches an external bank ACS, `acsTransactionID != dsTransactionID`. Exposed in client-facing APIs, this provides a deterministic topological signal confirming whether the candidate reached the bank mainframe.

## Threat Escalation: From Credential Checking to Generative Discovery

The payment industry historically assumed attackers only use public checkouts to test pre-existing stolen card lists purchased from darknet breaches in noisy, high-volume sweeps.

**Our research reveals a far more severe threat: Generative Account Discovery.**
* An attacker does not need pre-existing stolen card lists.
* By inspecting known or breached cards (e.g., Visa, Mastercard) from a target financial institution, an adversary can **crack the bank's internal card numbering and sub-allocation pattern** within a 6- or 8-digit Bank Identification Number (BIN) range.
* Using guided search tree pruning, an attacker may query **50 to 100 surgically targeted candidate numbers** to systematically discover live, active adjacent accounts.
* Because the query volume is so small (50–100 requests) and routed through rotating residential SOCKS5 proxies, traditional volumetric rate limiters, WAFs, and bot tripwires **never trigger**.

## Historical Precedent & Systemic Scope

In 2021, an isolated implementation flaw (**[CVE-2021-35060](https://gist.github.com/exviry/9527ce2ccdc0718d3ffd1e3ca62cf304)**, NVD [Detail](https://nvd.nist.gov/vuln/detail/CVE-2021-35060)) demonstrated that an OpenWay WAY4 ACS card enrollment endpoint (`/way4acs/enroll`) could be abused as an **enumeration oracle** due to differing error messages.

**Our research establishes that this vulnerability is not an isolated implementation bug in one vendor's web page, but a systemic architectural flaw embedded within the global EMV 3DS Core Specification itself.** It spans the entire multi-party payment rail:
$$\text{Merchant Checkout} \longrightarrow \text{Payment Gateway} \longrightarrow \text{Scheme Directory Server (e.g., Visa, Mastercard)} \longrightarrow \text{Issuer ACS}$$
The oracle is reachable through standard public checkout interfaces across major gateways (e.g., Braintree, Stripe, Adyen) and multiple ACS hosting platforms worldwide.

## Why Existing Defenses Fail

1. **IP Rate Limiting Fails:** Automated callers route lookups through rotating residential proxy pools, presenting distinct residential IP addresses that neutralize IP-based rate limiting.
2. **Clearing-Stage Fraud Engines Fail:** Traditional banking fraud systems (e.g., FICO Falcon, ACI PRM) monitor clearing-stage authorization messages (ISO 8583). They have zero visibility into upstream pre-authorization 3DS lookups.
3. **The In-Band Tripwire Paradox (Mastercard Patent US 2026/0134429 A1):** Payment card networks (e.g., Mastercard, Visa) deployed Directory Server anomaly scoring models to flag enumeration. However, commercial gateways deserialize the resulting error code directly into public client-visible JSON (`transStatusReason: "98"`). Attackers use this error code as an automated tuning signal to rotate proxies, turning the intended defense into an evasion feedback loop.

## The Solution: Protocol-Level Response Uniformity

Because an attacker in the browser channel (`02-BRW`) controls client-side execution, heuristic detection at checkout is inherently vulnerable to spoofing. The only permanent closure is **Response Uniformity**:
1. **Unadmitted Query:** Before an independently verified authorization proof exists for the exact account and operation, the protocol must return a single, indistinguishable, opaque public response regardless of whether the card exists, is inactive, or is blocked.
2. **Admitted Query:** Only after the cardholder's exact identity and transaction context are proven may the protocol release genuine continuation actions.

See [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md) for proposed specification requirements, [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md) for synthetic test fixtures, and [ACTION_REQUEST.md](ACTION_REQUEST.md) for requested owner deliverables.

## Direct public operational evidence

The public record includes reviewed, archived evidence that the lookup-stage
response surface has been turned into a service-oriented card-checking workflow.
An [archived membership-gated Telegram-bot Braintree 3DS/VBV handler](https://perma.cc/2QL8-9KKR)
contains a card-checking command that obtains merchant-scoped Braintree
authorization from a public checkout, submits caller-provided card credentials
(e.g., Visa, Mastercard) to a Braintree flow, invokes 3DS lookup, classifies
returned authentication status, supports rotating SOCKS5 routing, and gates use
through membership logic. This is direct public evidence of an implementation
designed to operationalize lookup-stage classification, not merely an
advertisement.

Additional public artifacts corroborate packaging, cross-family scriptability,
and commercial interest:

- [Adyen-labeled Telegram checker repository](https://perma.cc/Z7E3-KWYT)
  and its archived [`3dali.php` gateway file](https://perma.cc/PBA6-AUG5):
  an operational card-checking script targeting Adyen checkouts that submits
  encrypted card data and classifies `AUTHORIZATION_ACTION_REQUIRED` as an active "3D Card";
- [BraintreeCHK](https://perma.cc/A25F-XA7V), a repository advertising a
  Braintree VBV/3DS card-checking tool;
- [MeduzaV3](https://perma.cc/KV3L-7ZQG), a broader card-checking toolkit,
  with an [archived promotional video](https://perma.cc/9VUB-A9BE);
- [pubstripe's 3DS implementation](https://perma.cc/9VSU-SGYN), which shows
  constructed browser metadata, programmatic Stripe 3DS2 invocation, parsed
  transaction status, and optional proxy routing; and
- a [commercial 3DS Lookup API listing](https://perma.cc/G84X-8L43) advertising
  BIN/IIN lookup, 3DS support checks, issuer metadata, and IP/BIN risk scoring;
- **The "Non-VBV" Checker Duality:** Underground carding syndicates (across Telegram, darknet forums, and video channels) market automated tools as "3DS/VBV BIN Checkers" to discover non-challenging card ranges for fraud. Under the hood, the EMV 3DS protocol transmits the full 16-digit PAN to the Issuer ACS under Req 105, turning what is advertised as a coarse BIN check into an individual live cardholder verification oracle; and
- **Industry Incident Telemetry (G+D Netcetera Podcast):** In their *Tech Tribe* podcast (Episode S11E13, [*"Fraud Alert: Inside a Massive BIN Attack"*](https://youtu.be/IfHsmJHPOcs), Nov 18, 2025), leading 3DS provider Netcetera documented live botnets flooding 3DS rails at sustained rates >10 tx/s, doubling bank transaction volumes within seconds and abusing 3DS pre-authorization status codes as a reconnaissance tool to map bank defenses.

The evidence is stage-specific. The Telegram handler directly demonstrates an
implemented Braintree lookup account checker; it does not show that the separate
initial-CReq differential was used publicly. Public source material does not,
by itself, establish current operation, successful execution against a specific
target, accuracy, scale, third-party use, or prevalence. The repository links
to the archives for public-interest accountability but does not reproduce their
code, endpoints, tokens, or workflows.

## Living record, corrections, and feedback

The linked arXiv monograph is a living research record. The authors intend to
publish corrected and expanded versions as additional review, source checking,
affected-party feedback, and authorized evidence become available. Future
updates will preserve the distinction among protocol structure, bounded
observation, conditional inference, third-party source review, and proposal.

Corrections, technical feedback, affected-party statements, source pointers,
and reproducibility questions are welcome through a repository issue. Please
identify the relevant claim ID from [CLAIMS.md](CLAIMS.md), source entry from
[SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md), or correction ID from
[CORRECTIONS.md](CORRECTIONS.md). The authors will date, review, and link or
incorporate substantiated corrections.

AI assistance for writing and editorial support is disclosed in
[AI_ASSISTANCE.md](AI_ASSISTANCE.md).

## Scope and corrections

This release contains no enumeration tooling, PAN/BIN fragments, issuer maps,
live endpoint recipes, client tokens, CAVVs, transaction identifiers, raw
request/response captures, or executable reproductions. See
[SCOPE_AND_ETHICS.md](SCOPE_AND_ETHICS.md).

Use [CORRECTIONS.md](CORRECTIONS.md) as the authoritative supersession record.
Please report factual corrections through a repository issue. Cite the research
monograph for the study and this repository through [CITATION.cff](CITATION.cff)
for the public disclosure and standards proposal.
