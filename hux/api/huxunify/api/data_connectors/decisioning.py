from huxmodelclient import api_client, configuration
from huxmodelclient.api import DefaultApi as dec_client
from huxunify.api.config import get_config


class Decisioning:

    def __init__(self):
        config = configuration.Configuration(host="https://hux-kubeflow-api-dec.hux-decisioning-dev.in")
        # config = configuration.Configuration(get_config().DECISIONING_URL)
        self.decisioning_client = dec_client(api_client=api_client.ApiClient(configuration=config))

    def get_models(self) -> list:
        """ Gets a list of all models from decisioning.

        Returns:
            list: list of models.
        """
        return self.decisioning_client.get_models_api_v1alpha1_models_get()

    def get_model_info(self, model_id: str) -> dict:
        """ Gets the model info from decisioning.

        Args:
            model_id (str): ID of the model.

        Returns:
            dict: model info dictionary.
        """
        return self.decisioning_client.get_model_info_api_v1alpha1_models_model_id_get(model_id)[0]
