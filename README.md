# Fire Station Problem

## The Problem:
Imagine you have a fire station with four levels of employees: a junior, senior,
manager and a director. All callers and employees Ids and names are registered and
tracked.

## Specs:
- An incoming telephone call will be throttled to the system with a priority level (Low
and High.)
- For low-priority calls: any call must be first allocated to a junior who is free. If not,
then the call must be escalated to a senior. If a senior is not free or not able to
handle it, then the call should be escalated to one of the managers.
- For high-priority calls: these can only be answered by managers and directors.
Any call must be first allocated to a manager who is free. If not, then the call
should be escalated to one of the free directors.
- Sometimes, and via a random value for now, low-level calls can be changed to
high-level calls after being allocated and should then be pushed again to the
system to be picked up as a high-priority call.
- All employees start with ‘free’ status. They change their status upon allocation and
de-allocation of calls.
- the employee status changes to ‘free’ whenever:
    - a call is finished,
    - OR a call is escalated from the employee to another employee

## The System:
- Design the classes and data structures for this problem. Implement a call to
DispatchCall() which assigns a call to the first available employee.
- No need to develop an actual server or any use of threading. The system should
work as a simulation given a particular input and some random variables.
- You only need a script to generate and simulate the calls via intervals (random
timer). The system should be able then to consume these calls and allocate the
corresponding employees. In case of all employees are busy, the system should
put any call on hold till someone is available again.

## Running
- Virtual Environment:
    - Built with Python 3.10. To replicate the venv run:
    - `python3 -m venv venv`
    - `cd venv/source/bin`
    - `source activate`
    - `cd ../..`
    - `pip install -r requirements.txt`
- See [Useful Commands](#useful-commands) to run tests
- Simulation:
    - `python run_simulation.py`

## Useful Commands

- Testing:
    - `pytest --cov`
    - `pytest --cov --cov-report=html`
    - `coverage html`
    - `mypy --no-namespace-packages --config-file mypy.ini src`

- Linting:
    - `black -l 88 src`

- Requirements:
    - `pip-compile requirements.in -o requirements.txt`
    - `pip install -r requirements.txt`

## Implementation Limitations

- Inefficient Call Assignemt O(n)
    - Currently doesnt account for assigned/not assigned, goes through all employees regardless to find a fit
    - Solutions: (i) database filtering; (ii) 2 lists (free,available) - O(1)
- Inefficient active calls review - iterative poping O(n)
    - However, this functionality is just for mimicking, in reality should be managed when end of call is initiated by an agent
- Missing:
    - Docker
    - CI/CD