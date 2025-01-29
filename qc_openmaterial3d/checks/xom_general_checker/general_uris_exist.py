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
from qc_openmaterial3d.checks import models

from qc_openmaterial3d.checks.xom_general_checker import (
    general_valid_schema
)

CHECKER_ID = "check_asam.net:xom:1.0.0:general.uris_exist"
CHECKER_DESCRIPTION = "If an URI property to other file is set in a JSON file, the file linked in that property shall exist."
CHECKER_PRECONDITIONS = {}
RULE_UID = "asam.net:xom:1.0.0:general.uris_exist"


def check_uris_recursively(input_json: dict, base_dir: str, checker_data: models.CheckerData):
    """
    Recursively check all properties ending in 'Uri' and verify if the file exists.

    Args:
        input_json: The JSON data
        base_dir: The base directory of the JSON file for resolving relative paths
        checker_data: Checker data object used to raise issues
    """

    for key, uri_path in input_json.items():
        if key.endswith("Uri") and isinstance(uri_path, str):  # Ensure it's a string path
            absolute_path = os.path.join(base_dir, uri_path)

            if not os.path.exists(absolute_path):
                checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    description=f"The uri {uri_path} set in {key} does not exist.",
                    level=IssueSeverity.ERROR,
                    rule_uid=RULE_UID
                )
        elif key.endswith("Uris") and isinstance(uri_path, list):  # Ensure it's a string path
            for uri in uri_path:
                if isinstance(uri, str):
                    absolute_path = os.path.join(base_dir, uri)
                    if not os.path.exists(absolute_path):
                        checker_data.result.register_issue(
                            checker_bundle_name=constants.BUNDLE_NAME,
                            checker_id=CHECKER_ID,
                            description=f"The uri {uri} set in {key} does not exist.",
                            level=IssueSeverity.ERROR,
                            rule_uid=RULE_UID
                        )

        # Recur for nested dictionaries
        if isinstance(uri_path, dict):
            check_uris_recursively(uri_path, base_dir, checker_data)



def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if uris exist

    Args:
        checker_data: Checker data object used to raise issues
    """
    logging.info(f"Executing {CHECKER_ID}")

    # Check the precondition (whether the input file exists).
    file_path = Path(checker_data.json_file_path)
    # Get the absolute directory of the JSON file
    json_dir = os.path.dirname(os.path.abspath(file_path))

    if file_path.exists():
        # Load file
        with open(file_path, "r") as file:
            input_file = json.load(file)

        check_uris_recursively(input_file, json_dir, checker_data)

    else:
        checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="The input file does not exist.",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )