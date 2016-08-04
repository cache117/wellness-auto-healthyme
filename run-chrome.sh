#!/bin/bash -x
# Copyright 2016 Brigham Young University
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


docker run -d -P --name=selenium_hub selenium/standalone-chrome
port=`docker port selenium_hub | sed -e "s/.*://"`
docker run --rm -v $HOME/.byu:/root/.byu -v $(pwd):/usr/src/app --link=selenium_hub wellness-auto-healthyme python import.py import.json
docker rm -f selenium_hub