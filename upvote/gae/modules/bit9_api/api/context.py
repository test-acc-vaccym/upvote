# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines an interface for executing Bit9 REST API requests."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import httplib
import json
import urlparse

import requests
import six

from absl import logging

from upvote.gae.modules.bit9_api.api import constants
from upvote.gae.modules.bit9_api.api import exceptions as excs
from upvote.gae.modules.bit9_api.api import utils


class BaseContext(six.with_metaclass(abc.ABCMeta)):
  """Defines the configuration for communication with the API."""

  @abc.abstractmethod
  def ExecuteRequest(self, method, api_route=None, query_args=None, data=None):
    """Executes an API request and returns the JSON response."""

  @classmethod
  def _UnwrapResponse(cls, response):
    """Checks the status code and parses the contents of a response.

    Args:
      response: HttpResponse from Bit9.

    Returns:
      JSON encoded text from the response.

    Raises:
      NotFoundError: If the response returned a 404 (object not found).
      RequestError: The response had a failure status code.
    """
    if response.status_code == httplib.NOT_FOUND:
      raise excs.NotFoundError('Object in request cannot be found')
    # All 300s and 100s should be resolved by the requests library.
    elif response.status_code >= 400:
      raise excs.RequestError(
          '{} Error: {}'.format(response.status_code, response.text))
    elif response.text:
      try:
        return json.loads(response.text, object_hook=utils.unicode_to_ascii)
      except:
        raise excs.RequestError(
            'Error getting JSON from response: {}'.format(response.text))
    else:
      raise excs.RequestError('No content')


class Context(BaseContext):
  """Defines the configuration for communication with the API."""

  def __init__(self,
               server_address,
               api_token,
               request_timeout,
               version=constants.VERSION.V1):
    if not server_address.startswith('http'):
      server_address = 'https://' + server_address
    addr = urlparse.urlsplit(server_address)
    self.server_loc = addr.netloc
    self.server_path = addr.path.rstrip('/')

    self.api_token = api_token

    if not isinstance(request_timeout, int) or request_timeout <= 0:
      raise ValueError('Invalid timeout: {}'.format(request_timeout))
    self.timeout = request_timeout

    if version not in constants.VERSION.SET_ALL:
      raise ValueError('Invalid version: {}'.format(version))
    self.version = version

  def _GetApiUrl(self, api_route=None, query_args=None):
    if query_args is None: query_args = []

    api_path = '{}/api/bit9platform/{}'.format(self.server_path, self.version)
    path = '{}/{}'.format(api_path, api_route) if api_route else api_path
    return urlparse.urlunsplit(
        ['https', self.server_loc, path, '&'.join(query_args), ''])

  def _GetApiHeaders(self):
    return {
        'X-Auth-Token': self.api_token,
        'Content-Type': 'application/json'}

  def ExecuteRequest(self, method, api_route=None, query_args=None, data=None):
    """Execute an API request using the current API context."""
    if method not in constants.METHOD.SET_ALL:
      raise ValueError('Invalid method: {}'.format(method))

    url = self._GetApiUrl(api_route, query_args)

    if data is None:
      logging.info('API %s: %s', method, url)
    else:
      logging.info('API %s: %s (data: %s)', method, url, data)

    try:
      response = requests.request(
          method, url, headers=self._GetApiHeaders(), json=data, verify=True,
          timeout=self.timeout)
    except requests.RequestException as e:
      raise excs.RequestError(
          'Error performing {} {}: {}'.format(method, url, e))
    else:
      return self._UnwrapResponse(response)
