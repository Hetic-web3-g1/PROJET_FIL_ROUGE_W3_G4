# Contributing Guide !

## Backend

### Pull requests

```
<type>(<scope>): <short summary>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Commit Scope: api|services|database|etc.
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|test
```

The `<type>` and `<summary>` fields are mandatory, the `(<scope>)` field is optional.

- Follow the above convention for commits messages (At least on the first commit of the PR). PR name will take the value of the commit message.
- The PR can include multiples small commits. Github will squash them when merging.
- Provide detailed description of the bug in the PR, or link to an issue that does.
