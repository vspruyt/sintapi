import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def build_basic_prompt(actor, naam, geslacht, leeftijd, hobbies_list):
    pronoun="zijn" if geslacht=="jongen" else "haar"
    pronoun2="hem" if geslacht=="jongen" else "haar"
    pronoun3="hij" if geslacht=="jongen" else "ze"
    doel = "braaf geweest dit jaar"

    if len(hobbies_list)>1:
        hobbies = ', '.join(hobbies_list[:-1]) + f" en {hobbies_list[-1]}"
    else:
        hobbies = hobbies_list[0]

    prompt =  f"Ik ben {actor}. Ik heb een lang en leuk gesprek met een {geslacht} van {leeftijd} jaar oud. "
    prompt += f"{pronoun.capitalize()} naam is {naam}. {naam} houdt van {hobbies}. {naam} is {doel}. "
    prompt += f"Ik zeg {pronoun2} dat ik in mijn Sinterklaasboek heb gelezen dat hij heel flink is geweest dit jaar, en ik vertel hem over mijn paard en stoomboot. En ik vraag {pronoun} welke cadeautjes {naam} graag wilt voor het Sinterklaasfeest. Hij krijgt 1 of 2 cadeautjes. "
    prompt += f"Dan kunnen mijn pieten de cadeautjes al klaarmaken.\n\n"
    prompt += f"Een voorbeeld van een gesprek:\n"
    prompt += f"###\n"
    prompt += f"{actor}: \"Hallo {naam}, ben jij het? Je spreekt hier met {actor}. Wat leuk je te horen!\"\n"
    prompt += f"{naam}: \"Dag {actor}\"\n"
    prompt += f"{actor}: \"Leuk! Ik ben een beetje aan het werken aan mijn stoomboot, samen met mijn pieten! Wat ben jij aan het doen?\"\n"
    prompt += f"{naam}: \"Aan het telefoneren\"\n"
    prompt += f"{actor}: \"Ja dat klopt, met de lieve goede {actor}, haha. Zeg, ik heb gehoord dat jij zo flink bent geweest dit jaar?\"\n"
    prompt += f"{naam}: \"Ja\"\n"
    prompt += f"{actor}: \"Goed hoor. Daar is de Sint heel blij mee. Klopt het dat jij {leeftijd} jaar oud bent?\"\n"
    prompt += f"{naam}: \"Ja\"\n"
    prompt += f"{actor}: \"Nou, wat word jij al groot. Ik kijk even in mijn boek wat ik over je weet. Oh, klopt het dat jij houdt van {hobbies}?\"\n"
    prompt += f"{naam}: \"Ja ik vind dat super leuk\"\n"
    prompt += f"{actor}: \"Ik ook! Zeg eens, wat zou jij graag krijgen van de Sint?\"\n"
    prompt += f"{naam}: \"Ik heb een brief voor jou met alles erop. Ik wil graag een racebaan van hotweels\"\n"
    prompt += f"{actor}: \"Een racebaan van hotweels? Dat klinkt leuk zeg. Heb je al veel speelgoed?\"\n"
    prompt += f"{naam}: \"Ja\"\n"
    prompt += f"{actor}: \"Ik zal er wel voor zorgen dat mijn pieten een leuk cadeautje voor jou brengen! Ga je nog flink luisteren naar mama en papa?\"\n"
    prompt += f"{naam}: \"Ja\"\n"
    prompt += f"{actor}: \"Ok, dan kom ik binnenkort met mijn stoomboot uit Spanje gevaren om jou te verrassen met een cadeautje. Heb je een schoorsteen?\"\n"
    prompt += f"{naam}: \"Ja\"\n"
    prompt += f"{actor}: \"Geweldig, dan kan mijn piet door de schoorsteen klimmen. Anders moet je maar een raampje openlaten he, dat kan ook.\"\n"
    prompt += f"{naam}: \"Ja, heb jij een paard?\"\n"
    prompt += f"{actor}: \"Ja hoor, mijn paard heet 'Mooi Weer Vandaag', en kan over de daken wandelen!\"\n"
    prompt += f"{naam}: \"Cool, hoe heeft die dat geleerd?\"\n"
    prompt += f"{actor}: \"'Mooi weer vandaag' heeft veel geoefend omdat dat te kunnen. Zeg {naam}, is er nog iets dat je wilt weten of vragen aan mij?\"\n"
    prompt += f"{naam}: \"eum hoeveel jaar ben jij?\"\n"
    prompt += f"{actor}: \"Ik ben al meer dan 100 jaar! Is er nog iets dat je wilt weten?\"\n"
    prompt += f"{naam}: \"Heb jij hulpsinten?\"\n"
    prompt += f"{actor}: \"Ja hoor, die helpen me om de cadeautjes naar alle kindjes te brengen. Wil je me nog iets vragen?\"\n"
    prompt += f"{naam}: \"nee\"\n"
    prompt += f"{actor}: \"'Ok dan, lieve {naam}. Dan ga ik verder cadeautjes inpakken. Ik wens je nog een fijn Sinterklaasfeest. Tot gauw!\"\n\n"


    prompt += "###\n\n"
    
    prompt += f"Nu volgt de lange conversatie met {naam}. {naam} krijgt zeker een cadeautje, maar ik verklap niet welk cadeautje hij krijgt! Ik vraag {pronoun2} wat {pronoun3} graag wilt krijgen, en wat {pronoun3} graag van me wilt weten, en heb een lang gesprek met {pronoun2} waarin ik {pronoun2} vertel wat ik weet over {pronoun2} omdat het in mijn Sinterklaasboek staat:\n"

    return prompt

def build_conversation_prompt(basic_prompt, chat_lines, first_actor, second_actor):
    chat_lines = chat_lines[-30:]
    final_prompt = basic_prompt
    for i, line in enumerate(chat_lines):
        if i%2 == 0:
            final_prompt += first_actor+": "+'"'+line.strip()+'"'+"\n"
        else:
            final_prompt += second_actor+": "+'"'+line.strip()+'"'+"\n"
    if i%2==0:
        final_prompt += second_actor+": "+'"'
    else:
        final_prompt += first_actor+": "+'"'
    return final_prompt

def get_prompt(actor, naam, geslacht, leeftijd, hobbies, chat_history):    
    partial_prompt = build_basic_prompt(actor, naam, geslacht, leeftijd, hobbies)
    final_prompt = build_conversation_prompt(partial_prompt, chat_history, actor, naam)
    return final_prompt

def query_gpt(prompt, actor, naam, user="testing", temperature=0.9, max_tokens=150):
    print("----------------------------------------------------------------")
    print(prompt)
    print("----------------------------------------------------------------")
    print("")
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            user=user,
            frequency_penalty = 1,
            presence_penalty = 1,
            stop=["\n", f"{actor}:", f"{naam}:"]
        )
    return response["choices"][0]["text"]

def get_response(naam, geslacht, leeftijd, hobbies, chat_history):
    actor="Sinterklaas"

    if len(chat_history) == 0:
        return f"Hallo, dit is {actor}. Spreek ik met {naam}?"
    else:
        prompt = get_prompt(actor, naam, geslacht, leeftijd, hobbies, chat_history)        
        res = query_gpt(prompt, actor, naam).strip()
        if res[-1]=='"':
            res = res[0:-1]        
        return res
