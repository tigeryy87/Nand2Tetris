"""
Author: Tiger Chen

Project 8: VM translator 
"""

import re
import sys
import os,glob

def clean(file):
    '''remove comment, white space, and empty line'''
    output = []
    for line in file:
        remove_comment = re.sub(re.compile("//.*?\n" ) ,"" ,line)
        # Remove blank lines
        if remove_comment.strip():
            # Remove trailing space               
            new_file = remove_comment.strip()
            output.append(new_file)  
    return output

counter = 0 

def operation1(word):
    """ Operation for only 1 operator"""
    word = word.split('\n')[0]
    instructions = []
    global counter 
    if word == 'add':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D+M']
    elif word == 'sub':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=M-D']
    elif word == 'or':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D|M']
    elif word == 'and':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D&M']
    elif word == 'not':
        instructions = ['@SP', 'A=M-1', 'M=!M']
    elif word == 'neg':
        instructions = ['@SP', 'A=M-1', 'M=-M']
    elif word == 'gt':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=M-D', 'M=-1', f'@CONTINUE{counter}', 'D;JGT', '@SP', 'A=M-1', 'M=0', f'(CONTINUE{counter})']
        counter += 1
    elif word == 'eq':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=M-D', 'M=-1', f'@CONTINUE{counter}', 'D;JEQ', '@SP', 'A=M-1', 'M=0', f'(CONTINUE{counter})']
        counter += 1
    elif word == 'lt':
        instructions = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=M-D', 'M=-1', f'@CONTINUE{counter}', 'D;JLT', '@SP', 'A=M-1', 'M=0', f'(CONTINUE{counter})']
        counter += 1
    instructions = '\n'.join(instructions)
    return instructions


def operation3(line, files):
    """ Operation for three input, operator, segment and value"""
    line = line.split(' ')
    label = {'local' : 'LCL', 'argument' : 'ARG', 'this' : 'THIS', 'that' : 'THAT', 'temp' : 5, 'pointer' : 3}
    operator, segment, val1 = line[0], line[1], line[2]
    val = val1.split('\n')[0]

    instructions = []
    if operator == 'push':
        if segment == 'constant':
            instructions = [f'@{val}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        elif segment == 'static':
            instructions = [f'@{files}{val}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        elif segment == 'temp' or segment == 'pointer':
            number = label[segment] + int(val)
            instructions = [f'@{number}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] 
        else:
            instructions = [f'@{label[segment]}', 'D=M', f'@{val}', 'A=D+A', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    elif operator == 'pop':
        if segment == 'constant':
            raise ValueError('Error, constant can not come with pop')
        elif segment == 'static':
            instructions = ['@SP', 'M=M-1', 'A=M', 'D=M', f'@{files}{val}', 'M=D']
        elif segment == 'temp' or segment == 'pointer':
            number = label[segment] + int(val)
            instructions = ['@SP', 'AM=M-1', 'D=M', f'@{number}', 'M=D']
        else:
            instructions = [f'@{label[segment]}', 'D=M', f'@{val}', 'D=D+A', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
    
    instructions = '\n'.join(instructions)
    return instructions



def operation2(line):
    """label, goto, if-goto"""
    line = line.split(" ")
    operator, label1 = line[0], line[1]
    label = label1.split('\n')[0]
    instructions = []
    if operator == 'label':
        instructions  = [f'({label})']
    elif operator == 'goto':
        instructions = [f'@{label}', "0;JMP"]
    elif operator == 'if-goto':
        instructions = ['@SP', 'AM=M-1', 'D=M', f'@{label}', 'D;JNE']
    instructions = '\n'.join(instructions)
    return instructions
    

def func(line):
    """method for the function """
    line = line.split(" ")
    funName, num1 = line[1], line[2]
    num = num1.split('\n')[0]
    instructions = [f'({funName})']
    for i in range(0, int(num)):
        instructions += ['@SP', 'A=M', 'M=0', '@SP', 'M=M+1']
    instructions = '\n'.join(instructions)
    return instructions, funName

ID = 0
def call(line, curr_fun):
    """method for call function"""
    global ID 
    line = line.split(" ")
    func, num1 = line[1], line[2]
    num = num1.split('\n')[0]
    return_address = [f'@{curr_fun}{ID}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']  
    push_lcl = ['@LCL', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    push_arg = ['@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    push_this = ['@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']  
    push_that = ['@THAT', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    arg_sp = ['@SP', 'D=M', f'@{int(num) + 5}', 'D=D-A', '@ARG', 'M=D'] 
    lcl_sp = ['@SP', 'D=M', '@LCL', 'M=D']
    goto_f = [f'@{func}', '0;JMP', f'({curr_fun}{ID})'] 
    instructions = '\n'.join(return_address + push_lcl + push_arg + push_this + push_that + arg_sp + lcl_sp + goto_f)
    ID += 1
    return instructions
    
def return_func(word):
    """method to return function"""
    word = word.split('\n')[0]
    frame_lcl = ['@LCL', 'D=M', '@FRAME', 'M=D']
    ret = ['@FRAME', 'D=M', '@5', 'A=D-A', 'D=M', '@RET', 'M=D']
    arg_pop = ['@SP', 'AM=M-1', 'D=M', '@ARG', 'A=M', 'M=D']
    sp_arg = ['@ARG', 'D=M+1', '@SP', 'M=D']
    that = ['@FRAME', 'A=M-1', 'D=M', '@THAT', 'M=D']
    this = ['@FRAME', 'A=M-1', 'A=A-1', 'D=M', '@THIS', 'M=D']
    arg_frame = ['@FRAME', 'A=M-1', 'A=A-1', 'A=A-1', 'D=M', '@ARG', 'M=D']
    lcl = ['@FRAME', 'A=M-1', 'A=A-1', 'A=A-1', 'A=A-1', 'D=M', '@LCL', 'M=D']
    goto_ret = ['@RET', 'A=M', '0;JMP']
    instructions = '\n'.join(frame_lcl + ret + arg_pop + sp_arg + that + this + arg_frame + lcl + goto_ret)
    return instructions

def boot():
    instructions = ['@256', 'D=A', '@SP', 'M=D']
    instructions = '\n'.join(instructions) + '\n'
    instructions += call("call Sys.init 0", 'bootstrip')
    return instructions

def main():
    enter  = sys.argv[1]
    foldername = enter.split('/')[-1] 
    newfile = enter + '/' + foldername + '.asm'
    output = open(newfile, 'w')
    output.write(boot() + '\n')
    for filename in glob.glob(os.path.join(enter, '*.vm')):
        print(filename)
        files = filename[:-3].split('/')[-1]
        with open(filename, 'r') as f:
            clean_line = clean(f)
            for line in clean_line:
                size = line.split(' ')
                if len(size) == 1:
                    if size[0] == "return":
                        output.write(return_func(line) + '\n')
                    else:
                        output.write(operation1(line) + '\n')
                elif len(size) == 2:
                    output.write(operation2(line) + '\n')                
                elif len(size) == 3:
                    if size[0] == "function":
                        a, b = func(line)
                        output.write(a + '\n')
                    elif size[0] == 'call':
                        output.write(call(line, b) + '\n')
                    else:
                        output.write(operation3(line, files) + '\n')
    output.close()    
                

if __name__ == '__main__':
    main()