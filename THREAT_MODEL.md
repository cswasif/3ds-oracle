# Threat model and security objective

## Channels

The disclosure distinguishes six channels. A control valid on one channel does
not automatically protect another.

1. **Browser-observable:** HTML, JSON, form fields, HTTP status and headers,
   redirects, size and timing classes, iframe behavior, and accessible UI.
2. **Requestor-facing API:** inputs and outputs accepted by an upstream caller
   before a trusted server boundary.
3. **Authenticated backend:** merchant, gateway, and 3DS Server exchanges.
4. **3DS protocol links:** protected 3DS Server--DS--ACS processing.
5. **Operational channel:** detection, telemetry, review, incident, and reason
   data available only to authorized operators.
6. **Authorization handoff:** later financial authorization and any
   authentication-derived benefit.

## Threat condition

A practical pre-proof classifier requires all of the following:

- a caller can submit or influence an account-specific query;
- the caller lacks an independently verified authorization basis for that exact
  account and operation;
- a hidden account, enrollment, range, route, Method, ACS, or policy state is
  read or influences processing before authorized disclosure;
- the caller observes a repeatable difference in the declared public channel;
  and
- admission and aggregate controls permit useful sampling.

The bounded study establishes input-correlated differences in one tested
integration. It does not establish every premise for every deployment.

## Security objective

For an **unadmitted query**, all hidden account classes must receive one
profile-defined terminal browser-visible observation. The system must not
perform or release an attacker-triggerable hidden-state-dependent continuation
before an independent authorization basis for the exact account and operation
has been verified.

For an **admitted query**, the system may release the minimum genuine next
action required by the protocol, but only for the exact context that was
verified. The profile must separately bind requestor, merchant/acquirer scope,
checkout, payment-method reference, amount, currency, version, endpoint,
state transition, validity interval, and replay state.

## Consequences

- A transaction context proves preservation of selected inputs; it does not by
  itself prove authority over a newly supplied account.
- A browser correlation identifier is a public handle, not proof of browser or
  cardholder identity.
- Response normalization is complete only if the compared hidden states share
  the same public state machine. Otherwise it is containment, not closure.
- Authorization correlation is necessary for payment safety but cannot retract
  a disclosure made during authentication.
- First-use, cardholder-absent, recurring, and decoupled cases require their
  own authorization or disclosure policy. They must not inherit a claim of
  pre-proof closure by default.
