import re
import myFile
import string
import math


class staticWord:
    visited=False
    countlines=0
    check=0
    strcheck=False

def tokenize(path):
    try:
        f = open(path).read()
        lines = f.split("\n")
        count = 0
        for line in lines:
            count = count + 1
            staticWord.countlines=count
            tokens = correctTheDelimeter(line)
            print("\nProgram LINE No is : ", count)
            print("Tokens in this Line: ", tokens)
            for token in tokens:
                if len(token)!=0:
                  mainCheck(token)
        return True
    except FileNotFoundError:
        print("\nGiven path is invalid. Please try Again")
        run()


def run():
    path = input("Enter Path of your code: ")
    tokenize(path)
    again = int(input("""\n1. Retry\n2. Quit\n"""))
    if again == 1:
        run()
    elif again == 2:
        print("Quitting...")
    else:
        print('Invalid Request.')
        run()

def is_float_partition(element):
    partition=element.partition('.')
    if (partition[0].isdigit() and partition[1]=='.' and partition[2].isdigit()) or (partition[0]=='' and partition[1]=='.' and partition[2].isdigit()) or (partition[0].isdigit() and partition[1]=='.' and partition[2]==''):
        return True
    else:
        return False

def checkHader(strng):
    length=len(strng)
    pos=strng.find(".h>",(length-5),length)
    if pos!=-1 :
        return True
    else:
        return False

def checkIdentifier(token):
    first=0
    if not token.strip():
        return False
    for c in token:
        if first==0 and not (c.isalpha()):
            return False
        elif not( c.isalpha() or c.isdigit() or  c=="$"):#  or c=="'" or c=='"' ):
            return False
        first=first+1
    return True





def checkComment(token):
    if  (not "*//" in token and staticWord.visited==True) or staticWord.check==staticWord.countlines:
            print(token+"  Commented Line")
    elif "///" in token:
            pos=token.find("/")
            beforePos=token[:pos]
            afterPos=token[pos:]
            if len(beforePos)!=0 and beforePos in myFile.keywords():
                print(beforePos+"  Keyword")
            elif len(beforePos)!=0:
               checkOperator(beforePos)
            print(afterPos+"   Single Line Comment")
            staticWord.check=staticWord.countlines
    elif "//*" in token and "*//" in token:
            pos=token.find("//*")
            beforePos=token[:pos]
            afterPos=token[pos:]
            pos2=afterPos.find("*//")
            cmnt=afterPos[:pos2+3]
            endofcmnt=afterPos[pos2+3:]
            if len(beforePos)!=0 and beforePos in myFile.keywords():
                print(beforePos+"  Keyword")
            elif len(beforePos)!=0:
               checkOperator(beforePos)
            print(cmnt+"   Multiline Line Comment")
            if len(endofcmnt)!=0 and endofcmnt in myFile.keywords():
                print(endofcmnt+"  Keyword")
            elif len(endofcmnt)!=0:
                checkOperator(endofcmnt)
    elif "//*" in token:
            pos=token.find("/")
            beforePos=token[:pos]
            afterPos=token[pos:]
            if len(beforePos)!=0 and beforePos in myFile.keywords():
                print(beforePos+"  Keyword")
            elif len(beforePos)!=0:
               checkOperator(beforePos)
            print(afterPos+"  Start of Multiline Line Comment")
            staticWord.visited=True
    elif "*//" in token:
            pos=token.find("*//")
            beforePos=token[:pos+3]
            afterPos=token[pos+3:]
            print(beforePos+"  End of Multiline Line Comment")
            if len(afterPos)!=0 and afterPos in myFile.keywords():
                print(afterPos+"  Keyword")
            elif len(afterPos)!=0:
               checkOperator(afterPos)
            staticWord.visited=False
    else:
        pass
    
def checkString(token):
        length=len(token)
        if token[length-1]=='"' and staticWord.strcheck==True:
            staticWord.strcheck=False
            return True
        if token[0]=='"' or staticWord.strcheck==True:
            staticWord.strcheck=True
            return True

        return False
def checkNext(item,token):
    item1=""
    try: 
        if (item=='>'):
            if(token[0]=='='):
               item1=">=" 
        elif(item=='<'):
            if(token[0]=='='):
               item1="<="
        elif(item=='='):
            if(token[0]=='='):
               item1="=="
        elif(item=='&'):
            if(token[0]=='&'):
               item1="&&"
        elif(item=='|'):
            if(token[0]=='|'):
               item1="||"
    except IndexError:
        pass    

    if len(item1)!=0 :
        print(item1 +" " + myFile.opDelim()[item1])
        afteritem1operator=token[0+1:]
        checkOperator(afteritem1operator)
    else:
        print(item +" " + myFile.opDelim()[item])
        checkOperator(token)



def checkOperator(token):
        c=0
        beforeOperator=""
        for item in token:
            if item in myFile.opDelim().keys():     
                position = token.find(item)
                beforeOperator = token[:position]
                AfterOperator = token[position + 1 :]
                if(beforeOperator in myFile.keywords()):
                     print(beforeOperator +"  Invalid Position Of Keyword")
                elif(checkIdentifier(beforeOperator)):
                     print(beforeOperator +" Identifier")
                elif(is_float_partition(beforeOperator)):
                     print(beforeOperator+" Float")
                elif(beforeOperator.isdigit()):
                     print(beforeOperator+" Int")
                elif len(beforeOperator)!=0:
                     print(beforeOperator+" Invalid token")
             #   print(item +" " + myFile.opDelim()[item])
                c=c+1
             #   checkOperator(AfterOperator)
                checkNext(item,AfterOperator)
                break
            else:
                pass
        if(c==0):
             if(beforeOperator in myFile.keywords()):
                print(beforeOperator +"  Invalid Position Of Keyword")
             elif(checkIdentifier(token)):
                print(token+" Identifier")
             elif token.isdigit():
                print(token+" Int")
             elif (is_float_partition(token)):
                print(token+" Float")
             elif len(token)!=0:
                print(token+" Invalid Token")
                    
         

         
         

def mainCheck(token):
    if "///" in token or "///"==token or "//*" in token or "*//" in token or staticWord.visited==True or staticWord.countlines==staticWord.check: 
       checkComment(token)
    elif(checkString(token)):
        print(token+"  String")
    elif token in myFile.keywords():        
       print(token + " KEYWORD") 
    elif token in myFile.operators().keys():
       print(token + " ", myFile.operators()[token])
    elif token in myFile.delimiters().keys():
        description = myFile.delimiters()[token]
        if description == 'TAB' or description == 'NEWLINE':
            print(description)
        else:
           print(token + " ", description)
    elif (checkHader(token)):
        print(token + " HEADER")
       
    elif token.isdigit():
        print(token + "  Int")
    elif (is_float_partition(token)):
        print(token + "  Float")
  #  elif(checkString(token)):
  #      print(token+"  String")
    elif token:
         checkOperator(token)
    return True




def correctTheDelimeter(line):
    tokens = line.split(" ")              
    for token in tokens:
        if checkWhiteSpace(token):
            tokens.remove(token)
        elif ' ' in token:
            tokens.remove(token)
            token = token.split(' ')
            for d in token:
                tokens.append(d)
    return tokens

def checkWhiteSpace(word):
    return word in [" ", "\t", "\n"]




run()