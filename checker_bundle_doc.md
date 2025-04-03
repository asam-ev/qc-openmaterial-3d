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

### check_asam.net:xom:1.0.0:xoma.material_textures_exist

* Description: Textures mapped to material names in the 'materialTextureAssignment' field of .xoma files shall exist.
* Addressed rules:
  * asam.net:xom:1.0.0:xoma.material_textures_exist
