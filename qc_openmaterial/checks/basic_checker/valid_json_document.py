# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import json

from pathlib import Path

from qc_baselib import IssueSeverity
from qc_openmaterial import constants
from qc_openmaterial.checks import models

CHECKER_ID = "check_asam.net:xom:1.0.0:general.valid_json_document"
CHECKER_DESCRIPTION = "The given file to check must be a valid JSON document."
CHECKER_PRECONDITIONS = set()
RULE_UID = "asam.net:xom:1.0.0:general.valid_json_document"


def is_valid_json(file_path: str) -> bool:
    try:
        with open(file_path, "r") as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        return False


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file is a valid json document
    """
    logging.info("Executing valid_json_document check")

    # Check the precondition (whether the input file exists).
    file_path = Path(checker_data.json_file_path)
    if file_path.exists():
        # Execute the check logic as the precondition holds
        is_valid = is_valid_json(checker_data.json_file_path)

        if not is_valid:
            checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="The input file is not a valid json file.",
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
    else:
        checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="The input file does not exist.",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )