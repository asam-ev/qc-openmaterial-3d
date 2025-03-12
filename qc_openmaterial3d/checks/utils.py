# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# Copyright 2025, Persival GmbH
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import json

EXPRESSION_PATTERN = re.compile(r"[$][{][ A-Za-z0-9_\+\-\*/%$\(\)\.,]*[\}]")
PARAMETER_PATTERN = re.compile(r"[$][A-Za-z_][A-Za-z0-9_]*")


def get_open_material_version(json_file_path: str) -> str:
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data["metadata"]["openMaterial3dVersion"]


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings like "X.x.x"
        This function is to avoid comparing version string basing on lexicographical order
        that could cause problem. E.g.
        1.10.0 > 1.2.0 but lexicographical comparison of string would return the opposite

    Args:
        version1 (str): First string to compare
        version2 (str): Second string to compare

    Returns:
        int: 1 if version1 is bigger than version2. 0 if the version are the same. -1 otherwise
    """
    v1_components = list(map(int, version1.split(".")))
    v2_components = list(map(int, version2.split(".")))

    # Compare each component until one is greater, or they are equal
    for v1, v2 in zip(v1_components, v2_components):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1

    # If all components are equal, compare based on length
    if len(v1_components) < len(v2_components):
        return -1
    elif len(v1_components) > len(v2_components):
        return 1
    else:
        return 0


def recursive_search(hierarchy, lines, current_line):
    """
    Recursively traverses the JSON structure based on the property hierarchy.

    Args:
        hierarchy (list): The remaining parts of the property hierarchy to search for.
        lines (list): All lines of the JSON file.
        current_line (int): The current line number in the JSON file.

    Returns:
        int: The line number of the property if found, otherwise -1.
    """
    if not hierarchy:
        return current_line

    for line_num, line in enumerate(lines):
        # Start by checking if the current line corresponds to the first property in the hierarchy
        if f'"{hierarchy[0]}"' in line:
            if len(hierarchy) == 1:
                return current_line + line_num
            else:
                return recursive_search(hierarchy[1:], lines[line_num:], current_line + line_num)

    return -1


def find_property_line(json_file_path, property_hierarchy) -> int | None:
    """
    Finds the line number of a specific property in a JSON file.

    Args:
        json_file_path (str): Path to the JSON file.
        property_hierarchy (list): List of properties (e.g., ['materialProperties', 'surfaceRoughness']).

    Returns:
        int: The line number where the property is located, or -1 if not found.
    """
    with open(json_file_path, "r") as file:
        lines = file.readlines()

        # Traverse the file line by line to match the hierarchical property
        for line_num, line in enumerate(lines):
            # Start by checking if the current line corresponds to the first property in the hierarchy
            if f'"{property_hierarchy[0]}"' in line:
                return recursive_search(property_hierarchy[1:], lines[line_num:], line_num + 1)

    return None  # If the property was not found
