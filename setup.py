import setuptools
import pkg_resources
import gqylpy_ssh as g

gdoc: list = g.__doc__.split('\n')

for index, line in enumerate(gdoc):
    if line.startswith('@version: ', 4):
        version = line.split()[-1]
        break
_, author, email = gdoc[index + 1].split()
source = gdoc[index + 2].split()[-1]

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
    install_requires=[str(x) for x in pkg_resources.parse_requirements(
        open('requirements.txt', encoding='utf8')
    )],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public '
                                    'License (LGPL)',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals :: Telnet',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
