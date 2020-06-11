import requests
import re
from decouple import config

api_key=config('API_KEY')
number = 0
url = f'https://api.themoviedb.org/3/movie/{number}?api_key={api_key}'
res = requests.get(url).json

print(res)

# pattern = re.compile('type=')
# with open('movie.csv', 'w',encoding='utf-8' ) as f:
#     for i in range(len(imgs)):
#         name = imgs[i].get("alt")
#         src = imgs[i].get("src")
#         f.write(re.sub(r'\?type=\w*','',str(i+1) + ',' +name + ',' + src)+'\n')