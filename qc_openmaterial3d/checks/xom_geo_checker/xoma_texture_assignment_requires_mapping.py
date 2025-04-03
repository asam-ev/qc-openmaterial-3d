# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import json
import os

from pathlib import Path

from qc_baselib import IssueSeverity
from qc_openmaterial3d import constants
from qc_openmaterial3d.checks import models, utils

CHECKER_ID = "check_asam.net:xomgeo:1.0.0:xoma.texture_assignment_requires_mapping"
CHECKER_DESCRIPTION = "If the property 'materialTextureAssignment' is set, 'materialMappingUri' must also be set."
CHECKER_PRECONDITIONS = {}
RULE_UID = "asam.net:xomgeo:1.0.0:xoma.texture_assignment_requires_mapping"


def add_issue(checker_data: models.CheckerData, input_json_path: str):
    """
        Add issue to checker_data.

        Args:
            input_json_path: Absolute path of the input json needed to get issue locations
            checker_data: Checker data object used to raise issues
        """
    issue_id = checker_data.result.register_issue(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description=f"materialTextureAssignment is set in the xoma file but the materialMappingUri property is not set.",
        level=IssueSeverity.ERROR,
        rule_uid=RULE_UID
    )
    line = utils.find_property_line(input_json_path, ["materialTextureAssignment"])
    if line:
        checker_data.result.add_file_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            row=line,
            column=0,
            description="materialMappingUri does not exist.",
        )

def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if assigned textures exist

    Args:
        checker_data: Checker data object used to raise issues
    """
    logging.info(f"Executing {CHECKER_ID}")

    # Check the precondition (whether the input file exists).
    file_path = Path(checker_data.json_file_path)

    if file_path.exists():
        # Load file
        with open(file_path, "r") as file:
            input_file = json.load(file)

        if not os.path.splitext(file_path)[1].lower() == '.xoma':
            return

        if "materialTextureAssignment" not in input_file:
            return

        if not "materialMappingUri" in input_file:
            add_issue(checker_data, checker_data.json_file_path)

    else:
        checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="The input file does not exist.",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )