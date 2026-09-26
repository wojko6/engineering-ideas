# Publication policy

This repository is designed to remain safe for public viewing while still
containing useful engineering detail.

The policy is intentionally stricter than "do not commit passwords". A useful
portfolio repository should avoid exposing unnecessary deployment-specific
metadata even when that metadata is not itself a credential.

## Allowed content

Prefer:

- conceptual architecture;
- bounded MVP definitions;
- reproducible test methodology;
- sanitized diagrams;
- public product/model information;
- documentation-only example addresses and domains;
- summarized measurements that do not identify private infrastructure;
- links to public implementation repositories;
- explicit limitations and open questions.

## Do not commit

Do not add:

- passwords, API tokens, auth keys or session cookies;
- SSH, TLS, VPN or other private keys;
- Tailscale node state or authentication material;
- real public, private or tailnet device addresses;
- real hostnames, DDNS names or internal DNS names;
- MAC addresses;
- serial numbers, account IDs or device identifiers;
- disk UUIDs, PARTUUIDs or filesystem identifiers;
- raw packet captures;
- raw DNS logs;
- raw router/system logs;
- browser HAR files or raw WebRTC dumps;
- screenshots that reveal unrelated personal or infrastructure data;
- personal browsing history;
- production configuration copied verbatim from a device;
- secrets that have merely been redacted in the latest revision but remain in
  Git history.

Use RFC-defined documentation examples or abstract labels such as
`router`, `client-a`, `printer`, `collector` and `wan` instead of real
deployment identifiers.

## Before each public change

Check:

1. Does the change describe an idea as an idea rather than as a deployed fact?
2. Are all addresses, names and identifiers synthetic or intentionally public?
3. Does any screenshot, log excerpt or capture expose unrelated data?
4. Is raw evidence actually necessary, or can a minimized summary prove the
   same point?
5. Are links relative where appropriate and still valid?
6. Does the change duplicate operational source-of-truth material from another
   repository?
7. Does `python3 scripts/check-public-readiness.py` pass?

## If sensitive data is committed

Do not rely on a follow-up commit that simply deletes or masks it.

If a credential or secret was committed:

1. revoke or rotate it first;
2. remove it from the current tree;
3. rewrite affected Git history where appropriate;
4. invalidate old references/caches where possible;
5. re-audit the rewritten history before publication.

If the exposed value is deployment metadata rather than a credential, evaluate
whether history rewriting is still warranted based on the sensitivity of the
information.

## Evidence boundary

Implementation evidence belongs in the repository that owns the implementation,
after sanitization.

This incubator may link to that evidence, but should not accumulate raw captures,
private logs or device-specific exports merely for convenience.
