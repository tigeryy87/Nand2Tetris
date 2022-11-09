"""
Author: Tiger Chen

Project 7: VM translator 1
"""

import re
import sys

def clean():
    '''remove comment, white space, and empty line'''
    # Take the command after python project0 " " as arguments
    enter  = sys.argv[1]
    file = enter.split('.')[0] + '_clean.asm'
    # Read the file 
    with open(enter, 'r') as f: 
        # Write to the .out file
        with open(file, 'w') as output:
            for line in f:
                # Remove comment after //
                remove_comment = re.sub(re.compile("//.*?\n" ) ,"" ,line)
                # Remove blank lines
                if remove_comment.strip():
                    # Remove trailing space               
                    new_file = remove_comment.strip()
                    output.write(new_file + '\n')  
    return str(file)

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

def segment_op(segment):
    """ Segment type """
    file_name = clean().split('_')[0]
    label = file_name.split('/')[-1]
    if segment == 'local':
        return 'LCL'
    elif segment == 'argument':
        return 'ARG'
    elif segment == 'this':
        return 'THIS'
    elif segment == 'that':
        return 'THAT'
    elif segment == 'temp':
        return 5
    elif segment == 'pointer':
        return 3
    elif segment == 'static':
        return str(label)


def operation3(line):
    """ Operation for three input, operator, segment and value"""
    line = line.split(' ')
    operator, segment, val1 = line[0], line[1], line[2]
    val = val1.split('\n')[0]
    instructions = []
    if operator == 'push':
        if segment == 'constant':
            instructions = [f'@{val}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        elif segment == 'static':
            instructions = [f'@{segment_op(segment)}{val}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        elif segment == 'temp' or segment == 'pointer':
            number = str(segment_op(segment)+ int(val))
            instructions = [f'@{number}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] 
        else:
            instructions = [f'@{segment_op(segment)}', 'D=M', f'@{val}', 'A=D+A', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    elif operator == 'pop':
        if segment == 'constant':
            raise ValueError('Error, constant can not come with pop')
        elif segment == 'static':
            instructions = ['@SP', 'M=M-1', 'A=M', 'D=M', f'@{segment_op(segment)}{val}', 'M=D']
        elif segment == 'temp' or segment == 'pointer':
            number = str(segment_op(segment)+ int(val))
            instructions = ['@SP', 'AM=M-1', 'D=M', f'@{number}', 'M=D']
        else:
            instructions = [f'@{segment_op(segment)}', 'D=M', f'@{val}', 'D=D+A', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
    
    instructions = '\n'.join(instructions)
    return instructions


def main(file=clean()):
    new_file = file.split('_')[0] + '.asm'
    with open(file, 'r') as f:
        with open(new_file, 'w') as output:
            for line in f:
                size = line.split(' ')
                if len(size) == 1:
                    output.write(operation1(line) + '\n')
                elif len(size) == 3:
                    output.write(operation3(line) + '\n')
                

if __name__ == '__main__':
    main()