# Mitigation guidance

This guide separates **current-version containment** from **future
architectural closure**. A rate limit, payment intent, response wrapper,
transaction identifier, client-side telemetry signal, or downstream financial
authorization check alone does not resolve an observable response discrepancy
(CWE-204) or covert timing channel (CWE-208).

The control IDs refer to [CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md). The
relevant channels and threat prerequisites are in [THREAT_MODEL.md](THREAT_MODEL.md).

## Immediate containment for current EMV 3DS deployments

### 1. Bound and preserve transaction context: AR-01

Gateways, 3DS Servers, and requestors should create a short-lived server-side
context before AReq creation. Cryptographically bind Requestor identity,
merchant/acquirer scope, checkout session, payment-method token, amount,
currency, version, endpoint, state, expiry, and nonce. Create a new context
whenever a committed field changes.

This prevents detached and altered transitions. It does **not** establish caller
authority over a newly supplied payment account.

### 2. Make transitions one-use and idempotent: AR-03

Use atomic consume records for state-changing continuation values. An exact
retry may return a cached result reference; modified, expired, replayed, or
wrong-state input must not repeat account-dependent processing. Keep detailed
diagnostic failure reasons on trusted server channels.

### 3. Publish and enforce browser/API allowlists: AR-04 (CWE-209 mitigation)

For each visible protocol state, allow only the specific fields, headers, content
type, redirects, template, error class, and dynamic correlation values required
by that version and state. Do not reflect raw ARes/RReq objects, diagnostic
reasons (e.g., Reason 98, Reason 08), internal account status (e.g., whether an
account exists, is active, or expired), detector state, ECI, Authentication
Value/CAVV, or liability indicators into browser or Requestor-facing outputs.

Sanitizing error messages (CWE-209 mitigation) and confining authentication
artifacts prevents direct information disclosure. However, it does not conceal
prior route, challenge selection, or terminal-state differences.

### 3a. Review the initial frictionless result: AR-04 and AR-07

A frictionless initial ARes may be returned before financial authorization.
Review every browser- and Requestor-facing initial result for `transStatus`,
ECI, Authentication Value/CAVV, `paresStatus`, liability indicators, reason
fields, result handles, headers, redirects, content type, size, and timing.
Confine nonessential authentication artifacts to trusted channels. The presence
of an artifact is not proof of cryptogram validity, reuse, payment authorization,
or account validity.

### 4. Enforce response uniformity and constant-time processing: AR-05 (CWE-204 / CWE-208 mitigation)

Expired, malformed, replayed, consumed, wrong-state, wrong-audience, and
context-mismatched requests should receive one uniform, profile-defined terminal
observation across all card networks (e.g., Visa, Mastercard).

- **Response uniformity (CWE-204 mitigation):** Define the exact body schema,
  HTTP status, headers, redirects, size bucket, retry text, and terminal message
  in advance so the client receives identical output regardless of internal
  account status.
- **Constant-time / dummy processing (CWE-208 / CWE-385 mitigation):** When a
  range check fails or an account is not found, execute dummy processing or
  timing padding to ensure that early local drops do not finish hundreds of
  milliseconds faster than downstream Directory Server or ACS queries.

### 5. Treat telemetry as risk input, not authority: AR-06 (CWE-602 mitigation)

Track bound success, explicit failure, timeout, unavailable, not attempted,
and approved reuse distinctly on trusted channels. A browser flag, JavaScript
assertion, client-supplied success value, or transaction identifier must not
independently prove telemetry completion or account authority (mitigating
Client-Side Enforcement of Server-Side Security, CWE-602).

### 6. Confine authoritative results and bind authorization: AR-07

Return authoritative authentication results, reason codes, ECI, Authentication
Value, liability information, and risk scores exclusively through authenticated
backend or operational channels. At financial authorization, verify the exact
Requestor, merchant/acquirer, payment-token, amount, currency, message-category,
age, and consumption binding before granting any authentication-derived benefit.

This protects payment authorization. It cannot retract an earlier disclosure
leaked during authentication lookup.

### 7. Detect abnormal network traffic without creating a public signal: AR-14 (CWE-307 mitigation)

Schemes and operators should aggregate activity across Requestors,
merchant/acquirer context, ranges, context churn, devices, network identities,
and authentication-without-authorization patterns to prevent card testing
sweeps (CWE-307 mitigation). Per-IP rate limits alone are insufficient against
distributed proxy networks.

Detection concepts described in US 2026/0134429 A1 (e.g., feature data, snapshot
data, trained models, probability scores, thresholds, notifications, pauses, and
blocks) should influence internal risk scoring or trusted routing. They must
never trigger a detector-specific client response that leaks internal defense
state to the adversary.

## Future architectural closure: proof-first behavior ordering (CWE-696 remediation): AR-02 and AR-08

A profile claiming complete architectural closure must remediate the underlying
behavior ordering flaw (CWE-696: Incorrect Behavior Order). The protocol must
verify independent caller authorization before executing any attacker-triggerable
operation on internal account state (e.g., whether an account exists, is active,
or expired), enrollment, range routing, 3DS Method, or ACS availability.

If that authority is absent, the system must terminate processing without
querying core ledgers and return one uniform, state-independent observation.

This rule does not require all legitimate post-admission challenge and
frictionless outcomes to be identical. It establishes a strict security boundary
between an unadmitted query and an authorized transaction continuation.
First-use, 3RI, recurring, and decoupled flows require separately defined
authority and disclosure policies.

## Validate the complete state machine

Use the synthetic-only tests in [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md)
and the defensive procedures in [SELF_ASSESSMENT.md](SELF_ASSESSMENT.md).
Review lookup, first CReq, challenge UI, OOB, Final CRes, Notification URL,
RReq/RRes, timeout, abandonment, errors, abuse blocks, result retrieval, and
authorization handoff. A component-only pass cannot demonstrate composed-flow
closure.
