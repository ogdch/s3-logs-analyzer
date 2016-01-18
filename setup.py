# -*- coding: utf-8 -*-

import codecs
from distutils.core import setup

version = '1.1.0'

try:
    import pypandoc
    from unidecode import unidecode
    description = codecs.open('README.md', encoding='utf-8').read()
    description = unidecode(description)
    description = pypandoc.convert(description, 'rst', format='md')
except (IOError, ImportError):
    description = 'Python wrapper for the OSM API'

setup(
    name='s3-logs-analyzer',
    packages=['s3-logs-analyzer'],
    version=version,
    description='Generate daily download stats for files hosted on S3 from the logs',
    entry_points={
        'console_scripts': [
            's3-logs = s3_logs_analyzer.cli:main'
        ]
    },
    long_description=description,
    author='Liip AG',
    author_email='contact@liip.ch',
    maintainer='Liip AG',
    maintainer_email='contact@liip.ch',
    url='https://github.com/ogdch/s3-logs-analyzer',
    download_url='https://github.com/ogdch/s3-logs-analyzer/archive/v%s.zip' % version,
    keywords=['analyzer', 'logs', 's3', 'download', 'amazon'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
