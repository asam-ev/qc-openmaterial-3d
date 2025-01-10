# Checker bundle: openMaterialBundle

* Build version:  v0.0.0
* Description:    OpenMATRERIAL 3D checker bundle

## Parameters

* InputFile
* resultFile

## Checkers

### check_asam_openmaterial_valid_json_document

* Description: The given file to check must be a valid JSON document.
* Addressed rules:
  * asam.net:openmaterial:1.0.0:json.valid_json_document

### check_asam_openmaterial_version_is_defined

* Description: The metadata of the file must contain an openMaterialVersion field.
* Addressed rules:
  * asam.net:openmaterial:1.0.0:json.version_is_defined

### check_asam_openmaterial_valid_schema

* Description: Input JSON file must be valid according to the corresponding schema.
* Addressed rules:
  * asam.net:openmaterial:1.0.0:json.valid_schema
