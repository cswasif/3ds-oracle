# Scope, ethics, and publication safety

## Dual-use handling

This repository documents a public-interest security finding, disclosure history, evidence boundaries, mitigation guidance, and an authorized self-assessment procedure. It intentionally excludes operational material that would make live abuse easier.

It does not contain:

- tooling for enumerating or classifying card numbers;
- card-number lists, issuer range maps, or account-narrowing PAN fragments;
- client tokens, authorization fingerprints, CAVVs, transaction IDs, or reusable session material;
- merchant, issuer, or ACS endpoint recipes;
- reviewed archive links used to document third-party operationalization evidence; or
- scripts or requests that interact with live 3DS systems; or
- unredacted private correspondence or third-party personal data.

The public record may link to a reviewed third-party source snapshot only when
its evidentiary purpose, stage specificity, and limitations are stated beside
the link. It must not reproduce operational code, endpoints, tokens, account
data, or step-by-step workflow detail. Exact reproductions remain restricted to
authorized coordination channels.

## Test conduct

The live study was bounded and used researcher-owned issued controls with adjacent Luhn-valid comparison inputs. The comparison inputs did not have independently established issuance status. No mass scanning was performed.

The primary measurements stopped at the first requestor-visible lookup result. A separate bounded observation for one lookup-uniform cohort sent only the initial browser CReq to determine whether response uniformity persisted. The non-browser client did not execute the returned HTML, forward its form, select a delivery method, enter or submit credentials or an OTP, complete authentication, or submit payment authorization.

A separate exploratory A/B observation compared an identical bounded Mastercard input set under concentrated network egress and distributed residential SOCKS5 egress on the tested device-data path. This was not a production-scale evasion experiment. No internal detector, feature set, or decision was observed, and the result is not represented as bypass of a specifically identified model.

No SMS, email, OTP, or push notification was observed on researcher-controlled recipient channels while the returned credential-selection HTML was inspected as text. This non-observation is not generalized to a rendered browser flow, OOB, decoupled authentication, or independent issuer notification systems.

See the monograph's methodology and limitations for the full account.

## Evidence discipline

Public statements distinguish:

- normative protocol structure;
- bounded client-visible observations;
- conditional architectural inference;
- third-party reports and public advertisements; and
- untested risk scenarios.

Client-visible statuses and UI behavior are not presented as universal ground truth for account existence, issuance, card activity, or payment usability. Private evidence must be redacted and reviewed before publication. Raw requests, operational endpoint details, and reusable transaction material remain withheld.

## Public-interest rationale

The issue crosses administrative boundaries and related authentication-BIN abuse is documented publicly by industry sources. Coordination ran for more than 180 days before public disclosure. Local operators can close specific reachable paths, while consistent ecosystem treatment requires coordination among merchants, gateways, 3DS Server providers, schemes, directory servers, ACS operators, issuers, EMVCo, and PCI SSC.

## Authorized research only

The self-assessment procedure is for systems the operator owns or is explicitly authorized to test. Use isolated test environments, test accounts, approved volumes, monitoring, and stop conditions. Do not test third-party merchants, issuers, gateways, or live cardholders without written authorization.

## Corrections and affected-party statements

Open an issue for factual corrections or a takedown request concerning accidentally exposed sensitive information. Corrections will be dated and applied promptly. Affected parties are welcome to provide a public statement or technical clarification for linking from the disclosure record.
