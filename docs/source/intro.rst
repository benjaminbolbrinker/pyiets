Getting started
===============

Make sure Turbomole_ :cite:`turbomole2010development` or Gaussian_ :cite:`g16`, ARTAIOS_ :cite:`deffner2009artaios` and pyIETS are properly :ref:`installed <installation-label>`.

For this program to function three inputfiles have to be provided:

- :code:`input.json`: the main control file of the program containg containing (see :ref:`here <inputjson-label>`)

  - general settings 
  - options for single point calculation

- :code:`artaios.in`: control file for spin-dependent electron transport calculations for molecular junctions

- output file from previous calculation of vibrational normal modes. Supported formats are SNF-output and Gaussian-output.
  

When all three input files are provided type 

.. code-block:: bash

   pyiets .

After successfully finished call

.. code-block:: bash
   
   pyiets-plot iets.dat iets.png

to visualize the results. Clean up the temporary folders with

.. code-block:: bash

   pyiets-clean .


.. _Turbomole: http://www.turbomole.com/
.. _ARTAIOS: https://www.chemie.uni-hamburg.de/institute/ac/arbeitsgruppen/herrmann/software/artaios.html 
.. _Gaussian: http://gaussian.com/scf/
