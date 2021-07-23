schedule = {
    "periodicity": "Daily",
    "every": 2,
    "hour": 11,
    "minute": 15,
    "period": "PM",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": "*"
}

cron_exp = {
    "second": "*",
    "minute": "*",
    "hour": "*",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": "*",
    "year": "*"
}


def generate_cron(schedule):
    cron_exp["minute"] = schedule.get("minute")
    if schedule.get("period") == "AM":
        cron_exp["hour"] = 0 if schedule.get("hour") == 12 else schedule.get("hour")
    else:
        cron_exp["hour"] = schedule.get("hour") + 12
    cron_exp["day_of_month"] = schedule.get("day_of_month")
    cron_exp["month"] = schedule.get("month")
    if schedule["periodicity"] == "Weekly":
        cron_exp["day_of_month"] = "?"
        if schedule["every"] > 1:
            cron_exp["day_of_week"] = ",".join(schedule.get("day_of_week"))
            cron_exp["day_of_week"] += "{}{}".format("/", schedule["every"])

    if schedule["periodicity"] == "Daily":
        cron_exp["day_of_month"] = "?"
        if schedule["every"] > 1:
            cron_exp["day_of_week"] = "{}{}{}".format("1", "/", schedule["every"])
    return " ".join([str(val) for val in cron_exp.values()])


print(generate_cron(schedule))
