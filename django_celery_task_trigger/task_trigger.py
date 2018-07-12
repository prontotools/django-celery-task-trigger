from typing import Optional

import requests


class TaskTrigger:

    def __init__(
        self,
        base_task_url: str,
        minute: Optional = None,
        hour: Optional = None,
        day_of_week: Optional = None,
        day_of_month: Optional = None,
        month_of_year: Optional = None
    ):
        self.base_task_url = base_task_url
        self.cron_minute = minute
        self.cron_hour = hour
        self.cron_day_of_week = day_of_week
        self.cron_day_of_month = day_of_month
        self.cron_month_of_year = month_of_year
        self.cron_id = ''
        if any([minute, hour, day_of_week, day_of_month, month_of_year]):
            self.get_cron_info()

    def get_cron_info(self) -> bool:
        cron_data = {
            'minute': self.cron_minute,
            'hour': self.cron_hour,
            'day_of_week': self.cron_day_of_week,
            'day_of_month': self.cron_day_of_month,
            'month_of_year': self.cron_month_of_year
        }
        cron_response = requests.post(
            url=f'{self.base_task_url}crontab-schedule/',
            json=cron_data
        )
        if cron_response.status_code != requests.codes.ok:
            return False
        self.cron_id = cron_response.json()['id']
        return True

    def trigger_periodic_task(self, module_name: str, task_name: str, display_name: str, **kwargs):
        periodic_trigger_data = {
            'display_name': display_name,
            'module_name': module_name,
            'task_name': task_name,
            'cron_id': self.cron_id,
            'kwargs': kwargs
        }
        response = requests.post(
            url=f'{self.base_task_url}periodic-task/',
            json=periodic_trigger_data
        )
        return response.status_code

    def toggle_periodic_task(self, module_name: str, task_name: str, enabled: bool, **kwargs):
        periodic_trigger_data = {
            'module_name': module_name,
            'task_name': task_name,
            'enabled': enabled,
            'kwargs': kwargs
        }
        response = requests.patch(
            url=f'{self.base_task_url}periodic-task/',
            json=periodic_trigger_data
        )
        return response.status_code

    def trigger_task(self, module_name: str, task_name: str, **kwargs):
        trigger_data = {
            'module_name': module_name,
            'task_name': task_name,
            'kwargs': kwargs
        }

        response = requests.post(
            url=f'{self.base_task_url}trigger-task/',
            json=trigger_data
        )

        return response.status_code
