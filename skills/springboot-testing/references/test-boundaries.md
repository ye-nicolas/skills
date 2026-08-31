# Spring Test Boundaries

Choose the narrowest boundary that keeps the behavior under test real. Confirm
annotation and client availability from the repository's Spring Boot version.

| Claim | Typical boundary | Keep real | Usually isolate |
|---|---|---|---|
| Pure domain or service decision | Plain JUnit | Domain objects and decision code | Remote or expensive collaborators |
| MVC route, binding, validation, status, headers, body, controller advice | MVC slice or focused HTTP test | MVC configuration, codecs, validation, exception mapping | Service collaborator when its behavior is not the claim |
| WebFlux route or streaming contract | WebFlux slice or `WebTestClient` test | Publisher chain, codecs, error mapping, cancellation where material | Remote publishers when protocol behavior is not the claim |
| JSON mapping | JSON slice or focused mapper test | Configured modules, naming, null and unknown-field behavior | Unrelated application beans |
| Blocking or reactive HTTP client | Client slice, mock server, or focused integration | Request construction, status mapping, codecs, timeout/retry policy | Real downstream service unless contract integration is required |
| JPA mapping, query, constraint, or transaction | Persistence slice or focused integration | Entity mappings, repository, transaction manager, relevant database semantics | HTTP and unrelated services |
| Security filter or method authorization | Security-enabled slice or integration test | Filter chain, authentication mapping, authorization decision | Identity provider unless its protocol is under test |
| Message serialization, listener, acknowledgement, retry, or dead letter | Listener/container or broker integration test | The delivery mechanism named in the claim | Unrelated downstream effects |
| Configuration binding or conditional wiring | Focused context runner or application-context test | Binding, conditions, bean graph under the selected properties | Unrelated auto-configuration where exclusions are supported |
| Cross-boundary application behavior | Focused full application integration | Only the boundaries needed for the user-visible claim | External systems replaced at their owned ports |

Use a full application test only when the claim genuinely crosses several
Spring boundaries or verifies wiring that slices cannot represent. A context
that starts successfully does not prove endpoint, transaction, security,
message, or error behavior without a focused assertion.

For provider-specific claims, prefer the production technology through the
repository's existing container or managed-test support. An in-memory database
is sufficient only when the behavior does not depend on production SQL,
locking, isolation, constraints, or migration semantics.
