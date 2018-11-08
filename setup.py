from setuptools import setup

setup(

    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP'
    ],
    
    name = 'grabicon',
    version = '0.1.2',
    description = 'grab all favicons attached to a webpage by url',
    url = 'http://github.com/dsfx3d/grabicon',
    author = 'dsfx3d',
    author_email = 'dsfx3d@gmail.com',
    license = 'MIT',

    packages = ['grabicon'],
    install_requires = [
        'requests',
        'beautifulsoup4',
        'fleep',
    ],
    tests_require = ['nose'],
    test_suite = 'nose.collector',

    include_package_data = True,
    zip_safe = False
)