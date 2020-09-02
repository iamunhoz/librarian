# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import dictionary #my custom module


class ActionWordDetail(Action):

    def name(self) -> Text:
        return "action_word_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        word  = tracker.get_slot("word")
        word_detail = tracker.get_slot("word_detail")
        resultado = dictionary.consulta(word, word_detail)

        dispatcher.utter_message(text="the {} for {} is/are: {}".format(word_detail, word, resultado))

        return [SlotSet("search_result", resultado)]
