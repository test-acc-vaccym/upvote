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

"""Constants used in communication with Bit9."""

from upvote.shared import constants


# RFC 3339/ISO 8601 datetime format.
DATETIME_CONVERSION_STRING = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_CONVERSION_STRING_USEC = '%Y-%m-%dT%H:%M:%S.%fZ'
OLD_DATETIME_CONVERSION_STRING = '%Y-%m-%d %H:%M:%S'

# A subtype is the classification of the kind of event.
SUBTYPE = constants.Namespace(tuples=[

    # A file was blocked because it was unapproved.
    ('UNAPPROVED', 801),

    # A file was blocked because it was banned.
    ('BANNED', 802),

    # A file was blocked because of a user response to a prompt.
    ('PROMPTED_BLOCKED', 837),

    # A file was approved because of a user response to a prompt.
    ('PROMPTED_APPROVED', 838),

    # A file was blocked because of a timeout waiting for user response.
    ('PROMPTED_TIMED_OUT', 839)])

APPROVAL_STATE = constants.Namespace(
    tuples=[('UNAPPROVED', 1), ('APPROVED', 2), ('BANNED', 3)])
APPROVAL_STATE.DefineMap('TO_STR', {
    APPROVAL_STATE.UNAPPROVED: 'UNAPPROVED',
    APPROVAL_STATE.APPROVED: 'APPROVED',
    APPROVAL_STATE.BANNED: 'BANNED'})

SHA256_TYPE = constants.Namespace(tuples=[('REGULAR', 5), ('FUZZY', 6)])
SHA256_TYPE.DefineMap('TO_ID_TYPE', {
    SHA256_TYPE.REGULAR: constants.ID_TYPE.SHA256,
    SHA256_TYPE.FUZZY: constants.ID_TYPE.FUZZY_SHA256})


class FileFlags(object):
  """File flags for a Bit9 file catalog."""

  MARKED_INSTALLER = 0x00004
  DETECTED_INSTALLER = 0x00010
  MARKED_NOT_INSTALLER = 0x10000


class UpvoteHostHealthProperties(object):
  """Host health properties."""

  AGENT_CACHE_SIZE = 'agent_cache_size'
  AGENT_VERSION = 'agent_version'
  CONNECTED = 'connected'
  HAS_HEALTH_CHECK_ERRORS = 'has_health_check_errors'
  IS_INITIALIZING = 'is_initializing'
  LAST_REGISTER_DATE = 'last_register_date'
  NAME = 'name'
  POLICY_NAME = 'policy_name'
  POLICY_STATUS = 'policy_status'
  POLICY_STATUS_DETAILS = 'policy_status_details'
  UPGRADE_STATUS = 'upgrade_status'
