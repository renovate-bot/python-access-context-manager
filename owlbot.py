# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------
common = gcp.CommonTemplates()
templated_files = common.py_library(microgenerator=True)

for library in s.get_staging_dirs():
    s.move([library / "**/*.py*"])
s.remove_staging_dirs()

s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        ".gitignore",
        ".github/workflows",
        "noxfile.py",
        "README.rst",
    ],
)

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add license headers
python.fix_pb2_headers()
