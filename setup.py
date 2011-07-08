from setuptools import setup, find_packages

setup(
    name='healthmodels',
    version='0.1',
    license="BSD",

    install_requires = ["rapidsms"],

    description='A common set of models for mHealth-related applications.',
    long_description=open('README.rst').read(),
    author='David McCann',
    author_email='david.a.mccann@gmail.com',

    url='http://github.com/daveycrockett/healthmodels',
    #download_url='http://github.com/daveycrockett/healthmodels/downloads',

    include_package_data=True,

    packages=find_packages(),
    package_data={'healthmodels':['templates/*/*.html','templates/*/*/*.html','static/*/*']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
