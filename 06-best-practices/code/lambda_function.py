import os

import model

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_predictions')
RUN_ID = os.getenv('RUN_ID', "8ecb10409b7f4f33bc986937704f53da")
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

model_service = model.init(PREDICTIONS_STREAM_NAME, RUN_ID, TEST_RUN)


def lambda_handler(event, context):
    return model_service.lambda_handler(event)