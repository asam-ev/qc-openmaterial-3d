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

CHECKER_ID = "check_asam.net:xom:1.0.0:general.uris_exist"
CHECKER_DESCRIPTION = "If a URI property to other file is set in a JSON file, the file linked in that property shall exist."
CHECKER_PRECONDITIONS = {}
RULE_UID = "asam.net:xom:1.0.0:general.uris_exist"


def add_issue(checker_data: models.CheckerData, input_json_path: str, json_field_path: list, uri_path: str, key: str):
    """
        Add issue to checker_data.

        Args:
            input_json_path: Absolute path of the input json needed to get issue locations
            checker_data: Checker data object used to raise issues
            json_field_path: List of field hierarchy, e.g. ['metadata', 'fieldToFind'] used to get issue locations. Leave empty when initially calling this function.
            uri_path: Content of the uri field
            key: Name of the field
        """
    issue_id = checker_data.result.register_issue(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description=f"The URI {uri_path} set in {key} does not exist.",
        level=IssueSeverity.ERROR,
        rule_uid=RULE_UID
    )
    current_json_field_path = json_field_path.copy()
    current_json_field_path.append(key)
    line = utils.find_property_line(input_json_path, current_json_field_path)
    if line:
        checker_data.result.add_file_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            row=line,
            column=0,
            description="File does not exist.",
        )

def check_uris_recursively(input_json_path: str, input_json: dict, checker_data: models.CheckerData, json_field_path: list):
    """
    Recursively check all properties ending in 'Uri' or 'Uris' and verify if the file exists.

    Args:
        input_json_path: Absolute path of the input json needed to get issue locations
        input_json: The JSON data for the current recursion
        checker_data: Checker data object used to raise issues
        json_field_path: List of field hierarchy, e.g. ['metadata', 'fieldToFind'] used to get issue locations. Leave empty when initially calling this function.
    """
    # Get the absolute directory of the JSON file
    base_dir = os.path.dirname(os.path.abspath(input_json_path))

    for key, uri_field in input_json.items():
        if key.endswith("Uri") and isinstance(uri_field, str):  # Ensure it's a string path
            uri_path = uri_field
            absolute_path = os.path.join(base_dir, uri_path)

            if not os.path.exists(absolute_path):
                add_issue(checker_data, input_json_path, json_field_path, uri_path, key)
        elif key.endswith("Uris") and isinstance(uri_field, list):  # Ensure it's a string path
            for uri_path in uri_field:
                if isinstance(uri_path, str):
                    absolute_path = os.path.join(base_dir, uri_path)
                    if not os.path.exists(absolute_path):
                        add_issue(checker_data, input_json_path, json_field_path, uri_path, key)

        # Recur for nested dictionaries
        if isinstance(uri_field, dict):
            current_json_field_path = json_field_path.copy()
            current_json_field_path.append(key)
            check_uris_recursively(input_json_path, uri_field, checker_data, current_json_field_path)

def check_uris(input_json_path: str, input_json: dict, checker_data: models.CheckerData):
    """
        Call recursive check for all properties ending in 'Uri' or 'Uris' and verify if the file exists.

    Args:
        input_json_path: Absolute path of the input json needed to get issue locations
        input_json: The JSON data for the current recursion
        checker_data: Checker data object used to raise issues
    """
    check_uris_recursively(input_json_path, input_json, checker_data, list())

def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if uris exist

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

        check_uris(checker_data.json_file_path, input_file, checker_data)

    else:
        checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="The input file does not exist.",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )