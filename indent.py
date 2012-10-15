#!/usr/bin/python
# Exit codes are
#   1 for syntactic error
#   2 for semantic error
import sys
import argparse

def main(args):
    prefixes=[]
    prefix_linenums=[]
    linenum = 0
    for line in args.infile:
        linenum += 1
        if line[0]=="=":
            print(''.join(prefixes)+line[1:],end="")
        elif line[0]==">":
            prefixes.append(line[1:-1]) #TODO:generic line end support
            prefix_linenums.append(linenum)
        elif line[0]=="<":
            if not prefixes:
                print("Dedent with no corresponding indent on line {0}".format(linenum),file=sys.stderr)
                exit(2)
            elif prefixes[-1]==line[1:-1]:
                prefixes.pop()
            else:
                print("Indent and dedent do not match on lines {0},{1}".format(prefix_linenums[-1], linenum),file=sys.stderr)
                exit(2)
        else:
            print("Invalid event character",file=sys.stderr) # Event codes are basically the versioning system, so make sure not to add a default action without changing that
            print(line)
            exit(1)
    exit(0) # Be liberal; don't require all dedents at end

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse hierarchical indentation into a flat, event-based file format")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    main(args)
