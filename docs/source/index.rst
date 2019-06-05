.. pyIETS - a tool for calculating inelastic tunneling spectra documentation master file, created by
   sphinx-quickstart on Mon Feb 11 14:11:01 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyIETS - a tool for calculating inelastic tunneling spectra
===========================================================
This program calculates inelastic tunneling (IET) spectra of molecular junctions.
The implementation is equivalent to the on of SNF_ :cite:`neugebauer2002quantum`  :cite:`weymuth2012movipac` and allows for more flexible usage and extension. 
Specifically IET spectra can be calculated by incoorporating two-component calculations using Turbomole_ :cite:`turbomole2010development`

Essentially peak intensities :math:`W_{\alpha}` are calculated 

.. math::
   
     W_\alpha = G_0 \mathrm{Tr}({\boldsymbol{\Gamma}^{\mathrm{L}}(E_{\mathrm{F}})\boldsymbol{G}^\alpha(E_{\mathrm{F}})
     \boldsymbol{\Gamma}^{\mathrm{R}}(E_{\mathrm{F}})\boldsymbol{G}^\alpha(E_{\mathrm{F}})^\dagger)
     }


where :math:`G_0` and :math:`\boldsymbol{\Gamma}^{\mathrm{L}}(E_{\mathrm{F}})` denote the conductance quantum and the self-energy at the fermi-level respectively.
The greensmatrix :math:`\boldsymbol{G}^\alpha(E_{\mathrm{F}})` can be expressed by the derivative of electronic the electronic greensmatrix with respect to vibrational normal modes.

.. math::

     G_{ij}^\alpha = \frac{\sqrt{2}}{2}\frac{\delta G_{ij}(E_{\mathrm{F}}, \{Q_\alpha\})}{\delta Q_\alpha}|_{Q_\alpha = 0}


An theoretical introduction can be found here :cite:`troisi2008inelastic`. 

Prior knowledge of vibrational normal modes is required to calculate the derivative.
For that purpose interfaces to Gaussian_ :cite:`g16`, SNF_ :cite:`neugebauer2002quantum` :cite:`weymuth2012movipac` and Turbomole_ :cite:`turbomole2010development` are provided.
For each mode two static singlepoint calculations are performed - one for each distorted molecule - using Turbomole_ :cite:`turbomole2010development` or Gaussian_ :cite:`g16`. Greensmatrices and transmission functions are calculated using the code ARTAIOS_ :cite:`deffner2009artaios`.

Please cite this work as
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
