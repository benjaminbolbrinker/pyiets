Getting started
===============

Make sure Turbomole :cite:`turbomole2010development`, ARTAIOS :cite:`deffner2009artaios` and pyIETS are properly (see :ref:`installation-label`).

For this program to function three inputfiles have to be provided:

- :code:`input.json`: the main control file of the program containg containing (see :ref:`here <inputjson-label>`)

  - general settings 
  - options for single point calculation

- :code:`artaios.in`: control file for spin-dependent electron transport calculations for molecular junctions
- :code:`snf.out`: output file from previous calculation of vibrational normal modes


.. code-block:: bash

   pyiets.py .


