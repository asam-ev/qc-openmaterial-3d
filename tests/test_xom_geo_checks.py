# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openmaterial3d.checks import xom_geo_checker


def test_vehicle_class_data_defined_positive(monkeypatch) -> None:
    base_path = "tests/data/vehicle_class_data_defined/"
    target_file_name = "vehicle_class_data_defined.positive.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(xom_geo_checker.vehicle_class_data_defined.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xomgeo:1.0.0:xoma.vehicle_class_data_defined"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_vehicle_class_data_defined_negative(monkeypatch) -> None:
    base_path = "tests/data/vehicle_class_data_defined/"
    target_file_name = "vehicle_class_data_defined.negative.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(xom_geo_checker.vehicle_class_data_defined.CHECKER_ID)
        == StatusType.COMPLETED
    )

    issues = result.get_issues_by_rule_uid(
        "asam.net:xomgeo:1.0.0:xoma.vehicle_class_data_defined"
    )
    assert len(issues) == 1
    assert issues[0].level == IssueSeverity.ERROR

    test_utils.cleanup_files()


def test_vehicle_class_data_defined_non_vehicle(monkeypatch) -> None:
    base_path = "tests/data/valid_schema/"
    target_file_name = "json.valid_schema.positive.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(xom_geo_checker.vehicle_class_data_defined.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xomgeo:1.0.0:xoma.vehicle_class_data_defined"
            )
        )
        == 0
    )

    test_utils.cleanup_files()
