import sys
import json

from bs4 import BeautifulSoup

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Proper usage is python3 <file name> <html path>")
        sys.exit(1)
    with open(sys.argv[1]) as htmlFile:
        soup = BeautifulSoup(htmlFile, 'html.parser')
        divContainer = soup.find(id="histogram-json-data")
        jsonString = divContainer.contents[0]
        # there's an extra newline in the beginning, so skip
        # ignore the last newline so that we don't get an extra comma
        jsonString = jsonString[1:-1].replace('\n', ',\n')
        jsonString = '[' + jsonString + ']'
        jsonData = json.loads(jsonString)
        print(json.dumps(jsonData, indent=4))
