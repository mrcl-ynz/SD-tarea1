import requests
from bs4 import BeautifulSoup

def read_csv(path):
    urls = []

    with open(path, 'r') as f:
        seen = set()

        for line in f.readlines()[:-1]:
            url = line.split('\t')[4][:-1]

            if url == '' or url in seen: continue
            
            seen.add(url)
            urls.append(url)
        
    return urls


def getDataFromUrl(url):
    collected_data = {'url': url, 'title': None, 'description': None, 'keywords': None}
    try:
        r = requests.get(url, timeout=1)

        if r.status_code != 200: return None

        soup = BeautifulSoup(r.text, 'html.parser')
            
        if (title := soup.find('title')):
            title = title.get_text().replace("\n","")
            title = title.replace("\r","")
            title = title.replace("\t","")
            title = title.replace("'", '')
        
        if (description := soup.find("meta", {'name': "description"})):
            description = description['content']
            description = description.replace("'", '')
            description = description.replace('\n', '')
            description = description.replace('\r', '')

        if (keywords := soup.find("meta", {'name': "keywords"})):
            keywords = keywords['content']
            keywords = keywords.replace(" ", "")
            keywords = keywords.replace(".", "")
            keywords = keywords.replace("'", '')
            keywords = keywords.replace('\n', '')
            keywords = keywords.replace('\r', '')
        
        collected_data['title'] = title
        collected_data['description'] = description
        collected_data['keywords'] = keywords 
        
        return collected_data if collected_data['keywords'] else None
    
    except Exception:
        return None

if __name__ == '__main__':
    path = 'dataset.txt'
    urls = read_csv(path)

    insert_query = 'INSERT INTO Queries (link, title, descript, keywords) VALUES'
    
    with open('../db/init.sql', 'w') as f:
        f.write('CREATE TABLE Queries (id SERIAL, link TEXT, title TEXT, descript TEXT, keywords TEXT);\n')
        cont = 0
        for url in urls:
            if (cont == 1000): break

            data = getDataFromUrl(url)
            
            if data is None: continue
            
            cont += 1
            query_values = f"('{data['url']}', '{data['title']}', '{data['description']}', '{data['keywords']}');"
            f.write(f'{insert_query} {query_values}\n')