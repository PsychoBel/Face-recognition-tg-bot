# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Face-recognition-tg-bot",
    version = "1.0",
    author = "Mike Belous",
    author_email = "mike.belous@gmail.com",
    description = ("Final Project for X5 School"),
    python_requires='>=3.6, <4',
    url = "https://github.com/PsychoBel/Face-recognition-tg-bot",
    packages=['model', 'bot'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Education :: Telegram Bot",
    ],
)