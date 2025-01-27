import toml
import argparse
import requests
from bs4 import BeautifulSoup

# TSF Automation Arguments
parser = argparse.ArgumentParser(description='TSF Automation Tool', prog= 'at.py') 
parser.add_argument('-u', '--url', type=str, help='Enter Tool Github Link', required= True)
parser.add_argument('-f', '--file', type=str, help='Tool Help Text', required= True)
args = parser.parse_args()
url = args.url
input_file = args.file
output_file = "output.toml"


# Tool Name
parts = url.split('/')
if len(parts) > 4:
   name = parts[4]

# Tool Human
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser') 
tag = soup.find(class_="f4 my-3")   
tool_human = tag.text.strip()

# Header Tool
header_data = {
  "header": {
    "version": 0.5,
    "environment": 'oci',
    "id": f'{name}',
    "name": f'{name}',
    "image": f'reg.fuzzer.cloud/{name}',
    "category": ["enumeration"],
    "human": f'{tool_human}',
    "source": f'{url}'
  }
}

tool_execute = {
    "execute": {
      "command": f'{name}',  
    }
}

with open(output_file, "w") as toml_file:
    toml.dump(header_data, toml_file)
    
with open(output_file, "a") as f:
    f.write("\n")
    
with open(output_file, "a") as toml_file:
    toml.dump(tool_execute, toml_file)
    
with open(output_file, "a") as f:
    f.write("\n")
   

# Tool Switches
with open(input_file, 'r') as file:
    lines = file.readlines()

switch = []
descr = []

for line in lines:
    linee = line.strip()
    parts = linee.split("#")
    if parts and parts[0].startswith('-'):    
        if len(parts) == 2:
            switch.append(parts[0])
            descr.append(parts[1])
        if len(parts) == 3:
            switch.append(parts[0])
            descr.append(parts[2])
        if len(parts) == 4:
            switch.append(parts[0])
            descr.append(parts[3])


for i in range(len(switch)):
    print(switch[i], descr[i])
    hash = "#"
    data = {
    "execute": {
        "modifiers": [
            {
                "name": "",
                "human": descr[i].strip().capitalize(),
                "format": switch[i].strip(),
                "order": 0,
                "variables": [{
                        "name": "",
                        "type": "",
                        "class": "",
                        "human": ""
                    }]
            }
        ]}}
    with open(output_file, 'a') as file:
        file.write(hash)
        file.write(switch[i])
        file.write("\n")
        toml.dump(data, file)
   
 
with open(output_file, 'r') as file:
    lines = file.readlines()
    cleaned_lines = []
    execute_found = False
    
    for line in lines:
        if line.strip() == "[execute]":
            if not execute_found:
                execute_found = True
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
with open(output_file, 'w') as file:
    file.writelines(cleaned_lines)
