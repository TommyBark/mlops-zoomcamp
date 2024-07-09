import json
import base64
import boto3
import os
import mlflow
import pickle 
import io

kinesis_client = boto3.client("kinesis")

PREDICTIONS_STREAM_NAME = os.getenv("PREDICTIONS_STREAM_NAME","ride_predictions")
VECTORIZER_PATH = "./preprocessor.b"
RUN_ID = "8ecb10409b7f4f33bc986937704f53da"

s3 = boto3.client('s3')

bucket_name = 'mlflow-artifact-store-2'
object_key = '5/8ecb10409b7f4f33bc986937704f53da/artifacts/preprocessor/preprocessor.b'
# Get the object
response= s3.get_object(Bucket = bucket_name, Key= object_key)
file_content = response["Body"].read()
binary_stream = io.BytesIO(file_content)

dv = pickle.load(binary_stream)

logged_model_path = f"s3://mlflow-artifact-store-2/5/{RUN_ID}/artifacts/models_mlflow"
model = mlflow.pyfunc.load_model(logged_model_path)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = str(ride['PULocationID']) + '_' + str(ride['DOLocationID'])
    features["trip_distance"] = ride["trip_distance"]
    return features


def predict(features):
    X = dv.transform(features)
    pred= model.predict(X)
    return float(pred[0])

def lambda_handler(event, context):

    
    print(json.dumps(event))
    prediction_events = []
    for record in event["Records"]:
        encoded_data = record["kinesis"]["data"]
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        ride = ride_event['ride']
        ride_id = ride_event["ride_id"]
        
        features = prepare_features(ride)
        prediction_event  = {
            "model": "ride_duration_prediction_model",
            "version":"123",
            "ride_duration_prediction":predict(features),
            "ride_id":ride_id
            }
            
        prediction_events.append(prediction_event)
    
        # kinesis_client.put_record(
        #     StreamName=PREDICTIONS_STREAM_NAME,
        #     Data=json.dumps(prediction_event),
        #     PartitionKey=str(ride_id)
        #     )
            
    return {"predictions":prediction_events}