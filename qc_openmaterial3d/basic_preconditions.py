# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

from qc_openmaterial3d.checks.xom_general_checker import (
    general_valid_json_document,
    general_version_is_defined, general_valid_schema,
)

CHECKER_PRECONDITIONS = {
    general_valid_json_document.CHECKER_ID,
    general_version_is_defined.CHECKER_ID,
    general_valid_schema.CHECKER_ID,
}
