# Mitigation guidance

This guide separates **current-version containment** from **future
architectural closure**. Do not claim that a rate limit, payment intent,
response wrapper, transaction identifier, telemetry signal, or downstream
authorization check alone closes a pre-proof response differential.

The control IDs refer to [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md). The
relevant channels and threat prerequisites are in [THREAT_MODEL.md](THREAT_MODEL.md).

## Immediate containment for current EMV 3DS deployments

### 1. Bound and preserve transaction context — AR-01

Gateways, 3DS Servers, and requestors should create a short-lived server-side
context before AReq creation. Bind Requestor, merchant/acquirer scope,
checkout, payment-method token, amount, currency, version, endpoint, state,
expiry, and nonce. Create a new context when a committed field changes.

This prevents detached and altered transitions. It does **not** establish
authority over a newly supplied payment account.

### 2. Make transitions one-use and idempotent — AR-03

Use atomic consume records for state-changing continuation values. An exact
retry may return a cached result reference; modified, expired, replayed, or
wrong-state input must not repeat account-dependent processing. Keep detailed
failure reasons on trusted channels.

### 3. Publish and enforce browser/API allowlists — AR-04

For each visible state, allow only the fields, headers, content type,
redirects, template, error class, and dynamic correlation values required by
that version and state. Do not reflect raw ARes/RReq objects, raw reasons,
account-state semantics, detector state, ECI, Authentication Value/CAVV, or
liability data into browser or Requestor-facing outputs.

Result confinement reduces unnecessary disclosure. It does not hide a prior
Method, route, challenge, or terminal-state distinction.

### 3a. Review the initial frictionless result — AR-04 and AR-07

A frictionless initial ARes may be returned before financial authorization.
Review every browser- and Requestor-facing initial result for `transStatus`,
ECI, Authentication Value/CAVV, `paresStatus`, liability indicators, reasons,
result handles, headers, redirects, content type, size, and timing. Confine
nonessential authentication artifacts to trusted channels. The presence of an
artifact is not proof of cryptogram validity, reuse, payment authorization, or
account status.

### 4. Use one reject profile for unadmitted queries — AR-05

Expired, malformed, replayed, consumed, wrong-state, wrong-audience, and
context-mismatched requests should receive the same profile-defined terminal
browser observation. Define the exact body schema, status, headers, redirects,
size bucket, deadline, retry text, and timing test in advance. Remove semantic
and structural differences before evaluating timing.

### 5. Treat telemetry as risk input, not authority — AR-06

Track bound success, explicit failure, timeout, unavailable, not attempted,
and approved reuse distinctly on trusted channels. A browser flag, JavaScript
assertion, client-supplied success value, or transaction identifier must not
independently prove telemetry completion or account authority.

### 6. Confine authoritative results and bind authorization — AR-07

Return authoritative authentication result, reasons, ECI, Authentication Value,
liability information, and detector data through authenticated backend or
operational channels. At authorization, verify the exact Requestor,
merchant/acquirer, payment-token, amount, currency, message-category, age,
and consumption binding before granting any authentication-derived benefit.

This protects payment authorization. It cannot retract an earlier disclosure.

### 7. Detect abnormal network traffic without creating a new public signal

Schemes and operators should aggregate activity across Requestors,
merchant/acquirer context, ranges, context churn, devices, network identities,
and authentication-without-authorization patterns. Per-IP limits alone are not
enough. The patent terminology is useful here: feature data, snapshot data, a
trained model, probability score, threshold, notification, pause, and block
are detection concepts described in US 2026/0134429 A1. They should influence
trusted routing or containment, not create a detector-specific client response.

## Future architectural closure — AR-02 and AR-08

A profile claiming that an unadmitted caller cannot learn hidden account state
must verify independent exact-query authority before any attacker-triggerable
account, enrollment, range, route, Method, ACS, or online-status operation.
If that authority is absent, it must terminate without that operation and with
one hidden-state-independent public observation.

This rule does not require all legitimate post-admission challenge and
frictionless outcomes to be identical. It distinguishes an unadmitted query
from an authorized protocol continuation. First-use, 3RI, recurring, and
decoupled flows need a separately defined authority or disclosure policy.

## Validate the complete state machine

Use the synthetic-only tests in [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md)
and the safe procedure in [SELF_ASSESSMENT.md](SELF_ASSESSMENT.md). Review
lookup, first CReq, challenge UI, OOB, Final CRes, Notification URL, RReq/RRes,
timeout, abandonment, errors, abuse blocks, result retrieval, and authorization
handoff. A component-only pass cannot demonstrate composed-flow closure.
