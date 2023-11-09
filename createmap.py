
import json
import random
from collections import Counter
import jsonlines
import csv


def createDocString(d):
   ans = 'def '

   ans += d['tool_name']+'('

   for arg in d['required_parameters']:
      ans += arg['name']
      ans += ', '
   for arg in d['optional_parameters']:
      ans += arg['name']
      ans += ', '   
   ans = ans[:-2]
   ans += '):\n'
   ans += '"""\n'
   ans += d['tool_description']
   ans+='\n\n'
   ans+='Parameters:\n'
   for arg in d['required_parameters']:
      ans += '    '
      ans += arg['name']
      ans += ' ('
      ans += arg['type']
      ans += '): '
      ans += arg['description']
      ans += '\n'
   for arg in d['optional_parameters']:
      ans += '    '
      ans += arg['name']
      ans += ' ('
      ans += arg['type']
      ans += '): '
      ans += arg['description']
      ans += '\n'
   ans+='\nReturns:\n'
   for key in d['template_response']:
      ans+= f"{d['template_response'][key]}"
      ans +=': '
      ans += key
   ans += '\n"""\n'

   return ans


with open('datasets/G1_query.json', 'r') as f:
  
   data = json.load(f)


def checkCompatibility(api):
   if api["api_description"] == " ":
      return False
   for p in api["required_parameters"]:
      if p["description"] == "":
         return False
   return True         


possibleapis = set()


def available(toolist):
    apilist = []
    for q in data:
       for api in q['api_list']:
         if api['tool_name'] in toolist:
            p = dict()
            if(checkCompatibility(api) == True):
                p = {
            "tool_name": f"{api['tool_name']}/{api['api_name']}",
            "tool_description": api["api_description"],
            "required_parameters": api["required_parameters"],
            "optional_parameters": api["optional_parameters"],
            
            }
                
            if 'template_response' in api:
                p["template_response"] = api["template_response"]

            if p not in apilist:
             apilist.append(p)

    return apilist
       

for q in data:
   for api in q['relevant APIs']:
      possibleapis.add(api[0])

print(len(possibleapis))
possibleapilist = list(possibleapis)

x = available(possibleapilist)
print(len(x))
ans =[]

print(x)
exit(0)

for d in x: 
    temp={'tool name':d['name'],'docstring':createDocString(d)}
    ans.append(temp)

field_names = ['tool name', 'docstring']
with open("mapfile.csv", 'w') as csvfile:
   writer = csv.DictWriter(csvfile, fieldnames=field_names)
   writer.writeheader()
   writer.writerows(ans)