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

CHECKER_ID = "check_asam.net:xommat:1.0.0:xomp.look_up_tables_unique_wavelengths"
CHECKER_DESCRIPTION = (
    "Look-up tables referenced in a .xomp file should not have overlapping wavelength ranges."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xommat:1.0.0:xomp.look_up_tables_unique_wavelengths"

_URI_CATEGORIES = [
    ("brdfUris", "brdf", "wavelengths"),
    ("reflectionCoefficientUris", "reflectionCoefficient", "wavelengths"),
]


def _load_wavelengths(xompt_path: str, top_key: str) -> list | None:
    try:
        with open(xompt_path, "r") as f:
            data = json.load(f)
        return data.get(top_key, {}).get("wavelengths", [])
    except Exception:
        return None


def _check_category(
    uris: list[str],
    uri_property: str,
    top_key: str,
    xomp_dir: str,
    checker_data: models.CheckerData,
) -> None:
    seen = {}  # wavelength value -> first URI that listed it

    for uri in uris:
        abs_path = os.path.join(xomp_dir, uri)
        wavelengths = _load_wavelengths(abs_path, top_key)
        if wavelengths is None:
            continue

        for wl in wavelengths:
            if wl in seen:
                line = utils.find_property_line(
                    checker_data.json_file_path,
                    ["materialProperties", uri_property],
                )
                issue_id = checker_data.result.register_issue(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    description=(
                        f"Overlapping wavelength {wl} m: present in both "
                        f"'{seen[wl]}' and '{uri}'."
                    ),
                    level=IssueSeverity.WARNING,
                    rule_uid=RULE_UID,
                )
                if line is not None:
                    checker_data.result.add_file_location(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        issue_id=issue_id,
                        row=line,
                        column=0,
                        description=(
                            f"'{uri_property}' references files with overlapping wavelengths."
                        ),
                    )
            else:
                seen[wl] = uri


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {CHECKER_ID}")

    file_path = checker_data.json_file_path

    if not file_path.endswith(".xomp"):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "Rule only applies to .xomp files. Skip the check.",
        )
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    xomp_dir = os.path.dirname(os.path.abspath(file_path))
    material_props = data.get("materialProperties", {})

    for uri_property, top_key, _ in _URI_CATEGORIES:
        uris = material_props.get(uri_property, [])
        if len(uris) < 2:
            continue
        _check_category(uris, uri_property, top_key, xomp_dir, checker_data)
