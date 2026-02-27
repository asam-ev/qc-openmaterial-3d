# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import test_utils
from qc_baselib import Result, StatusType
from qc_openmaterial3d.checks import xom_geo_checker


def test_texture_assignment_requires_mapping_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/texture_assignment_requires_mapping/"
    target_file_name = "texture_assignment_requires_mapping.positive.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(xom_geo_checker.texture_assignment_requires_mapping.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(result.get_issues_by_rule_uid("asam.net:xomgeo:1.0.0:xoma.texture_assignment_requires_mapping")) == 0
    )
    test_utils.cleanup_files()


def test_texture_assignment_requires_mapping_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/texture_assignment_requires_mapping/"
    target_file_name = "texture_assignment_requires_mapping.negative.xoma"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(xom_geo_checker.texture_assignment_requires_mapping.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(result.get_issues_by_rule_uid("asam.net:xomgeo:1.0.0:xoma.texture_assignment_requires_mapping")) == 1
    )
    test_utils.cleanup_files()
