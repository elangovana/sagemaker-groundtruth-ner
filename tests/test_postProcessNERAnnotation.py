import json
from io import StringIO, BytesIO
from unittest import TestCase
from unittest.mock import Mock

from postprocess_handler import PostProcessNERAnnotation


class TestPostProcessNERAnnotation(TestCase):

    def test_post_process(self):
        # Arrange
        sut = PostProcessNERAnnotation()

        event = {"version": "2018-10-06",
                 "labelingJobArn": "arn:aws:sagemaker:us-east-2:111:labeling-job/entityrecognition-protienname",
                 "payload": {
                     "s3Uri": "s3://mybucket/output/EntityRecognition-ProtienName/annotations/consolidated-annotation/consolidation-request/iteration-1/2018-12-20_11:42:13.json"},
                 "labelAttributeName": "EntityRecognition-ProtienName",
                 "roleArn": "arn:aws:iam::324346001917:role/Sagemaker",
                 "outputConfig": "s3://mybucket/output/EntityRecognition-ProtienName/annotations"}

        payload = [
            {
                "datasetObjectId": "21277",
                "dataObject": {
                    "content": "24525236"
                },
                "annotations": [
                    {
                        "workerId": "private.us-east-2.LMI3IGP47RB6RXWSMWOAYMG57U",
                        "annotationData": {
                            "content": "{\"entities\":\"{\\\"0\\\":\\\"17135270\\\"}\"}"
                        }
                    }
                ]
            },
            {
                "datasetObjectId": "6323",
                "dataObject": {
                    "content": "17135270"
                },
                "annotations": [
                    {
                        "workerId": "private.us-east-2.LMI3IGP47RB6RXWSMWOAYMG57U",
                        "annotationData": {
                            "content": "{\"entities\":\"{\\\"0\\\":\\\"17135270\\\"}\"}"
                        }
                    }
                ]
            },
            {
                "datasetObjectId": "15098",
                "dataObject": {
                    "content": "19524513|a|Programmed necrosis is a form of caspase-independent cell death whose molecular regulation is poorly understood. The kinase RIP1 is crucial for programmed necrosis, but also mediates activation of the prosurvival transcription factor NF-kappaB. We postulated that additional molecules are required to specifically activate programmed necrosis. Using a RNA interference screen, we identified the kinase RIP3 as a crucial activator for programmed necrosis induced by TNF and during virus infection. RIP3 regulates necrosis-specific RIP1 phosphorylation. The phosphorylation of RIP1 and RIP3 stabilizes their association within the pronecrotic complex, activates the pronecrotic kinase activity, and triggers downstream reactive oxygen species production. The pronecrotic RIP1-RIP3 complex is induced during vaccinia virus infection. Consequently, RIP3(-/-) mice exhibited severely impaired virus-induced tissue necrosis, inflammation, and control of viral replication. Our findings suggest that RIP3 controls programmed necrosis by initiating the pronecrotic kinase cascade, and that this is necessary for the inflammatory response against virus infections."
                },
                "annotations": [
                    {
                        "workerId": "private.us-east-2.LMI3IGP47RB6RXWSMWOAYMG57U",
                        "annotationData": {
                            "content": "{\"entities\":\"{\\\"17\\\":\\\"RIP1\\\",\\\"32\\\":\\\"NF-kappaB.\\\",\\\"47\\\":\\\"RNA\\\",\\\"53\\\":\\\"kinase\\\",\\\"54\\\":\\\"RIP3\\\",\\\"69\\\":\\\"RIP3\\\",\\\"72\\\":\\\"RIP1\\\",\\\"77\\\":\\\"RIP1\\\",\\\"79\\\":\\\"RIP3\\\",\\\"101\\\":\\\"RIP1-RIP3\\\",\\\"110\\\":\\\"RIP3(-/-)\\\",\\\"128\\\":\\\"RIP3\\\"}\"}"
                        }
                    }
                ]
            }
        ]

        expected = [
            {
                "datasetObjectId": "21277",
                "consolidatedAnnotation": {
                    "content": {
                        "EntityRecognition-ProtienName": {
                            "entities": [
                                {
                                    "start_index": "0",
                                    "length": 8,
                                    "token": "17135270"
                                }
                            ]
                        }
                    }
                }
            },
            {
                "datasetObjectId": "6323",
                "consolidatedAnnotation": {
                    "content": {
                        "EntityRecognition-ProtienName": {
                            "entities": [
                                {
                                    "start_index": "0",
                                    "length": 8,
                                    "token": "17135270"
                                }
                            ]
                        }
                    }
                }
            },
            {
                "datasetObjectId": "15098",
                "consolidatedAnnotation": {
                    "content": {
                        "EntityRecognition-ProtienName": {
                            "entities": [
                                {
                                    "start_index": "17",
                                    "length": 4,
                                    "token": "RIP1"
                                },
                                {
                                    "start_index": "32",
                                    "length": 10,
                                    "token": "NF-kappaB."
                                },
                                {
                                    "start_index": "47",
                                    "length": 3,
                                    "token": "RNA"
                                },
                                {
                                    "start_index": "53",
                                    "length": 6,
                                    "token": "kinase"
                                },
                                {
                                    "start_index": "54",
                                    "length": 4,
                                    "token": "RIP3"
                                },
                                {
                                    "start_index": "69",
                                    "length": 4,
                                    "token": "RIP3"
                                },
                                {
                                    "start_index": "72",
                                    "length": 4,
                                    "token": "RIP1"
                                },
                                {
                                    "start_index": "77",
                                    "length": 4,
                                    "token": "RIP1"
                                },
                                {
                                    "start_index": "79",
                                    "length": 4,
                                    "token": "RIP3"
                                },
                                {
                                    "start_index": "101",
                                    "length": 9,
                                    "token": "RIP1-RIP3"
                                },
                                {
                                    "start_index": "110",
                                    "length": 9,
                                    "token": "RIP3(-/-)"
                                },
                                {
                                    "start_index": "128",
                                    "length": 4,
                                    "token": "RIP3"
                                }
                            ]
                        }
                    }
                }
            }
        ]

        mock_s3_client = Mock()
        mock_s3_Object = Mock()
        mock_s3_Object.get.return_value = {"Body": BytesIO(json.dumps(payload).encode("utf-8"))}
        mock_s3_client.Object.return_value = mock_s3_Object
        sut.s3_client = mock_s3_client

        # Act
        actual = sut.post_process(event)

        # Assert
        self.assertEqual(actual, expected)
