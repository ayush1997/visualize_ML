from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='visualize_ML',

    version='0.2.2',

    description='To visualize various processes involved in dealing with a Machine Learning problem.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ayush1997/visualize_ML',


    author='ayush1997',
    author_email='ayushkumarsingh97@gmail.com',


    license='MIT',


    classifiers=[

        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='visualization MachineLearning DataScience',

    packages=['visualize_ML'],


    install_requires=["scikit-learn","pandas","numpy","matplotlib"],



)
