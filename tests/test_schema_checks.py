# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import test_utils
from qc_baselib import Result, StatusType
from qc_openmaterial.checks import schema_checker


def test_valid_schema_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = "json.valid_schema.positive.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(schema_checker.valid_schema.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(result.get_issues_by_rule_uid("asam.net:openmaterial:1.0.0:json.valid_schema")) == 0
    )

    test_utils.cleanup_files()


def test_valid_schema_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = "json.valid_schema.negative.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(schema_checker.valid_schema.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(result.get_issues_by_rule_uid("asam.net:openmaterial:1.0.0:json.valid_schema")) == 1
    )
    test_utils.cleanup_files()
