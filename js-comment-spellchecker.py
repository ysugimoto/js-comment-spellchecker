import sys
import re
import os
import glob
from functools import reduce

import enchant
import pyparsing

# Parse comments in JavaScript content
class JavaScriptCommentParser:

    # Parse from supplied file content
    def parseFile(self, filePath):
        fp = open(filePath, 'r')
        contents = fp.read()
        fp.close()
        return self.parseComment(contents)

    # Parse comment list from string
    def parseComment(self, content):
        comments = []
        for match in pyparsing.javaStyleComment.scanString(content):
            words = re.findall('[a-zA-Z]+', match[0][0])
            comments.append(words)

        return comments


# Spellcheck executor
class SpellChecker:
    def __init__(self):
        self.checker = enchant.Dict('en_US')

    # Check words
    def check(self, comments, whiteList):
        suggestList = []

        for words in comments:
            words = filter(lambda w:w not in whiteList, words)
            for word in words:
                if self.checker.check(word):
                    continue

                suggestList.append({
                    'word': word,
                    'suggest': self.checker.suggest(word)
                    })

        return suggestList

def get_white_list_words():
    whiteListWords = []
    rcFile = os.environ['HOME'] + '/.jcsrc'
    if os.path.exists(rcFile) == False:
        return whiteListWords

    fp = open(rcFile, 'r')
    whiteListWords.append(fp.readline(64).strip('\r\n'))
    fp.close()

    return whiteListWords

# Glob file list
def file_list(base):
    if os.path.isdir(base):
        base = base + '/**/*.js'
        return glob.glob(base, recursive=True)
    elif os.path.isfile(base):
        return [base]
    else:
        return None


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        sys.exit('Target file must supplied')

    print('Finding target files')

    fileList = file_list(argv[1])

    if fileList == None:
        sys.exit('%s is invalid or not found' % argv[1])

    for f in fileList:
      jsc = JavaScriptCommentParser()
      comments = jsc.parseFile(f)
      sc = SpellChecker()
      result = sc.check(comments, get_white_list_words())

      if len(result) == 0:
          continue

      maxWordLen = reduce(lambda a,b:max(a, len(b['word'])), result, 0)

      print('Suggestion found in %s' % f)
      print('')
      for r in result:
          fmt = '%' + str(maxWordLen) + 's -> "%s"'
          print(fmt % (r['word'], ', '.join(r['suggest'])))
      print('')
      print('===========================')
      print('')




