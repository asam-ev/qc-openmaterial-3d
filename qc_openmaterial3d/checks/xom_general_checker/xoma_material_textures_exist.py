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

CHECKER_ID = "check_asam.net:xom:1.0.0:xoma.material_textures_exist"
CHECKER_DESCRIPTION = "Textures mapped to material names in the 'materialTextureAssignment' field of .xoma files shall exist."
CHECKER_PRECONDITIONS = {}
RULE_UID = "asam.net:xom:1.0.0:xoma.material_textures_exist"


def add_issue(checker_data: models.CheckerData, input_json_path: str, uri_path: str):
    """
        Add issue to checker_data.

        Args:
            input_json_path: Absolute path of the input json needed to get issue locations
            checker_data: Checker data object used to raise issues
            uri_path: Content of the uri field
        """
    issue_id = checker_data.result.register_issue(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description=f"The texture path {uri_path} set in the materialTextureAssignment does not exist.",
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
            description="File does not exist.",
        )

def check_paths(input_json_path: str, input_json: dict, checker_data: models.CheckerData):
    """
        Check if textures assigned in the materialTextureAssignment field exist.

    Args:
        input_json_path: Absolute path of the input json needed to get issue locations
        input_json: The JSON data for the current recursion
        checker_data: Checker data object used to raise issues
    """
    base_dir = os.path.dirname(os.path.abspath(input_json_path))
    texture_assignment = input_json["materialTextureAssignment"]

    for assignment in texture_assignment:
        file_path = assignment[1]
        if isinstance(file_path, str):
            absolute_path = os.path.join(base_dir, file_path)
            if not os.path.exists(absolute_path):
                add_issue(checker_data, input_json_path, file_path)

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

        check_paths(checker_data.json_file_path, input_file, checker_data)

    else:
        checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="The input file does not exist.",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )