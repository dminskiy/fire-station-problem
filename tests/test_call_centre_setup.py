import pytest

from call_centre import CallCentre, CallCentreConfig
from employee import EmployeeSeniorotyLevel


class TestCallCentreSetup:
    def test_call_centre_config_escalation_prob(self):
        # call_escalation_prob not in range
        with pytest.raises(ValueError):
            CallCentreConfig(
                juniors=5,
                seniors=0,
                managers=0,
                directors=0,
                max_call_duration_sec=10,
                call_escalation_prob=2,
            )

    def test_call_centre_config_num_employees(self):
        # juniors not in range
        with pytest.raises(ValueError):
            CallCentreConfig(
                juniors=0,
                seniors=0,
                managers=-1,
                directors=0,
                max_call_duration_sec=10,
                call_escalation_prob=0.2,
            )

    def test_juniors_setup(self):
        config = CallCentreConfig(
            juniors=5,
            seniors=0,
            managers=0,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        assert len(call_centre.employees[EmployeeSeniorotyLevel.JUNIOR]) == 5

    def test_seniors_setup(self):
        config = CallCentreConfig(
            juniors=0,
            seniors=5,
            managers=0,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        assert len(call_centre.employees[EmployeeSeniorotyLevel.SENIOR]) == 5

    def test_managers_setup(self):
        config = CallCentreConfig(
            juniors=5,
            seniors=0,
            managers=5,
            directors=0,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        assert len(call_centre.employees[EmployeeSeniorotyLevel.MANAGER]) == 5

    def test_directors_setup(self):
        config = CallCentreConfig(
            juniors=0,
            seniors=0,
            managers=0,
            directors=5,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )

        call_centre = CallCentre(config)

        assert len(call_centre.employees[EmployeeSeniorotyLevel.DIRECTOR]) == 5

    def test_employee_uid(self):
        config = CallCentreConfig(
            juniors=2,
            seniors=3,
            managers=4,
            directors=5,
            max_call_duration_sec=10,
            call_escalation_prob=0.1,
        )
        expected_uids = list(range(0, 14))

        call_centre = CallCentre(config)

        created_uids = []
        created_uids += [
            item.uid for item in call_centre.employees[EmployeeSeniorotyLevel.JUNIOR]
        ]
        created_uids += [
            item.uid for item in call_centre.employees[EmployeeSeniorotyLevel.SENIOR]
        ]
        created_uids += [
            item.uid for item in call_centre.employees[EmployeeSeniorotyLevel.MANAGER]
        ]
        created_uids += [
            item.uid for item in call_centre.employees[EmployeeSeniorotyLevel.DIRECTOR]
        ]

        assert set(expected_uids) == set(created_uids)
