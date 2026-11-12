# Release checklist

Run this checklist before tagging, depositing, or widely announcing a release.

- [ ] Every public assertion maps to [CLAIMS.md](CLAIMS.md).
- [ ] Every standards or patent assertion maps to [SOURCE_CROSSWALK.md](SOURCE_CROSSWALK.md).
- [ ] Live evidence uses `input-correlated`, not account-validity language,
      unless synthetic ground truth is independently recorded.
- [ ] Every organization outcome is marked researcher-reported unless a
      reviewed acknowledgment is included.
- [ ] Third-party source snapshots are described as static review only; no
      direct operational code, live endpoint recipe, token, PAN fragment,
      transaction identifier, CAVV, or reusable session material is included.
- [ ] Outbound links were reviewed for sensitive or uncorrected content.
- [ ] `evidence/` either contains reviewed aggregate-only artifacts and a
      manifest, or the release is labeled a narrative disclosure and proposal.
- [ ] Any evidence file has source, capture date, redaction review status,
      limitations, SHA-256, and publication-rights record.
- [ ] `CITATION.cff` and `.zenodo.json` have the exact tag version and release
      date, valid schema, current abstract, and correct related identifier.
- [ ] The release distinguishes current-version containment from future
      architectural closure.
- [ ] The proposed conformance framework identifies test inputs, normalization,
      sample size, timing method, thresholds, and pass/fail artifacts.
- [ ] The license covers every included file type, including scripts.
- [ ] A final human reviewer checked the rendered GitHub Markdown and all links.
