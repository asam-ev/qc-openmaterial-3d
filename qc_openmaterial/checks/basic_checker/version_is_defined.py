# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import json

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial import constants
from qc_openmaterial.checks import models

from qc_openmaterial.checks.basic_checker import (
    valid_json_document,
)

CHECKER_ID = "check_asam_openmaterial_version_is_defined"
CHECKER_DESCRIPTION = "The metadata of the file must contain an openMaterialVersion field."
CHECKER_PRECONDITIONS = {
    valid_json_document.CHECKER_ID
}
RULE_UID = "asam.net:openmaterial:1.0.0:json.version_is_defined"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    The metadata of the file must contain an openMaterialVersion field.
    """
    logging.info("Executing version_is_defined check")

    with open(checker_data.json_file_path, "r") as file:
        data = json.load(file)

    # Check if "metadata.openMaterialVersion" exists
    if "metadata" not in data or "openMaterialVersion" not in data["metadata"]:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Version attributes revMajor-revMinor missing or invalid",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )
