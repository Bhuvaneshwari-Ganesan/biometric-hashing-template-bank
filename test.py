import os
import random


class split_and_store():
    def read_text_data(self,fname):
        a1=""
        a2=""
        a3=""
        a4=""
        a5=""
        x1=os.path.join("data/", fname+".txt")

        with open(x1) as f1:
            a1 = f1.readlines()


    def split_file(self,txt,id):
        letters_and_digits = txt
        result_str = ''.join((random.choice(letters_and_digits) for i in range(5)))
        lst = []
        for i in result_str:
            lst.append(i)
        result = []
        for x in lst:
            temp = txt.split(x)
            tmp1 = len(temp)
            if tmp1 < 2:
                result.append(temp[tmp1 - 1])
            else:
                result.append(str(temp) + str(tmp1))
        dir1 = 'data'


        if not os.path.exists(dir1):
            os.makedirs(dir1)

        file1 = os.path.join(dir1, (str(id) + ".txt"))


        f = open(file1, 'w')
        f.write(txt)
    def generte_key(self,s):
        min = pow(10, s - 1)
        max = pow(10, s) - 1
        return random.randint(min, max)


    def encrypt(self,message, key=20):
        # print(message)
        LETTERS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
        LETTERS = LETTERS.lower()
        encrypted = ''
        for chars in message:
            if chars in LETTERS:
                num = LETTERS.find(chars)
                num += key
                encrypted += LETTERS[num]
        # print(encrypted)
        return encrypted

    def decrypt(self,message, key=20):
        # print(message)
        LETTERS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
        LETTERS = LETTERS.lower()
        encrypted = ''
        for chars in message:
            if chars in LETTERS:
                num = LETTERS.find(chars)
                num -= key
                encrypted += LETTERS[num]
        # print(encrypted)
        return encrypted








