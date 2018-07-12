from unittest import TestCase
from unittest.mock import Mock, patch

import requests

from django_celery_task_trigger.task_trigger import TaskTrigger


class TaskTriggerTest(TestCase):

    def setUp(self):
        self.base_task_url = 'http://task-broker/'
        self.minute = '0'
        self.hour = '3'
        self.day_of_week = '*'
        self.day_of_month = '*'
        self.month_of_year = '*'

    def test_initialize_object_should_set_attribute(self):
        with patch('requests.post'):
            task_trigger = TaskTrigger(
                base_task_url=self.base_task_url,
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year
            )

        self.assertEqual(task_trigger.base_task_url, self.base_task_url)
        self.assertEqual(task_trigger.cron_minute, self.minute)
        self.assertEqual(task_trigger.cron_hour, self.hour)
        self.assertEqual(task_trigger.cron_day_of_week, self.day_of_week)
        self.assertEqual(task_trigger.cron_day_of_month, self.day_of_month)
        self.assertEqual(task_trigger.cron_month_of_year, self.month_of_year)

    def test_initialize_object_should_set_cron_id(self):
        mock_body = {'id': 1}
        mock_response = Mock(status_code=requests.codes.ok, json=Mock(return_value=mock_body))
        with patch('requests.post', return_value=mock_response):

            task_trigger = TaskTrigger(
                base_task_url=self.base_task_url,
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year
            )

        self.assertEqual(task_trigger.cron_id, 1)

    def test_initialize_object_without_cron_should_not_set_cron_id(self):

        task_trigger = TaskTrigger(base_task_url=self.base_task_url,)

        self.assertEqual(task_trigger.cron_id, '')

    def test_initialize_object_should_get_cron_from_correct_url(self):
        with patch('requests.post') as mock_request:

            TaskTrigger(
                base_task_url=self.base_task_url,
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year
            )

        expected_data = {
            'minute': self.minute,
            'hour': self.hour,
            'day_of_week': self.day_of_week,
            'day_of_month': self.day_of_month,
            'month_of_year': self.month_of_year
        }

        mock_request.assert_called_once_with(
            url=f'{self.base_task_url}crontab-schedule/',
            json=expected_data
        )

    def test_trigger_periodic_task_should_request_with_correct_data(self):
        survey_url = 'http://gateway:8000/survey/1234/'
        company_account = 'http://gateway:8000/company/1000/'
        mock_body = {'id': 1}
        mock_response = Mock(status_code=requests.codes.ok, json=Mock(return_value=mock_body))
        with patch('requests.post', return_value=mock_response) as mock_request:
            task_trigger = TaskTrigger(
                base_task_url=self.base_task_url,
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year
            )
            task_trigger.trigger_periodic_task(
                module_name='tests.tasks',
                task_name='test_task',
                display_name='Test Task',
                survey_url=survey_url,
                company_account=company_account
            )

        expected_periodic_trigger_data = {
            'display_name': f'Test Task',
            'module_name': 'tests.tasks',
            'task_name': 'test_task',
            'cron_id': 1,
            'kwargs': {
                'survey_url': survey_url,
                'company_account': company_account
            }
        }

        mock_request.assert_called_with(
            url=f'{self.base_task_url}periodic-task/',
            json=expected_periodic_trigger_data
        )

    def test_trigger_task_should_request_with_correct_data(self):
        survey_url = 'http://gateway:8000/survey/1234/'
        company_account = 'http://gateway:8000/company/1000/'
        with patch('requests.post') as mock_request:
            task_trigger = TaskTrigger(base_task_url=self.base_task_url)
            task_trigger.trigger_task(
                module_name='tests.tasks',
                task_name='test_task',
                survey_url=survey_url,
                company_account=company_account
            )

        expected_trigger_task_data = {
            'module_name': 'tests.tasks',
            'task_name': 'test_task',
            'kwargs': {
                'survey_url': survey_url,
                'company_account': company_account
            }
        }

        mock_request.assert_called_with(
            url=f'{self.base_task_url}trigger-task/',
            json=expected_trigger_task_data
        )

    def test_toggle_periodic_task_with_enabled_true_should_request_with_correct_data(self):
        survey_url = 'http://gateway:8000/survey/1234/'
        company_account = 'http://gateway:8000/company/1000/'
        with patch('requests.patch') as mock_request:
            task_trigger = TaskTrigger(base_task_url=self.base_task_url)
            task_trigger.toggle_periodic_task(
                module_name='tests.tasks',
                task_name='test_task',
                enabled=True,
                survey_url=survey_url,
                company_account=company_account
            )

        expected_periodic_trigger_data = {
            'module_name': 'tests.tasks',
            'task_name': 'test_task',
            'enabled': True,
            'kwargs': {
                'survey_url': survey_url,
                'company_account': company_account
            }
        }

        mock_request.assert_called_with(
            url=f'{self.base_task_url}periodic-task/',
            json=expected_periodic_trigger_data
        )

    def test_toggle_periodic_task_with_enabled_false_should_request_with_correct_data(self):
        survey_url = 'http://gateway:8000/survey/1234/'
        company_account = 'http://gateway:8000/company/1000/'
        with patch('requests.patch') as mock_request:
            task_trigger = TaskTrigger(base_task_url=self.base_task_url)
            task_trigger.toggle_periodic_task(
                module_name='tests.tasks',
                task_name='test_task',
                enabled=False,
                survey_url=survey_url,
                company_account=company_account
            )

        expected_periodic_trigger_data = {
            'module_name': 'tests.tasks',
            'task_name': 'test_task',
            'enabled': False,
            'kwargs': {
                'survey_url': survey_url,
                'company_account': company_account
            }
        }

        mock_request.assert_called_with(
            url=f'{self.base_task_url}periodic-task/',
            json=expected_periodic_trigger_data
        )
