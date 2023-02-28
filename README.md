The pyGLV package
=================
[![PyPI](https://badgen.net/pypi/v/pyglv)](https://pypi.org/project/pyglv/)
[![Documentation](https://readthedocs.org/projects/pyglv/badge/?version=latest)](http://pyglv.readthedocs.io/en/latest/?badge=latest)


## pyGLV (computer **G**raphics for deep **L**earning and scientific **V**isualization)

A python, pure software design pattern based package that used plain and simple **E**ntities, **C**omponents and **S**ystems in a **S**cenegraph architecture from thge `pyECSS` package, in order to showcase basic, cross-platform OpenGL-based real-time computer graphics with applications to scientific visualization and deep learning.

- **Documentation:** https://pyglv.readthedocs.io
- **Source code:** https://github.com/papagiannakis/pyglv
- **Bug Reports:** https://github.com/papagiannakis/pyglv/issues

---

## **Why GLV?**:

This package is aimed as a basic behind-the-black-box implementation of several classic as well as modern computer graphics  methodologies, algorithms and techniques, aimed for teaching as well as framework for novel research.

> The following software design patterns are employed:
> - Decorator Pattern: *RenderDecorator, ComponentDecorator, SystemDecorator*
> - game-loop pattern (GPP non GoF): *Scene*

---

## Installation

- For `standalone` use, via `pip`

  ```
  pip install pyglv
  ```

- For `developing`, fork this repository and run

  ```
  pip install -e . --config-settings editable_mode=strict
  ```

  in the same directory with `setup.py`.


More information can be found in [Documentation](https://pyglv.readthedocs.io) and specifically at 
[Installation](https://pyglv.readthedocs.io/en/latest/installation.html).


## Contributors

- Prof. George Papagiannakis
- Dr. Kamarianakis Manos
- Geronikolakis Stratos
- Zack Pervolarakis
- George Kokiadis
  

---
## Licensing

pyGLV is licensed under the Apache License, Version 2.0. See
[LICENSE.txt](https://github.com/papagiannakis/pyGLV/blob/develop/LICENSE.txt) for the full license text.

---

### *Copyright 2021-2023 Dr. George Papagiannakis,  papagian@csd.uoc.gr*

### *All Rights Reserved*

### *University of Crete & Foundation for Research & Technology - Hellas (FORTH)*