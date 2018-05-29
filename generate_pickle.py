import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import pickle

tree = ET.parse('joukahainen.xml')
root = tree.getroot()

wordlets = Counter()

for word in root.findall('./word'):
	forms = [f.text for f in word.findall('./forms/form')]
	#classes = {c.text for c in word.findall('./classes/wclass')}
	#infs = [(i.text, i.attrib) for i in word.findall('./inflection/infclass')]
	#word_id = word.get('id')
	for form in forms:
		wordlets.update(form.split('='))

print(f'Read {len(wordlets)} wordlets')

by_first_letter = defaultdict(set)
for wordlet in wordlets.keys():
	by_first_letter[wordlet[0].lower()].add(wordlet)

with open('wordtrie.pickle', 'wb') as outf:
	pickle.dump(by_first_letter, outf, protocol=-1)
	print(f'Wrote {outf.tell()} bytes of {outf.name}')