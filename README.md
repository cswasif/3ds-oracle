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

## Summary

EMV 3-D Secure (3DS) Browser processing can expose two distinct pre-
authorization surfaces. A frictionless result may be returned after the initial
AReq/ARes exchange, while a selected challenge requires browser-carried
flow-control and transaction-correlation state. The Core also defines account-
and range-dependent operations before either a frictionless result or a later
fresh challenge proof. Those protocol facts do **not** require an arbitrary
external caller to receive raw results or imply that every deployment exposes a
useful oracle.

In one tested browser-channel integration, seven bounded ACS/card-range cohorts
produced repeatable input-correlated response classes: six at the first
Requestor-visible lookup and one after the initial CReq. A practical classifier
requires more than this structural ordering: caller reachability,
attacker-influenced account input, insufficient exact-query authority,
repeatable public differences, and useful sampling. See [CLAIMS.md](CLAIMS.md)
and [THREAT_MODEL.md](THREAT_MODEL.md).

## Corrected bounded finding

The primary observation used seven researcher-owned issued controls, each paired
with three adjacent same-range Luhn-valid comparison inputs. The 28 inputs were
observed in five fresh sessions each, yielding 140 lookup observations.
Repetitions measured within-input stability, not independent card samples.
Comparison-input issuance was not independently established.

- Six cohorts separated the issued control from adjacent comparison inputs at
  the first Requestor-visible lookup response.
- One cohort returned `transStatus=C` at lookup for all tested inputs.
- In that cohort, a separately bounded initial-CReq observation returned
  immediate HTML wrappers carrying Final CRes `N` for comparison inputs, while
  the issued control received HTML defining a credential-choice/OTP interface.

The client inspected returned HTML as text. It did not render the page, select
a delivery method, submit credentials or an OTP, complete authentication, or
submit financial authorization. No SMS, email, OTP, or push was observed on
researcher-controlled recipient channels during that narrow observation. This
does not establish behavior in a rendered browser, OOB, decoupled, or separate
issuer notification flow.

The study establishes response-class separation in the tested integration. In
selected challenge-free responses, it also observed non-empty CAVV fields, ECI,
`paresStatus`, authentication identifiers, and integration-reported liability
indicators before financial authorization. These are client-visible
authentication artifacts, not proven valid or reusable cryptograms and not
proof that authorization would succeed. The study does not establish account
existence, account usability, comparison-input issuance, internal DS/ACS
attribution, prevalence, or financial impact.

## Why single controls are insufficient

- A transaction context is useful, but possession of it does not by itself
  authorize a caller to query a newly supplied account.
- A uniform lookup response can leave a distinction at the first CReq, while a
  frictionless initial result can itself be an early branch or artifact-release
  surface.
- Response filtering can suppress unnecessary semantics, but cannot close a
  hidden-state distinction if one unadmitted class receives a frictionless
  success-like artifact, another visibly continues, or another terminates.
- Required transaction identifiers are public correlation handles, not
  authentication credentials; hiding them alone is not a remedy.
- Authorization-side correlation prevents downstream misuse but cannot retract
  information disclosed during authentication.
- Feature-data detection of abnormal network traffic can reduce sampling. It
  does not alone define a confidential client response. The patent terminology
  and limits are documented in [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md).

## Requested ecosystem action

The public request is not “make all frictionless and challenge outcomes look
the same.” It is to distinguish two cases:

1. **Unadmitted query:** before an independently verified authorization basis
   exists for the exact account and operation, return one declared terminal
   public observation and do not perform attacker-triggerable hidden-state
   work.
2. **Admitted query:** after the exact context is verified, release only the
   minimum genuine next action required by the protocol and bind all later
   transitions to that context.

[CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md) gives eight technology-neutral
requirements. [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md) defines the
necessary synthetic-fixture tests. [ACTION_REQUEST.md](ACTION_REQUEST.md) names
requested deliverables and owners.

## Direct public operational evidence

The public record includes reviewed, archived evidence that the lookup-stage
response surface has been turned into a service-oriented card-checking workflow.
An [archived membership-gated Telegram-bot Braintree 3DS/VBV handler](https://perma.cc/2QL8-9KKR)
contains a card-checking command that obtains merchant-scoped Braintree
authorization from a public checkout, submits caller-provided card credentials
to a Braintree flow, invokes 3DS lookup, classifies returned authentication
status, supports rotating SOCKS5 routing, and gates use through membership
logic. This is direct public evidence of an implementation designed to
operationalize lookup-stage classification, not merely an advertisement.

Additional public artifacts corroborate packaging, cross-family scriptability,
and commercial interest:

- [Adyen-labeled Telegram checker repository](https://perma.cc/Z7E3-KWYT)
  and its archived [`3dali.php` gateway file](https://perma.cc/PBA6-AUG5):
  the source labels the gate “3D Adyen,” selects `app.saleor.adyen`, submits
  encrypted card and browser/risk data to a merchant checkout transaction
  endpoint, and classifies `AUTHORIZATION_ACTION_REQUIRED` as `3D Card`.
  This is direct evidence of an implemented Adyen/Saleor action-required
  card-checking workflow. Saleor's Adyen documentation states that its app
  returns `AUTHORIZATION_ACTION_REQUIRED` when the Adyen response includes an
  action for the storefront; Saleor's payment-app documentation lists 3DS,
  redirect, and mobile approval as examples. Adyen separately defines
  `ChallengeShopper` as issuer-required shopper interaction. The archived file
  does not preserve or parse the underlying Adyen `resultCode` or action type,
  so it proves the broader 3DS/action-required classification but not that this
  particular response was literally `ChallengeShopper`.
- [BraintreeCHK](https://perma.cc/A25F-XA7V), a repository advertising a
  Braintree VBV/3DS card-checking tool;
- [MeduzaV3](https://perma.cc/KV3L-7ZQG), a broader card-checking toolkit,
  with an [archived promotional video](https://perma.cc/9VUB-A9BE);
- [pubstripe's 3DS implementation](https://perma.cc/9VSU-SGYN), which shows
  constructed browser metadata, programmatic Stripe 3DS2 invocation, parsed
  transaction status, and optional proxy routing; and
- a [commercial 3DS Lookup API listing](https://perma.cc/G84X-8L43) advertising
  BIN/IIN lookup, 3DS support checks, issuer metadata, and IP/BIN risk scoring.

The evidence is stage-specific. The Telegram handler directly demonstrates an
implemented Braintree lookup classifier; it does not show that the separate
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
