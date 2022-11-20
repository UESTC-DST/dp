from utils.semanticScholarScraper import getPaperInfo
# 
import json

if __name__ == '__main__':
    search = getPaperInfo()
    result = json.loads(json.dumps(search.get_paperInfo_from_name('Hinton',1)))

    print(len(result))
