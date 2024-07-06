.. # Licensed under the Apache License, Version 2.0 (the "License");
   # you may not use this file except in compliance with the License.
   # You may obtain a copy of the License at
   #
   #     http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.
   #
   # SPDX-License-Identifier: Apache-2.0

Examples
========

.. _unit-tests:

Models used in Unit Tests
-------------------------

.. literalinclude:: ../tests/model.py
   :language: python
   :linenos:

Logging and log access
----------------------

This library utilizes an own instance of `Logger`_, which you may access and add handlers to.

.. _Logger: https://docs.python.org/3/library/logging.html#logger-objects

.. code-block:: python
   :caption: Example: send all logs messages to stdErr

   import sys
   import logging
   import serializable

   my_log_handler = logging.StreamHandler(sys.stderr)
   my_log_handler.setLevel(logging.DEBUG)
   my_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
   serializable.logger.addHandler(my_log_handler)
   serializable.logger.setLevel(my_log_handler.level)
   serializable.logger.propagate = False

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
