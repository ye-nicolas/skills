---
name: springboot-security
description: Design, implement, or review Spring Boot security boundaries including authentication, authorization, CSRF/CORS, secrets, sensitive data, rate limiting, uploads, and dependency risk. Use when security behavior is materially in scope, not merely because a project depends on Spring Security.
metadata:
  origin: ECC
---

# Spring Boot Security

Establish the threat model, trust boundaries, credential transport, deployment
topology, and supported Spring Security version before changing configuration.
Preserve deny-by-default behavior and test the actual filter chain and method
authorization rather than reasoning from annotations alone.

## Framework-first security

Before writing a custom filter, token parser, authorization helper, validator, header writer, or rate-limit wrapper, inspect the configured Spring Security and Spring Boot extension points. Prefer `SecurityFilterChain`, resource-server support, method security, `AuthorizationManager`, Bean Validation, built-in CSRF/CORS/header configuration, password encoders, and the project's existing security components when they satisfy the requirement. Do not bypass framework security with ad hoc checks in controllers or services. Verify the actual dependency version and security configuration before using an API.

For security tests, use Spring Security test support and the project's assertion
conventions. Do not add a custom filter or token parser when resource-server,
session, authorization-manager, or framework header support already owns the
contract.

## When to Activate

- Adding authentication (JWT, OAuth2, session-based)
- Implementing authorization (@PreAuthorize, role-based access)
- Validating user input (Bean Validation, custom validators)
- Configuring CORS, CSRF, or security headers
- Managing secrets (Vault, environment variables)
- Adding rate limiting or brute-force protection
- Scanning dependencies for CVEs

## Authentication

Choose sessions, JWT access tokens, opaque tokens, mTLS, or another mechanism
from the clients, revocation requirement, identity provider, and operational
model; none is a universal default.

- Prefer Spring Security resource-server support for bearer tokens and its
  configured decoder/introspector, validators, entry points, and error mapping.
- Prefer framework session management for browser sessions. Set cookie
  `HttpOnly`, `Secure`, path/domain, and `SameSite` according to the actual
  cross-site login and request flows; `Strict` is not always compatible.
- Define issuer, audience, algorithm/key trust, clock skew, expiry, revocation,
  and credential rotation. Do not accept a token merely because it parses.
- Add a custom authentication filter only for a protocol the framework cannot
  represent. Specify ordering, failure handling, context cleanup, async
  dispatch behavior, and tests before implementation.

## Authorization

- Deny by default and grant the smallest authorities/scopes required.
- Put URL rules and method authorization at deliberate boundaries. Do not rely
  on URL matching alone when object, tenant, or state ownership matters.
- Use method security and a domain-aware `AuthorizationManager` or authorization
  service when the decision needs resource data. Keep SpEL expressions small
  enough to remain testable and reviewable.
- Verify unauthenticated, insufficient-authority, wrong-tenant/owner, stale
  resource, and permitted cases, including whether denied requests leak resource
  existence.

## Input Validation

- Use Bean Validation with `@Valid` on controllers
- Apply constraints on DTOs: `@NotBlank`, `@Email`, `@Size`, custom validators
- Validate syntax and domain constraints at the owning boundary. Encode output
  for its destination; sanitize only content intentionally supporting a
  restricted markup format.

Use dedicated request types with size, format, collection-cardinality, and
nested validation appropriate to the endpoint. Revalidate authorization and
invariants after loading authoritative server-side state; client validation is
not a security boundary.

## Injection boundaries

Use parameter binding for repository, JDBC, and native queries. Never build SQL,
JPQL, shell commands, LDAP filters, redirects, templates, or log formats by
concatenating untrusted data. Validate identifiers that cannot be bound, such
as dynamic sort fields, against an explicit allowlist.

## Password Encoding

- Use the application's configured adaptive `PasswordEncoder`; never store
  plaintext or invent a password-hashing format.
- Select and benchmark algorithm parameters for the deployment and support
  gradual rehash through an explicit migration policy.

Use a `PasswordEncoder` bean and the project's delegating/versioned encoding
format so parameters can migrate. Keep raw credentials out of logs, events,
exceptions, long-lived objects, and equality/diagnostic methods.

## CSRF Protection

- For browser session apps, keep CSRF enabled; include token in forms/headers
- Disable CSRF only when browsers cannot automatically attach any credential
  accepted by the endpoint. The label "API" or the presence of bearer-token
  support is not sufficient by itself.

When disabling CSRF is justified, keep the decision next to the accepted
credential and session configuration and add a test proving that no
automatically attached credential can authorize the protected request.

## Secrets management

- Never store a live secret in source, committed configuration, examples, logs,
  or agent configuration.
- Resolve secrets from the platform's secret store or an approved injected
  reference. Environment variables may be a delivery mechanism but are not a
  secret store by themselves.
- Scope credentials to the minimum permissions and lifetime. On suspected
  exposure, revoke or rotate first; deleting the plaintext copy is not enough.

Prefer workload identity or short-lived platform credentials over a long-lived
bootstrap token. Keep only a secret reference in ordinary configuration and
ensure failure messages do not echo the resolved value.

## Security headers

Use Spring Security's header support. Configure CSP, framing, referrer policy,
HSTS, content-type behavior, and permissions policy from the deployment and
rendered-content contract. Do not add obsolete headers mechanically, enable
HSTS on an HTTP-only development path, or assume one CSP works for every
endpoint.

## CORS

Configure CORS in the Spring Security chain using the servlet or reactive source
appropriate to the stack. Restrict origins, methods, headers, and exposed
headers to supported browser clients. Do not combine credentialed requests with
wildcard origins, and do not treat CORS as authentication or protection for
non-browser clients.

## Rate limiting and abuse controls

Define what is protected, the stable identity, trusted-proxy boundary, limit
scope, burst policy, distributed consistency, storage cardinality, eviction,
and failure mode. Prefer an existing gateway or shared limiter. An unbounded
per-IP map inside one JVM is not a production default. Return the API's
documented `429` response and retry hints, and observe rejects without logging
sensitive identity data.

## Dependency Security

- Apply the repository's configured dependency and support policy. Run its
  existing scanner and CI gate when present; do not introduce OWASP Dependency
  Check, Snyk, or another service without a requested build or security change.
- Keep Spring Boot and Spring Security within the application's supported and
  compatible version policy; do not upgrade solely to make a scanner green.
- Triage findings by
  affected version, exploitability/reachability, severity, available fix, and
  documented suppression; do not treat every scanner match as equally blocking.

## Logging and PII

- Never log secrets, tokens, passwords, or full PAN data
- Redact sensitive fields; use structured JSON logging

## File Uploads

- Enforce request and decompressed size limits; validate media by content rather
  than trusting filename or client-provided content type.
- Generate storage names, prevent traversal, store outside executable/web
  roots, and scan or isolate content according to its risk.

## Checklist Before Release

- [ ] Auth tokens validated and expired correctly
- [ ] Authorization guards on every sensitive path
- [ ] Inputs validated; output encoded or intentionally sanitized for its sink
- [ ] No string-concatenated SQL
- [ ] CSRF posture correct for app type
- [ ] Secrets externalized; none committed
- [ ] Security headers configured
- [ ] Abuse controls applied where the threat model requires them
- [ ] Configured dependency checks passed and versions meet support policy
- [ ] Logs free of sensitive data

**Remember**: Deny by default, validate inputs, least privilege, and secure-by-configuration first.
