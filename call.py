from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass

import datetime
import random

from employee import Employee, EmployeeSeniorotyLevel


class CallPriority(Enum):
    HIGH = auto()
    LOW = auto()


EMPLOYEE_ASSIGNMENT_ORDER = {
    CallPriority.LOW: [
        EmployeeSeniorotyLevel.JUNIOR,
        EmployeeSeniorotyLevel.SENIOR,
        EmployeeSeniorotyLevel.MANAGER,
    ],
    CallPriority.HIGH: [
        EmployeeSeniorotyLevel.MANAGER,
        EmployeeSeniorotyLevel.DIRECTOR,
    ],
}


@dataclass
class Caller:
    uid: int
    name: str


@dataclass
class CallInfo:
    timestamp: datetime.datetime
    caller: Caller
    priority: CallPriority
    duration_sec: int
    call_escalation_prob: float
    assigned_to: Optional[Employee] = None
    assigned_at: Optional[datetime.datetime] = None


class Call:
    def __init__(self, *args, **kwargs) -> None:
        self._info = CallInfo(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"Call. Priority: {self.priority} | Claller ID: {self.caller.uid}"
            f" | Assigned to: {self.assigned_to} | Duration: {self.duration_sec}"
        )

    def assign(self, call_centre):
        """
        Assign a call to the first applicable employee.
        If such employee is not found, add the call to the backlog.
        """
        if self.assigned_to is not None:
            raise ValueError("Cannnot assign a call that is already assigned")

        for seniority_level in EMPLOYEE_ASSIGNMENT_ORDER[self.priority]:
            if self.assigned_to:
                break

            for employee in call_centre.employees[seniority_level]:
                if employee.is_free:
                    self.assigned_to = employee
                    self.assigned_at = datetime.datetime.now()
                    call_centre.active_calls.append(self)
                    employee.is_free = False
                    break

        if self.assigned_to is None:
            call_centre.call_backlog.append(self)

    def end(self, call_centre, escalate: Optional[bool] = None):
        assigned_employee = self.assigned_to
        if assigned_employee is None:
            raise RuntimeError("Cannot end an unassigned call")

        self.assigned_to = None
        assigned_employee.is_free = True

        if self.priority == CallPriority.LOW and self._should_escalate(escalate):
            self.priority = CallPriority.HIGH
            self.assign(call_centre)

    def _should_escalate(self, escalate: Optional[bool] = None):
        prob_escalate = self.call_escalation_prob
        return (
            escalate
            if escalate is not None
            else random.choices(
                [True, False], weights=[prob_escalate, 1 - prob_escalate], k=1
            )[0]
        )

    @property
    def expired(self):
        if self.assigned_to is None:
            return False

        since_assignment = datetime.datetime.now() - self.assigned_at
        if since_assignment.total_seconds() >= self.duration_sec:
            return True
        else:
            return False

    @property
    def timestamp(self) -> datetime.datetime:
        return self._info.timestamp

    @timestamp.setter
    def timestamp(self, val: datetime.datetime):
        self._info.timestamp = val

    @property
    def caller(self) -> Caller:
        return self._info.caller

    @caller.setter
    def caller(self, val: Caller):
        self._info.caller = val

    @property
    def priority(self) -> CallPriority:
        return self._info.priority

    @priority.setter
    def priority(self, val: CallPriority):
        self._info.priority = val

    @property
    def duration_sec(self) -> int:
        return self._info.duration_sec

    @duration_sec.setter
    def duration_sec(self, val: int):
        self._info.duration_sec = val

    @property
    def assigned_to(self) -> Employee:
        return self._info.assigned_to

    @assigned_to.setter
    def assigned_to(self, val: Employee):
        self._info.assigned_to = val

    @property
    def assigned_at(self) -> datetime.datetime:
        return self._info.assigned_at

    @assigned_at.setter
    def assigned_at(self, val: datetime.datetime):
        self._info.assigned_at = val

    @property
    def call_escalation_prob(self) -> float:
        return self._info.call_escalation_prob
