from ..core.enums import Severity, Priority


SEVERITY_TO_PRIORITY = {
    Severity.CRITICAL: Priority.P1,
    Severity.HIGH: Priority.P2,
    Severity.MEDIUM: Priority.P3,
    Severity.LOW: Priority.P4,
}


def normalize_priority(severity: str) -> str:
    """Convert severity to priority using deterministic backend rules.

    Raises ValueError if severity is not recognized.
    """
    severity_enum = Severity(severity)
    return SEVERITY_TO_PRIORITY[severity_enum]


def priority_from_severity(severity: str) -> str:
    """Alias for normalize_priority for clarity."""
    return normalize_priority(severity)