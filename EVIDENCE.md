# Evidence index and release status

## Release status

This repository is a **narrative disclosure and standards proposal**. It is not
a complete public evidence bundle. The `evidence/` directory contains no raw
traffic, row-level observations, account data, PAN/BIN material, tokens,
transaction identifiers, CAVVs, endpoint details, or executable reproduction
material. See [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) and
[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

Every public statement is classified in [CLAIMS.md](CLAIMS.md).

## Corrected empirical statement

The bounded study used one browser-channel integration and seven EMV 3DS 2.2.0
ACS/card-range cohorts. Seven researcher-owned issued controls were paired with
three adjacent same-range Luhn-valid comparison inputs each. The 28 inputs were
observed in five fresh sessions, yielding 140 lookup observations.

Six cohorts produced separate Requestor-visible lookup response classes. One
lookup-uniform cohort separated after the initial CReq: comparison inputs
returned immediate HTML wrappers carrying Final CRes `N`, while the issued
control received HTML defining a credential-choice/OTP interface. The client
inspected the returned HTML as text and did not render it, submit data, complete
authentication, or attempt authorization.

This establishes repeatable input-correlated response classes in the tested
integration. The comparison inputs had unknown issuance status. The observation
does not establish account validity, payment usability, internal component
attribution, notification behavior in other flows, prevalence, or impact.

### C-03a: client-visible frictionless authentication artifacts

Selected challenge-free responses exposed non-empty CAVV fields, ECI,
`paresStatus`, authentication identifiers, and integration-reported liability
indicators before financial authorization. These observations establish
client-visible authentication artifacts in selected responses. They do not
establish that a cryptogram is valid, reusable, sufficient for authorization,
or tied to an active or usable account.

## Evidence ledger

| Claim ID | Evidence class | Scope | What it establishes | Limit |
|---|---|---|---|---|
| C-03 | Bounded live observation | Seven cohorts; 28 inputs; five fresh sessions each | Six lookup-stage and one initial-CReq-stage response-class separations | Comparison-input issuance unknown; no prevalence or account-validity conclusion |
| C-04 | Bounded continuation observation | One lookup-uniform cohort; initial CReq only | Lookup uniformity did not persist to the first CReq in that integration | Text-HTML inspection only; no rendered UI, authentication, or authorization |
| C-06 | Patent disclosure | US 2026/0134429 A1 | Disclosed abnormal-network-traffic detection architecture | Not evidence of deployment or operation in the study |
| C-07 | Third-party static review | Archived source snapshots | Intended lookup classification, access gating, and optional proxy-routing code paths | Not evidence of execution, current availability, accuracy, use, or prevalence |
| P-01/P-02 | Proposal | Public reform and test documents | A concrete requirements and testing framework | No implementation is certified |

## Supporting material categories

### Normative sources

Use [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md) for versioned Core, FAQ, and
patent pinpoint references. Protocol sources establish message ordering and
responsibilities. They do not establish public reachability, deployment behavior,
or account-state truth.

### Direct public operationalization evidence

The public evidence set includes reviewed archives, listed below without
reproducing their code:

| Artifact | Archive | What the public source establishes | Limit |
|---|---|---|---|
| Telegram-bot Braintree 3DS/VBV handler | https://perma.cc/2QL8-9KKR | A membership-gated workflow intended to obtain Braintree authorization, submit caller-provided card data, invoke lookup, classify returned status, and select rotating SOCKS5 routing. | Does not establish present execution, endpoint availability, accuracy, volume, third-party use, or prevalence. |
| Adyen-labeled Telegram checker | https://perma.cc/Z7E3-KWYT | Repository snapshot presenting a Telegram card-checking bot with an Adyen-labeled gateway. | Repository metadata alone does not establish the exact downstream response. |
| `3dali.php` Adyen-labeled gateway | https://perma.cc/PBA6-AUG5 | Source labels the gate `3D Adyen`, selects `app.saleor.adyen`, submits encrypted payment and browser/risk data, and classifies Saleor `AUTHORIZATION_ACTION_REQUIRED` as `3D Card`. Saleor documents that its Adyen app returns this state when an Adyen response contains a storefront action; Adyen defines `ChallengeShopper` as one specific 3DS shopper-interaction result. | Direct evidence of an implemented Adyen/Saleor 3DS action-required classifier. The file does not preserve or parse the underlying Adyen `resultCode` or action type, so it cannot distinguish `ChallengeShopper`, `IdentifyShopper`, `RedirectShopper`, or another provider action. |
| BraintreeCHK | https://perma.cc/A25F-XA7V | Public packaging and advertised Braintree VBV/3DS card-checking functionality. | Advertisement/repository snapshot; exact runtime behavior was not independently measured. |
| MeduzaV3 | https://perma.cc/KV3L-7ZQG | Public packaging of broader card-checking functionality. | Does not establish use against the study cohorts or current operation. |
| MeduzaV3 promotion | https://perma.cc/9VUB-A9BE | Public promotion and distribution interest. | Promotional material, not technical validation. |
| pubstripe 3DS implementation | https://perma.cc/9VSU-SGYN | Code showing constructed browser metadata, programmatic Stripe 3DS invocation, parsed status, and optional proxy routing. | Cross-family scriptability evidence; not classified as proof of unlawful use. |
| Commercial 3DS Lookup API listing | https://perma.cc/G84X-8L43 | Publicly advertised 3DS support, issuer metadata, and risk-scoring functionality. | Advertisement only; backend and accuracy not verified. |

The Telegram handler is direct public evidence of an implemented lookup-stage
classification workflow, rather than an advertisement alone. This conclusion
is stage-specific: it does not show public use of the separate initial-CReq
differential observed in the controlled study. It also does not establish
current operation, execution success, accuracy, volume, or prevalence.

### Documentation and interface mapping

The documented 24-path core corpus and separate 16-path extension are ecosystem
interface mapping. They show where documentation describes branch or progression
output. They are not tested deployments, vulnerability prevalence, or evidence
that an unauthorized caller can use a classifier.

## Future aggregate evidence

A future public artifact must contain only safe aggregates with:

- claim IDs, capture date, source category, scope, limitations, and hash;
- no account, range, issuer, endpoint, token, correlation, raw-message, or
  fine-grained timing information; and
- completed redaction, rights, and independent-review metadata.

Use the schema in [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md). Add
metadata to `EVIDENCE_MANIFEST.json` and regenerate `evidence/SHA256SUMS` only
after human review.

## Living record and feedback

The linked arXiv monograph will receive corrected and expanded versions as
additional review, sources, affected-party feedback, and authorized evidence
become available. Corrections and technical feedback are welcome through a
repository issue and should name the relevant claim or evidence entry. The
public record will date and track substantiated changes in
[CORRECTIONS.md](CORRECTIONS.md).

AI assistance for writing and editorial support only is disclosed in
[AI_ASSISTANCE.md](AI_ASSISTANCE.md).

## Coordination records

Tracker identifiers and organization outcomes in [TIMELINE.md](TIMELINE.md) are
researcher-reported unless a reviewed, publishable acknowledgment is included.
They document contact and chronology, not independent technical validation.
