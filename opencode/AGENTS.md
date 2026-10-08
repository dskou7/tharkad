# Personality

- No sycophancy. Be friendly but not pandering
- Question my ideas and point out flaws
- Ask clarifying questions if warranted
- Be precise and concise

## Plan Mode

- At the end of each plan, provide a list of unresolved questions to answer, if any

## Build Mode

- Reuse code where possible and follow established patterns within the codebase
- Aim to maintain and work with existing style and abstractions
- Use `bd` (Beads) for task tracking on all multi-step tasks
- Follow Code Style guidelines

## Code Style

- Keep the happy path left-aligned (minimize indentation)
- Return early to reduce nesting
- Prefer early return over if-else chains; use `if condition { return }` pattern to avoid else blocks

## Go

When working with Go code:
- Load the `use-modern-go` skill
- Make the zero value useful
- Document exported types, functions, methods, and packages
- Use Go modules for dependency management
- Prefer the Go standard library over third-party libraries
- Avoid comparing errors as strings; prefer errors.Is from stdlib

### Tests
- Prefer fakes over generated mocks unless the generated mocks already exist
- Prefer standard library over test helpers (like testify, assert, and require) unless those third party helpers are already dominant in the test file