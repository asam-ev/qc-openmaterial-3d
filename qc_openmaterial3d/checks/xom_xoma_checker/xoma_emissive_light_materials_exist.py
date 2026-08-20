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

CHECKER_ID = "check_asam.net:xom:1.1.0:xoma.emissive_light_materials_exist"
CHECKER_DESCRIPTION = (
    "If the property 'emissiveLightMapping' is set, all materials referenced in the "
    "'emissiveLightMapping[*].materialName' fields shall exist in the corresponding 3D data file."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xom:1.1.0:xoma.emissive_light_materials_exist"


def check_rule(checker_data: models.CheckerData) -> None:

    file_path = checker_data.json_file_path

    if not file_path.endswith(".xoma"):
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

    if checker_data.gltf is None:
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            CHECKER_ID,
            "No corresponding .gltf or .glb file found. Skip the check.",
        )
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    emissive_mappings = data.get("emissiveLightMapping", [])
    if not emissive_mappings:
        return

    gltf_material_names = {
        mat.name for mat in checker_data.gltf.materials if mat.name is not None
    }

    for i, mapping in enumerate(emissive_mappings):
        material_name = mapping.get("materialName")
        if material_name is not None and material_name not in gltf_material_names:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description=(
                    f"Material '{material_name}' referenced in emissiveLightMapping[{i}].materialName "
                    f"does not exist in the 3D model file."
                ),
                level=IssueSeverity.ERROR,
                rule_uid=RULE_UID,
            )
            material_line = utils.find_property_line(
                file_path, ["emissiveLightMapping", i, "materialName"]
            )
            if material_line is not None:
                checker_data.result.add_file_location(
                    checker_bundle_name=constants.BUNDLE_NAME,
                    checker_id=CHECKER_ID,
                    issue_id=issue_id,
                    row=material_line,
                    column=0,
                    description="'emissiveLightMapping' references a material that does not exist in the 3D model.",
                )
