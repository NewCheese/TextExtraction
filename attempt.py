import re

def remove_names(text):
    pattern = r"(\b\S+\s)(?:X\s)?(?:\S+\s){1,2}"
    return re.sub(pattern, r"\1", text)

text = '''
M Merchant F 2 X 4242727604295A5427272 X 5A5A5272 2427242 24242
J Turner X 2 515 44 W1 5 44 14 15 460 515 415 4249 X 2 5 W 5 13E 43 2 515 42 532 52 5249
R Cheng A38 5F 88 160 5154 X 2 523 X 2442 494 83 2 24 582 242 58
B Chavez E2 5 8 38 34 41 5 42 7 63 4 X 315 43 15 42 4 9 13 31 542 5249 8154249
'''

result = remove_names(text)
print(result)