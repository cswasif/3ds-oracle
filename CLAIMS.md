# Claim ledger

This ledger separates what the public record establishes from what it proposes.
Each public statement must link to one of these claim IDs. No claim in this
repository establishes account existence, payment usability, exploitation
prevalence, financial loss, or the internal decision of a 3DS component.

| ID | Claim | Class | Evidence and scope | Explicit limit |
|---|---|---|---|---|
| C-01 | A Browser frictionless response can return an initial result before financial authorization, while a Browser challenge needs flow-control and correlation state after it is selected. | Protocol structure | EMV 3DS Core v2.3.1.1, Browser AReq/ARes and CReq/CRes processing; see [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md). | Does not require raw ARes reflection to an arbitrary external caller. |
| C-02 | Core Browser processing includes account- or range-dependent operations before an initial frictionless result or a later optional fresh challenge proof. | Protocol structure | Core Req. 80, 89, 97--98, and 105. | Internal processing alone is not a public oracle. |
| C-03 | The tested browser-channel integration produced repeatable input-correlated response classes in seven bounded ACS/card-range cohorts: six at lookup and one after the initial CReq. | Bounded observation | 28 inputs, five fresh sessions each, 140 lookup observations; [EVIDENCE.md](EVIDENCE.md). | Comparison-input issuance was not independently established; no prevalence, component-attribution, or account-validity conclusion follows. |
| C-03a | Selected challenge-free client responses exposed non-empty CAVV fields, ECI, `paresStatus`, authentication identifiers, and integration-reported liability indicators before authorization. | Bounded observation | Selected challenge-free responses in the tested integration. | The cryptograms were not independently validated or tested in authorization; no usability, account-status, or reuse conclusion follows. |
| C-04 | A uniform lookup response can leave a later observable distinction at the first CReq. | Bounded observation | One lookup-uniform cohort under the separately bounded initial-CReq observation. | Returned HTML was inspected as text; no browser render, credential submission, completed authentication, or authorization occurred. |
| C-05 | Under the stated admission and release premises, an attacker can use a pre-proof input-correlated distinction as a classifier. | Conditional inference | The logical implication is stated in [THREAT_MODEL.md](THREAT_MODEL.md). | The premises are not asserted for every 3DS deployment. |
| C-06 | Detection of an authentication BIN attack can use feature data, snapshot data, a trained model, a probability score, a threshold, notification, pausing, or blocking. | Patent disclosure | US 2026/0134429 A1, paragraphs [0013]--[0044]; terminology follows the application. | A patent application is not evidence of deployment, effectiveness, or use in the tested integration. |
| C-07 | Public operationalization evidence | Archived third-party sources | The Telegram Braintree handler contains a membership-gated lookup-classification workflow with optional SOCKS5 routing. A separate Adyen-labeled gateway selects `app.saleor.adyen` and classifies `AUTHORIZATION_ACTION_REQUIRED` as `3D Card`; related archives show packaging, promotion, and cross-family scriptability. | The Adyen-labeled source does not contain literal `resultCode=ChallengeShopper`; source review does not establish current operation, successful execution against a target, accuracy, volume, third-party use, or prevalence. |
| C-08 | Current-version controls can reduce reachability, replay, and unnecessary semantics, but cannot prove removal of a pre-proof distinction when the public state machine itself branches on hidden state. | Engineering conclusion | Derived from C-01 through C-05 and the proposed control model. | It is not a claim that all current deployments leak. |
| P-01 | The Anti-Oracle Requirements (AR) are proposed requirements for future certification and deployment profiles. | Proposal | [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md). | They are not current EMVCo, PCI SSC, scheme, issuer, or vendor requirements. |
| P-02 | The proposed conformance-test framework can measure a versioned profile against synthetic account classes and a declared public observation contract. | Proposal | [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md). | No implementation has yet been certified by this repository. |

## Claim rules

- State the claim ID in issues, releases, and action-register updates.
- Use **input-correlated** for the live comparison inputs. Reserve
  **account-class** for issuer-controlled synthetic fixtures with known ground
  truth.
- Label all organization outcomes as researcher-reported unless a reviewed,
  publishable acknowledgment is linked.
- A proposal must never be described as a deployed fix.
- A claim is superseded only through [CORRECTIONS.md](CORRECTIONS.md).
