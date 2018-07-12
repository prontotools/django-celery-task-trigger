from setuptools import setup

setup(name='django-celery-task-trigger',
      description='Dynamic Task trigger for django-celery-task-broker ',
      version='0.4.0',
      url='https://github.com/lifez/django-celery-task-trigger',
      author='Prontotools',
      author_email='prontotools@prontomarketing.com',
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Topic :: Software Development :: Object Brokering',
          'Topic :: System :: Distributed Computing',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      packages=['django_celery_task_trigger'],
      install_requires=['requests>=2.19.1']
)
