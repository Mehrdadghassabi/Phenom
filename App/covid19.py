from covid import Covid
from google_trans_new import google_translator
import sys

def func(e):
    return e['confirmed']
def all():
    covid=Covid(source="worldometers")
    data=covid.get_data()
    data.sort(reverse=True,key=func)
    k=data[0]
    print(f'confirmed:{k["confirmed"]} deaths:{k["deaths"]} recovered:{k["recovered"]}\n'
          f'new_cases:{k["new_cases"]} new_deaths:{k["new_deaths"]}\n'
          f'active:{k["active"]} critical:{k["critical"]}')
def byCountry(country):
    try:
        translator=google_translator()
        k=covid.get_status_by_country_name(translator.translate(country,lang_tgt='en').strip())
        print(f'confirmed:{k["confirmed"]} deaths:{k["deaths"]} recovered:{k["recovered"]}\n'
              f'new_cases:{k["new_cases"]} new_deaths:{k["new_deaths"]}\n'
              f'active:{k["active"]} critical:{k["critical"]}')
    except:
        print("can't find that country")

covid=Covid(source="worldometers")
if(sys.argv[1]=='country'):
    byCountry(sys.argv[2])
else:
    all()