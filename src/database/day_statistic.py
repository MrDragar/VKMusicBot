from datetime import date, timedelta

from .models import DayStatistic

from typing import Dict, Optional


async def get_day_statistic(day: Optional[date] = None) -> DayStatistic:
    if day is None:
        day = date.today()
    day_statistic = await DayStatistic.get_or_create(date=day)
    return day_statistic[0]


async def add_user():
    day_statistic = await get_day_statistic()
    day_statistic.new_users += 1
    await day_statistic.save()


async def add_download():
    day_statistic = await get_day_statistic()
    day_statistic.downloads += 1
    await day_statistic.save()


async def add_error():
    day_statistic = await get_day_statistic()
    day_statistic.errors += 1
    await day_statistic.save()


async def get_monthly_statistics(month: Optional[date] = None) -> Dict[str, int]:
    if month is None:
        month = date.today()

    start_date = month.replace(day=1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    query = await DayStatistic.filter(date__gte=start_date, date__lte=end_date)

    new_users = downloads = errors = 0
    for day in query:
        new_users += day.new_users
        downloads += day.downloads
        errors += day.errors

    return {
        'new_users': new_users,
        'downloads': downloads,
        'errors': errors,
    }
