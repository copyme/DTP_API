# BIM2TWIN - Itegration with ThingIn platform

This repository contains the first version of the integration between python written code and the Digital Twin
Platform (DTP), i.e., Thing'in.
The purpose of this document is to explain the code and its usage.

The code was extracted from the internal code of WP3.

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

## Code structure
* `DTP_API.py` : implementation of the DTP's API calls
* `DTP_config.py` : class which maps the XML configuration and is the primary source of information shared in the
   other parts of the code
* `helpers.py` : some function shared across the project


## How to start

Please see the folder named `examples` and there file therein.
