from setuptools import setup

setup(name='django-trim',
      version='0.1',
      description='Django Trim',
      url='http://github.com/strangemother/django-short-shorts',
      author='Just Jay',
      author_email='django-trim@strangemother.com',
      license='MIT',
      py_modules=['trim'],
      classifiers=[
        'Programming Language :: Python :: 3',
      ],
      zip_safe=True,
      entry_points = {
            'console_scripts': [
                  'trim=trim.cli.primary:main'
            ],
      }
)
