import requests
import random
import re
import json

from datetime import datetime, timedelta

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from pyowm.exceptions.api_response_error import UnauthorizedError, NotFoundError

class Domoka(NeuronModule):
    def __init__(self, **kwargs):
        # get message to spell out loud
        super(Domoka, self).__init__(**kwargs)

        self.url = kwargs.get('url', 'domoka.local')
        self.answers = kwargs.get('answers', 'C\'est fait')
        self.room = kwargs.get('room', None)
        self.action = kwargs.get('action', None)
        self.action_augmentation = kwargs.get('action_augmentation', None)
        self.action_diminution = kwargs.get('action_diminution', None)
        self.action_unknown = kwargs.get('action_unknown', None)
        self.action_information = kwargs.get('action_information', None)
        self.answer_information = kwargs.get('answer_information', None)

        # check if parameters have been provided
        if not self._is_parameters_ok():
            raise InvalidParameterException

        action_found = 0

        try:
            self.action_information.index(self.action)
            action_found = 1
            self._information_chauffage()
        except:
            pass

        try:
            self.action_diminution.index(self.action)
            action_found = 1
            self._diminution_chauffage()
        except:
            pass

        try:
            self.action_augmentation.index(self.action)
            action_found = 1
            self._augmentation_chauffage()
        except:
            pass

        if action_found == 0 :
            self.say(self.action_unknown)

    def _augmentation_chauffage(self):
        data = self._get_data_from_domoka(self.room)
        new_temp = int(data['max_temp'])+1
        self._update_temperature(new_temp, data, self.room)
        answer_for_say = random.choice(self.answers)
        self.say(answer_for_say)

    def _diminution_chauffage(self):
        data = self._get_data_from_domoka(self.room)
        new_temp = int(data['max_temp'])-1
        self._update_temperature(new_temp, data, self.room)
        answer_for_say = random.choice(self.answers)
        self.say(answer_for_say)

    def _information_chauffage(self):
        data = self._get_data_from_domoka(self.room)
        temp = str(data['temperature'])
        t = re.sub(r"##\s?\b\s?temperature\s?\b\s?##", temp, self.answer_information)
        self.say(t)

    def _get_data_from_domoka(self,name):
        url = 'http://'+self.url+'/get-temperature'
        myobj = {'name': self._clean_room_name(name)}
        x = requests.post(url, data = myobj)
        data = json.loads(x.text)
        return data

    def _update_temperature(self,temperature, data ,name):
        url = 'http://'+self.url+'/reglage-chauffage'
        myobj = {'reglage':temperature, 'ecart':data['ecart'], 'mode_nuit': data['mode_nuit'], 'mode_jour':data['mode_jour'], 'name': self._clean_room_name(name)}
        x = requests.post(url, data = myobj)

    def _clean_room_name(self,name):
        return re.sub(r"\b\s?(le|la|les|du|de|des|les|a|au|l')\s?\b"," ",name)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: NotImplementedError
        """
        if self.url is None:
            raise MissingParameterException("Domoka neuron needs an url")

        return True
