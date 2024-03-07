import os, openai
CAT = (
  ('Orthopedics','Orthopedics'),
  ('Cardiology','Cardiology'),
  ('Neurology','Neurology'),
  ('Oncology','Oncology'),
  ('Pediatrics','Pediatrics'),
  ('Dermatology','Dermatology'),
  ('Gastroenterology','Gastroenterology'),
  ('Gynecology','Gynecology'),
  ('Psychiatry','Psychiatry'),
  ('Ophthalmology','Ophthalmology'),
  ('Pulmonology','Pulmonology'),
  ('Nephrology','Nephrology'),
)

os.environ['OPENAI_API_KEY'] = 'key_here'
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

def get_disease_name(symptoms):
    query = 'The following symptoms are observed\n'+symptoms+'\nWhat is the most probable disease? Return the disease name only.'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        max_tokens=5,
        temperature=0
    )
    probable_disease = response['choices'][0]['text']
    return probable_disease

symptoms = 'back pain, numb hands, difficulty in moving hands'
probable_disease = get_disease_name(symptoms=symptoms)
print(probable_disease)
def get_category(probable_disease):
    query = 'The disease'+probable_disease+' falls under which one of the following category? Only category name\n'
    for i in CAT:
        query = query +', '+i[0]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        max_tokens=7,
        temperature=0
    )
    related_category = response['choices'][0]['text']
    return related_category

related_category = get_category(probable_disease=probable_disease)
print(related_category)
