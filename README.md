# asam-qc-openmaterial

This repository provides a [Checker Bundle](checker_bundle_doc.md) designed for the [ASAM Quality Checker Framework](https://github.com/asam-ev/qc-framework).
It tests ASAM OpenMATERIAL 3D files for conformity with the standard.

- [asam-qc-openmaterial](#asam-qc-openmaterial)
  - [Installation and usage](#installation-and-usage)
    - [Installation using pip](#installation-using-pip)
    - [Installation from source](#installation-from-source)
    - [Example output](#example-output)
  - [Register Checker Bundle to ASAM Quality Checker Framework](#register-checker-bundle-to-asam-quality-checker-framework)
    - [Linux Manifest Template](#linux-manifest-template)
    - [Windows Manifest Template](#windows-manifest-template)
    - [Example Configuration File](#example-configuration-file)
  - [Tests](#tests)
  - [Contributing](#contributing)


## Installation and usage

asam-qc-openmaterial can be installed using pip or from source.

### Installation using pip

asam-qc-openmaterial can be installed using pip.

**From a local repository**

```bash
git clone https://github.com/Persival-GmbH/qc-openmaterial.git
pip install ./qc-openmaterial
```

To run the application:

```bash
qc_openmaterial --help
usage: QC OpenMATERIAL 3D Checker [-h] (-d | -c CONFIG_PATH)
This is a collection of scripts for checking validity of OpenMATERIAL 3D (.xoma, .xomm, .xomp, .xompt) files.
options:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config_path CONFIG_PATH
```

The following commands are equivalent:

```bash
qc_openmaterial --help
python qc_openmaterial/main.py --help
python -m qc_openmaterial.main --help
```

### Installation using poetry

After cloning the repository, install the project using [Poetry](https://python-poetry.org/).

```bash
poetry install
```

After installing from source, the usage are similar to above.

```bash
poetry shell
qc_openmaterial --help
python qc_openmaterial/main.py --help
python -m qc_openmaterial.main --help
```

### Example output

```bash
python qc_openmaterial/main.py -c example_config.xml

2025-01-10 14:43:13,238 - Initializing checks
2025-01-10 14:43:13,246 - Executing valid_json_document check
2025-01-10 14:43:13,247 - Done

```

## Register Checker Bundle to ASAM Quality Checker Framework

Manifest file templates are provided in the [manifest_templates](manifest_templates/) folder to register the ASAM OpenMATERIAL 3D Checker Bundle with the [ASAM Quality Checker Framework](https://github.com/asam-ev/qc-framework/tree/main).

### Linux Manifest Template

To register this Checker Bundle in Linux, use the [linux_openmaterial_manifest.json](manifest_templates/linux_openmaterial_manifest.json) template file.

If the asam-qc-openmaterial is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": ". <venv>/bin/activate && cd $ASAM_QC_FRAMEWORK_WORKING_DIR && qc_openmaterial -c $ASAM_QC_FRAMEWORK_CONFIG_FILE"
```

Replace `<venv>/bin/activate` by the path to your virtual environment.

### Windows Manifest Template

To register this Checker Bundle in Windows, use the [windows_openmaterial_manifest.json](manifest_templates/windows_openmaterial_manifest.json) template file.

If the asam-qc-openmaterial is installed in a virtual environment, the `exec_command` needs to be adjusted as follows:

```json
"exec_command": "C:\\> <venv>\\Scripts\\activate.bat && cd %ASAM_QC_FRAMEWORK_WORKING_DIR% && qc_openmaterial -c %ASAM_QC_FRAMEWORK_CONFIG_FILE%"
```

Replace `C:\\> <venv>\\Scripts\\activate.bat` by the path to your virtual environment.

### Example Configuration File

An example configuration file for using this Checker Bundle within the ASAM Quality Checker Framework is as follows.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Config>

    <Param name="InputFile" value="my_openmaterial_asset_file.xoma" />

    <CheckerBundle application="openMaterialBundle">
        <Param name="resultFile" value="openmaterial_bundle_report.xqar" />
        <Checker checkerId="check_asam_openmaterial_valid_json_document" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_openmaterial_version_is_defined" maxLevel="1" minLevel="3" />
        <Checker checkerId="check_asam_openmaterial_valid_schema" maxLevel="1" minLevel="3" />
    </CheckerBundle>

    <ReportModule application="TextReport">
        <Param name="strInputFile" value="Result.xqar" />
        <Param name="strReportFile" value="Report.txt" />
    </ReportModule>

</Config>
```

## Tests

To run the tests, you need to install the extra test dependency after installing from source.

```bash
poetry install --with dev
```

To execute tests

```bash
python -m pytest -vv
```

or

```bash
poetry run pytest -vv
```

They should output something similar to:

```
===================== test session starts =====================
platform linux -- Python 3.11.9, pytest-8.2.2, pluggy-1.5.0
```

You can check more options for pytest at its [own documentation](https://docs.pytest.org/).

## Contributing

For contributing, you need to install the development requirements besides the
test and installation requirements, for that run:

```bash
poetry install --with dev
```

You need to have pre-commit installed and install the hooks:

```
pre-commit install
```

**To implement a new checker**

1. Create a new Python module for each checker.
2. Specify the following global variables for the Python module

| Variable | Meaning |
| --- | --- |
| `CHECKER_ID` | The ID of the checker |
| `CHECKER_DESCRIPTION` | The description of the checker |
| `CHECKER_PRECONDITIONS` | A set of other checkers in which if any of them raise an issue, the current checker will be skipped |
| `RULE_UID` | The rule UID of the rule that the checker will check |

3. Implement the checker logic in the following function:

```python
def check_rule(checker_data: models.CheckerData) -> None:
    pass
```

1. Register the checker module in the following function in [main.py](qc_openmaterial/main.py).

```python
def run_checks(config: Configuration, result: Result) -> None:
    ...
    # Add the following line to register your checker module
    execute_checker(your_checker_module, checker_data)
    ...
```

All the checkers in this checker bundle are implemented in this way. Take a look at some of them before implementing your first checker.
