# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib.resources
import logging

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial import constants
from qc_openmaterial.schemas import schema_files
from qc_openmaterial.checks import models

from qc_openmaterial.checks.basic_checker import (
    valid_json_document,
    version_is_defined,
)

CHECKER_ID = "check_asam_openmaterial_valid_schema"
CHECKER_DESCRIPTION = "Input JSON file must be valid according to the corresponding schema."
CHECKER_PRECONDITIONS = {
    valid_json_document.CHECKER_ID,
    version_is_defined.CHECKER_ID,
}
RULE_UID = "asam.net:openmaterial:1.0.0:json.valid_schema"


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file is valid according to OpenSCENARIO schema
    """
    logging.info("Executing valid_schema check")

    # schema_version = checker_data.schema_version
    # xsd_file = schema_files.SCHEMA_FILES.get(schema_version)
    #
    # if xsd_file is None:
    #     checker_data.result.set_checker_status(
    #         checker_bundle_name=constants.BUNDLE_NAME,
    #         checker_id=CHECKER_ID,
    #         status=StatusType.SKIPPED,
    #     )
    #
    #     checker_data.result.add_checker_summary(
    #         constants.BUNDLE_NAME,
    #         CHECKER_ID,
    #         f"- Schema file for version {schema_version} does not exist. Skip the check.",
    #     )
    #
    #     return
    #
    # xsd_file_path = str(
    #     importlib.resources.files("qc_openmaterial.schema").joinpath(xsd_file)
    # )
    # schema_compliant, errors = _is_schema_compliant(
    #     checker_data.input_file_xml_root, xsd_file_path
    # )
    #
    # if not schema_compliant:
    #     for error in errors:
    #         issue_id = checker_data.result.register_issue(
    #             checker_bundle_name=constants.BUNDLE_NAME,
    #             checker_id=CHECKER_ID,
    #             description="Input file does not follow its version schema",
    #             level=IssueSeverity.ERROR,
    #             rule_uid=RULE_UID,
    #         )
    #         checker_data.result.add_file_location(
    #             checker_bundle_name=constants.BUNDLE_NAME,
    #             checker_id=CHECKER_ID,
    #             issue_id=issue_id,
    #             row=error.line,
    #             column=error.column,
    #             description=error.message,
    #         )
