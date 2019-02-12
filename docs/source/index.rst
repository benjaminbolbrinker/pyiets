.. pyIETS - a tool for calculating inelastic tunneling spectra documentation master file, created by
   sphinx-quickstart on Mon Feb 11 14:11:01 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyIETS - a tool for calculating inelastic tunneling spectra
===========================================================
This program calculates inelastic tunneling spectra of molecules between molecular junctions using the ansatz from Troisi :cite:`troisi2008inelastic`. It reads vibrational modes from the output of the program SNF :cite:`neugebauer2002quantum` which is part of the MoViPac package :cite:`weymuth2012movipac`. For each mode two static singlepoint calculations are performed - one for each distorted molecule - using Turbomole :cite:`turbomole2010development`. Greensmatrices are calculated using the code ARTAIOS :cite:`deffner2009artaios` for each distorted molecule.

Cite this work as
------
    [1] B. Bolbrinker, M. Deffner, M. Zoellner, and C. Herrmann.
    pyIETS — a code for calculating inelastic tunneling spectra, available from
    https://github.com/


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   installation



References
-----
.. bibliography:: bibfile.bib



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
