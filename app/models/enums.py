from enum import StrEnum


class ProjectStatus(StrEnum):
    IDEA = "idea"
    DESIGN = "design"
    ASSEMBLY = "assembly"
    BRING_UP = "bring_up"
    INTEGRATION = "integration"
    TEST = "test"
    DONE = "done"


class RepositoryPlatform(StrEnum):
    GITHUB = "github"
    GITLAB = "gitlab"


class HardwareIssueCategory(StrEnum):
    POWER = "power"
    MCU_BOARD = "mcu_board"
    SENSOR = "sensor"
    COMMUNICATION = "communication"
    STORAGE = "storage"
    MECHANICAL_WIRING = "mechanical_wiring"
    ENVIRONMENT_TEMPERATURE = "environment_temperature"
    OTHER = "other"


class HardwareIssueSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HardwareIssueStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    FIXED = "fixed"
    DEFERRED = "deferred"
