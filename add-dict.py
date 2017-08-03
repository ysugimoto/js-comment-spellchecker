import os
import sys

rcFile = os.environ['HOME'] + '/.jcsrc'

def read_rc_file():
    whiteListWords = []
    if os.path.exists(rcFile) == False:
        return whiteListWords

    fp = open(rcFile, 'r')
    words = fp.readlines()
    for w in words:
        whiteListWords.append(w.strip('\r\n'))
    fp.close()

    return whiteListWords

def write_rc_file(whiteListWords):
    with open(rcFile, 'a') as file:
        file.write('\n'.join(whiteListWords))

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        sys.exit('Add words must be supplied at least one.')

    whiteListWords = read_rc_file()
    appendWords = list(filter(lambda w:w not in whiteListWords, args[1:]))

    if len(appendWords) == 0:
        sys.exit('Nothing to add dictionary words.')
    else:
        write_rc_file(appendWords)

    print('Added to dictionary!')



