def run_daily_cleanup():
    file_age_days = 2

    now = datetime.now()

    cleanup_time = datetime(now.year, now.month, now.day, 1, 0, 0)

    if now > cleanup_time:
        cleanup_time += timedelta(days=1)

    time_to_wait = (cleanup_time - now).total_seconds()

    time.sleep(time_to_wait)

    delete_old_models("./models", file_age_days)