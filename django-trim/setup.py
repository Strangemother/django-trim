from setuptools import setup

setup(name='django-trim',
      version='0.1a',
      description='Django Trim',
      url='http://github.com/strangemother/django-trim',
      author='Just Jay',
      author_email='django-trim@strangemother.com',
      license='MIT',
      # py_modules=['trim'],
      package_dir={'':'src'},     # Directory of the source code of the package
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
