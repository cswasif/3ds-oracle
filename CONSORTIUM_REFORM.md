# Consortium reform proposal

## A proposed anti-oracle profile for browser-mediated EMV 3DS

This is a research proposal for EMVCo, payment schemes, PCI SSC, 3DS Server
providers, Directory Servers (DSs), ACS operators, gateways, acquirers,
issuers, and requestors. It is **not** a statement of adopted EMVCo, scheme,
or PCI requirements.

The proposal separates two goals that are often conflated:

1. **Current-version containment:** restrict query reachability, prevent replay,
   reduce unnecessary client semantics, keep authoritative results on trusted
   channels, and detect abnormal network traffic.
2. **Future architectural closure:** before any attacker-triggerable,
   account-dependent operation, verify independent authority for the exact
   account and operation, or return a single hidden-state-independent terminal
   observation without performing that operation.

Containment reduces practical exploitability. It cannot prove closure when the
public protocol state machine itself branches on hidden state before adequate
query authorization.

See [THREAT_MODEL.md](THREAT_MODEL.md) and [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md)
for terms, boundaries, and source limits.

## 1. Protocol facts and limits

The Core specification establishes an ordering, not a universal public oracle.
A Browser frictionless result may be returned after the initial AReq/ARes
exchange, while a selected Browser challenge requires client flow-control and
correlation state. The following operations may precede either an initial
frictionless result or later fresh challenge proof:
- Req. 80 may retrieve range-specific protocol versions and 3DS Method data;
- Reqs. 97--98 perform range and ACS-capability checks;
- Req. 105 evaluates whether authentication is available; and
- Browser challenge continuation uses correlation state after a challenge is
  selected.

The Core does not require an arbitrary external caller to initiate these steps
or receive raw outcomes. An observable classifier requires the conditions in
[THREAT_MODEL.md](THREAT_MODEL.md).

The 2026 Mastercard patent application uses the terms **estimated or guessed
credential**, **authentication BIN attack**, **abnormal network traffic**,
**feature data**, **snapshot data**, **trained model**, **probability score**,
and **threshold**. It describes notifying, pausing, or blocking after a
processing network identifies a suspected attack. This supports detection as a
complementary control. It does not show that a detector is deployed, that it
operated in the studied integration, or that detection replaces confidential
response handling. See [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md).

## 2. Required channel model

Every profile must identify whether each value is permitted on the browser,
Requestor-facing API, authenticated backend, 3DS protocol link, operational,
or authorization-handoff channel. A value allowed on one channel must not be
copied to another unless the profile explicitly allows that transfer at that
state.

## 3. Anti-oracle requirements

The following use **MUST**, **MUST NOT**, **SHOULD**, and **MAY** as proposed
normative language. Parameters are profile values, not universal constants.

### AR-01: server-created, monotonic transaction context

1. Before creating an AReq, an authorized server component MUST create a
   context identified by an unpredictable reference with at least 128 bits of
   entropy.
2. The context MUST commit to Requestor, merchant/acquirer scope, checkout
   reference, payment-method token reference, amount, currency, message
   category, protocol version, notification-endpoint identity, creation time,
   expiry, current state, permitted next transition, and unique context nonce.
3. Later protocol transaction identifiers MUST be appended through an
   authenticated server transition. No earlier committed field may change.
4. Changed amount, currency, Requestor, payment method, endpoint, version, or
   checkout reference MUST require a new context.
5. Raw PAN and deterministic PAN-derived identifiers MUST NOT appear in
   browser values or assurance logs.

A context preserves submitted fields. It MUST NOT by itself establish authority
over a newly supplied account.

### AR-02: exact-query authority before hidden-state work

1. Before an attacker-triggerable account, enrollment, range, route, Method,
   ACS, or online-status operation, the enforcing component MUST verify an
   authorization basis bound to the exact account and operation, or terminate
   the unadmitted query as defined by AR-08.
2. The authorization basis MUST identify its issuer, intended audience,
   account or token reference, Requestor, merchant/acquirer scope, operation,
   amount, currency, issue time, expiry, and unique event identifier.
3. Possession of a payment intent, browser cookie, TLS session, transaction
   identifier, client JavaScript value, or opaque handle MUST NOT alone satisfy
   this requirement.
4. A profile MAY define distinct authority bases for stored instruments,
   holder-mediated confirmation, or a narrowly scoped prior mandate. Each basis
   MUST define scope, age, revocation, reuse, and audit behavior.

> **Relation to wallet-mediated models (EUDI / OpenID4VP):** Emerging wallet
> architectures (e.g., OpenID4VP with `transaction_data` dynamic linking)
> structurally eliminate lookup-stage oracles by requiring user-initiated
> credential presentation rather than arbitrary card-number probing. For
> standard card-not-present browser flows, AR-02 achieves an equivalent
> boundary by demanding verified query authority before any account-dependent work.

### AR-03: verified, one-use state transitions

1. A security-relevant transition MUST verify evidence source, audience,
   context, predecessor state, requested successor state, payload digest,
   issue time, expiry, and event identifier.
2. The receiver MUST atomically consume each transition identifier at most
   once. Concurrent first-use attempts MUST create at most one new
   account-dependent decision.
3. A permitted retry MUST match the original canonical request digest and MAY
   return only a cached result reference. A changed retry MUST not repeat
   account-dependent processing.
4. Browser values, JavaScript booleans, callback parameters, or correlation
   identifiers MUST NOT independently authorize a transition.

### AR-04: browser-visible allowlists

For every supported version and browser-visible state, the profile MUST publish
a machine-readable allowlist of fields, values, headers, content types,
redirects, templates, error classes, and dynamic correlation fields. Anything
not allowlisted fails certification.

Authoritative reasons, account-state semantics, detector state, ECI,
Authentication Value/CAVV, liability data, and raw ARes/RReq objects MUST be
restricted to authenticated server or operational channels unless a profile
explicitly proves their browser release is necessary and non-sensitive.

### AR-05: unadmitted-query reject equivalence

1. An expired, malformed, replayed, consumed, wrong-state, wrong-audience,
   or context-mismatched unadmitted query MUST use one declared terminal
   browser-visible reject profile.
2. The profile MUST define exact categorical output, headers, content type,
   redirect graph, body schema, retry text, size bucket, deadline, and timing
   test method.
3. Detailed causes MUST stay on authenticated server or operational channels.
4. Random delay does not satisfy this requirement. Deterministic semantic and
   structural differences must be removed before timing equivalence is tested.

### AR-06: telemetry provenance

Telemetry MUST use a closed state set including `bound_success`,
`explicit_failure`, `timeout`, `unavailable`, `not_attempted`, and
`approved_reuse`. Records MUST carry context reference, attempt identifier,
authoritative producer, issue/completion times, and provenance class. Missing,
stale, contradictory, client-only, or context-mismatched telemetry MUST NOT be
upgraded to success.

Telemetry can inform risk. It does not establish exact-query authority or make
a hidden-state-dependent response safe to release.

### AR-07: authoritative-result confinement and authorization linkage

1. The browser MAY receive only an opaque flow reference and the allowlisted
   next action for an admitted query.
2. The authoritative authentication result must be delivered to the Requestor
   or 3DS Server on an authenticated server channel.
3. Before granting an authentication-derived authorization benefit, the
   authorization side MUST match Requestor, merchant/acquirer scope, payment
   token, amount, currency, message category, permitted age, and consumption
   state.
4. Mismatch, expiry, or unauthorized reuse MUST deny the benefit. Each scheme
   exception MUST define allowed variance, age, reuse count, and audit event.

Result confinement is containment. It does not hide an earlier branch, Method,
route, or challenge difference.

### AR-08: complete state-machine and negotiation closure

1. Certification MUST test initiation, preparation/range handling, ARes
   mapping, first CReq response, each challenge method, OOB handoff, Final
   CRes, Notification URL, RReq/RRes reconciliation, checkout return,
   duplicate, error, abuse block, abandonment, and timeout.
2. When all required participants support a protection, offer and selected mode
   MUST be authenticated and committed to the context. Omission, alteration,
   or ignoring of the selected protection MUST cause generic client failure and
   a specific trusted-channel event. Silent fallback is prohibited.
3. Current-version deployments MUST apply AR-01, AR-03--AR-07 as containment.
4. A future profile claiming closure MUST add an account-independent transition
   before range-derived Method work and must make AR-02 mandatory. An optional
   AReq extension alone cannot gate work that has already happened; Req. 210
   also permits unrecognized non-critical extensions to be ignored.

## 4. Proposed conformance-test framework

The detailed framework is [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md).
All tests use issuer- or scheme-controlled synthetic accounts in isolated or
explicitly authorized environments. A certification report must contain the
profile version, input matrix, channel allowlist, canonicalization algorithm,
sample size, invalid-run policy, statistical method, equivalence margins,
results, exceptions, expiry date, evidence hashes, and control owner.

## 5. Ownership and closure

| Party | Requested deliverable |
|---|---|
| EMVCo | Versioned channel model, authority requirement, state-machine profile, and test vectors. |
| Schemes and DS operators | Synthetic-account program, aggregate abnormal-network-traffic controls, trusted-only detector output, and conformance reporting. |
| PCI SSC | Composed-flow assessment scope and evidence requirements. |
| 3DS Server providers and integrators | Context, allowlist, retry, trusted-result, and authorization-linkage implementation evidence. |
| Gateways and Requestors | Bounded initiation, response filtering, context enforcement, and abuse-control reports. |
| ACS operators and issuers | First-CReq/UI/OOB equivalence evidence and issuer-side incident controls. |
| Acquirers and authorization systems | Contextual authentication-result verification and mismatch/replay denial evidence. |

A component certificate alone must not close a composed-flow finding. Closure
requires a versioned conformance report for the Requestor, gateway, 3DS Server,
DS, ACS, notification, result retrieval, and authorization handoff path.

## 6. Rollout

1. Publish current-version containment guidance and the conformance framework.
2. Provide synthetic fixtures and test vectors.
3. Deploy monitored, authenticated capability negotiation where compatible.
4. Require the profile for new and materially changed integrations.
5. Standardize a future mandatory closure profile before range-derived work.
6. Announce legacy sunset only after interoperable evidence exists.

Use [ACTION_REQUEST.md](ACTION_REQUEST.md) for public deliverables and
[ACTION_REGISTER.csv](ACTION_REGISTER.csv) for dated status updates.
