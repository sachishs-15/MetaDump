
import json
import random
from collections import Counter
import jsonlines
import csv


def modify(param):

   ls = [{"argument_name": k, "argument_value": v} for param_dict in param for k, v in param_dict.items()]
   # ls = []
   # for j in param:
   #    for i in j:
   #       ls.append({"argument_name": i, "argument_value": j[i]})
   
   return ls


def checkCompatibility(api):
   if api["api_description"] == " ":
      return False
   for p in api["required_parameters"]:
      if p["description"] == "":
         return False
   return True         

with open('datasets/G1_query.json', 'r') as f:
  
   data = json.load(f)

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

possibleapilist = list(possibleapis)[:200]

nd = 200 # number of datasets required]

ans = []
for d in range(0, nd):
   

   toolist = random.sample(possibleapilist, 10)
   print(toolist)

   avtool = available(toolist)
   print(len(avtool))
   for q in data: 

      s = set()

      for i in q["relevant APIs"]:
         s.add(i[0])

      a = dict()
      for t in q['api_list']:
         x = tuple((t["tool_name"], t["api_name"]))
         param = t["required_parameters"]

         a[x] = param
      
      if s.issubset(toolist):
            query = q['query']
            tlist = dict()

            tlist["query"] = query
            
            ls = []

            flag = 0
            for api in q['api_list']:
               if checkCompatibility(api) == False:
                  flag = 1
                  break

            if flag == 1:
               continue

            for api in q['relevant APIs']:
               reqpar = a[tuple((api[0], api[1]))]

               tl = dict()
               tl["tool_name"] = f"{api[0]}/{api[1]}"
               tl["arguments"] = modify(reqpar)
               ls.append(tl)

            tlist["completion"] = ls
            tlist["tools"] = avtool
            
            ans.append(tlist)

#   with jsonlines.open(f'output{d}.jsonl', 'w') as writer:
#    writer.write_all(ans)
   
field_names = ['query', 'completion','tools']
with open("outfile.csv", 'w') as csvfile:
   writer = csv.DictWriter(csvfile, fieldnames=field_names)
   writer.writeheader()
   writer.writerows(ans)