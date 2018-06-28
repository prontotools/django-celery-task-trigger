from setuptools import setup

setup(name='django-celery-task-trigger',
      description='Dynamic Task trigger for django-celery-task-broker ',
      version='1.0.0',
      url='https://github.com/massenz/filecrypt',
      author='Prontotools',
      author_email='prontotools@prontomarketing.com',
      license='MIT',
      classifiers=[
          'FRAMEWORK :: DJANGO',
          'SYSTEM :: SOFTWARE DISTRIBUTION',
          'Software Development :: Object Brokering',
          'LICENSE :: OSI APPROVED :: MIT LICENSE',
          'Programming Language :: Python :: 3'
      ],
      packages=['django-celery-task-trigger'],
      install_requires=['requests>=2.19.1']
)
