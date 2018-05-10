from textgenrnn.textgenrnn import textgenrnn
textgen = textgenrnn()

# cat cocktails_dbcocktails.txt cocktails_webtender.txt > cocktails.txt

textgen.train_from_file('cocktails.txt', num_epochs=10)
textgen.generate(5)
