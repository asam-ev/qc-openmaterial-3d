# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

from qc_openmaterial.checks.basic_checker import (
    valid_json_document,
    version_is_defined,
)

from qc_openmaterial.checks.schema_checker import valid_schema

CHECKER_PRECONDITIONS = {
    valid_json_document.CHECKER_ID,
    version_is_defined.CHECKER_ID,
    valid_schema.CHECKER_ID,
}
