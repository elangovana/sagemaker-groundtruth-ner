def lambda_handler(event, context):
    print(event)
    text = event['dataObject']['source']
    # TODO: use nltk tokeniser..
    tokens = text.split(" ")
    token_values = [{"id": i, "value": val} for i, val in enumerate(tokens)]
    result = {
        "taskInput": {"tokens": token_values, "text": text},
        "humanAnnotationRequired": True
    }
    print(result)
    return result
