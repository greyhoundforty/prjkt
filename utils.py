import os
import requests
from bs4 import BeautifulSoup

url = 'https://github.com/github/gitignore/tree/main'

def get_gitignore(language, project_dir):

  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  for a in soup.find_all('a', class_='js-navigation-open Link--primary'):
      filename = a.text.strip()
      if filename.lower() == f'{language.lower()}.gitignore':
          gitignore_url = 'https://github.com' + a['href']
          
          print(f"Found {language} gitignore at: {gitignore_url}")
          
          raw_response = f'https://raw.githubusercontent.com/github/gitignore/main/{language}.gitignore'
          response = requests.get(raw_response)
          gitignore_path = os.path.join(project_dir, '.gitignore')
          with open(gitignore_path, 'w') as f:
                f.write(response.text)
          return
  
if __name__ == '__main__':
  get_gitignore()
