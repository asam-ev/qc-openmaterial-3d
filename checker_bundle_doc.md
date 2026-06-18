# Checker bundle: xomBundle

* Build version:  v1.0.0
* Description:    OpenMATERIAL 3D Checker Bundle

## Parameters

* InputFile 
* resultFile 

## Checkers

### check_asam.net:xom:1.0.0:general.valid_json_document

* Description: The given file to check must be a valid JSON document.
* Addressed rules:
  * asam.net:xom:1.0.0:general.valid_json_document

### check_asam.net:xom:1.0.0:general.version_is_defined

* Description: The metadata of the file must contain an openMaterial3dVersion field.
* Addressed rules:
  * asam.net:xom:1.0.0:general.version_is_defined

### check_asam.net:xom:1.0.0:general.valid_schema

* Description: Input JSON file must be valid according to the corresponding schema.
* Addressed rules:
  * asam.net:xom:1.0.0:general.valid_schema

### check_asam.net:xom:1.0.0:general.uris_exist

* Description: If a URI property to other file is set in a JSON file, the file linked in that property shall exist.
* Addressed rules:
  * asam.net:xom:1.0.0:general.uris_exist

### check_asam.net:xomgeo:1.0.0:xoma.vehicle_class_data_defined

* Description: If an asset is of type 'vehicle', the property 'vehicleClassData' must be set in the metadata.
* Addressed rules:
  * asam.net:xomgeo:1.0.0:xoma.vehicle_class_data_defined

### check_asam.net:xomgeo:1.0.0:xoma.human_class_data_defined

* Description: If an asset is of type 'human', the property 'humanClassData' must be set in the metadata.
* Addressed rules:
  * asam.net:xomgeo:1.0.0:xoma.human_class_data_defined

### check_asam.net:xommat:1.0.0:xompt.tables_sorted_correctly

* Description: Arrays in look-up tables shall be sorted based on the columns starting with the first.
* Addressed rules:
  * asam.net:xommat:1.0.0:xompt.tables_sorted_correctly

### check_asam.net:xommat:1.0.0:xomp.look_up_tables_unique_wavelengths

* Description: Look-up tables referenced in a .xomp file should not have overlapping wavelength ranges.
* Addressed rules:
  * asam.net:xommat:1.0.0:xomp.look_up_tables_unique_wavelengths