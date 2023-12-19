# encoding: utf-8

# This file is part of py-serializable
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
# Copyright (c) Paul Horton. All Rights Reserved.


from logging import NullHandler, getLogger
from sys import version_info

# Use the package's dist-name here.
# Name is prefixed, as the name SHALL not be public API!
_LOGGER = getLogger('__py-serializable')

# This handler does nothing. It's intended to be used to avoid the
# "No handlers could be found for logger XXX" one-off warning. This is
# important for library code, which may contain code to log events.
_LOGGER.addHandler(NullHandler())

# `logger.warning()` got additional kwarg since py38
_warning_kwargs = {'stacklevel': 2} if version_info >= (3, 8) else {}
