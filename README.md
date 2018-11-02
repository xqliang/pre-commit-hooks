pre-commit-hooks
==========

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/xqliang/pre-commit-hooks
        rev: v0.0.1  # Use the ref you want to point at
        hooks:
        -   id: check-author-identity
        # -   id: ...


### Hooks available

- `check-author-identity` - Check git author name and email.
