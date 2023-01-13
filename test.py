import re

string = "Zoeken, sturen en bewegen"

new_string = re.sub(r'"', "", string)

print(new_string)