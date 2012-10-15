#!/usr/bin/python
import sys
import argparse

def remove_prefix(prefix, line):
    if not line.startswith(prefix):
        return line
    return line[len(prefix):]
def remove_postfix(postfix, line):
    if not line.endswith(postfix):
        return line
    return line[:len(line)-len(postfix)]

def main(args):
    prefixes=[]
    for line in args.infile:
        postfix = line.lstrip(args.chars)
        prefix = remove_postfix(postfix, line)
        # Dedent
        dedented = False
        while not prefix.startswith(''.join(prefixes)):
            print("<"+prefixes.pop())
            dedented = True

        # Indent
        additional = remove_prefix(''.join(prefixes), prefix)
        if additional!="":
            if(dedented and args.must_match):
                print("Hanging indent or other mismatched indentation", file=sys.stderr)
                exit(1)
            prefixes.append(additional)
            print(">"+additional)

        # Nodent
        print("="+postfix,end="")
    while prefixes:
        print("<"+prefixes.pop())
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse hierarchical indentation into a flat, event-based file format")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-m', '--mismatched', dest='must_match', action='store_const', const=False, default=True, help='remove the strict hierarchy requirement and allow mismatched or "hanging" indentation')
    parser.add_argument('-w', '--whitespace', dest='chars', action='store', default=" \t", help='provide an alternate set of whitespace characters (default is spaces and tabs)')
    args = parser.parse_args()
    main(args)
