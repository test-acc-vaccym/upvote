// Copyright 2017 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

goog.provide('upvote.settings.SettingResource');

goog.require('upvote.app.constants');
goog.require('upvote.lib.resources.buildResource');

goog.scope(function() {
var buildResource = upvote.lib.resources.buildResource;


/** @export {function(angular.$resource):!angular.Resource} */
upvote.settings.SettingResource =
    buildResource(upvote.app.constants.WEB_PREFIX + 'settings/:setting');
});  // goog.scope
