"""Purpose of this module is to park schedule modules for delivery schedule
Sample object
schedule = {
    "periodicity": "Weekly",
    "every": 2,
    "hour": 11,
    "minute": 15,
    "period": "PM",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": ['Weekend']
}
"""

# TODO Modify this module as Class Based in upcoming implementation.


def generate_cron(schedule: dict) -> str:
    """To generate cron expression based on the schedule object
    Args:
        schedule: dictionary object of schedule

    Returns:
        str: cron expression
    """
    cron_exp = {
        "minute": "*",
        "hour": "*",
        "day_of_month": "*",
        "month": "*",
        "day_of_week": "?",
        "year": "*",
    }

    cron_exp["minute"] = schedule.get("minute", "*")
    if schedule.get("period") == "AM":
        cron_exp["hour"] = (
            0 if schedule.get("hour") == 12 else schedule.get("hour", "*")
        )
    else:
        if schedule.get("hour"):
            cron_exp["hour"] = schedule.get("hour") + 12

    cron_exp["month"] = schedule.get("month", "*")

    if schedule["periodicity"] == "Weekly":
        cron_exp["day_of_month"] = "?"

        cron_exp["day_of_week"] = ",".join(schedule.get("day_of_week"))
        if schedule["every"] > 1:
            cron_exp[
                "day_of_week"
            ] = f"{cron_exp['day_of_week']}#{schedule['every']}"

    if schedule["periodicity"] == "Daily":
        cron_exp["day_of_month"] = "*"
        if schedule["every"] > 1:
            cron_exp[
                "day_of_month"
            ] = f"{cron_exp['day_of_month']}/{schedule['every']}"

    if schedule["periodicity"] == "Monthly":
        cron_exp["day_of_month"] = ",".join(schedule.get("day_of_month"))
        if schedule["every"] > 1:
            cron_exp["month"] = f"{cron_exp['month']}/{schedule['every']}"
    return " ".join([str(val) for val in cron_exp.values()])
