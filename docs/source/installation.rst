.. _installation-label:

Installation
============
This program requires Turbomole_ :cite:`turbomole2010development` and ARTAIOS_ :cite:`deffner2009artaios` to be properly installed on your machine.
PyIETS is tested with Turbomole_ version 7.1 and ARTAIOS_ version 2.0

For installing this package simply type:

.. code-block:: bash

   make install

To confirm the environment was installed properly type:

.. code-block:: bash

   make test_all

Note that Turbomole_ 7.1 does not support parallelism for calculations with ridft.

.. _Turbomole: http://www.turbomole.com/
.. _ARTAIOS: https://www.chemie.uni-hamburg.de/institute/ac/arbeitsgruppen/herrmann/software/artaios.html 
