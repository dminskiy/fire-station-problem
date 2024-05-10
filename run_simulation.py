import random
import time

from faker import Faker

from src.call import CallPriority
from src.call_centre import CallCentre, CallCentreConfig

MAX_CALL_INTERVAL_SEC = 2
PROB_OF_HIGH_PRIORITY_CALL = 0.3


def main():
    fire_station_config = CallCentreConfig(
        juniors=5,
        seniors=3,
        managers=2,
        directors=2,
        max_call_duration_sec=20,
        call_escalation_prob=0.5,
    )
    faker = Faker()
    call_centre = CallCentre(fire_station_config)

    time_count = 0
    next_call = 0
    while True:
        # Simulate continous running of the system:
        # Check for completed calls & assign released resources
        call_centre.review_active_calls()
        call_centre.review_backlog()

        print(f"\n\n>>>> Time count: {time_count}")

        if time_count == next_call:
            call_centre.dispatch_call(
                caller_name=faker.name(),
                priority=random.choices(
                    [CallPriority.HIGH, CallPriority.LOW],
                    weights=[
                        PROB_OF_HIGH_PRIORITY_CALL,
                        1 - PROB_OF_HIGH_PRIORITY_CALL,
                    ],
                    k=1,
                )[0],
                verbose=True,
            )
            next_call = time_count + random.randint(1, MAX_CALL_INTERVAL_SEC)

        call_centre.display_status()

        time_count += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
