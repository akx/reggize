all: wordtrie.pickle

wordtrie.pickle: joukahainen.xml
	python3 generate_pickle.py

joukahainen.xml:
	curl https://joukahainen.puimula.org/sanastot/joukahainen.xml.gz | gunzip > joukahainen.xml

#omorfi-sanalista.xml:
#	curl -L https://github.com/flammie/omorfi/releases/download/20170515/omorfi-sanalista.xml.xz | xz -d > omorfi-sanalista.xml