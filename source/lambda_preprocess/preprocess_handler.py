import json
import boto3
from urllib.parse import urlparse
import math


def preprocess_handler(event, context):
    # TODO implement
    print(event)

    payload_uri = event["payload"]["s3Uri"]
    labelAttributeName = event["labelAttributeName"]
    bucket_name = urlparse(payload_uri).netloc
    key = urlparse(payload_uri).path.strip("/")

    s3 = boto3.resource('s3')
    payload_object = s3.Object(bucket_name, key)
    payload = payload_object.get()["Body"].read().decode('utf-8')

    print(payload)
    result = []

    for r in json.loads(payload):
        annotations_hit = {}
        valid_annotations = []

        # Annotations for various workers for the same record.. Pick the majority ones
        num_workers = len(r["annotations"])
        # threshold atleast 10% of the workers should have identified this
        threshold = math.ceil(num_workers * 10 / 100)

        for a in r["annotations"]:
            entities_annotations = json.loads(a["annotationData"]["content"])

            for start_index, token in json.loads(entities_annotations["entities"]).items():

                length = len(token)
                hit_key = "{}#{}".format(start_index, length)
                if hit_key not in annotations_hit: annotations_hit[hit_key] = 0

                annotations_hit[hit_key] += 1
                if annotations_hit[hit_key] == threshold:
                    valid_annotations.append({"start_index": start_index, "length": length, "token": token})

        result.append({
            "datasetObjectId": r["datasetObjectId"],
            "consolidatedAnnotation": {
                "content": {
                    labelAttributeName: {"entities": valid_annotations}
                }
            }
        })

    return result
