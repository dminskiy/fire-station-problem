import pytest

from call_centre import CallCentre, CallCentreConfig, CallPriority
from employee import EmployeeSeniorotyLevel


class TestCallFunctions:
    def test_call_registration(self):
        config = CallCentreConfig(
            juniors=5,
            seniors=0,
            managers=0,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)
        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.LOW,
        )

        assert registered_call.assigned_to is None
        assert registered_call.duration_sec > 0
        assert registered_call.priority == CallPriority.LOW
        assert registered_call.caller.name == "John Cena"
        assert registered_call.caller.uid == 0

    def test_call_registration_uid(self):
        config = CallCentreConfig(
            juniors=5,
            seniors=0,
            managers=0,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)
        for _ in range(10):
            call_centre._register_call(
                caller_name="John Cena",
                priority=CallPriority.LOW,
            )

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.LOW,
        )

        # check uids are incrementing as axpected
        assert registered_call.caller.uid == 10

    def test_call_assignment_low_priority_simple(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=1,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.LOW,
        )

        registered_call.assign(call_centre)

        assert len(call_centre.active_calls) == 1
        assert registered_call.assigned_to.seniority == EmployeeSeniorotyLevel.JUNIOR
        assert not call_centre.employees[EmployeeSeniorotyLevel.JUNIOR][0].is_free
        assert (
            call_centre.employees[EmployeeSeniorotyLevel.JUNIOR][0].uid
            == registered_call.assigned_to.uid
        )

    def test_call_assignment_high_priority_simple(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=1,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.HIGH,
        )

        registered_call.assign(call_centre)

        assert len(call_centre.active_calls) == 1
        assert registered_call.assigned_to.seniority == EmployeeSeniorotyLevel.MANAGER
        assert not call_centre.employees[EmployeeSeniorotyLevel.MANAGER][0].is_free
        assert (
            call_centre.employees[EmployeeSeniorotyLevel.MANAGER][0].uid
            == registered_call.assigned_to.uid
        )

    def test_call_assignment_low_priority_min_seniority(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=1,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.HIGH,
        )

        registered_call.assign(call_centre)

        assert len(call_centre.active_calls) == 1
        assert registered_call.assigned_to.seniority == EmployeeSeniorotyLevel.MANAGER
        assert not call_centre.employees[EmployeeSeniorotyLevel.MANAGER][0].is_free
        assert (
            call_centre.employees[EmployeeSeniorotyLevel.MANAGER][0].uid
            == registered_call.assigned_to.uid
        )

    def test_call_assignment_low_priority_many(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=1,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        expected_outcomes = [
            {"sl": EmployeeSeniorotyLevel.JUNIOR, "active_len": 1, "backlog_len": 0},
            {"sl": EmployeeSeniorotyLevel.SENIOR, "active_len": 2, "backlog_len": 0},
            {"sl": EmployeeSeniorotyLevel.MANAGER, "active_len": 3, "backlog_len": 0},
            {"sl": None, "active_len": 3, "backlog_len": 1},
            {"sl": None, "active_len": 3, "backlog_len": 2},
        ]

        call_centre = CallCentre(config)

        for expected_outcome in expected_outcomes:
            registered_call = call_centre._register_call(
                caller_name="John Cena",
                priority=CallPriority.LOW,
            )
            registered_call.assign(call_centre)

            assert len(call_centre.active_calls) == expected_outcome["active_len"]
            assert len(call_centre.call_backlog) == expected_outcome["backlog_len"]
            if expected_outcome["sl"] is None:
                assert registered_call.assigned_to is None
            else:
                assert registered_call.assigned_to.seniority == expected_outcome["sl"]

    def test_call_assignment_high_priority_many(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=1,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        expected_outcomes = [
            {"sl": EmployeeSeniorotyLevel.MANAGER, "active_len": 1, "backlog_len": 0},
            {"sl": EmployeeSeniorotyLevel.DIRECTOR, "active_len": 2, "backlog_len": 0},
            {"sl": None, "active_len": 2, "backlog_len": 1},
            {"sl": None, "active_len": 2, "backlog_len": 2},
        ]

        call_centre = CallCentre(config)

        for expected_outcome in expected_outcomes:
            registered_call = call_centre._register_call(
                caller_name="John Cena",
                priority=CallPriority.HIGH,
            )
            registered_call.assign(call_centre)

            assert len(call_centre.active_calls) == expected_outcome["active_len"]
            assert len(call_centre.call_backlog) == expected_outcome["backlog_len"]
            if expected_outcome["sl"] is None:
                assert registered_call.assigned_to is None
            else:
                assert registered_call.assigned_to.seniority == expected_outcome["sl"]

    def test_end_call_do_not_escalate(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=0,
            managers=0,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        call_centre = CallCentre(config)

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.LOW,
        )
        with pytest.raises(RuntimeError):
            # Cannot end an unassigned call
            registered_call.end(call_centre)

        registered_call.assign(call_centre)

        call = call_centre.active_calls.pop()
        assigned_employee = call.assigned_to
        assert not assigned_employee.is_free

        call.end(call_centre, escalate=False)

        assert call.assigned_to is None
        assert assigned_employee.is_free
        # active calls managed separately
        assert len(call_centre.active_calls) == 0
        assert len(call_centre.call_backlog) == 0

    def test_end_call_do_escalate(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        call_centre = CallCentre(config)

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.LOW,
        )
        with pytest.raises(RuntimeError):
            # Cannot end an unassigned call
            registered_call.end(call_centre)

        registered_call.assign(call_centre)

        call = call_centre.active_calls.pop()
        initial_assignment = call.assigned_to
        assert not initial_assignment.is_free

        call.end(call_centre, escalate=True)

        assert initial_assignment.is_free
        # active calls managed separately
        assert len(call_centre.active_calls) == 1
        # result of escalation
        assert call.priority == CallPriority.HIGH
        assert call.assigned_to.seniority == EmployeeSeniorotyLevel.MANAGER
        assert call.assigned_to.uid != initial_assignment.uid
        assert len(call_centre.call_backlog) == 0

    def test_random_escalation(self):
        config = CallCentreConfig(
            juniors=1,
            seniors=1,
            managers=1,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.23,
        )
        call_centre = CallCentre(config)

        registered_call = call_centre._register_call(
            caller_name="John Cena",
            priority=CallPriority.LOW,
        )

        esc_count = 0
        for _ in range(10000):
            if registered_call._should_escalate():
                esc_count += 1

        assert esc_count / 10000 == pytest.approx(config.call_escalation_prob, abs=0.1)
