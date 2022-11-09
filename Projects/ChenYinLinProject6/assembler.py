"""
Author: Tiger Chen

Project 6: assembler
"""
import sys
import re


symbol_table = {
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9,
    'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576,
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4
}

comp_table = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000",
    "!D": "0001101", "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111",
    "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001",
    "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011",
    "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"
}

dest_table = { "null": "000", "M": "001", "D": "010", "A": "100", "MD": "011",
    "AM": "101", "AD": "110", "AMD": "111" }

jump_table = { "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

next_variable = 16

def clean():
    '''remove comment, white space, and empty line'''
    # Take the command after python project0 " " as arguments
    enter  = sys.argv[1]
    file = enter.split('.')[0] + '_clean.asm'
    print("File: ", enter)
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

def symbol_handling(file=clean()):
    """Handle the symbol with (), transfer into line number and put into symbol table"""
    line_number = 0
    new_file = file.split('_')[0] + '_new.asm'
    with open(file, 'r') as f:
        with open(new_file, 'w') as output:
            for line in f:
                if line[0] == '(':
                    label = line[1:-2]
                    symbol_table[label] = line_number
                else:
                    line_number += 1
                    output.write(line)
    return new_file

def add(label):
    '''Add the next variable into the symbol table, start from 16'''
    global next_variable
    symbol_table[label] = next_variable
    next_variable += 1
    return symbol_table[label]

def instruction_A(line):
    """Transfer instuction A symbol into binary number"""
    first = line[1]
    if first.isnumeric():
        val = int(line[1:])
    else:
        label = line[1:-1]
        val = symbol_table.get(label, -1)
        if val == -1:
            val = add(label)
    return '{0:016b}'.format(val)
    
def generalize_instr_c(line):
    """Generalize instruction C by adding null, if there is no '=' or ';' """
    new_line = ''
    if not '=' in line:
        new_line = 'null=' + line[:-1]
    if not ';' in line:
        new_line = line[:-1] + ';null'
    return new_line

def instruction_C(line):
    """Transfer instuction C symbol into binary number, dest=comp;jump"""
    new_line = generalize_instr_c(line)
    print(new_line)
    dest = new_line.split('=')
    bin_dest = dest_table.get(dest[0], 'no found')
    comp = dest[1].split(';')
    bin_comp = comp_table.get(comp[0], 'no found')
    bin_jump = jump_table.get(comp[1], 'no found')
    instr_c = '111' + bin_dest + bin_comp + bin_jump
    return instr_c

def assemble():
    """Read the file, if line starts with @, use instruction A. If not, use instruction C"""
    file = symbol_handling()
    with open(file, 'r') as f:         
        with open(file.split('_')[0] + '.hack', 'w') as output:
            for line in f:
                if line[0] == '@':
                    transfer = instruction_A(line)
                else:
                    transfer = instruction_C(line)
                output.write(transfer + '\n')

def main():
    assemble()
    #print(symbol_table)

if __name__ == '__main__':
    main()

