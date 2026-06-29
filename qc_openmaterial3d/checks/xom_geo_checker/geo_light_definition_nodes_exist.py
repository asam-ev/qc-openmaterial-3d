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

CHECKER_ID = "check_asam.net:xomgeo:1.1.0:xoma.light_definition_nodes_exist"
CHECKER_DESCRIPTION = (
    "If the property 'lightDefinitions' is set, all nodes referenced in the "
    "'lightDefinitions[*].node' fields shall exist in the corresponding 3D data file."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xomgeo:1.1.0:xoma.light_definition_nodes_exist"


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {CHECKER_ID}")

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

    light_definitions = data.get("lightDefinitions", [])
    if not light_definitions:
        return

    gltf_node_names = {
        node.name for node in checker_data.gltf.nodes if node.name is not None
    }

    table_line = utils.find_property_line(file_path, ["lightDefinitions"])

    for i, light in enumerate(light_definitions):
        node_name = light.get("node")
        if node_name is not None and node_name not in gltf_node_names:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description=(
                    f"Node '{node_name}' referenced in lightDefinitions[{i}].node "
                    f"does not exist in the 3D model file."
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
                    description="'lightDefinitions' references a node that does not exist in the 3D model.",
                )
