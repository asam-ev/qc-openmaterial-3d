# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial3d import constants, basic_preconditions
from qc_openmaterial3d.checks import models, utils

CHECKER_ID = "check_asam.net:xom:1.1.0:xoma.cone_angles_ordered_correctly"
CHECKER_DESCRIPTION = (
    "If the properties 'lightDefinitions.innerConeAngle' and 'lightDefinitions.outerConeAngle' "
    "are both set, the value of 'lightDefinitions.innerConeAngle' shall be smaller than "
    "the value of 'lightDefinitions.outerConeAngle'."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xom:1.1.0:xoma.cone_angles_ordered_correctly"


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

    light_definitions = data.get("lightDefinitions", [])

    for i, light in enumerate(light_definitions):
        inner = light.get("innerConeAngle")
        outer = light.get("outerConeAngle")
        if inner is None or outer is None:
            continue
        if inner >= outer:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description=(
                    f"lightDefinitions[{i}].innerConeAngle ({inner}) is not smaller than "
                    f"outerConeAngle ({outer})."
                ),
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            inner_line = utils.find_property_line(
                file_path, ["lightDefinitions", i, "innerConeAngle"]
            )
            if inner_line is not None:
                checker_data.result.add_file_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    issue_id=issue_id,
                    row=inner_line,
                    column=0,
                    description=f"innerConeAngle must be smaller than outerConeAngle.",
                )
