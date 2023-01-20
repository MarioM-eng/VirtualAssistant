# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json

class ActionName(Action):#Action que le informa al bot si el usuario proporcionó su nombre o no para saludarlo de acuerdo a esto

     def name(self) -> Text:
         return "action_name"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_name")
         name = tracker.get_slot('name')
         print(name)
         g = tracker.get_slot('user_provided_name')
         print(g)
         if name is not None:
             return [SlotSet("user_provided_name",True)]
         else:
            return [SlotSet("user_provided_name",False)]

class ActionResponder(Action):#accion para respponder y mostrar sugerencia de los principales terminos relacionados con investigación

     

     def name(self) -> Text:
         return "action_responder"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_responder")
         dato = tracker.get_slot('dato')
         print(dato)
         dispatcher.utter_message(template ='utter_' + dato)
         dispatcher.utter_message(text = "De {} te puede interesar: ".format(dato))
         self.interesar(dato,dispatcher)

         return []

     def interesar(self, dato, dispatcher: CollectingDispatcher):
        man_arc = open('actions/elementos.json')
        elementos = json.load(man_arc)
        for elemento in elementos:
            if dato == "investigar":
                for val in elemento.get(dato).keys():
                    dispatcher.utter_message(text = "¿Qué es " + val + "?")
            if dato == "paradigma":
                for val in elemento.get("investigar").get(dato):
                    dispatcher.utter_message(text = val)
            if dato == "enfoque":
                for val in elemento.get("investigar").get(dato):
                    dispatcher.utter_message(text = "¿Qué es el enfoque " + val + "?")
            if dato == "muestra":
                for val in elemento.get("investigar").get(dato):
                    dispatcher.utter_message(text = "¿Cueles son los " + val + " de " + dato + "?")
        man_arc.close()


class ActionResponderParadigma(Action):#acctión para mostrar los tipos de paradigma

     

     def name(self) -> Text:
         return "action_responder_paradigma"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_responder_paradigma")
         dato = tracker.get_slot('para')
         print(dato)
         dispatcher.utter_message(template ='utter_paradigma_' + dato)
         #dato = "paradigma " + dato
         self.interesar(dato,dispatcher)

         return [SlotSet("para",None)]#reestablecemos el slot para evitar que influya en la próxima predicción

     def interesar(self, dato, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma").get(dato)
        if elementos is not None:
            dispatcher.utter_message(text = "Te puede interesar: ")
            for key, values in elementos.items():
                if type(values) != dict: #si no es un diccionario, quiere decir que contiene una palabra
                    dispatcher.utter_message(text = key + " " + values)
                else:
                    for v in values:
                        dispatcher.utter_message(text = key + " " + v)
        man_arc.close()                    

class ActionResponderEnfoque(Action):#acctión para mostrar el enfoque perteneciente a un paradigma

     

     def name(self) -> Text:
         return "action_responder_enfoque"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_responder_enfoque")
         dato = tracker.get_slot('enfoque')
         #paradigma = "paradigma " + para
         print(dato)
         dispatcher.utter_message(template ='utter_enfoque_' + dato)
         if tracker.get_slot('para') is not None:
            paradigma = tracker.get_slot('para')
            self.interesar(dato,paradigma,dispatcher)
         else:
            self.interesar(dato,dispatcher)

         return []

     def interesar(self, dato, paradigma, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        enfoque = el[0].get("investigar").get("paradigma").get(paradigma).get("enfoque")
        dispatcher.utter_message(text = "Te puede interesar: ")
        dispatcher.utter_message(text = paradigma)
        if type(enfoque) is not str: #si el enfoque no es un string, si no un dict(Lo esperado)
            elementos = enfoque.get(dato)
            if elementos is not None:
                for key, values in elementos.items():
                    dispatcher.utter_message(text = key + " del enfoque " + dato)
        man_arc.close()

     def interesar(self, dato, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma")
        for paradigma in elementos:
            enf = elementos.get(paradigma).get("enfoque")
            if type(enf) == dict:
                for en in enf:
                    if en == dato:
                        dispatcher.utter_message(text = "Paradigma {}".format(paradigma))
                    for x in enf.get(en):#Recorremos los elementos de los enfoques
                        if en == dato:#Si el enfoque es igual al ingresado por el usuario
                            dispatcher.utter_message(text = "{} del enfoque {}".format(x,en))#Se muestran los elementos que pueden interesarle de dicho enfoque
        man_arc.close()

class ActionCaracteristicaDeEnfoque(Action):#acctión para mostrar el enfoque perteneciente a un paradigma

     

     def name(self) -> Text:
         return "action_caracteristica_enfoque"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_caracteristica_enfoque")
         enfoque = tracker.get_slot('enfoque')
         datoEnfoque = tracker.get_slot('datoEnfoque')
         # if datoEnfoque == "diseno":
         #    datoEnfoque = "dise&#241;o"
         #paradigma = "paradigma " + para
         print(enfoque +" "+datoEnfoque)
         dispatcher.utter_message(template ='utter_enfoque_' + enfoque + "_" + datoEnfoque)
         self.interesar(enfoque, datoEnfoque, dispatcher)

         return [SlotSet("datoEnfoque",None)]#reestablecemos el slot para evitar que influya en la próxima predicción

     def interesar(self, enfoque, datoEnfoque, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma")
        for paradigma in elementos:
            enf = elementos.get(paradigma).get("enfoque")
            if type(enf) == dict:
                for en in enf:
                    if en == enfoque:
                        dato = enf.get(en).get(datoEnfoque)
                        if dato is not None:
                            dispatcher.utter_message(text = "De {} te puede interesar:".format(datoEnfoque))
                            for value in dato:
                                dispatcher.utter_message(text = value)
            else:
                if enf == enfoque:
                    print(enf)

        man_arc.close()

class ActionParadigmaDeEnfoque(Action):#action para modificar el slot de para

     

     def name(self) -> Text:
         return "action_paradigma_de_enfoque"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_paradigma_de_enfoque")
         #dato = tracker.get_slot('dato')
         enfoque = tracker.get_slot('enfoque')
         print(enfoque)

         return [self.paradigmaDeEnfoque(enfoque, dispatcher)]

     def paradigmaDeEnfoque(self, enfoque, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma")
        if elementos is not None:
            for key, values in elementos.items():
                for v in values:
                    for enfo in elementos.get(key).get(v):
                        if enfo == enfoque:
                            #dispatcher.utter_message(text = "Debes seguir el paradigma {}".format(key))
                            return SlotSet("para",key)
                    #print(key + " " + v)
        man_arc.close()

class ActionEnfoqueDeParadigma(Action):#action para modificar el slot de enfoque

     

     def name(self) -> Text:
         return "action_enfoque_de_paradigma"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_enfoque_de_paradigma")
         paradigma = tracker.get_slot('para')
         print(paradigma)

         return [self.enfoqueDeParadigma(paradigma)]

     def enfoqueDeParadigma(self, paradigma):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma").get(paradigma).get("enfoque")
        if elementos is not None:
            if type(elementos) == dict:
                for key in elementos.items():
                    return SlotSet("enfoque",key[0])
            else:
                return SlotSet("enfoque",elementos)
        man_arc.close()

class ActionRelacionTipoInvestigacionEnfoque(Action):#action para modificar el slot de enfoque

     

     def name(self) -> Text:
         return "action_relacion_tipo_investigacion_enfoque"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_relacion_tipo_investigacion_enfoque")
         datoEnfoque = tracker.get_slot('dise&#241;o')
         print(datoEnfoque)
         self.tiposInvestigacionDeEnfoque(datoEnfoque, dispatcher)

         return []

     def tiposInvestigacionDeEnfoque(self, datoEnfoque, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma")

        for paradigma, values in elementos.items():
            for key, values in values.items():
                if type(values) == dict:
                    for enfoque, values in values.items():
                        if type(values) == dict:
                            for key2, values in values.items():
                                if type(values) == list:
                                    for aux in values:
                                        if aux == datoEnfoque:
                                            dispatcher.utter_message(text = "Según lo escrito por Sampieri, debes seguir un enfoque " + enfoque)
        man_arc.close()

class ActionRelacionTipoInvestigacionParadigmaEnfoque(Action):#action para modificar el slot de enfoque

     

     def name(self) -> Text:
         return "action_relacion_tipo_investigacion_paradigma_enfoque"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     
         print('Ejecutó ' + "action_relacion_tipo_investigacion_paradigma_enfoque")
         dato = tracker.get_slot('dato')
         datoEnfoque = tracker.get_slot('dise&#241;o')
         print(datoEnfoque)
         self.tiposInvestigacionDeEnfoque(datoEnfoque, dato, dispatcher)

         return []

     def tiposInvestigacionDeEnfoque(self, datoEnfoque, dato, dispatcher: CollectingDispatcher):
        man_arc = open('actions/investigar.json')
        el = json.load(man_arc)
        elementos = el[0].get("investigar").get("paradigma")

        for paradigma, values in elementos.items():
            for key, values in values.items():
                if type(values) == dict:
                    for enfoque, values in values.items():
                        if type(values) == dict:
                            for key2, values in values.items():
                                if type(values) == list:
                                    for aux in values:
                                        if aux == datoEnfoque:
                                            if dato == "paradigma":
                                                dispatcher.utter_message(text = "Según lo escrito por Sampieri, debes seguir un paradigma " + paradigma + '\nPara conocer más acerca del tema <a target="_blank" href="http://observatorio.epacartagena.gov.co/wp-content/uploads/2017/08/metodologia-de-la-investigacion-sexta-edicion.compressed.pdf">da click aquí</a>')
                                            if dato == "enfoque":
                                                dispatcher.utter_message(text = "Según lo escrito por Sampieri, debes seguir un enfoque " + enfoque + '\nPara conocer más acerca del tema <a target="_blank" href="http://observatorio.epacartagena.gov.co/wp-content/uploads/2017/08/metodologia-de-la-investigacion-sexta-edicion.compressed.pdf">da click aquí</a>')
        man_arc.close()