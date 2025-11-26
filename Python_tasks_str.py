# https://pynative.com/python-string-exercise/
# 1A: Create a string made of the first, middle and last character
import string

str1 = "James"
out = str1[0]+str1[2]+str1[-1]
print(out)

# Create a string made of the middle three characters
def get_middle_three_chars(str1):
    print("Original String is", str1)

    # first get middle index number
    mi = int(len(str1) / 2)

    # use string slicing to get result characters
    res = str1[mi - 1:mi + 2]
    print("Middle three chars are:", res)

get_middle_three_chars("JhonDipPeta")
get_middle_three_chars("JaSonAy")


# 2: Append new string in the middle of a given string
s1 = "Ault"
s2 = "Kelly"
mid_index = len(s1) // 2
s3 = s1[:mid_index] + s2 + s1[mid_index:]
print(s3)  # ➜ AuKellylt


# 3: Create a new string made of the first, middle, and last characters of each input string
s1 = "America"
s2 = "Japan"
res = s1[0] + s2[0] + s1[len(s1)//2] + s2[len(s2)//2] + s1[-1] +s2[-1]
print(res)


# 4: Arrange string characters such that lowercase letters should come first
str1 = 'PyNaTive'

def task4(s):
    s2 = ''
    s3 = ''
    for i in s:
        if i.islower():
            s2 += i
        else:
            s3 += i
    return s2+s3

print(task4(str1))


# 5: Count all letters, digits, and special symbols from a given string
str1 = "P@#yn26at^&i5ve"

def task5(str1:str):
    c = 0
    d = 0
    s = 0
    for i in str1:
        if i.isalpha():
            c += 1
        elif i.isdigit():
            d +=1
        else:
            s += 1
    return c, d, s

print(task5(str1))

# 6: Create a mixed String using the following rules
s1 = "Abcxxxx"
s2 = "Xyz"

def task6(s1, s2):
    s3 = ''
    s4 = s2[::-1]
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        s3 += s1[i]+s4[i]
    # добавляем остатки
    s3 += s1[min_len:] + s4[min_len:]
    return s3

print(task6(s1,s2))


# Exercise 7: String characters balance Test
# Write a program to check if two strings are balanced. For example, strings s1 and s2 are balanced if all the characters in the s1 are present in s2. The character’s position doesn’t matter.
s1 = "Ynf"
s2 = "PYnative"


def task7(s1, s2):
    for i in s1:
        if i not in s2:
            return False
    else:
        return True

print(task7(s1,s2))


# Exercise 8: Find all occurrences of a substring in a given string by ignoring the case
str1 = "Welcome to USA. usa awesome, isn't it?"
str2 = str1.upper()
n = str2.count('USA')
print(n)


# Exercise 9: Calculate the sum and average of the digits present in a string
str1 = "PYnative29@#8496"

def task9(s):
    # l = []
    # for i in s:
    #     if i.isdigit():
    #         l.append(int(i))
    l = [int(i) for i in s if i.isdigit()]
    mean = sum(l)/len(l)
    s = sum(l)
    return s, mean

print(task9(str1))  # (38, 6.333333333333333)


# Exercise 10: Write a program to count occurrences of all characters within a string
str1 = "Apple"
def task10(s):
    k = []
    w = []
    for i in s:
        if i not in k:
            k.append(i)
            c = s.count(i)
            w.append(c)
    d=dict(zip(k,w))
    return d

print(task10(str1))


# create a result dictionary
char_dict = dict()

for char in str1:
    count = str1.count(char)
    # add / update the count of a character
    char_dict[char] = count
print('Result:', char_dict)


# Exercise 11: Reverse a given string
str1 = "PYnative"
print(str1[::-1])

# Exercise 12: Find the last position of a given substring
str1 = "Emma is a data scientist who knows Python. Emma works at google."
print(str1.rfind('Emma'))

# Exercise 13: Split a string on hyphens
str1 = 'Emma-is-a-data-scientist'
s2 = str1.split('-')
print(s2)
for _ in s2:
    print(_)


# Exercise 14: Remove empty strings from a list of strings
str_list = ["Emma", "Jon", "", "Kelly", None, "Eric", ""]
s2 = list(filter(None, str_list))
print(s2)
cleaned = [s for s in str_list if s]
print(cleaned)


# Exercise 15: Remove special symbols / punctuation from a string
str1 = "/*Jon is @developer & musician"
s2=str1.translate(str.maketrans('','', string.punctuation))
print(s2)

# Exercise 16: Removal all characters from a string except integers
str1 = 'I am 25 years and 10 months old'
res = "".join([item for item in str1 if item.isdigit()])
print(res)


# Exercise 17: Find words with both alphabets and numbers
str1 = "Emma25 is Data scientist50 and AI Expert"
def task17(s):
    l = str1.split(' ')
    l2 = []
    a = False
    b = False
    for i in l:
        for j in i:
            if j.isdigit():
                a = True
            elif j.isalpha():
                b = True
            if a and b:
                print(i)
                a = False
                b = False
                break

task17(str1)

def task17_2(s):
    words = s.split()
    result = [word for word in words if any(c.isalpha() for c in word) and any(c.isdigit() for c in word)]
    return result

print(task17_2(str1))  # ➜ ['Emma25', 'scientist50']


# Exercise 18: Replace each special symbol with # in the following string
str1 = '/*Jon is @developer & musician!!'

def task18(s):
    s2 = ''
    for i in s:
        if i in string.punctuation:
            s2 += '#'
        else:
            s2 += i
    return s2

print(task18(str1))

s2 = ''.join('#' if i in string.punctuation else i for i in str1)
print(s2)

for char in string.punctuation:
    str1 = str1.replace(char, '#')



#