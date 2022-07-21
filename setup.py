import setuptools
import gqylpy_ssh as g

setuptools.setup(
    name=g.__name__,
    version='.'.join(str(n) for n in g.__version__),
    author=g.__author__.split()[0],
    author_email=g.__author__.split()[1][1:-1],
    license='LGPL',
    url='http://gqylpy.com',
    project_urls={'Source': g.__source__},
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=[g.__name__],
    requires=['paramiko(>=2.10.4,<3.0)'],
    install_requires=['paramiko>=2.10.4,<3.0'],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)
