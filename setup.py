# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: setup.py.py
@ time: $19-2-20 下午3:51
"""

from setuptools import setup, find_packages

setup(
    name='cfnlp',
    version='0.1',
    description=(
        'CQFAE nlp python lib'
    ),
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='cc',
    author_email='412214410@qq.com',
    license='MIT',
    maintainer='cc&zhangyu&tanrui',
    maintainer_email='412214410@qq.com',
    packages=find_packages(),
    platforms=['all'],
    url='https://github.com/invoker4zoo',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ]

)