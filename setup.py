# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 11:33:57 2023

@author: nfama
"""

from setuptools import setup, find_packages

setup(
    name="asana_api",
    version="0.1",
    description="Um pacote para facilitar o uso dos dados da api da Asana",
    author="Nathália Martins",
    author_email="nathalia@akaua.com.br",
    packages=find_packages(),
		install_requires=[
        'pandas',
        'asana'
    ],
)