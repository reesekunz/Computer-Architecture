# Tip: Think of it as a boolean changing from True to False. 0 represents False and 1 represents True.

# NOT operator is '~' (called a tilde). 
a = 1
~a == 0

a = 0
~a ==1

# AND operator is '&' (called an ampersand). 

a = 0
b = 0
a & b == 0

a = 1
b = 0
a & b == 0

a = 1
b = 1
a & b == 1

# OR operator is '|' (called a pipe).

a = 0
b = 0
a | b == 0

a = 1
b = 0
a | b == 1

a = 1
b = 1
a | b == 1

# NAND operator can be made with '~' and '&'. (opposite of AND. Not AND = NAND)

a = 0
b = 0
~(a & b) == 1

a = 1
b = 0
~(a & b) == 1

a = 1
b = 1
~(a & b) = 0

# NOR operator can be made with '~' and '|' (opposite of OR. Not OR = NOR)

a = 0
b = 0
~(a | b) = 1

a = 1
b = 0
~(a | b) = 0

a = 1
b = 1
~(a | b) = 0

# XOR operator is '^' (called an caret). Exclusive OR. Only true if one of the OR's is True, but NOT both.

a = 0
b = 0
a ^ b = 0

a = 1
b = 0
a ^ b = 1

a = 1
b = 1
a ^ b = 0

# Multi bit numbers
# Add up the 1 and 0's in each place value depending on which operation is being performed.

  11101011
& 10011101
----------
  10001001

  11011010
^ 11100011
----------
  00111001

    11010110
&   11110000
------------
    11010000

# Shifting bits left or right with <<  >>

1111 
<<1
-----
11110

1111
>>1
----
111


################ GUIDED PROJECT NOTES

AND    &&    &
OR     ||    |
NOT    !     ~  # unary operator 
XOR   N/A    ^

#1.
    0b 1010 1010
&   0b 0111 0111
----------------
     0b 0010 0010 # only return 1 if BOTH are TRUE since & 

# converting binary to decimal for sake of practice
0b 1010 1010 = 170
0b 0111 0111 = 119
170 & 119 = 34

0b 0010 0010 = 34

#2. 

    0b 1010 1010
|   0b 0111 0111
----------------
     0b 1111 1111 # only return 1 if EITHER are TRUE since |

#3. 
   ~ 0b 1010 1010
   ---------------
   0b 0101 0101

#4. XOR - exclusive OR

    0b 1010 1010
^   0b 0111 0111
-----------------
    0b 1101 1101 # only return 1 if EITHER are TRUE but NOT BOTH since ^ (used in cypto)



# SHIFTING
# Left shift: add 0s to right (everything else stays same)
# Right shift: add 0s to left (chop off whatever doesnt make it)

# Right Shift

# Tip when shifting to the right (>>). Add 0's starting from the left however many values you're shifting and work your way from left->right. Whatever values that don't make it at the end are cut off.
 
#1.

0b 1110 >> 1 # move all the values over 1 to the right. 
0b 0111

# another way to put this in decimal: 
# 14 >> 1 = 7

#2. 

0b 1110 >> 2 # move all the values over 2 to the right
0b 0011 

#3. 
0b 1110 >> 3 # move all the values over 3 to the right
0b 0001 

# another way to put this in decimal: 
# 14 >> 3 = 1

# Left  Shift

# Tip when shifting to the left(<<). Add 0's at the end, everything else remains untouched.

#4. 
0b 1110 << 1
0b 11100

#5. 
0b 1110 << 3
0b 1110000

# MASKING

#6. ADD 10100000
pc += 1 + num_operands
# want to grab the first two bits (10), which are the num_operands.
# Do this by right shifting by 6.
x = 0b10100000
x >> 6
0b10 

#7. Grab 3rd value out of ADD 10100000 (1). 
# masking - using & to get rid of anything that were not interested in.
    0b10100000
&   0b00100000 # only put a 1 in the place value you want to grab (since both have to be 1 to be returned)
---------------
    0b00100000

0b00100000 >> 5
0b01

# Grab 4th value out of ADD 10100000 (0).

    0b10100000
&   0b00010000
--------------
    0b00000000

0b00000000 >> 4
0b00

## Example related to project
IR = 0b10100000
add_to_pc = (IR >> 6) + 1








































