# Contributing

Contributions that improve technical accuracy, reproducibility or architecture
clarity are welcome.

## Good contributions

Examples include:

- correcting a technical error;
- improving a validation method;
- narrowing an over-broad claim;
- identifying a missing failure case;
- improving rollback or acceptance criteria;
- fixing broken internal links;
- proposing a clearly bounded alternative architecture.

## Keep ideas bounded

An idea should normally contain:

- the problem;
- the intended outcome;
- constraints;
- a bounded MVP;
- risks and failure modes;
- validation/evidence expectations;
- promotion criteria.

Avoid turning a concept document into an unbounded feature list.

## Scope and source-of-truth rule

Before expanding an idea, check whether another document already owns the same
engineering question.

Prefer:

```text
one primary owner for the result
+ links from related ideas
```

over copying the same test plan, evidence or conclusion into multiple concepts.

When a test supports several ideas:

- keep the canonical methodology/result with the idea that owns the question;
- link to it from adjacent ideas;
- keep implementation/runtime evidence in the repository that owns the running
  system;
- use this incubator for architecture, bounded plans, sanitized summaries and
  promotion criteria.

## Public-data rule

Before opening a pull request, read [PUBLICATION.md](PUBLICATION.md).

Do not include private deployment details, real infrastructure identifiers,
credentials, raw captures, logs or other personal data.

Run:

```sh
python3 scripts/check-public-readiness.py
```

before submitting a change.

## Status language

Use precise wording:

- **Concept** — design only.
- **Planned** — intended work, not yet performed.
- **Observed** — directly measured in a defined test.
- **Validated** — acceptance criteria were met with retained evidence.
- **Not tested** — no evidence exists yet.
- **Inconclusive** — available evidence does not support a firm result.

A proposal should never be written as though it were already deployed.
