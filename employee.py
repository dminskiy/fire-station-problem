from enum import Enum
from dataclasses import dataclass


class EmployeeSeniorotyLevel(Enum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    MANAGER = "Manager"
    DIRECTOR = "Director"


@dataclass
class Employee:
    seniority: EmployeeSeniorotyLevel
    uid: int
    is_free: bool

    def __str__(self) -> str:
        return f"uid: {self.uid} | seniority: {self.seniority.value} | is_free: {self.is_free}"
