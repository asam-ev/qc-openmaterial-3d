# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib.resources
from jsonschema import Draft7Validator
import logging
import json
import os

from qc_baselib import IssueSeverity

from qc_openmaterial3d import constants
from qc_openmaterial3d.schemas import schema_files
from qc_openmaterial3d.checks import utils, models

from qc_openmaterial3d.checks.xom_general_checker import (
    general_valid_json_document,
    general_version_is_defined,
)

CHECKER_ID = "check_asam.net:xom:1.0.0:general.valid_schema"
CHECKER_DESCRIPTION = "Input JSON file must be valid according to the corresponding schema."
CHECKER_PRECONDITIONS = {
    general_valid_json_document.CHECKER_ID,
    general_version_is_defined.CHECKER_ID,
}
RULE_UID = "asam.net:xom:1.0.0:general.valid_schema"


def get_schema_file(version: str, file_path: str) -> str:
    """Retrieves the schema file corresponding to the given file path and version.

    Args:
        file_path: Path to the file.
        version: Version string to construct the schema key.

    Returns:
        The schema file path if found, otherwise None.

    Raises:
        ValueError: If the file extension is not supported.
    """
    # Extract the file name and extension
    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()  # Ensure extension is lowercase

    # Supported extensions
    supported_extensions = [".xoma", ".xomm", ".xomp", ".xompt"]

    schema_key = ""

    if file_extension in supported_extensions:
        if file_extension == ".xompt":
            # Handle .xompt case with additional string from file name
            previous_string = file_name.split('_')[-1]
            combined_extension = f"{previous_string}.xompt"
            schema_key = f"{version}:{combined_extension}"
        else:
            # Handle other cases
            schema_key = f"{version}:{file_extension[1:]}"  # Remove leading dot
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    return schema_files.SCHEMA_FILES.get(schema_key)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file is valid according to the respective OpenMATERIAL 3D schema

    Args:
        checker_data: Checker data object used to raise issues
    """
    logging.info(f"Executing {CHECKER_ID}")

    with open(checker_data.json_file_path, "r") as file:
        data = json.load(file)

    schema_version = checker_data.schema_version
    schema_path = get_schema_file(schema_version, checker_data.json_file_path)
    schema_file_path = str(
        importlib.resources.files("qc_openmaterial3d.schemas").joinpath(schema_path)
    )

    with open(schema_file_path, "r") as file:
        schema_file = json.load(file)

    validator = Draft7Validator(schema_file)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    for error in errors:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description=f"Error in {error.json_path[2:]}: {error.message}",
            level=IssueSeverity.ERROR,
            rule_uid=RULE_UID,
        )

        error_path = list(error.absolute_path)
        line = utils.find_property_line(checker_data.json_file_path, error_path)
        if line:
            checker_data.result.add_file_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                issue_id=issue_id,
                row=line,
                column=0,
                description=error.message,
            )
