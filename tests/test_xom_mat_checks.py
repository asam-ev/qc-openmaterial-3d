# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openmaterial3d.checks import xom_mat_checker

# --- tables_sorted_correctly constants ---

TABLES_SORTED_RULE_UID = "asam.net:xommat:1.0.0:xompt.tables_sorted_correctly"
TABLES_SORTED_CHECKER_ID = xom_mat_checker.tables_sorted_correctly.CHECKER_ID
TABLES_SORTED_BASE_PATH = "tests/data/tables_sorted_correctly/"


def _load_tables_sorted_result(monkeypatch, file_name):
    test_utils.create_test_config(os.path.join(TABLES_SORTED_BASE_PATH, file_name))
    test_utils.launch_main(monkeypatch)
    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)
    return result


def test_tables_sorted_correctly_emp_positive(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_positive_emp.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    assert len(result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)) == 0

    test_utils.cleanup_files()


def test_tables_sorted_correctly_emp_negative(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_negative_emp.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    issues = result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)
    assert len(issues) == 1
    assert issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_tables_sorted_correctly_optical_positive(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_positive_optical.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    assert len(result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)) == 0

    test_utils.cleanup_files()


def test_tables_sorted_correctly_optical_negative(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_negative_optical.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    issues = result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)
    assert len(issues) == 1
    assert issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_tables_sorted_correctly_brdf_positive(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_positive_brdf.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    assert len(result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)) == 0

    test_utils.cleanup_files()


def test_tables_sorted_correctly_brdf_negative(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_negative_brdf.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    issues = result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)
    assert len(issues) == 1
    assert issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_tables_sorted_correctly_reflCoeff_positive(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_positive_reflCoeff.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    assert len(result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)) == 0

    test_utils.cleanup_files()


def test_tables_sorted_correctly_reflCoeff_negative(monkeypatch) -> None:
    result = _load_tables_sorted_result(monkeypatch, "tables_sorted_correctly_negative_reflCoeff.xompt")

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.COMPLETED
    issues = result.get_issues_by_rule_uid(TABLES_SORTED_RULE_UID)
    assert len(issues) == 1
    assert issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_tables_sorted_correctly_non_xompt_skipped(monkeypatch) -> None:
    test_utils.create_test_config("tests/data/valid_schema/json.valid_schema.positive.xoma")
    test_utils.launch_main(monkeypatch)
    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_checker_status(TABLES_SORTED_CHECKER_ID) == StatusType.SKIPPED

    test_utils.cleanup_files()


# --- look_up_tables_unique_wavelengths constants ---

UNIQUE_WL_RULE_UID = "asam.net:xommat:1.0.0:xomp.look_up_tables_unique_wavelengths"
UNIQUE_WL_CHECKER_ID = xom_mat_checker.look_up_tables_unique_wavelengths.CHECKER_ID
UNIQUE_WL_BASE_PATH = "tests/data/look_up_tables_unique_wavelengths/"


def test_look_up_tables_unique_wavelengths_positive(monkeypatch) -> None:
    test_utils.create_test_config(
        os.path.join(UNIQUE_WL_BASE_PATH, "look_up_tables_unique_wavelengths_positive.xomp")
    )
    test_utils.launch_main(monkeypatch)
    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_checker_status(UNIQUE_WL_CHECKER_ID) == StatusType.COMPLETED
    assert len(result.get_issues_by_rule_uid(UNIQUE_WL_RULE_UID)) == 0

    test_utils.cleanup_files()


def test_look_up_tables_unique_wavelengths_negative(monkeypatch) -> None:
    test_utils.create_test_config(
        os.path.join(UNIQUE_WL_BASE_PATH, "look_up_tables_unique_wavelengths_negative.xomp")
    )
    test_utils.launch_main(monkeypatch)
    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_checker_status(UNIQUE_WL_CHECKER_ID) == StatusType.COMPLETED
    issues = result.get_issues_by_rule_uid(UNIQUE_WL_RULE_UID)
    assert len(issues) == 1
    assert issues[0].level == IssueSeverity.WARNING

    test_utils.cleanup_files()


def test_look_up_tables_unique_wavelengths_non_xomp_skipped(monkeypatch) -> None:
    test_utils.create_test_config("tests/data/valid_schema/json.valid_schema.positive.xoma")
    test_utils.launch_main(monkeypatch)
    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert result.get_checker_status(UNIQUE_WL_CHECKER_ID) == StatusType.SKIPPED

    test_utils.cleanup_files()
