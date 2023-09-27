Logging
====================================================

This library utilizes an own instance of `Logger`_, which you may access and add handlers to.

.. _logger: https://docs.python.org/3/library/logging.html#logger-objects


.. code-block:: python
   :caption: Example: send all logs messages to the console

   import sys
   import logging
   import serializable

   my_log_handler = logging.StreamHandler(sys.stderr)
   my_log_handler.setLevel(logging.DEBUG)
   my_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
   serializable.LOGGER.addHandler(my_log_handler)

   print(serializable.LOGGER.name)


   @serializable.serializable_class
   class Chapter:

   def __init__(self, *, number: int, title: str) -> None:
     self._number = number
     self._title = title

   @property
   def number(self) -> int:
     return self._number

   @property
   def title(self) -> str:
     return self._title


   moby_dick_c1 = Chapter(number=1, title='Loomings')
   print(moby_dick_c1.as_json())

