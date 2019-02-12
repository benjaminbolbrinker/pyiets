.. _documentation-label:

Documentation
=============

In the following sections explain all relevant input files and corresponding parameters.

.. _inputfiles-label:

Inputfiles
----------

.. _inputjson-label: 

:code:`input.json`
^^^^^^^^^^^^^^^^^^
- :code:`sp_control` dictionary containing options for single point calculation:
   - :code:`qc_prog` string defining the quantum chemistry program (default: :code:`"turbomole"`).
   - :code:`params` dictionary containing parameters for single point calculation (default: :code:`null`).

- :code:`sp_restart` if set to :code:`true` looks for :code`mode_folder` and :code:`output_folder` to restart old calculation. This can save a lot of time and resources (default: :code:`false`).

- :code:`artaios`: 

  (e.g. :code:`define_str` for Turbomole :cite:`turbomole2010development`)

- general settings 

(e.g. number of cores :code:`mp`)



.. _artaiosin-label: 

:code:`artaios.in`
^^^^^^^^^^^^^^^^^^





.. _snfout-label: 

:code:`snf.out`
^^^^^^^^^^^^^^^

