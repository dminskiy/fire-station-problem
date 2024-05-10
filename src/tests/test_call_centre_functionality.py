import time

from src.call_centre import CallCentre, CallCentreConfig, CallPriority
from src.employee import EmployeeSeniorotyLevel


class TestCallCentreFunctionality:
    def test_review_active_calls(self):
        config = CallCentreConfig(
            juniors=5,
            seniors=0,
            managers=0,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        call_centre = CallCentre(config)

        for i in range(5):
            call = call_centre._register_call(
                caller_name="John Cena",
                priority=CallPriority.LOW,
            )
            if i % 2 == 0:
                call.duration_sec = 1
            else:
                call.duration_sec = 99999
            call.assign(call_centre)

        assert len(call_centre.active_calls) == 5

        time.sleep(1)

        call_centre.review_active_calls(escalate=False)

        assert len(call_centre.active_calls) == 2
        assert call_centre.free_staff == 3

    def test_review_backlog(self):
        config = CallCentreConfig(
            juniors=2,
            seniors=2,
            managers=1,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        call_centre = CallCentre(config)

        call_priorities = [CallPriority.HIGH] * 2 + [CallPriority.LOW] * 5

        for priority in call_priorities:
            call = call_centre._register_call(caller_name="Abc", priority=priority)
            call.duration_sec = 1
            call_centre.call_backlog.append(call)

        # Assings 1 High to Manager & 4 Low
        call_centre.review_backlog()

        assert len(call_centre.call_backlog) == 2
        assert call_centre.free_staff == 0

        time.sleep(1)

        # End current calls
        call_centre.review_active_calls(escalate=False)
        assert len(call_centre.active_calls) == 0
        assert call_centre.free_staff == 5

        # Fill in the remaining two calls
        call_centre.review_backlog()

        assert len(call_centre.call_backlog) == 0
        assert call_centre.free_staff == 3

        time.sleep(1)

        # End the final 2 calls
        call_centre.review_active_calls(escalate=False)
        assert len(call_centre.active_calls) == 0
        assert len(call_centre.call_backlog) == 0
        assert call_centre.free_staff == 5

    def test_dispatch_call(self):
        config = CallCentreConfig(
            juniors=2,
            seniors=2,
            managers=2,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        call_centre = CallCentre(config)

        for _ in range(5):
            call_centre.dispatch_call(
                caller_name="John Cena", priority=CallPriority.HIGH
            )

        call_centre.display_status()

        assert len(call_centre.active_calls) == 2
        assert len(call_centre.call_backlog) == 3
        assert call_centre.free_staff_detailed[EmployeeSeniorotyLevel.JUNIOR] == 2
        assert call_centre.free_staff_detailed[EmployeeSeniorotyLevel.SENIOR] == 2
