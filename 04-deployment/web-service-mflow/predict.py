from flask import Flask,request,jsonify
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
import pickle

RUN_ID = "f5520aca4b114fb199caa353f566ab35"

mlflow.set_tracking_uri("http://127.0.0.1:5000")

logged_model = f'runs:/{RUN_ID}/models_mlflow'
client = MlflowClient()
# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

path = client.download_artifacts(run_id = RUN_ID, path = "preprocessor/preprocessor.b")
with open(path, "rb") as f_in:
    dv = pickle.load(f_in)


# Predict on a Pandas DataFrame.

#loaded_model.predict(pd.DataFrame(data))


def prepare_features(ride):
    features = {}
    features['PU_DO'] = ride['PULocationID'] + '_' + ride['DOLocationID']
    features['PU_DO'] = ride['PULocationID'] + '_' + ride['DOLocationID']
    features["trip_distance"] = ride["trip_distance"]
    return features

def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]

app = Flask("duration-prediction")

@app.route("/predict", methods = ["POST"])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    pred = predict(features)

    result = {
        "duration":float(pred)
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 9696)