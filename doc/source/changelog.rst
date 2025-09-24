.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.14.1 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.14.1>`_ - September 24, 2025
==============================================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump twine from 6.1.0 to 6.2.0
          - `#323 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/323>`_

        * - Update pytest-cov requirement from <6.3,>=4.0.0 to >=4.0.0,<7.1
          - `#327 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/327>`_

        * - Bump ansys/actions from 10.0.20 to 10.1.1
          - `#329 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/329>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#324 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/324>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Deprecated pyaedt argument
          - `#330 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/330>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.14.0
          - `#321 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/321>`_

        * - Bump 0.15.dev0
          - `#322 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/322>`_

        * - Update README.rst
          - `#325 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/325>`_


`0.14.0 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.14.0>`_ - September 10, 2025
==============================================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update flit-core requirement from <3.11,>=3.2 to >=3.2,<4
          - `#229 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/229>`_

        * - Bump codecov/codecov-action from 5.4.3 to 5.5.0
          - `#311 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/311>`_

        * - Bump actions/setup-python from 5.6.0 to 6.0.0
          - `#314 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/314>`_

        * - Bump ansys/actions from 10.0.14 to 10.0.20
          - `#316 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/316>`_

        * - Bump pypa/gh-action-pypi-publish from 1.12.4 to 1.13.0
          - `#317 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/317>`_

        * - Bump actions/labeler from 5.0.0 to 6.0.1
          - `#318 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/318>`_

        * - Bump codecov/codecov-action from 5.5.0 to 5.5.1
          - `#319 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/319>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update documentation sphinx dependency
          - `#299 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/299>`_

        * - Fix pyside version in tests and doc
          - `#307 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/307>`_

        * - Pydantic deprecation and CI warning spotted in CI logs
          - `#309 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/309>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.13.3
          - `#306 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/306>`_

        * - Strengthen workflow's job dependencies
          - `#313 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/313>`_

        * - Update SECURITY.md
          - `#320 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/320>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fix flaky test using geometry thread
          - `#308 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/308>`_

        * - Improve menu testing
          - `#312 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/312>`_


`0.13.3 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.13.3>`_ - August 21, 2025
===========================================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump actions/checkout from 4.2.2 to 5.0.0
          - `#304 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/304>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.13.2
          - `#303 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/303>`_

        * - Revert pyside6 6.9.0
          - `#305 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/305>`_


`0.13.2 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.13.2>`_ - August 14, 2025
===========================================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump ansys/actions from 10.0.12 to 10.0.14
          - `#300 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/300>`_

        * - Bump actions/download-artifact from 4.3.0 to 5.0.0
          - `#301 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/301>`_

        * - Bump build from 1.2.2.post1 to 1.3.0
          - `#302 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/302>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update changelog for v0.13.1
          - `#294 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/294>`_

        * - Pin vtk-osmesa version
          - `#296 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/296>`_

        * - Use aedt 2025r2
          - `#297 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/297>`_


`0.13.1 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.13.1>`_ - July 19, 2025
=========================================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update pytest-qt requirement from <4.5,>=4.0.0 to >=4.0.0,<4.6
          - `#291 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/291>`_

        * - Bump ansys/actions from 10.0.11 to 10.0.12
          - `#292 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/292>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``contributors.md`` with the latest contributors
          - `#293 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/293>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update changelog for v0.13.0
          - `#288 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/288>`_

        * - Update v0.14.dev0
          - `#289 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/289>`_

        * - Add safety check to all dependencies
          - `#290 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/290>`_


`0.13.0 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.13.0>`_ - July 07, 2025
=========================================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add last example tests
          - `#281 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/281>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update pytest requirement from <8.4,>=7.4.0 to >=7.4.0,<8.5
          - `#274 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/274>`_

        * - Bump pyside6 from 6.9.0 to 6.9.1
          - `#275 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/275>`_

        * - Update pytest-cov requirement from <6.2,>=4.0.0 to >=4.0.0,<6.3
          - `#277 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/277>`_

        * - Update numpydoc requirement from <1.9,>=1.5.0 to >=1.5.0,<1.10
          - `#287 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/287>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Added deepwiki badge
          - `#286 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/286>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update changelog for v0.12.6
          - `#273 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/273>`_

        * - Cleanup and updates
          - `#280 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/280>`_

        * - Add vulnerability check and refactor the code accordingly
          - `#285 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/285>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Improve example and test ui
          - `#276 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/276>`_


`0.12.6 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.6>`_ - June 13, 2025
=========================================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump ansys/actions from 9 to 10
          - `#272 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/272>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.12.5
          - `#271 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/271>`_


`0.12.5 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.5>`_ - June 06, 2025
=========================================================================================================

.. tab-set::


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - add doc section for distribution
          - `#269 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/269>`_

        * - Update distributing.rst
          - `#270 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/270>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.12.4
          - `#268 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/268>`_


`0.12.4 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.4>`_ - June 02, 2025
=========================================================================================================

.. tab-set::


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#266 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/266>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Widget misaligment
          - `#267 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/267>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.12.3
          - `#265 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/265>`_


`0.12.3 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.3>`_ - May 30, 2025
========================================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Auto resolution
          - `#264 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/264>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.12.2
          - `#262 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/262>`_

        * - Add changelog upper case
          - `#263 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/263>`_


`0.12.2 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.2>`_ - May 26, 2025
========================================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add specific application if passed
          - `#260 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/260>`_

        * - Add ON/OFF in toggle
          - `#261 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/261>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.12.1
          - `#257 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/257>`_


`0.12.1 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.1>`_ - May 20, 2025
========================================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add set_visible_button for left menu
          - `#256 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/256>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.12.0
          - `#252 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/252>`_

        * - Update v0.13.dev0
          - `#253 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/253>`_


`0.12.0 <https://github.com/ansys-internal/pyaedt-toolkits-common/releases/tag/v0.12.0>`_ - May 10, 2025
========================================================================================================

.. tab-set::


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update Python 3.12
          - `#248 <https://github.com/ansys-internal/pyaedt-toolkits-common/pull/248>`_


.. vale on