# BIM2TWIN - WP3 integration with ThingIn platform

This repository contains the first version of the integration between Work Package Three (WP3) and the Digital Twin
Platform (DTP).
The purpose of this document is to explain the code and its usage.

## Setting up the environment

The integration code has been written in python, and the environment has been set up using conda.

In order to re-create the provided conda environment it is sufficient to run:

```conda env create -n DTP_V1 python=3.9```

after this step the environment can be activated and install packages by:

```
conda activate DTP_V1
pip install -r requirements.txt
```

Once the conda environment is set up and activated, we are ready to run the code.

## Running the code

The integration program can be run via:

```python executer.py -w <work_dir> -x DTP_config.xml -p tests\dummy_GA_PCD.ply```

The arguments taken by the ```executer.py``` are as follows:

* `-h` : this argument, when provided, makes `executer.py` print the help information,
* `-w` : the path to the working folder, in which the program will create, if necessary, folders such as `download` used
  for storing data from DTP; `tmp` used for storing temporary files,
* `-x` : the path to an XML file with the configuration. See the corresponding section,
* `-p` : the path to the LiDAR data in the PLY file format,
* `-s` : a flag (no argument), which if given enables the simulation mode that allows running the program without
  changing the database,
* `-r` : the path to a valid database session log. If provided, the last session described in the log will be reverted.

## Data flow and the architecture chart

![Data flow chart and the architecture](./doc/img/data-chart-applications.png)

## Logged information

Currently, the program is using two logs: the general log stored in `DTP_WP3.log`, and the second `db_session.log`, used
for storing information about database changing queries. The second log can be used to revert changes done on the
database. In order to revert to the last session, it is necessary to call the program with the argument `-r` followed by
the path to the file. In principle, the database can also be restored from the general log file, but this option has not
been sufficiently tested.

**Note that, the general log file `DTP_WP3.log`, contains also raw HTTP requests, together with the authentication
token.**

### Example of the general log file

```
9-Oct-22 15:57:34 : INFO : New session has been started.
09-Oct-22 15:57:34 : INFO : Work folder set to: C:\Users\kpluta\Projects\BIM2TWIN-WP3\DTP\integration_v1
09-Oct-22 15:57:34 : INFO : XML config set to: C:\Users\kpluta\Projects\BIM2TWIN-WP3\DTP\integration_v1\DTP_config.xml
09-Oct-22 15:57:34 : INFO : PCD set to: C:\Users\kpluta\Projects\BIM2TWIN-WP3\DTP\integration_v1\tests\dummy_GA_PCD.ply
09-Oct-22 15:57:34 : INFO : Running in the simulator mode.
09-Oct-22 15:57:34 : INFO : DTP_API - START SESSION
09-Oct-22 15:57:34 : INFO : HTTP request: 
-----------START-----------
POST https://api.thinginthefuture.bim2twin.eu/avatars/find

Content-Type: application/json

Accept: application/json

Authorization: Bearer <token_removed>

Content-Length: 170


{
   "query":{
      "$domain":"http://bim2twin.eu/general_assembly_wp3/",
      "$classes":"https://w3id.org/bot#Element",
      "https://www.bim2twin.eu/ontology/Core#isAsDesigned":true
   }
}
-----------END-----------
09-Oct-22 15:57:34 : DEBUG : Starting new HTTPS connection (1): api.thinginthefuture.bim2twin.eu:443
09-Oct-22 15:57:34 : DEBUG : https://api.thinginthefuture.bim2twin.eu:443 "POST /avatars/find HTTP/1.1" 308 284
09-Oct-22 15:57:34 : DEBUG : https://api.thinginthefuture.bim2twin.eu:443 "POST /avatars/find/ HTTP/1.1" 200 2227
09-Oct-22 15:57:34 : INFO : Response code: 200
```

### Example of the db session log file

```
10-Oct-22 13:49:01 : DTP_API - START SESSION
10-Oct-22 13:49:12 : DTP_API - NEW_ELEMENT_IRI: http://bim2twin.eu/general_assembly_wp3/asbuiltelement0021
10-Oct-22 13:49:13 : DTP_API - NEW_BLOB: ad6f0631-6c01-4aa6-a62a-600e9be1f087
10-Oct-22 13:49:13 : DTP_API - NEW_LINK_ELEMENT_BLOB: 4a93f8c6-9a51-5682-b787-94de731965eb, ad6f0631-6c01-4aa6-a62a-600e9be1f087
10-Oct-22 13:49:35 : DTP_API - END SESSION
```

## Control via XML

Below is an example of ax XML used to generalize the integration and push certain information from the code to the
external configuration file to make the implementation general and easy to maintain.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DTP_config>
    <NAME>ThingIn</NAME>
    <VERSION>1.2</VERSION>
    <DEV_TOKEN type="xs:anyURI">C:\Users\kpluta\Projects\BIM2TWIN-WP3\DTP\integration_v1\token_kpluta.txt</DEV_TOKEN>
    <DTP_DOMAIN type="xs:anyURI">http://bim2twin.eu/mislata_building_and_processes/</DTP_DOMAIN>
    <API_URIS>
        <URI function="get_find_elements" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/avatars/find</URI>
        <URI function="add_node" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/batch/avatars</URI>
        <URI function="count_nodes" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/avatars/count</URI>
        <URI function="get_blobs_per_element" type="xs:anyURI">
            https://api.thinginthefuture.bim2twin.eu/avatars/_ID_/blobs
        </URI>
        <URI function="delete_avatar" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/avatars/_ID_</URI>
        <URI function="download_blob" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/blobs/_ID_/download
        </URI>
        <URI function="send_blob" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/blobs</URI>
        <URI function="delete_blob" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/blobs/_ID_</URI>
        <URI function="link_blob" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/blobs/link</URI>
        <URI function="unlink_blob" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/blobs/unlink</URI>
        <URI function="update_set" type="xs:anyURI">https://api.thinginthefuture.bim2twin.eu/batch/avatars/update/set
        </URI>
    </API_URIS>
    <ONTOLOGY_URIS>
        <URI function="isAsDesigned" type="xs:anyURI">https://www.bim2twin.eu/ontology/Core#isAsDesigned</URI>
        <URI function="progress" type="xs:anyURI">https://www.bim2twin.eu/ontology/Core#progress</URI>
        <URI function="timeStamp" type="xs:anyURI">https://www.bim2twin.eu/ontology/Core#timeStamp</URI>
        <URI function="id" type="xs:anyURI">https://www.bim2twin.eu/ontology/Core#id</URI>
        <URI function="hasElementType" type="xs:anyURI">https://www.bim2twin.eu/ontology/Core#hasElementType</URI>
        <URI function="hasGeometryStatusType" type="xs:anyURI">
            https://www.bim2twin.eu/ontology/Core#hasGeometryStatusType
        </URI>
        <URI function="CompletelyDetected" type="xs:anyURI">https://www.bim2twin.eu/ontology/Core#CompletelyDetected
        </URI>
        <URI function="intentStatusRelation" type="xs:anyURI">
            https://www.bim2twin.eu/ontology/Core#intentStatusRelation
        </URI>
        <URI function="hasDefectType" type="xs:anyURI">https://www.bim2twin.eu/ontology/CoreExtension#hasDefectType
        </URI>
        <URI function="defect_criticality" type="xs:anyURI">https://www.bim2twin.eu/ontology/CoreExtension#criticality
        </URI>
        <URI function="defect_class_volumetric" type="xs:anyURI">
            https://www.bim2twin.eu/ontology/CoreExtension#VolumetricDefect
        </URI>
        <URI function="hasGeometricDefect" type="xs:anyURI">
            https://www.bim2twin.eu/ontology/CoreExtension#hasGeometricDefect
        </URI>
        <URI function="GeometricDefect" type="xs:anyURI">
            https://www.bim2twin.eu/ontology/CoreExtension#GeometricDefect
        </URI>
        <URI function="PositionDefect" type="xs:anyURI">https://www.bim2twin.eu/ontology/CoreExtension#PositionDefect
        </URI>
    </ONTOLOGY_URIS>
    <OBJECT_TYPES>
        <OBJECT_TYPE field="https://www.bim2twin.eu/ontology/Core#hasElementType">
            https://www.bim2twin.eu/ontology/Core#Wall
        </OBJECT_TYPE>
        <OBJECT_TYPE field="ifc:Class">IfcWall</OBJECT_TYPE>
        <OBJECT_TYPE field="ifc:Class">IfcWallStandardCase</OBJECT_TYPE>
        <OBJECT_TYPE field="ifc:Class">IfcColumn</OBJECT_TYPE>
    </OBJECT_TYPES>
    <OBJECT_TYPE_CONVERSIONS>
        <CONVERSION from="IfcWall" to="https://www.bim2twin.eu/ontology/Core#Wall"/>
        <CONVERSION from="IfcWallStandardCase" to="https://www.bim2twin.eu/ontology/Core#Wall"/>
        <CONVERSION from="IfcColumn" to="https://www.bim2twin.eu/ontology/Core#Column"/>
    </OBJECT_TYPE_CONVERSIONS>
    <METHODS>
        <METHOD>
            <NAME>mesh2pcd</NAME>
            <EXE input_file_types="ply" output_file_types="ply" Windows="mesh2pcd.exe"/>
            <PATH type="xs:anyURI">C:\Users\kpluta\Projects\BIM2TWIN-WP3\DTP\bin</PATH>
            <PARAMS>
                <INPUT type="xs:string" arg="-i">external</INPUT>
                <OUTPUT type="xs:string" arg="-o">external</OUTPUT>
                <SAMPLING_DENSITY type="xs:float" arg="-d">1000</SAMPLING_DENSITY>
            </PARAMS>
        </METHOD>
        <METHOD>
            <NAME>presence</NAME>
            <EXE input_file_types="ply" output_file_types="csv" Windows="presence.exe"/>
            <PATH type="xs:anyURI">C:\Users\kpluta\Projects\BIM2TWIN-WP3\DTP\bin</PATH>
            <PARAMS>
                <INPUT type="xs:string" arg="-i">external</INPUT>
                <INPUT_MODEL type="xs:string" arg="-I">external</INPUT_MODEL>
                <CLUSTER type="xs:string" arg="-l">external</CLUSTER>
                <SINGLE_MODE_FLAG type="xs:flag" arg="-S"/>
            </PARAMS>
        </METHOD>
    </METHODS>
    <KPIS>
        <KPI indicator_type="defect">
            <OBJECT_CLASSES>
                <CLASS name="IfcColumn"/>
                <CLASS name="https://www.bim2twin.eu/ontology/Core#Column"/>
            </OBJECT_CLASSES>
            <DEFECT type="displacement" computation_strategy="as_designed-vs-as_built"/>
            <VALUE_RANGE_MAPS>
                <RANGE lower_bound="0" upper_bound="0.05" type="good"/>
                <RANGE lower_bound="0.05" upper_bound="0.15" type="acceptable"/>
                <RANGE lower_bound="0.15" upper_bound="infinity" type="unacceptable"/>
            </VALUE_RANGE_MAPS>
        </KPI>
    </KPIS>
</DTP_config>
```

### The below list explains the tags:

* `DTP_config`: the root of the XML configuration,
* `NAME`: name given to the configuration, for example, the name of the platform,
* `VERSION` : version of the configuration file,
* `DEV_TOKEN` : the path to the file, which contains the developer token needed for the authentication,
* `DTP_DOMAIN` : the domain used for the session,
* `API_URIS` : a list of API uri calls that are then mapped by the program,
    * `URI` :  nested tag representing an API uri, which has the following attributes,
        * `function` : the name used to map the API URI to its function,
        * `type` : for now only `xs:anyURI`,
* `ONTOLOGY_URIS` : a list of ontology uris mapped by the program
    * `URI` :  nested tag representing an ontology uri, which has the following attributes,
        * `function` : the name used to map the ontology URI to its function,
        * `type` : for now only `xs:anyURI`,
* `OBJECT_TYPES` : a list of recognized types of objects used to filter elements of interest,
    * `OBJECT_TYPE` : nested tag representing an object type,
        * `field` : an attribute that describes the field under which the object type is stored (DTP related),
* `OBJECT_TYPE_CONVERSIONS` : a list of defined object types' conversions,
  * `CONVERSION` : a tag which attributes `from` and `to` define the type conversion,
* `METHODS` : a list of methods mapped by the program,
    * `METHOD` : the main tag describing a method used in the code (external program called by the integration code),
    * `NAME` : method name used to map the method with the corresponding executable file,
    * `EXE` : the tag used to describe the available executable files,
        * `filetype` : a list of supported file formats (both input output),
        * `Windows, Linux, Darwin` : name of the executable file for Windows, Linux, and macOS,
    * `PATH` : the path to the folder containing the executable files,
    * `PARAMS` : a list of parameters which names are currently used provided, nevertheless each entry on the list needs
      to provide:
        * `type` : supported types
          are: `xs:string`, `xs:positiveInteger`, `xs:integer`, `xs:float`, `xs:double`, `xs:boolean`, and `xs:flag`. If
          any other type is provided, then it will not be handled by the CMD_Builder class,
        * `arg` : attributes passed to the program e.g., -i. Finally, the value between the closing and opening tags is
          the argument's value. **Note that if `external` is provided as a value, then this value is assumed to be
          computed by the program, and it has to be properly mapped in the function calling CMD_Builder.execute(). For
          an example see: `INT_WP3_API.mesh2PCD(CMD_BUILDER, mesh_path, DIRS)`**,
* `KPIS` : a list of KPIs mapped by the program,
    * `KPI` : the main tag describing a KPI,
        * `indicator_type` : attribute which contains the information about the type of KPI, e.g., 'defect',
        * `OBJECT_CLASSES` : a list of classes (e.g., ifcColumn), which are considered by the KPI,
            * `CLASS` : descriptor of the class considered by the KPI the name of the class has to be given in the
              attribute `name`,
        * `DEFECT` : if a KPI is a 'defect', then this tag needs to be added with two attributes: `type` e.g., '
          displacement';  `computation_strategy`, which indicates how the defect is computed.
        * `VALUE_RANGE_MAPS` : list of ranges that define the criticality of the KPI, e.g., for a defect it will
          describe the criticality,
            * `RANGE` : range of the KPI which contains three attributes: `lower_bound`; `upper_bound`, and `type`.

## Code structure

* `executer.py` : the main entry point
    * `DTP_API.py` : implementation of the DTP's API calls
    * `INT_WP3_API.py` : implementation of the support code used to interact with the external methods and providing a
      bridge between the DTP's API and the WP3 methods
    * `DTP_config.py` : class which maps the XML configuration and is the primary source of information shared in the
      other parts of the code
    * `CMD_builder.py` : class which maps the external methods described by the XML and provides a way to execute them
      within the python code
    * `KPI_computer.py` : class which implements the logic responsible for computing KPIs
    * `KPIs.py` : contains classes which implement different KPIs
    * `Disparity_computer.py` : class which computes disparities between As-Designed and As-Built data
    * `helpers.py` : some function shared across the project
