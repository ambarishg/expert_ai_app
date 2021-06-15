from expertai.nlapi.cloud.client import ExpertAiClient
import os
import json

language = 'en'
os.environ["EAI_USERNAME"] = 'ambarish.ganguly@gmail.com'
os.environ["EAI_PASSWORD"] = 'Ambarish@1234'

class textinsights:
    keyphrases = ""
    keyentities = ""
    keyrelationsrelated =""
    sentiments = ""
    emotions =""
    behavior =""
    personalinfo=""

def get_client():
    client = ExpertAiClient()
    return(client)

def get_key_phrases(text,client):
    output = client.specific_resource_analysis(body={"document": {"text": text}}, 
    params={'language': language, 
    'resource': 'relevants'})

    key_phrases = ""

    for lemma in output.main_lemmas:
        key_phrases = key_phrases + str(lemma.value) + "  "

    return(key_phrases)



def get_named_entities(text,client):
    output = client.specific_resource_analysis(body={"document": {"text": text}}, 
    params={'language': language, 
    'resource': 'entities'})

    key_entities = ""

    for entity in output.entities:
            key_entities = key_entities + str(entity.lemma) + "  "

    return(key_entities)

def get_sentiments(text,client):
    input_text = str(text)
    result = client.specific_resource_analysis(
        body={"document": {"text": input_text}}, 
        params={'language':  language, 'resource': 'sentiment'
       })

    return(result.sentiment.overall)


def get_pii(text,client):

    detector = 'pii'
    output = client.detection(body={"document": {"text": text}}, 
    params={'detector': detector, 'language': language})

    return(json.dumps(output.extra_data, 
    indent=4, sort_keys=True))

def get_relations(text,client):
    output = client.specific_resource_analysis(
    body={"document": {"text": text}}, 
    params={'language': language, 
    'resource': 'relations'})
    
    key_relations_related = ""
    for relation in output.relations:        
        key_relations_related = key_relations_related + "<p> The verb is "
        key_relations_related = key_relations_related + str(relation.verb.lemma) + " - Relations are  "
        for related in relation.related:
            key_relations_related = key_relations_related +  str(related.lemma) + " "  
     
        if(len(relation.related)):
            key_relations_related = key_relations_related + " None "

    key_relations_related = key_relations_related + " </p> "

    return(key_relations_related)

def emotional_traits(client, text,taxonomy = "emotional-traits"):
    input_text = str(text)
    emotional_categories = ""
    output = client.classification(body={"document": {"text": input_text}}, 
                                   params={'taxonomy': taxonomy, 'language': language})

    for category in output.categories:
        if(emotional_categories == ""):
            emotional_categories = emotional_categories + str(category.hierarchy[-1])
        else:
            emotional_categories = emotional_categories + " " + str(category.hierarchy[-1])
    
    return(emotional_categories)

def get_insights(text):
    client = get_client()
    insights = textinsights()
    insights.keyphrases = get_key_phrases(text,client)
    insights.keyentities = get_named_entities(text,client)
    insights.keyrelationsrelated = get_relations(text,client)
    insights.sentiments = get_sentiments(text,client)
    insights.emotions = emotional_traits(client, text,taxonomy = "emotional-traits")
    insights.behavior = emotional_traits(client, text,taxonomy = "behavioral-traits")

    return(insights)
