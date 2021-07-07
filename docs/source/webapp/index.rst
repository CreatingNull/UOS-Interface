.. Documenting the use of the web app package

Webapp
======

The webapp package simultaneously serves a dashboard and an :ref:`API <API Automation Layer>` for control of UOS hardware.

API Automation Layer
--------------------

The UOS Interface supports automated control of UOS devices through a RESTful web API.
This API interface exists on the url :code:`served-address/api`.

The interface is designed to be replicate the functionality of the :doc:`../hardware/index`.

webapp package
--------------

Subpackages
-----------

.. toctree::
   :maxdepth: 3

   api
   auth
   dashboard
   database

Submodules
----------

forms module
------------

.. automodule:: uosinterface.webapp.forms
   :members:
   :undoc-members:

Module contents
---------------

.. automodule:: uosinterface.webapp
   :members:
   :undoc-members:
