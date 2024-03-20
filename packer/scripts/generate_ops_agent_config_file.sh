#!/bin/bash

filename="/etc/google-cloud-ops-agent/config.yaml"

content=$(cat <<EOF
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# <== Enter custom agent configurations in this file.
# See https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/configuration
# for more details.

logging:
  receivers:
    webapp:
      type: files
      include_paths:
      - /var/log/webapp.log
      record_log_file_path: true

  processors:
    webapp-processor:
      type: parse_json
      time_key: timeStamp
      time_format: "%Y-%m-%dT%H:%M:%S.%L%Z"
    modify-fields:
      type: modify_fields
      fields:
        severity:
          copy_from: jsonPayload.severity

  service:
    pipelines:
      pipeline1:
        receivers: [webapp]
        processors: [webapp-processor,modify-fields]

EOF
)

echo "$content" | sudo tee "$filename" > /dev/null

echo "File '$filename' created successfully!"
