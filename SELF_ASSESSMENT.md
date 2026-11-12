# Authorized self-assessment procedure

This is a defensive procedure for systems you own or are explicitly authorized
to test. It is not a tool and does not authorize testing public merchants,
issuers, gateways, or real cardholders.

## Safety rules

- Use an isolated environment with issuer- or scheme-controlled synthetic
  accounts and independently established ground truth.
- Obtain written authorization covering the Requestor, gateway, 3DS Server, DS,
  ACS, issuer, notification, and authorization components in scope.
- Predeclare volume, repetition count, network conditions, monitoring contacts,
  stop conditions, cleanup, and any permitted continuation step.
- Never use real third-party account data. Do not publish PAN/BIN fragments,
  tokens, transaction IDs, CAVVs, raw captures, endpoint recipes, or reusable
  material.
- Stop before credential submission, OTP, completed authentication, or payment
  authorization unless authorization expressly includes that step.

## Pre-registration

Before testing, record:

1. implementation and profile versions;
2. synthetic fixture classes: active, inactive, blocked, nonexistent, and out
   of range;
3. channel under observation: browser, Requestor-facing API, authenticated
   backend, operational, or authorization handoff;
4. canonicalization rule for dynamic transaction/correlation values;
5. samples per class, warm/cold-cache policy, invalid-run criteria, and
   stopping rule;
6. categorical comparison rule; and
7. timing/size method, equivalence margin, confidence level, and
   multiple-comparison policy.

## Procedure

1. **Map the state machine.** Identify initiation, preparation/range handling,
   initial ARes, frictionless result release, first CReq, each challenge method,
   OOB, Final CRes, Notification URL, RReq/RRes, result retrieval,
   authorization handoff, timeout, abandonment, error, replay, and abuse-block
   transitions.
2. **Review early frictionless release.** Before authorization, test every
   browser- and Requestor-facing initial result for `transStatus`, ECI,
   Authentication Value/CAVV, `paresStatus`, liability indicators, reason
   fields, result handles, headers, redirects, content type, size, and timing.
   Do not infer cryptogram validity, reuse, payment approval, or account status
   from an artifact's presence alone.
3. **Test unadmitted queries.** For each controlled hidden class, submit only
   the profile-approved unadmitted request. Record whether a hidden-state read
   occurred and compare the complete declared terminal observation.
4. **Test admitted continuations.** Verify that a successful authorization
   basis is bound to exactly one account/token, Requestor, merchant/acquirer,
   checkout, amount, currency, state, endpoint, age, and replay record before
   hidden-state-dependent work or result release.
5. **Test mutation controls.** Change one context field at a time; test expiry,
   wrong audience, wrong state, replay, concurrent first use, exact retry,
   altered retry, missing/altered negotiated protection, and legacy fallback.
6. **Record each public stage.** Capture only approved aggregate classes for
   protocol/integration state, status, headers, content type, redirect graph,
   normalized outer template, size bucket, timing distribution, UI category,
   and notification telemetry.
7. **Assess detection safely.** Run the preapproved synthetic campaign matrix
   across authorized source identities and contexts. Measure declared detection
   rate, false-positive rate, time-to-detect, containment action, and whether a
   detector outcome created a unique client-visible class.
8. **Fix and retest.** Apply the relevant AR controls and rerun the same
   pre-registered matrix. Do not call a changed test matrix a retest.
9. **Publish safely.** Release only redacted aggregate results using the schema
   in [CONFORMANCE_FRAMEWORK.md](CONFORMANCE_FRAMEWORK.md).

## Result template

| Test ID | Stage | Channel | Fixture class | Samples | Categorical match | Size match | Timing method/pass | Hidden read before authority | Exception |
|---|---|---|---|---:|---|---|---|---|---|

## Success criteria

A deployment passes only when it shows, for the declared profile and test
matrix:

- unadmitted fixture classes receive the same declared terminal public profile
  before attacker-triggerable hidden-state work;
- admitted processing is bound to the exact verified context;
- invalid and replayed transitions do not create another hidden-state decision;
- browser/API output remains within its stage allowlist;
- authoritative reasons and authentication artifacts remain on trusted channels;
- detector actions do not produce their own client-visible classification signal;
  and
- all exceptions are documented, owned, time-bounded, and retested.
