# Threat model and security objective

## Channels and weakness mapping

The disclosure distinguishes six protocol and operational channels. Under MITRE
CWE guidelines, a defense applied on one channel does not automatically protect
another.

1. **Browser-observable channel:** HTML, JSON, form fields, HTTP status and
   headers, redirects, response size, timing discrepancies (CWE-208 / CWE-385),
   iframe behavior, and accessible UI. Relying on client-side browser execution
   or script checks introduces Client-Side Enforcement of Server-Side Security
   (CWE-602).
2. **Requestor-facing API:** inputs and outputs accepted by an upstream caller
   (e.g., merchant checkout or gateway API) before a trusted server boundary.
   In-band error reflection here exposes sensitive diagnostic codes (CWE-209).
3. **Authenticated backend:** merchant, gateway, and 3DS Server exchanges.
4. **3DS protocol links:** protected 3DS Server, Directory Server (DS, operated
   by card schemes, e.g., Visa, Mastercard), and Access Control Server (ACS)
   processing.
5. **Operational channel:** detection telemetry, dispute review, incident logs,
   and scheme monitoring available only to authorized infrastructure operators.
6. **Authorization handoff:** subsequent financial authorization requests (ISO
   8583 / ISO 20022) and authentication-derived liability benefits.

## Threat condition: account enumeration oracle (CWE-204)

An adversary exploits the pre-authorization protocol as an account enumeration
oracle (CWE-204: Observable Response Discrepancy) when all of the following
conditions are satisfied:

- **Caller query access:** an unauthenticated or untrusted caller can submit or
  influence an account-specific authentication query (AReq);
- **Incorrect behavior order (CWE-696):** the protocol architecture inspects
  core ledger or cardholder account state before establishing that the caller
  possesses verified authority to query that specific account;
- **Internal state query:** internal account status (e.g., whether an account
  exists, is active, or expired), enrollment, range routing, 3DS Method, ACS,
  or policy state is evaluated before caller proof-of-authority;
- **Observable response discrepancy (CWE-204 / CWE-203):** the caller observes a
  repeatable difference in client-visible responses, status codes, error payloads
  (CWE-209), or timing behavior (CWE-208) on a public channel; and
- **Sampling capacity:** upstream admission and rate-limiting controls (CWE-307)
  permit the caller to execute sufficient probes across card ranges.

The bounded study in this repository establishes observable response
discrepancies in one tested integration. It does not claim that every deployment
exhibits identical behavior.

## Security objective: response uniformity and complete mediation

For an **unadmitted or unauthenticated query**, all account classes (e.g.,
active, inactive, expired, nonexistent, or blocked) must receive one uniform,
profile-defined terminal response. The system must not execute or expose an
attacker-triggerable ledger query or state-dependent continuation before an
independent authorization basis for the exact account and operation has been
verified.

For an **admitted query**, the system may release only the minimum necessary
next action required by the protocol, strictly bound to the verified context.
The security profile must cryptographically bind Requestor identity,
merchant/acquirer scope, checkout session, payment token reference, transaction
amount, currency code, protocol version, endpoint, state transition, validity
interval, and replay state.

## Protocol consequences

- A transaction context proves preservation of selected caller inputs; it does
  not by itself prove caller authority over a newly supplied account number.
- A browser session cookie or correlation identifier is a public handle, not
  cryptographic proof of cardholder identity.
- Response normalization achieves true closure only if the compared internal
  account states share the exact same state-machine transitions and constant
  timing (CWE-208 mitigation). Otherwise, superficial wrapper normalization
  provides only containment, not closure.
- Downstream payment authorization linkage is necessary for transaction safety,
  but it cannot retract an earlier information disclosure (CWE-204 / CWE-209)
  leaked during pre-authorization lookup.
- First-use, cardholder-absent, recurring, and decoupled payment flows require
  their own explicit authorization policies. They must not inherit an assumption
  of pre-authorization security by default.
