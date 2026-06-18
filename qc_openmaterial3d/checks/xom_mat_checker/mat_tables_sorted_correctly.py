# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import json
import os

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial3d import constants, basic_preconditions
from qc_openmaterial3d.checks import models, utils

CHECKER_ID = "check_asam.net:xommat:1.0.0:xompt.tables_sorted_correctly"
CHECKER_DESCRIPTION = "Arrays in look-up tables shall be sorted based on the columns starting with the first."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xommat:1.0.0:xompt.tables_sorted_correctly"

_XOMPT_TABLES = {
    "emp": (["electromagneticProperties"],),
    "optical": (["opticalProperties"],),
    "brdf": (["brdf", "lookupTable"],),
    "reflCoeff": (["reflectionCoefficient", "lookupTable"],),
}


def _get_table(xompt_type: str, data: dict) -> tuple[list | None, list[str]]:
    entry = _XOMPT_TABLES.get(xompt_type)
    if entry is None:
        return None, []
    property_path = entry[0]
    obj = data
    for key in property_path:
        if not isinstance(obj, dict) or key not in obj:
            return None, property_path
        obj = obj[key]
    return obj if isinstance(obj, list) else None, property_path


def _is_out_of_order(prev_row: list, curr_row: list) -> bool:
    """Return True if curr_row is lexicographically less than prev_row (None = -inf)."""
    for prev_val, curr_val in zip(prev_row, curr_row):
        if prev_val is None and curr_val is None:
            continue
        if curr_val is None:
            return True   # -inf < any number
        if prev_val is None:
            return False  # any number >= -inf
        if curr_val < prev_val:
            return True
        if curr_val > prev_val:
            return False
    return False  # rows are equal — not out of order


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {CHECKER_ID}")

    file_path = checker_data.json_file_path

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() != ".xompt":
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Rule only applies to .xompt files. Skip the check.",
        )
        return

    xompt_type = os.path.splitext(file_path)[0].split("_")[-1]
    if xompt_type not in _XOMPT_TABLES:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            f"Unknown .xompt type '{xompt_type}'. Skip the check.",
        )
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    table, property_path = _get_table(xompt_type, data)
    if not table:
        return

    table_line = utils.find_property_line(file_path, property_path)

    for i in range(1, len(table)):
        if _is_out_of_order(table[i - 1], table[i]):
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description=(
                    f"Look-up table row {i} is not sorted correctly: "
                    f"{table[i]} is less than preceding row {table[i - 1]}."
                ),
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            if table_line is not None:
                checker_data.result.add_file_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    issue_id=issue_id,
                    row=table_line,
                    column=0,
                    description=f"Look-up table '{'.'.join(str(p) for p in property_path)}' contains unsorted rows.",
                )
