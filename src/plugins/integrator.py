import logging
import os
import glob
from os.path import isfile
from importlib import import_module


class Integrator:
    
    def __init__(self):
        """ 
            Load all modules into an array so they can be used when required

            Inputs:
             - plugin_path: Local path to the plugins directory
        """

        self.plugins = []
        
        plugin_paths = glob.glob(f'./modules/*.py')
        plugin_paths = [f for f in plugin_paths if isfile(f)]

        for path in plugin_paths:
            basename, extension = os.path.splitext(path)
            import_location = basename.replace("\\", ".")
            import_location = import_location.replace("/", ".")

            try:
                plugin = import_module(import_location)
            except Exception as e:
                print(f'Could not load plugin {import_location}')
                return

            self.plugins.append(plugin)


    def generate_response(self, intent: str, entities: dict) -> str:
        """
            Execute all plugins

            Inputs:
            - intent:   stringified intent provided by the NLP module
            - entities: dictionary of stringified entities provided by the NLP module

            Outputs:
            - response: Dictionary containing the plugin's responce in natural language
        """

        active_plugins = [p for p in self.plugins if intent in p.accepted_intents]

        if len(active_plugins) == 0:
            return "Sorry, I don't know how to do that yet"

        active_plugin = active_plugins[0]
        for p in active_plugins:
            if p != active_plugin:
                if p.priority > active_plugin.priority:
                    active_plugin = p

        try:
            response = active_plugin.execute(intent, entities)
        except:
            response = f'Error executing plugin {active_plugin.__name__}'

        return response
