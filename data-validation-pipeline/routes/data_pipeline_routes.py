from flask import Blueprint
from flask_restful import Api
from resources import DataResources


DATA_PIPELINE_BLUEPRINT = Blueprint("data_pipeline", __name__)

Api(DATA_PIPELINE_BLUEPRINT).add_resource(
    DataResources, "/dataset_validation"
)

