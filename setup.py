from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

# imports from __version__
with open(path.join(this_directory, 'pyGLV', '_version.py'), encoding='utf-8') as f:
    exec(f.read())

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyGLV',
    version=__version__, 
    license='Apache 2', 
    description = "pyGLV (computer Graphics for deep Learning and scientific Visualization)",
    long_description=long_description,
    # long_description= file: README.md, LICENSE.txt
    long_description_content_type='text/markdown',
    author = "George Papagiannakis", 
    author_email = "papagian@csd.uoc.gr",
    maintainer='Manos Kamarianakis',
    maintainer_email='m.kamarianakis@gmail.com',
    url='https://github.com/papagiannakis/pyGLV',
    keywords = ['ECS','Scenegraph','Python design patterns','Computer Graphics'],
    package_dir={'pyGLV':'pyGLV'},
    packages=find_packages(exclude=["tests","tests.*", "tests/*" ]),
    install_requires=[
        'pip',
        'setuptools>=61',
        'wheel',
        'numpy',
        'scipy',
        'pyECSS',
        'imgui',
        'PyOpenGL',
        'PyOpenGL_accelerate',
        'pysdl2',
        'pysdl2-dll',
        'ipykernel',
    ],
    

    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        "Homepage" : "https://github.com/papagiannakis/pyGLV",
        "Documentation" : "https://pyglv.readthedocs.io",
    },

    python_requires=">=3.8,<3.10",
)