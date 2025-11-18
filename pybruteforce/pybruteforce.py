'''


@author: Donggeun Kwon (donggeun.kwon@gmail.com)
Last updated 2025.11.18.

'''
import itertools
import string
import sys
import math

import pyautogui
from tqdm import tqdm


warning_script = """
Before using this program, read the following warning carefully 
and confirm that you understand it.
---

!!! WARNING !!!

This program is intended only for authorized security testing. 
Do not use it in any environment that has not been explicitly 
approved. You must verify that the developer or the responsible 
organization of the target system has granted clear prior 
permission. Unauthorized use may violate applicable laws and 
any resulting consequences are the sole responsibility of the user.
"""


def brute_force(pass_len):
    ### combination of 
    # (1) ascii letters (2) digits (3) special characters
    charset = string.ascii_letters + string.digits + string.punctuation
    total_iterations = len(charset) ** int(pass_len) 

    for attempt in tqdm(itertools.product(charset, repeat=int(pass_len)), 
                                                   total=total_iterations):
        guess = ''.join(attempt)

        ### filtering
        # digit_count = sum(c.isdigit() for c in guess)
        # if digit_count in {1, 2, 3}: yield guess

        pyautogui.write(guess)
        pyautogui.hotkey('enter')
        
        ### set the button click
        # pyautogui.moveTo(100, 200)
        # pyautogui.click(button='left')

    return None

def main():
    if sys.argv[1] == '-h':
        print("python pybruteforce.py [password try length]\n")
        print("Your display size is : ", pyautogui.size())
        print("Your mouse is in     : ", pyautogui.position())
        return None

    # warning
    print(warning_script)
    sure_str = input("Do you understand and accept this warning before proceeding? (yes/no)\n")
    if (sure_str!='yes'): 
        exit()

    # check input (password length)
    try:
        pass_len = int(sys.argv[1])
    except Exception as e:
        print(f"Password length input error: {e}") 
        return None

    # try brute force attack
    brute_force(pass_len)
    
    return None


if __name__ == '__main__':
    main()