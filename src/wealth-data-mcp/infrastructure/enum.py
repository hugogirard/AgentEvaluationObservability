from enum import Enum


class AdvisorId(str, Enum):
    ADV_118 = "ADV-118"
    ADV_205 = "ADV-205"
    ADV_301 = "ADV-301"


class RiskProfile(str, Enum):
    AGGRESSIVE = "Aggressive"
    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
