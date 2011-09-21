import sys
import argparse


def Cli():
    verbose = False
    debug = False
    cpp = True



def main():
    parser = argparse.ArgumentParser(description='Generate Wireshark'
            ' dissectors from C structs.')

    # C-header file
    parser.add_argument('-ch', '--cheader', nargs='*',
            help='C-header file to parse', metavar='HEADER')

    # Configuration file
    parser.add_argument('-c', '--config', nargs='*',
            action='store',help='Configuration file')

    # Write output to destination file
    parser.add_argument('-output', nargs='*', help='Write output to file')

    # Verbose flag
    parser.add_argument('-v', '--verbose', action='store_true',
            dest='verbose', help='Print information about AST tree, ect.')

    # Debug flag
    parser.add_argument('-d', '--debug', action='store_true',
            dest='debug', help='Enable debugger')

    # No CPP flag
    parser.add_argument('-nocpp', action='store_false',
            dest='cpp', help='Disable C preprocessor')


    args = parser.parse_args()
    parser.print_usage()


if __name__ == "__main__":
    main()

