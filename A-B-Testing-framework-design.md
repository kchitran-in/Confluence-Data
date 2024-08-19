 **Overview** When new usability feature need to be launched or we need to re-vamp/change the current usability dramatically, we cannot go full fledged testing out the idea across the whole audience. To collect the data and feedback on such usability features, one can employ A/B testing. In this approach multiple ways of same feature are rendered to target audience, with intent of collecting feedback via user engagement. Example, we give 2 different button colors for Enroll, with target audience of teachers teaching in english medium school. We can capture the likelihood of Enroll button getting clicked vs the default audience. Such experiments are based on limited duration as well as a toggle to turn the experiment on/off for centralized control.



 **Design** Primarily design involves following considerations:


1. Defining the experiment & variants
1. Defining the audience selection criteria
1. Defining the user engagement criteria

 **Problem Statement 1: Need a way to store & retrieve the A/B testing experiments to be conducted** We can first define the experiment to be conducted, with following attributes


* id - unique identifier for experiment to be carried out
* purpose - defines with what target in mind the experiment is being carried out
* duration - start-date & end-date between which the experiment is applicable
* version - Deployment version for which this experiment should be enabled. It can have two variants, exact version or version range.
* toggle - a toggle to turn the experiment on/off

Each experiment can have random variants which we want to experiment together, this gives us freedom to test several ideas together.

 **Example** : "Green Enroll Button" or  "Blue Enroll Button" could be two variants


* variant id -
* variant-description - highlights, what distinguishes this variant from base component or other variants in the group.
* experiment-id - the experiment to which this variant belongs to.

For comparative study between the old and new component, we can define old component as one of the variants so that we can easily compare response to old component vs the new component.



 **Approach 1** : Data is stored based on version

 **Pros** 


* Flexibility to adapt new data with upcoming versions

 **Cons** 


* Need to handle version specific configurations in code.

 **DB design** 

experiment: (experiment_id, version, jsonConfig)

variants: (experiment_id, variant_id, jsonConfig)



 **Approach 2:**  Data is stored in pre-defined structure across versions

 **Pros** 


* Consistent data storage across versions, so no version specific code
* Data-type safety provided by database.

 **Cons** 


* Cannot have different configurations across versions
* Will have additional efforts in terms of database migrations



 **DB Design** 

 **Experiment** 



| Column name | Data-type | Description | 
|  --- |  --- |  --- | 
| id | uuid | unique-id | 
| identifier | string | unique identifier string | 
| description | string | describe the purpose of this experiment. | 
| start-date | date | experiment applicable from start of this date | 
| end-date | date | experiement expires at end of this date | 
| version | string | deployment version on which the experiment is applicable | 
| flag | bool | flag - which can be used to stop experiement regardless of other parameters | 





| Column name | Data-type | Description | 
|  --- |  --- |  --- | 
| id | uuid | unique-id | 
| identifier | string | unique-variant identifier string | 
| description | string | defines what this variant is for | 
| criteria | varchar | audience selection criteria - syntax will be declared in next section | 

 **API Defintion**  **POST /v1/api/abtest** 




```
URI: v1/abtest
Method: POST
Request body :
	{
		"request": {
			"identifier":"ab-test-1",
			"description":"Ab-test for new look-n-feel in view courses",
			"start-date" : "2019-01-01",
			"end-date" : "2019-01-31",
			"version" : "1.14",
		variants:[
			{
				"identifier":"ab-test-1-variant-1",
				"description": "for testing module of type1"
				"criteria": "audience selection criteria"
			},
			{
				"identifier":"ab-test-1-variant-1",
				"description": "for testing module of type1"
				"criteria": "audience selection criteria"
			}
		]
	}
Response body:
   {
    {
    "id": "api.abtest.create",
    "ver": "v1",
    "ts": "2018-11-21 08:55:04:708+0000",
    "params": {
        "resmsgid": null,
        "msgid": "8e27cbf5-e299-43b0-bca7-8347f7e5abcf",
        "err": null,
        "status": "success",
        "errmsg": null
    },
    "responseCode": "OK",
    "result": {
      //Will contain the created configuration along with uuid
         }
  }
```



```
URI: v1/abtest/:abtestid
Method: PUT
Request body :
	{
		"request": {
			"identifier":"ab-test-1",
			"description":"Ab-test for new look-n-feel in view courses",
			"start-date" : "2019-01-01",
			"end-date" : "2019-01-31",
			"version" : "1.14"
		}
		variants:[
			"add": [
				{
				"identifier":"ab-test-1-variant-1",
				"description": "for testing module of type1"
				"criteria": "audience selection criteria"
				}
			],
			"remove: [
				{
				"identifier":"ab-test-1-variant-1",
				"description": "for testing module of type1"
				"criteria": "audience selection criteria"
				}
			]
		]
	}
Response body:
{
{
"id": "api.abtest.update",
"ver": "v1",
"ts": "2018-11-21 08:55:04:708+0000",
"params": {
"resmsgid": null,
"msgid": "8e27cbf5-e299-43b0-bca7-8347f7e5abcf",
"err": null,
"status": "success",
"errmsg": null
},
"responseCode": "OK",
"result": {
}
}
```



```
URI: v1/abtest/:abtestid
Method: DELETE
Request body :
Response body:
{
{
"id": "api.abtest.delete",
"ver": "v1",
"ts": "2018-11-21 08:55:04:708+0000",
"params": {
"resmsgid": null,
"msgid": "8e27cbf5-e299-43b0-bca7-8347f7e5abcf",
"err": null,
"status": "success",
"errmsg": null
},
"responseCode": "OK",
"result": {
}
}



```



```
URI: v1/abtest/:abtestid
Method: DELETE
Request body :

Response body:
{
{
"id": "api.abtest.update",
"ver": "v1",
"ts": "2018-11-21 08:55:04:708+0000",
"params": {
"resmsgid": null,
"msgid": "8e27cbf5-e299-43b0-bca7-8347f7e5abcf",
"err": null,
"status": "success",
"errmsg": null
},
"responseCode": "OK",
"result": {
"identifier":"ab-test-1",
"description":"Ab-test for new look-n-feel in view courses",
"start-date" : "2019-01-01",
"end-date" : "2019-01-31",
"version" : "1.14",
variants:[
{
"identifier":"ab-test-1-variant-1",
"description": "for testing module of type1"
"criteria": "audience selection criteria"
},
{
"identifier":"ab-test-1-variant-1",
"description": "for testing module of type1"
"criteria": "audience selection criteria"
}
]
}
}

```
 **Problem Statement 2: How to select and execute A/B tests on devices based on some criteria** As experiment cannot be run across all the users, we need a way to restrict for which audience the A/B tests get loaded for evaluation purposes.

Need to evaluate different criteria on which we can pick the audience for experiment:


* Usage - users who have used app at least for a month, or only fresh users.
* User attributes - State/District user belongs to, Gender, Age, Geo-location co-ordinates etc.
* Device profile - type of device/screen-size, os-type, browser-type etc.



 **Example configuration could be as follows per variant:** 

 **Approach 1** : Simple configuration

Fetch the data from device database, and evaluate the simple criteria against the given data.

 **Sample syntax:** 

device = \["android","iOs"]&firstAccessed>"2018-09-01"

 **Pros:** 


* Simple to implement
* No i/o calls involved

 **Cons:** 


* Limited support, lacks flexibility.  

    

    

 **Approach 2** : Generic configuration

Support generic query structure based on elastic-search


```js
````
{
  "and": {
    "device": {
      "eq": "android"
    },
    "or": {
      "firstAccessed": {
        "gt": "2018-09-01 00:00:00"
      },
      "lastAccessed": {
        "gt": "2019-01-30 00:00:00"
      }
    }
  }
}

````
```
 **Pros:** 


* Easy to implement 
* Ability to evaluate complex scenarios

 **Cons:** 


* Would involve call for storage and evaluation which are I/O calls

Leveraging elastic search for evaluation of query, by inserting the available data on elastic-search index.





We could come up with simple criteria definitions, based on criteria we support, once we finalise, to simplify the syntax.

Above syntax can take care of all combinations and all search types.

 **Approach to decide whether to load experiment on device**  **Approach 1:**  Use the local data, and local data available with experiment as part of the code.

 **Pros:** 


* No API calls required, which makes this approach faster.

 **Cons:** 


* Only feasible for supporting selection criteria, which are local to device or user-profile. e.g. device-type, user-profile data like state/district (which is as such available data)
* Cannot support global flag like turning the experiment off regardless of other factors.
* All data like duration of experiment etc, need to be stored statically.



 **Approach 2:**  API which flags off, whether experiment need to be loaded on the device.

 **Definition** :

POST /api/v1/abtest




```
{
"request" :
{ 
"deviceid" :"device-id",
"device-type" : "mobile/portal",
"version":
}
}
```
 **Responses:** If experiment flag is on & current time is within experiment duration & user or device-id meets configured experiment criteria.




```
{
    {
    "id": "api.abtest",
    "ver": "v1",
    "ts": "2018-11-21 08:55:04:708+0000",
    "params": {
        "resmsgid": null,
        "msgid": "8e27cbf5-e299-43b0-bca7-8347f7e5abcf",
        "err": null,
        "status": "success",
        "errmsg": null
    },
    "responseCode": "OK",
    "result": [
			{
			    "experiment-id": "exp-id",
			    "variant": "variant-id"
			},
			{
				"experiment-id": "exp-id", 
				"variant": "variant-id"
			}
		]
  }
```
 **404  - Not Found** 

If device id not found.



 **Pros:** 


* Can support more selection criteria.
* Can support global flagging
* Storage of history of all experiments conducted will be maintained in database for reference

 **Cons:** 


* Requires API access, which would make this slower

 **Problem Statement 3: Collecting the data for results** Once selection criteria is setup new UI will get loaded only for the selected audience.

Now we need to capture the effectiveness of the component usage, it depends on definition of user-engagement and experiment under progress.

 **Telemetry data collection** 


```
{
  "eid":"IMPRESSION",
  ...
  "context":{
     "channel":"b00bc992ef25f1a9a8d63291e20efc8d",
     "cdata": 
		[ 
			{
				"type": "A/B Test",
				"id": "<experiment-id>"
			},
			{
				"type": "A/B Test Variant",
				"id": "<variant-id>"
			}
		],
	},
     "rollup":{
        "l1":"ORG_001"
     },
     "uid":"781c21fc-5054-4ee0-9a02-fbb1006a4fdd"
  },
  "object":{ },
  "tags":[
     "ORG_001"
  ],
  "edata":{
     "id":"library tab",
     "type":"view",
     "pageid":"resources"
  }
}
```


 **Overall flow** 
* Admin configure the experiment and variants within back-end.
* Each variant will have selection criteria, for default or other users the criteria will be kept empty.
* Now UI components will have meta-data like experiment-id and associated variant-id with it.
* By default variants' are off and on call of API, it will be determined, based on given device-id and user :
    * If experiment need to be loaded
    * and which variant needs to be loaded

    
* Now impressions and interactions will be recorded based on UI events.
* One can analyze based on collected events data such as ratio of impressions vs interactions for different variants





*****

[[category.storage-team]] 
[[category.confluence]] 
