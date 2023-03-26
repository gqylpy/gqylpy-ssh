import setuptools
import pkg_resources
import gqylpy_ssh as g

with open(g.__file__, encoding='UTF-8') as f:
    for line in f:
        if line.startswith('@version: ', 4):
            version = line.split()[-1]
            break
    author, email = f.readline().split(maxsplit=1)[-1].rstrip().split()
    source = f.readline().split()[-1]

with open('requirements.txt', encoding='UTF-8') as f:
    requires = [str(x) for x in pkg_resources.parse_requirements(f)]

setuptools.setup(
    name=g.__name__,
    version=version,
    author=author,
    author_email=email,
    license='LGPL',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='在远程服务器执行命令并得到执行结果，它是对 paramiko 库的二次封装。',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    packages=[g.__name__],
    python_requires='>=3.6, <4',
    install_requires=requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public '
                                    'License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
