import os, sys, getopt

gbk = 'gbk'
utf8 = 'utf8'

args = dict()
args['source_enc'] = gbk
args['target_enc'] = utf8

def convert_path(path):
    size = 0
    if os.path.isdir(path):
        subpaths = os.listdir(path)
        for name in subpaths:
            subpath = os.path.join(path, name)
            size += convert_path(subpath)
    else:
        if convert_file(path):
            size = 1
               
    return size

def convert_file(path):
    result = False
    try:
        f = open(path, 'r', encoding=args['source_enc'])
        t = f.read()
        f.close()
        f = open(path, 'w', encoding=args['target_enc'])
        f.write(t)
        f.close()
        if args['verbose'] :
            print('|  ' + path)
        result = True
    except:
        result = False
    finally:
        return result

def usage():
    print('Usage: python3 convert.py [options...] [input_path...]')
    print('This script Converts text encoding between gbk and utf8, and')
    print('the default input path is the current working directory.')
    print('  -h, --help       Show this message.')
    print('  -v, --verbose    Print all paths of converted text files.')
    print('  -e, --encoding   Specify the target encoding, gbk or utf8,') 
    print('                   the default value is utf8.')
    print('')
    

def args_parse():
    try:
        print(sys.argv[1:])
        opt_list, paths = getopt.getopt(sys.argv[1:], 'hve:', ['help', 'verbose', 'encoding='])
        print(opt_list)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(-1)
  
    args['verbose'] = False
    for opt, arg in opt_list:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        if opt in ('-v', '--verbose'):
            args['verbose'] = True
        if opt in ('-e','--encoding'):
            args['target_enc'] = arg
    if args['target_enc'] in (None, gbk, utf8) :
        if args['target_enc'] == gbk:
            args['target_enc'] = gbk
            args['source_enc'] = utf8
        else:
            args['target_enc'] = utf8
            args['source_enc'] = gbk
    else:
        usage()
        sys.exit('Invalid encoding !')
    
    if len(paths) > 0:
        args['paths'] = paths
    else:
        args['paths'] = [os.getcwd()]

def main():
    args_parse()
    if args['target_enc'] == gbk:
        print('|Start converting: utf8 => gbk')
    else:
        print('|Start converting: gbk => utf8')
    nTotal = 0
    for path in args['paths']:    
        if os.path.exists(path):
            nTotal += convert_path(path)
    print('|Totally %d files converted.' % nTotal)

if __name__ == '__main__':
    main()
