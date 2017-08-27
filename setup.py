from distutils.core import setup

setup(
    name='vvrenderer',
    version='0.0.1',
    packages=['vvrenderer'],
    url='https://github.com/verum-visu-toolkit/renderer',
    license='MIT',
    author='Jacob Zimmerman (jczimm)',
    author_email='jczimm@jczimm.com',
    description='',
    install_requires=[
        'gizeh==0.1.10',
        'moviepy==0.2.3.2'
    ],
    entry_points={
        'console_scripts': ['vv-renderer = vvrenderer.__main__:main']
    }
)
