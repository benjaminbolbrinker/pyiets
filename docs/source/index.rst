.. pyIETS - a tool for calculating inelastic tunneling spectra documentation master file, created by
   sphinx-quickstart on Mon Feb 11 14:11:01 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyIETS - a tool for calculating inelastic tunneling spectra
===========================================================
This program calculates inelastic tunneling spectra of molecular junctions using the ansatz from Troisi :cite:`troisi2008inelastic`. It reads vibrational modes from the a previous calculation of Gaussian_ :cite:`g16`  SNF_ :cite:`neugebauer2002quantum` which is part of the MoViPac_ package :cite:`weymuth2012movipac`. For each mode two static singlepoint calculations are performed - one for each distorted molecule - using Turbomole_ :cite:`turbomole2010development`. Greensmatrices and transmission functions are calculated using the code ARTAIOS_ :cite:`deffner2009artaios`.

Cite this work as
------
    B. Bolbrinker, M. Deffner, M. Zoellner, and C. Herrmann.
    pyIETS — a code for calculating inelastic tunneling spectra, available from
    https://github.com/


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   intro
   documentation


References
-----
.. bibliography:: bibfile.bib
   :style: unsrt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Turbomole: http://www.turbomole.com/
.. _ARTAIOS: https://www.chemie.uni-hamburg.de/institute/ac/arbeitsgruppen/herrmann/software/artaios.html 
.. _MoViPac: http://www.reiher.ethz.ch/software/movipac.html
.. _SNF: http://www.reiher.ethz.ch/software/snf.html 
.. _Gaussian: http://gaussian.com/scf/
