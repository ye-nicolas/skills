# Finding Calibration

Use the lowest priority that accurately reflects the demonstrated impact.

| Priority | Meaning | Typical evidence |
|---|---|---|
| P0 | Immediate release blocker or catastrophic impact | Reliable data loss, critical security boundary bypass, or service-wide failure on the normal path |
| P1 | High-impact correctness or security defect that should be fixed before merge | Common input returns the wrong result, transaction leaves inconsistent state, authorization can be bypassed |
| P2 | Material defect, regression risk, or verification gap with bounded impact | Important failure path is wrong, compatibility breaks a known caller, changed framework behavior is untested |
| P3 | Low-impact but actionable maintainability or robustness problem introduced by the change | Misleading contract or localized complexity likely to cause a future error |

Do not report preferences, speculative hardening, or unrelated cleanup as P3.

Use this compact structure:

```text
[P1] Short outcome-focused title
Location: path/to/File.java:line
Trigger: concrete input, state, caller, or deployment condition
Impact: expected versus actual behavior and consequence
Evidence: relevant code path, contract, test, or configuration
Remedy: smallest coherent correction
Verification: focused test or command
Confidence: high | medium | low
```

Keep the location on changed code and the range as small as possible. If the
root cause is outside the diff, anchor the finding to the changed line that
exposes or depends on it and explain the connection.
