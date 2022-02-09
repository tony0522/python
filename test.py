import re

s = "國立臺灣大學              數學系         (00124)"
# re.sub("\s\s+", " ", s)

# print(" ".join(s.split()))
k = re.sub(' +', ' ', s)
print(k)