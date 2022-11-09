"""

Tiger Chen

Project 0

"""
import sys
import re

def strip():

    # Take the command after python project0 " " as arguments
    enter  = sys.argv[1]
    print("Argument: ", enter)

    # Read the file 
    with open(enter, 'r') as f: 
        # Write to the .out file
        with open(enter.split('.')[0] + '.out', 'w') as output:
            for line in f:
                # Remove comment after //
                remove_comment = re.sub(re.compile("//.*?\n" ) ,"" ,line)
                # Remove blank lines
                if remove_comment.strip():
                    # Remove trailing space               
                    new_file = remove_comment.strip()
                    output.write(new_file + '\n')            
    
def main():
    strip()

if __name__ == '__main__':
    main()