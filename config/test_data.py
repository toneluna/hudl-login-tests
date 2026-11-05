"""Shared test data that is safe to commit (no secrets)."""

# An address with no Hudl account, used to reach the password step without
# touching a real account. example.com is reserved for documentation and
# testing, so this can never belong to a real user.
UNKNOWN_EMAIL = "no.such.user.12345@example.com"
