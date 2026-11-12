# Public disclosure: browser-mediated EMV 3DS 2.x

## Status

This is a public-interest disclosure and proposed standards response. It omits
operational reproduction instructions and distinguishes protocol structure,
bounded observations, conditional inferences, static third-party review, and
proposals. See [CLAIMS.md](CLAIMS.md).

## Executive statement

EMV 3DS Browser processing can expose two distinct pre-authorization surfaces:
a frictionless initial AReq/ARes result may return before financial
authorization, and a selected challenge carries browser flow-control and
correlation data. The Core also places range- and account-dependent operations
before either a frictionless result or a later fresh challenge proof. These
facts create a security review surface. They do not require arbitrary caller
access, raw result reflection, or a practical oracle in every deployment.

A practical pre-proof classifier requires an attacker-influenced account query,
insufficient independently verified exact-query authority, a hidden-state-
dependent public distinction, and enough repeatable access to sample it. The
security objective and conditions are specified in [THREAT_MODEL.md](THREAT_MODEL.md).

## Observed result

A bounded study used one browser-channel integration and EMV 3DS 2.2.0 messages.
It compared seven researcher-owned issued controls with three adjacent,
same-range Luhn-valid comparison inputs per control. The 28 unique inputs were
observed in five fresh sessions each, for 140 lookup observations.

- Six cohorts produced distinct Requestor-visible lookup response classes for
the issued control and adjacent comparison inputs.
- One cohort returned `transStatus=C` at lookup for all tested inputs.
- A separate, bounded initial-CReq observation in that lookup-uniform cohort
received immediate HTML wrappers carrying Final CRes `N` for comparison inputs
and HTML defining a credential-choice/OTP interface for the issued control.

The non-browser client inspected that HTML as text. It did not render the page,
forward forms, select a delivery method, submit credentials or an OTP, complete
authentication, or attempt payment authorization. No SMS, email, OTP, or push
was observed on researcher-controlled recipient channels during that narrow
text-HTML observation.

The study establishes repeatable input-correlated response classes in the
tested integration. Selected challenge-free responses also exposed non-empty
CAVV fields, ECI, `paresStatus`, authentication identifiers, and
integration-reported liability indicators before financial authorization. Those
are client-visible authentication artifacts. They are not independently
validated or reusable cryptograms and do not show downstream authorization
success. The study does not establish comparison-input issuance, account
existence or usability, internal component attribution, production throughput,
ecosystem prevalence, financial loss, or cardholder-notification behavior in
other channels.

## Patent and detection context

US 2026/0134429 A1 describes a threat model in which an estimated or guessed
credential is submitted and an authentication response may be used as a signal.
It describes detection of an authentication BIN attack using feature data and
snapshot data, a trained model, probability score, and threshold; it also
describes notification, AReq/ARes signaling, pausing, and blocking. These are
patent disclosures, not evidence that the described system is deployed or that
it operated in the study. A Reason-98-related client-visible class does not
identify the component, model, or detection logic that produced it. See
[SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md).

## Required response

Current deployments should use containment: bounded server-created contexts,
replay protection, trusted-channel result handling, browser-output allowlists,
full state-machine review, and aggregate abuse detection. These reduce
reachability and unnecessary semantics but cannot erase a distinction already
required by a public state machine.

A future profile that claims closure must establish independent authority for
the exact account and operation before an attacker-triggerable account,
enrollment, range, route, Method, ACS, or online-status read, or return one
hidden-state-independent terminal public observation without performing that
read. This is technology-neutral and does not prescribe a particular
credential, signature scheme, browser API, or message format.

The requested requirements, tests, owners, and rollout are in:

- [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md)
- [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md)
- [ACTION_REQUEST.md](ACTION_REQUEST.md)

## Direct public operational evidence

An [archived membership-gated Telegram-bot Braintree 3DS/VBV handler](https://perma.cc/2QL8-9KKR)
contains a service-oriented card-checking workflow: it obtains merchant-scoped
Braintree authorization from a public checkout, submits caller-provided card
credentials, invokes 3DS lookup, classifies returned status, supports rotating
SOCKS5 routing, and gates access through membership logic. This is direct
public evidence that lookup-stage Braintree classification was implemented as
operational code, rather than merely advertised.

The public record also links to an
[Adyen-labeled Telegram checker repository](https://perma.cc/Z7E3-KWYT) and
its archived [`3dali.php` gateway file](https://perma.cc/PBA6-AUG5). That
source labels the gate “3D Adyen,” selects `app.saleor.adyen`, submits
encrypted payment and browser/risk data to a merchant checkout endpoint, and
classifies `AUTHORIZATION_ACTION_REQUIRED` as `3D Card`. Saleor's Adyen
application documentation says it returns that state when an Adyen response
contains an action the storefront must perform, while Saleor lists 3DS,
redirect, and mobile approval as examples of follow-up actions. Adyen defines
`ChallengeShopper` specifically as issuer-required shopper interaction. The
archive therefore establishes Adyen/Saleor 3DS action-required classification,
but not the exact underlying Adyen result code because `3dali.php` does not
preserve or parse `resultCode` or the action type.

The record also links to [BraintreeCHK](https://perma.cc/A25F-XA7V),
[MeduzaV3](https://perma.cc/KV3L-7ZQG), its
[promotional video](https://perma.cc/9VUB-A9BE),
[pubstripe's 3DS implementation](https://perma.cc/9VSU-SGYN), and a
[commercial 3DS Lookup API listing](https://perma.cc/G84X-8L43). Together they
provide public evidence of packaging, promotion, cross-family scriptability,
and commercial interest around 3DS/card-checking functionality.

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
