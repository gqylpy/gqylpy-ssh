import setuptools
import gqylpy_ssh as g

setuptools.setup(
    name=g.__name__,
    version='.'.join(str(n) for n in g.__version__),
    author='竹永康',
    author_email='gqylpy@outlook.com',
    license='LGPL',
    url=g.__home__,
    long_description=open('README.md', encoding='utf8').read(),
    packages=[g.__name__],
    requires=['paramiko(>=2.10.4)'],
    install_requires=['paramiko>=2.10.4'],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License',
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
