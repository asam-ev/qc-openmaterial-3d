# SPDX-License-Identifier: MPL-2.0
# Copyright 2025, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
import os

from qc_baselib import IssueSeverity, StatusType

from qc_openmaterial3d import constants, basic_preconditions
from qc_openmaterial3d.checks import models, utils

CHECKER_ID = "check_asam.net:xom:1.0.0:xoma.all_texture_rgba_codes_defined"
CHECKER_DESCRIPTION = (
    "If the property 'materialTextureAssignment' is set, all color codes of all "
    "referenced textures shall be covered by the material mapping table referenced "
    "in 'materialMappingUri'."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xom:1.0.0:xoma.all_texture_rgba_codes_defined"


def add_issue(
    checker_data: models.CheckerData, description: str, location_description: str
):
    issue_id = checker_data.result.register_issue(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description=description,
        level=IssueSeverity.ERROR,
        rule_uid=RULE_UID,
    )
    line = utils.find_property_line(
        checker_data.json_file_path, ["materialTextureAssignment"]
    )
    if line is not None:
        checker_data.result.add_file_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            row=line,
            column=0,
            description=location_description,
        )


def get_mapped_colors(mapping_path: str) -> set[tuple[int, int, int]]:
    """Collect all RGB codes used as keys in a material mapping table.

    Keys that are material names instead of RGB codes are ignored.

    Args:
        mapping_path (str): Path to the material mapping file (.xomm).

    Returns:
        set[tuple[int, int, int]]: The mapped colors as (R, G, B) tuples.
    """
    with open(mapping_path, "r", encoding="utf-8") as file:
        mapping_file = json.load(file)

    mapped_colors = set()
    for mapping in mapping_file.get("materialMapping", []):
        if not mapping:
            continue
        color = utils.parse_rgb_code(mapping[0])
        if color is not None:
            mapped_colors.add(color)

    return mapped_colors


def check_texture(
    checker_data: models.CheckerData,
    texture_path: str,
    absolute_texture_path: str,
    mapping_uri: str,
    mapped_colors: set[tuple[int, int, int]],
):
    """Check a single assignment texture against the mapped colors."""
    try:
        texture_colors = utils.get_texture_colors(absolute_texture_path)
    except Exception as e:
        # A texture that cannot be decoded cannot be checked. Do not fail the
        # whole checker over it, the remaining textures are still worth checking.
        logging.warning(f"Could not read the assignment texture {texture_path}: {e}")
        return

    if texture_colors is None:
        add_issue(
            checker_data,
            f"The assignment texture {texture_path} contains more than "
            f"{utils.MAX_ASSIGNMENT_TEXTURE_COLORS} distinct colors and is therefore "
            f"not a valid ASAM OpenMATERIAL 3D assignment texture.",
            "Assignment texture contains too many distinct colors.",
        )
        return

    for color in sorted(texture_colors - mapped_colors):
        add_issue(
            checker_data,
            f"The color code rgb:{color[0]};{color[1]};{color[2]} used in the assignment "
            f"texture {texture_path} is not covered by the material mapping table {mapping_uri}.",
            "Color code is not covered by the material mapping table.",
        )


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

    with open(file_path, "r", encoding="utf-8") as file:
        input_file = json.load(file)

    if "materialTextureAssignment" not in input_file:
        return

    # A missing material mapping is reported by xoma.texture_assignment_requires_mapping
    # and a missing mapping file by general.uris_exist. Do not report them twice.
    mapping_uri = input_file.get("materialMappingUri")
    if not isinstance(mapping_uri, str):
        return

    base_dir = os.path.dirname(os.path.abspath(file_path))
    mapping_path = os.path.join(base_dir, mapping_uri)
    if not os.path.exists(mapping_path):
        return

    try:
        mapped_colors = get_mapped_colors(mapping_path)
    except (json.JSONDecodeError, OSError) as e:
        logging.warning(f"Could not read the material mapping table {mapping_uri}: {e}")
        return

    for assignment in input_file["materialTextureAssignment"]:
        texture_path = assignment[1]
        if not isinstance(texture_path, str):
            continue

        absolute_texture_path = os.path.join(base_dir, texture_path)
        # A missing texture is reported by xoma.material_textures_exist.
        if not os.path.exists(absolute_texture_path):
            continue

        check_texture(
            checker_data,
            texture_path,
            absolute_texture_path,
            mapping_uri,
            mapped_colors,
        )
