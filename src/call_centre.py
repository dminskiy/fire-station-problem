from typing import List, Optional
from dataclasses import dataclass
import datetime
import random

from src.call import CallPriority, Call, Caller
from src.employee import EmployeeSeniorotyLevel, Employee


@dataclass
class CallCentreConfig:
    juniors: int
    seniors: int
    managers: int
    directors: int
    max_call_duration_sec: int
    call_escalation_prob: float

    def __post_init__(self):
        if not 0.0 <= self.call_escalation_prob <= 1.0:
            raise ValueError("Escalation probability must be between 0 and 1")

        if (
            self.juniors < 0
            or self.juniors < 0
            or self.seniors < 0
            or self.managers < 0
            or self.directors < 0
        ):
            raise ValueError("Number of employees must be positive")


class CallCentre:
    def __init__(self, config: CallCentreConfig):
        # mimic DB id count
        self._employee_count = 0
        self._caller_count = 0
        self._config = config

        self.employees = {
            EmployeeSeniorotyLevel.JUNIOR: self._create_employees_batch(
                config.juniors, EmployeeSeniorotyLevel.JUNIOR, is_free=True
            ),
            EmployeeSeniorotyLevel.SENIOR: self._create_employees_batch(
                config.seniors, EmployeeSeniorotyLevel.SENIOR, is_free=True
            ),
            EmployeeSeniorotyLevel.MANAGER: self._create_employees_batch(
                config.managers, EmployeeSeniorotyLevel.MANAGER, is_free=True
            ),
            EmployeeSeniorotyLevel.DIRECTOR: self._create_employees_batch(
                config.directors, EmployeeSeniorotyLevel.DIRECTOR, is_free=True
            ),
        }

        # First in first out (queue)
        self.call_backlog: List[Call] = []
        self.active_calls: List[Call] = []

    def dispatch_call(
        self, caller_name: str, priority: CallPriority, verbose: bool = False
    ):
        call = self._register_call(caller_name, priority)
        call.assign(call_centre=self)
        if verbose:
            print("\n !! New Call Received !!")
            print(call)

    def review_active_calls(self, escalate: Optional[bool] = None):
        """
        Mimics end of chat

        escalate = None for random escalation
        """
        inds_to_remove = []
        for ind in range(len(self.active_calls)):
            call = self.active_calls[ind]
            if call.expired:
                inds_to_remove.append(ind)
                call.end(call_centre=self, escalate=escalate)

        # remove back to front to keep the order
        inds_to_remove.sort(reverse=True)
        for ind in inds_to_remove:
            self.active_calls.pop(ind)

    def review_backlog(self):
        backlog_len = len(self.call_backlog)
        for _ in range(backlog_len):
            call = self.call_backlog.pop(0)
            call.assign(call_centre=self)

    def display_status(self):
        free_staff = self.free_staff_detailed
        total_staff = (
            self._config.juniors
            + self._config.seniors
            + self._config.managers
            + self._config.directors
        )

        print("\nFire Station Call Centre Current Status")
        print("\n#### Employees (available/total):")
        print(f"\n## Staff Available: {free_staff['total']} / {total_staff}")
        print(
            f"## Juniors: {free_staff[EmployeeSeniorotyLevel.JUNIOR]} / {self._config.juniors}"
        )
        print(
            f"## Seniors: {free_staff[EmployeeSeniorotyLevel.SENIOR]} / {self._config.seniors}"
        )
        print(
            f"## Managers: {free_staff[EmployeeSeniorotyLevel.MANAGER]} / {self._config.managers}"
        )
        print(
            f"## Directors: {free_staff[EmployeeSeniorotyLevel.DIRECTOR]} / {self._config.directors}"
        )
        print("\n#### Call Queues:")
        print(f"\n## Active Calls: {len(self.active_calls)}")
        print(f"## Calls in Backlog: {len(self.call_backlog)}")

    def _create_employees_batch(
        self, num_employees: int, seniority: EmployeeSeniorotyLevel, is_free: bool
    ) -> List[Employee]:

        out_list = []
        for _ in range(num_employees):
            out_list.append(
                Employee(
                    uid=self._employee_count,
                    seniority=seniority,
                    is_free=is_free,
                )
            )
            self._employee_count += 1

        return out_list

    def _register_call(self, caller_name: str, priority: CallPriority) -> Call:
        caller = Caller(name=caller_name, uid=self._caller_count)
        self._caller_count += 1

        return Call(
            timestamp=datetime.datetime.now(),
            caller=caller,
            priority=priority,
            duration_sec=random.randint(1, self._config.max_call_duration_sec),
            call_escalation_prob=self._config.call_escalation_prob,
            assigned_to=None,
        )

    @property
    def free_staff(self) -> int:
        free_staff = 0
        for seniority_level in self.employees.keys():
            for employee in self.employees[seniority_level]:
                if employee.is_free:
                    free_staff += 1

        return free_staff

    @property
    def free_staff_detailed(self):
        free_staff = {}
        free_staff_total = 0
        for seniority_level in self.employees.keys():
            free_staff[seniority_level] = 0

        for seniority_level in self.employees.keys():
            for employee in self.employees[seniority_level]:
                if employee.is_free:
                    free_staff[seniority_level] += 1
                    free_staff_total += 1

        free_staff["total"] = free_staff_total  # type: ignore
        return free_staff
