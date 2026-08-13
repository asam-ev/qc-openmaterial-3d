# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial3d import constants, basic_preconditions
from qc_openmaterial3d.checks import models, utils

CHECKER_ID = "check_asam.net:xom:1.1.0:xoma.bounding_box_min_max_values"
CHECKER_DESCRIPTION = (
    "In the 'metadata.boundingBox' property of .xoma files, the first value of the 'x', 'y', "
    "and 'z' arrays is the minimum and the second value is the maximum. "
    "The first value shall be smaller than or equal to the second value."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xom:1.1.0:xoma.bounding_box_min_max_values"


def check_rule(checker_data: models.CheckerData) -> None:
    file_path = checker_data.json_file_path

    if not file_path.endswith(".xoma"):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Rule only applies to .xoma files. Skip the check.",
        )
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bounding_box = data.get("metadata", {}).get("boundingBox", {})

    for axis in ("x", "y", "z"):
        values = bounding_box.get(axis)
        if not values or len(values) < 2:
            continue
        min_val, max_val = values[0], values[1]
        if min_val > max_val:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description=(
                    f"metadata.boundingBox.{axis}[0] ({min_val}) is greater than "
                    f"{axis}[1] ({max_val}): first value must be the minimum."
                ),
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            axis_line = utils.find_property_line(
                file_path, ["metadata", "boundingBox", axis]
            )
            if axis_line is not None:
                checker_data.result.add_file_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    issue_id=issue_id,
                    row=axis_line,
                    column=0,
                    description=f"'boundingBox.{axis}' first value exceeds second value.",
                )
