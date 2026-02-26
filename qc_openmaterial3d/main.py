# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import argparse
import logging
import types

from qc_baselib import Configuration, Result, StatusType

from qc_openmaterial3d import constants
from qc_openmaterial3d.checks import xom_general_checker, xom_geo_checker
from qc_openmaterial3d.checks import utils, models

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def args_entrypoint() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ASAM OpenMATERIAL 3D Checker Bundle",
        description="This is a collection of scripts for checking validity of OpenMATERIAL 3D (.xoma, .xomm, .xomp, .xompt) files.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--config_path")

    parser.add_argument("-g", "--generate_markdown", action="store_true")

    return parser.parse_args()


def execute_checker(
    checker: types.ModuleType,
    checker_data: models.CheckerData,
    required_definition_setting: bool = True,
) -> None:
    # Register checker
    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        description=checker.CHECKER_DESCRIPTION,
    )

    # Register rule uid
    checker_data.result.register_rule_by_uid(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        rule_uid=checker.RULE_UID,
    )

    # Check preconditions. If not satisfied then set status as SKIPPED and return
    if not checker_data.result.all_checkers_completed_without_issue(
        checker.CHECKER_PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            checker.CHECKER_ID,
            "Preconditions are not satisfied. Skip the check.",
        )

        return

    # Checker definition setting. If not satisfied then set status as SKIPPED and return
    if required_definition_setting:
        schema_version = checker_data.schema_version

        splitted_rule_uid = checker.RULE_UID.split(":")
        if len(splitted_rule_uid) != 4:
            raise RuntimeError(f"Invalid rule uid: {checker.RULE_UID}")

        definition_setting = splitted_rule_uid[2]
        if (
            schema_version is None
            or utils.compare_versions(schema_version, definition_setting) < 0
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            checker_data.result.add_checker_summary(
                constants.BUNDLE_NAME,
                checker.CHECKER_ID,
                f"Version {schema_version} is lower than definition setting {definition_setting}. Skip the check.",
            )

            return

    # Execute checker
    try:
        checker.check_rule(checker_data)

        # If checker is not explicitly set as SKIPPED, then set it as COMPLETED
        if (
            checker_data.result.get_checker_status(checker.CHECKER_ID)
            != StatusType.SKIPPED
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.COMPLETED,
            )
    except Exception as e:
        # If any exception occurs during the check, set the status as ERROR
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.ERROR,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME, checker.CHECKER_ID, f"Error: {str(e)}."
        )

        logging.exception(f"An error occurred in {checker.CHECKER_ID}.")


def run_checks(config: Configuration, result: Result) -> None:
    checker_data = models.CheckerData(
        json_file_path=config.get_config_param("InputFile"),
        config=config,
        result=result,
        schema_version=None,
    )

    # 1. Run basic checks
    execute_checker(
        xom_general_checker.valid_json_document,
        checker_data,
        required_definition_setting=False,
    )

    execute_checker(
        xom_general_checker.version_is_defined,
        checker_data,
        required_definition_setting=False,
    )

    # Get schema version if file and version exist
    if result.all_checkers_completed_without_issue(
        {
            xom_general_checker.valid_json_document.CHECKER_ID,
            xom_general_checker.version_is_defined.CHECKER_ID,
        }
    ):
        checker_data.schema_version = utils.get_open_material_version(checker_data.json_file_path)

    # Run further xom:general checker
    execute_checker(xom_general_checker.valid_schema, checker_data)
    execute_checker(xom_general_checker.uris_exist, checker_data)

    # Run xom-geo:xoma checker
    execute_checker(xom_geo_checker.xoma_texture_assignment_requires_mapping, checker_data)

def main():
    args = args_entrypoint()

    logging.info("Initializing checks")


    config = Configuration()
    config.load_from_file(xml_file_path=args.config_path)

    result = Result()
    result.register_checker_bundle(
        name=constants.BUNDLE_NAME,
        description="OpenMATERIAL 3D Checker Bundle",
        version=constants.BUNDLE_VERSION,
        summary="",
    )
    result.set_result_version(version=constants.BUNDLE_VERSION)

    run_checks(config, result)

    result.copy_param_from_config(config)

    result.write_to_file(
        config.get_checker_bundle_param(
            checker_bundle_name=constants.BUNDLE_NAME, param_name="resultFile"
        ),
        generate_summary=True,
    )

    if args.generate_markdown:
        result.write_markdown_doc("generated_checker_bundle_doc.md")

    logging.info("Done")


if __name__ == "__main__":
    main()
