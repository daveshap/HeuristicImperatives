from uuid import uuid4
import openai
from time import time,sleep
import re


scales = [
    'an individual person',
    'a pair of people', 
    'one family', 
    'a small company', 
    'a local religious community', 
    'a medium company', 
    'a whole town', 
    'a whole city', 
    'a global company', 
    'an entire state', 
    'an entire nation', 
    'multiple nations', 
    'an entire continent', 
    'the entire world'
]

severities = [
    'mild daily hubbub', 
    'moderate once-in-a-week commotion', 
    'moderate once-in-a-month disturbance', 
    'severe once-in-a-year uproar', 
    'critical once-in-a-decade upheaval', 
    'catastrophic once-in-a-century pandemonium'
]

modifiers = [
    'an emotional', 
    'a political', 
    'a technological', 
    'an environmental', 
    'a social', 
    'a financial'
]


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = open_file('openaiapikey.txt')


def gpt3_completion(prompt, engine='text-davinci-002', temp=1.0, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['USER:', 'TIM:']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    for scale in scales:
        for severity in severities:
            for modifier in modifiers:
                prompt = open_file('prompt_scenario.txt')
                prompt = prompt.replace('<<UUID>>', str(uuid4()))
                prompt = prompt.replace('<<SCALE>>', scale)
                prompt = prompt.replace('<<SEVERITY>>', severity)
                prompt = prompt.replace('<<MODIFIER>>', modifier)
                print('\n\n============================\n\n', prompt, '\n\n')
                response = gpt3_completion(prompt)
                print(response)
                filename = (scale + modifier + severity[0:10]).replace(' ', '').replace('-','').replace('the','').replace('an','').replace('a','') + '_%s.txt' % time()
                print(filename)
                save_file('scenarios/%s' % filename, response)