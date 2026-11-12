# Source crosswalk

This crosswalk records what each source supports and, equally importantly, what
it does not support. It is a source map, not a substitute for the normative
source documents.

| Source | Pinpoint | Supports | Does not support |
|---|---|---|---|
| EMV 3-D Secure Protocol and Core Functions Specification v2.3.1.1 | Browser flow Req. 80 | Range-specific protocol-version lists and, when present, 3DS Method URL retrieval from prior PRes data. | A fresh DS query per transaction, arbitrary-caller access, or public account-status disclosure. |
| Same | Req. 89 | 3DS Server DS selection using BIN and optionally other Cardholder Account Information. | A requirement to expose selected routing to an upstream caller. |
| Same | Reqs. 97--98 | DS participating-range and ACS-capability checks before forwarding to an ACS. | That a failed check proves account nonexistence or becomes browser-visible. |
| Same | Req. 105 | ACS uses Cardholder Account Number to determine whether authentication is available or can be completed. | A deterministic mapping from a particular account state to a public result. |
| Same | Req. 117 | The Requestor Environment determines challenge continuation after the response reaches it. | A requirement to project raw branch data to an arbitrary API consumer. |
| Same | Reqs. 447--451 | Requestor-initiated SPC can return status S, credential-list data, and SPC transaction data before the later holder assertion and second AReq. | That any particular deployment exposes this material to an untrusted party. |
| Same | Req. 210 and Annex A.12.3 | Unknown non-critical extensions are ignored and passed; unknown critical extensions are invalid, and critical extensions require EMVCo assignment. | That an optional extension prevents omission or legacy fallback. |
| EMV 3DS FAQ | Version-specific CRes and timeout guidance | Final-CRes and timeout interpretation used to scope the observation. | Behavior of the tested integration beyond captured observations. |
| US 2026/0134429 A1, *Systems and Methods for Use in Identifying Feature Data Consistent with Abnormal Network Traffic* | [0005], [0013]--[0015] | The disclosed threat model: estimated or guessed credentials and authentication responses used as signals. | Deployment, incidence, or effectiveness of the disclosed method. |
| Same | [0027]--[0035] | Feature data, snapshot data, transaction/BIN/merchant context, and trained-model examples. | That a specific deployed detector uses every example feature. |
| Same | [0036]--[0044]; claims 1--20 | Score/threshold decision, notification, AReq/ARes signaling, pausing, and blocking as disclosed responses to abnormal network traffic. | That a Reason-98-related client response proves this application or its model was used. |

## Citation policy

Use the patent's terms — **estimated or guessed credential**, **authentication
BIN attack**, **abnormal network traffic**, **feature data**, **snapshot data**,
**trained model**, **probability score**, **threshold**, **notify**, **pause**,
and **block** — only when describing the patent's disclosed threat and
detection architecture. Use EMV role names elsewhere.

All public claims should link to [CLAIMS.md](CLAIMS.md) and this crosswalk.

## Adyen/Saleor action-required mapping

| Source | Pinpoint | Supports | Does not support |
|---|---|---|---|
| [Saleor Adyen App overview](https://docs.saleor.io/developer/app-store/apps/adyen/overview) | Assumptions for transaction initialization/processing | The Adyen app can return `AUTHORIZATION_ACTION_REQUIRED` or `CHARGE_ACTION_REQUIRED` when an Adyen response contains an `action` for the storefront; the state can also occur when no `pspReference` is returned. | That every `AUTHORIZATION_ACTION_REQUIRED` is an Adyen `ChallengeShopper` result. |
| [Saleor payment-app guide](https://docs.saleor.io/developer/extending/apps/building-payment-app) | Follow-Up Actions | An action-required Saleor result asks the customer to complete 3DS, a redirect, mobile approval, or another provider step; Saleor passes provider action data to the storefront. | Which provider-specific result caused an archived action-required state. |
| [Adyen payment result codes](https://docs.adyen.com/online-payments/build-your-integration/payment-result-codes) | 3DS2 result codes | `ChallengeShopper` means issuer-required shopper authentication; `IdentifyShopper` means device fingerprinting; `RedirectShopper` means external authentication. | That Saleor's generic action-required state preserves the exact Adyen result-code name. |
| [Adyen Browser 3DS2 integration](https://docs.adyen.com/online-payments/classic-integrations/classic-api-integration/3d-secure-authentication/native-3ds2/browser-based-integration) | Challenge flow | A `ChallengeShopper` result instructs the integration to create a challenge flow; it may follow the initial payment request or device-fingerprint result. | That the archived `3dali.php` response took this exact path, because the file does not parse the underlying result code or action object. |
