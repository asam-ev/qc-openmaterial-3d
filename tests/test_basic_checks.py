# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openmaterial.checks import basic_checker


def test_valid_json_document_positive(monkeypatch,) -> None:
    base_path = "tests/data/valid_json_document/"
    target_file_name = f"json.valid_json_document.positive.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
            result.get_checker_status(basic_checker.valid_json_document.CHECKER_ID)
            == StatusType.COMPLETED
    )
    assert (
            len(result.get_issues_by_rule_uid("asam.net:openmaterial:1.0.0:json.valid_json_document"))
            == 0
    )

    test_utils.cleanup_files()


def test_valid_json_document_negative(monkeypatch,) -> None:
    base_path = "tests/data/valid_json_document/"
    target_file_name = f"json.valid_json_document.negative.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
            result.get_checker_status(basic_checker.valid_json_document.CHECKER_ID)
            == StatusType.COMPLETED
    )

    json_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:openmaterial:1.0.0:json.valid_json_document"
    )
    assert len(json_doc_issues) == 1
    assert json_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_version_is_defined_positive(monkeypatch,) -> None:
    base_path = "tests/data/version_is_defined/"
    target_file_name = f"version_is_defined.positive.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
            result.get_checker_status(basic_checker.version_is_defined.CHECKER_ID)
            == StatusType.COMPLETED
    )

    assert (
            len(result.get_issues_by_rule_uid("asam.net:openmaterial:1.0.0:json.version_is_defined"))
            == 0
    )

    test_utils.cleanup_files()


def test_version_is_defined_missing_attr(monkeypatch,) -> None:
    base_path = "tests/data/version_is_defined/"
    target_file_name = f"version_is_defined.negative.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
            result.get_checker_status(basic_checker.version_is_defined.CHECKER_ID)
            == StatusType.COMPLETED
    )

    json_doc_issues = result.get_issues_by_rule_uid(
        "asam.net:openmaterial:1.0.0:json.version_is_defined"
    )
    assert len(json_doc_issues) == 1
    assert json_doc_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
