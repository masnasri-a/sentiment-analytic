import json
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class ReprocessData:
    def __init__(self, text:str) -> None:
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()
        self.text = text

    def cleaner(self):
        temp = self.text.lower()
        temp = re.sub("'", "", temp) # to avoid removing contractions in english
        temp = re.sub("@[A-Za-z0-9_]+","", temp)
        temp = re.sub("#[A-Za-z0-9_]+","", temp)
        temp = re.sub(r'http\S+', '', temp)
        temp = re.sub('[()!?]', ' ', temp)
        temp = re.sub('\[.*?\]',' ', temp)
        temp = re.sub("[^a-z0-9]"," ", temp)
        self.text = temp
        
    def stemming(self):
        temp = self.text
        output = self.stemmer.stem(temp)
        self.text = output

    def slang(self):
        temp = self.text
        splits = temp.split(' ')
        with open('slang.json','r') as files:
            list_data = json.load(files)
            index = 0
            for word in splits:
                if word in list_data:
                    splits[index] = list_data[word]
                index += 1
        self.text = ' '.join(splits)

    def return_data(self):
        self.cleaner()
        self.slang()
        self.stemming()
        return self.text


if __name__ == "__main__":
    sentence = 'Keren @nasri #pembersihan Om Ded 👏 Semoga suatu hari ada bintang tamu yang ga di dibikin uncomfortable with your questions ya.'
    print('raw = ',sentence)
    data = ReprocessData(sentence)
    print(data.return_data())