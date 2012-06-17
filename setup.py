from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-gevent',
    version=__import__('django_gevent').__version__,
    description='A library to add gevent support to django.',
    long_description=read('README'),
    author='Sam Willis',
    author_email='sam.willis@gmail.com',
    url='http://github.com/samwillis/django-gevent',
    download_url='http://github.com/samwillis/django-gevent/downloads',
    license='BSD',
    packages=find_packages(exclude=['testproject']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'gevent >= 0.13',
        'django >= 1.4',
    ]
)