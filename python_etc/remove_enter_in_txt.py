# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:15:08 2019



@author: Donggeun Kwon (donggeun.kwon@gmail.com)

Cryptographic Algorithm Lab.
Graduate School of Information Security, Korea University

"""

def remove_enter_in_txt(filename='poly_opt.txt'):
    f = open(filename, mode='r')
    text = f.readlines()
    
    while(True):
        try:
            text.remove('\n') # '\n' << what we want to remove
        except:
            break
    
    f.close()
    
    f = open(filename[:-4]+'_removed.txt', mode='w')
    for i in text:
        f.write(i)
        
    f.close()
