#ROT13 tutorial
#(C)2008 Robin Wellner (gvx): I placed this in Public Domain
#Level: 2 (Medium)

#This script defines two functions:
# * rotn(intext, n), a generalised ROT function
# * rot13(intext), the same as rotn(intext, 13)

#From Wikipedia:
#ROT13 ("rotate by 13 places", sometimes hyphenated ROT-13) is a simple
#substitution cipher [...]. ROT13 is a variation of the Caesar cipher,
#developed in ancient Rome.

#A lookup table for ROT13:
#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
#NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm

def rotn(intext, n):
#The output is accumulated in a list, before returning a string
#constructed from that list:
    outtext = []
#Iterating over all characters in the string:
    for char in intext:
#Information needed for understanding this:
# * ord(char) returns the ASCII-code of char
# * ord('A') == 65, ord('Z') == 65+26
# * 65 <= ord(char) < (65+26) is effectively "if char is an upper case letter"
        if 65 <= ord(char) < (65+26):
#chr(i) returns the character with ASCII-code of i
#so, chr(65) returns 'A', and chr(ord(x)) == x
            char = chr(((ord(char) - 65) +n) % 26 + 65)
#Let's just spread that out:
#            char = chr(
#                       (
#                        (ord(char) - 65)
#                                         + n)
#                                              % 26 + 65)

#And this is just the same as the above, only ord('a') == 97
#So this is the code for lower case letters:
        elif 97 <= ord(char) < (97+26):
            char = chr(((ord(char) - 97) +n) % 26 + 97)
#This is a simple trick: if char was a letter, this code appends
#the ROTn'ed char (so 'A' becomes 'N', etc.)
#But any other character stays the same ('.', '0', '+' and anything
#not a letter)!
        outtext.append(char)
#Now, the list is joined to a ROTn'ed string, which is returned:
    return ''.join(outtext)

def rot13(intext):
    return rotn(intext, 13)