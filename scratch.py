import unicodedata
import re

with open('F:\\VReality\\PizzaWeek\\PW_LP_1ra\\TEMP\\mds-010922_003110\\16. Nina.txt', 'r+', encoding="utf-8") as f:
	text = f.read()
	text = unicodedata.normalize('NFKD', text)
	text = re.sub(r'^\n+', '*------*', text,flags=re.M)
	text = re.sub('\n', '', text)
	text = re.sub('\*------\*', '\n', text)
	print(text)
	f.seek(0)
	f.write(text)
	f.truncate()
