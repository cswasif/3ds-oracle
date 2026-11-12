# Proposed conformance-test framework

This framework tests the proposed Anti-Oracle Requirements in
[CONSORTIUM_REFORM.md](CONSORTIUM_REFORM.md). It is not a current certification
program and must use isolated or expressly authorized environments with
issuer- or scheme-controlled synthetic accounts.

## Required report header

Every report must state:

- profile and implementation versions; component ownership; and test date;
- written authorization scope, contacts, stop conditions, and cleanup plan;
- synthetic account fixture classes and independently established ground truth;
- browser, network, cache, clock, and load conditions;
- canonicalization algorithm for dynamic correlation values;
- sample size per class, exclusions, invalid-run policy, and stopping rule;
- categorical pass criteria; timing/size equivalence method, margin,
  confidence level, and multiple-comparison treatment; and
- SHA-256 hashes of reviewed aggregate results and redaction review status.

## Test matrix

| ID | Requirement | Test | Pass criterion |
|---|---|---|---|
| T-01 | AR-01 | Change one committed context field at a time: Requestor, payment token, amount, currency, endpoint, version, state, expiry. | Each changed request creates a new context or reaches AR-05 reject; no hidden-state work occurs. |
| T-02 | AR-02 | Compare unadmitted synthetic active, inactive, blocked, nonexistent, and out-of-range classes. | Every class reaches the identical declared terminal browser profile before hidden-state work. |
| T-03 | AR-03 | Replay, race, retry, and mutate one transition identifier. | At most one decision occurs; exact retry returns only the cached reference; all invalid cases use AR-05 reject. |
| T-04 | AR-04 | Capture browser and Requestor-facing output at every state, including initial frictionless ARes release. | Every output validates against the versioned stage allowlist; raw reasons/artifacts are absent. |
| T-04a | AR-04/AR-07 | Compare selected initial frictionless outputs before authorization. | `transStatus`, ECI, Authentication Value/CAVV, `paresStatus`, liability data, reasons, and result handles are confined or explicitly allowlisted; report does not infer authorization success from presence. |
| T-05 | AR-05 | Compare malformed, expired, replayed, wrong-state, wrong-audience, and missing evidence. | Exact categorical profile match; size and timing distributions satisfy the declared pre-registered equivalence criterion. |
| T-06 | AR-06 | Exercise bound success, failure, timeout, unavailable, not-attempted, stale reuse, and contradictory callback. | Trusted telemetry records the declared state; no invalid state becomes success. |
| T-07 | AR-07 | Compare browser callback with authenticated backend result; test downstream mismatch, expiry, and reuse. | Browser has only allowlisted flow control; benefit is granted only to exact valid contextual match. |
| T-08 | AR-08 | Cover lookup, first CReq, challenge UI, Final CRes, OOB, Notification URL, RReq/RRes, timeout, abuse block, and abandonment. | Each client output is allowlisted; omitted or altered negotiated protection fails closed. |
| T-09 | AR-14 | Execute a predeclared synthetic campaign matrix distributed across approved source identities and contexts. | Report declared detection rate, false-positive rate, time-to-detect, containment action, and confirm no detector-specific client output. |

## Statistical rules

A profile must publish the timing and size method before testing. At minimum it
must define: sample size, warm/cold cache treatment, outlier policy, clock
source, response-size canonicalization, a two-sided equivalence margin,
confidence level, and multiple-comparison method. A single delay, median, or
unbounded “normal variation” claim is not evidence of equivalence.

## Safe result schema

Release only aggregates. Do not publish PAN, BIN, issuer name, endpoint,
transaction identifier, token, CAVV, raw HTTP body, fine-grained timestamp, or
reusable session material.

| Field | Example |
|---|---|
| test_id | `T-05` |
| profile_version | `draft-1` |
| fixture_class | `synthetic_nonexistent` |
| stage | `first_creq` |
| sample_count | `100` |
| categorical_match | `true` |
| size_bucket_match | `true` |
| timing_method | `predeclared_equivalence_test` |
| timing_pass | `true` |
| exception_id | `none` |
| aggregate_hash | `sha256:...` |

## Closure artifact

A closure report must identify every tested component and version, AR and test
IDs, owners, exceptions, expiration date, aggregate hash, and reviewer. A
component-only test cannot close a composed-flow finding.
