# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import json

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial3d import constants, basic_preconditions
from qc_openmaterial3d.checks import models, utils

CHECKER_ID = "check_asam.net:xom:1.0.0:xoma.vehicle_class_data_defined"
CHECKER_DESCRIPTION = "If an asset is of type 'vehicle', the property 'vehicleClassData' must be set in the metadata."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xom:1.0.0:xoma.vehicle_class_data_defined"


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {CHECKER_ID}")

    if not checker_data.json_file_path.endswith(".xoma"):
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

    with open(checker_data.json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    metadata = data.get("metadata", {})
    object_class = metadata.get("objectClass")

    if object_class != "vehicle":
        return

    if "vehicleClassData" not in metadata:
        line = utils.find_property_line(
            checker_data.json_file_path, ["metadata", "objectClass"]
        )
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Asset objectClass is 'vehicle' but 'vehicleClassData' is not set in metadata.",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )
        if line is not None:
            checker_data.result.add_file_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                row=line,
                column=0,
                description="objectClass is 'vehicle' here but vehicleClassData is missing.",
            )
