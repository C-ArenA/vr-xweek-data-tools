def cardinal_to_ordinal(cardinal:int)->str:
    base = {
		0: "ma",
		1: "ra",
		2: "da",
		3: "ra",
		4: "ta",
		5: "ta",
		6: "ta",
		7: "ma",
		8: "va",
		9: "na",
	}
    
    return str(cardinal) + base[int(cardinal)%10]

if __name__ == "__main__":
	print(cardinal_to_ordinal(input("Ingrese número")))