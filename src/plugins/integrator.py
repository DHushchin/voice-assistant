from plugins.modules.factory import PluginsFactory


class Integrator:
    """
        Integrator class

        This class is responsible for loading all plugins and executing them
    """

    def generate_response(self, intent: str, entities: dict) -> str:
        """
            Execute all plugins

            Inputs:
            - intent:   stringified intent provided by the NLP module
            - entities: dictionary of stringified entities provided by the NLP module

            Outputs:
            - response: Dictionary containing the plugin's responce in natural language
        """
            
        plugin = PluginsFactory(intent)

        try:
            response = plugin.execute(entities)
        except Exception as e:
            print(e)
            print(f'Error executing plugin: {intent}')
            response = ''

        return response
