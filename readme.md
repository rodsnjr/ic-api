# IC API

Image Catalog API.

## Event Examples

<!--
TODO -Traduzir isso pro Inglês
--> 

Given two images, and a catalog filter for red, an green cars in a **parking lot** (this will have to be a parent node)
The API will generate events in a pipeline action (other services will chain new events).

The request will be like:

```json
{
    "id": "102938102938102938",
    "images": [
        {
            "id": "10938103891",
            "image_key": "parking_lot_1.jpg"
        },
        {  
            "id": "1209381028931290",
            "image_key": "random_image_2.jpg" 
        }
    ],
    "scenes" : [{
      "uid": "194",
      "labels": ["Parking Lot"]
    }],
    "detections" : [{
      "uid": "195",
      "labels": ["Car"],
      "depends_on": "194"
    }],
    "colors": [
        {
          "uid": "196",
          "color": "Red",
          "depends_on": "195"
        },
        {
          "uid": "197",
          "color": "Green",
          "depends_on": "195"
        }
    ]
}
```

The generated events will be:

```json
[
    {
        "uid": "09129078",
        "catalog_id": "102938102938102938",
        "image_key": "parking_lot_1.jpg",
        "subject": "SCENE_RECOGNITION",
        "filters": ["Parking Lot"],
        "children": [{
          "uid": "195",
          "subject": "OBJECT_DETECTION",
          "filters": ["Car"],
          "children": [
              {
                "uid": "196",
                "subject": "COLOR_RECOGNITION",
                "filters": ["Red"]
              },
              {
                "uid": "197",
                "subject": "COLOR_RECOGNITION",
                "filters": ["Green"]
              }
          ]
        }]
    }, 
    {
        "uid": "13098139",
        "catalog_id": "102938102938102938",
        "image_key": "random_image_2.jpg",
        "subject": "SCENE_RECOGNITION",
        "filters": ["Parking Lot"],
        "children": [
              {
                "uid": "196",
                "subject": "COLOR_RECOGNITION",
                "filter": ["Red"]
              },
              {
                "uid": "197",
                "subject": "COLOR_RECOGNITION",
                "filter": ["Green"]
              }
          ]
        }]
    }
]
```

The AI Service will then chain one new event for the positive filter.
 
```json
[
    {
        "uid": "29083102938",
        "catalog_id": "102938102938102938",
        "image_key": "parking_lot_1.jpg",
        "subjects": "OBJECT_DETECTION",
        "filters": ["Car"],
        "children": [
              {
                "uid": "196",
                "subject": "COLOR_RECOGNITION",
                "filters": ["Red"]
              },
              {
                "uid": "197",
                "subject": "COLOR_RECOGNITION",
                "filters": ["Green"]
              }
        ]
    }
]
```

Then the service will chain for each car in the picture a new event for the given task.
And also this event might be specialized and will contain specific metadata (such as object positions).
Let's say there are two cars in the picture, the next event will be:

```json
[
    {
        "uid": "019381908319038",
        "catalog_id": "102938102938102938",
        "image_key": "parking_lot_1.jpg",
        "subjects": "COLOR_RECOGNITION",
        "filters": ["Red"],
        "metadata": {
          "object": {
            "x": "223",
            "y": "255",
            "w": "100",
            "h": "250"
          }
        }
    },
    { 
        "uid": "8967464568735489",
        "catalog_id": "102938102938102938",
	    "image_key": "parking_lot_1.jpg",
	    "subjects": ["COLOR_RECOGNITION"],
	    "filters": ["Red"],
        "metadata": {
          "object": {
            "x": "430",
            "y": "380",
            "w": "225",
            "h": "365"
          }
        }
    },
    {
        "uid": "8435498431894351894",
        "catalog_id": "102938102938102938",
        "image_key": "parking_lot_1.jpg",
        "subjects": "COLOR_RECOGNITION",
        "filters": ["Green"],
        "metadata": {
          "object": {
            "x": "223",
            "y": "255",
            "w": "100",
            "h": "250"
          }
        }
    },
    { 
        "uid": "6846543219684321918987",
        "catalog_id": "102938102938102938",
	    "image_key": "parking_lot_1.jpg",
	    "subjects": ["COLOR_RECOGNITION"],
	    "filters": ["Green"],
        "metadata": {
          "object": {
            "x": "430",
            "y": "380",
            "w": "225",
            "h": "365"
          }
        }
    }
]
```

Lastly this service will chain the result event.
**TODO**