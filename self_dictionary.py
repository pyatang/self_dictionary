# coding:utf-8
# 自制词典
# 1.存储单词释义
# 2.查询
# 3.添加n
# 4.用SQLite 存储

''' self_dictionary

This script allows user to look up English word and update the meaning

This tool accept one word look up each time 

'''


import sys
import sqlite3

# initial dictionary with 370101 english words with id

    
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def help_file():
     
    '''\n
    Introduction to self_dictionary.py 
    Use -h --help to open the this Help file
    query function to look up and update definition when there is no definition.
    '''
    print('This help function.')



# manipulate the dictionary which exist
class dictionary:
    ''' Dictionary docstring '''
    
    def __init__(self, word=None, Chinese_definition=None):
        self.word = word
    
    def init_dictionary(self):
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE dictionary
                     (id, word, definition, Chinese_definition)''')

        with open("words_alpha.txt") as f:
            read_word = f.readlines()
        
        word_list = []
        for i in range(len(read_word)):               # read word from text add index to each word, make a tuple then a word list, then insert to sqlite3 database
            word_id = i+1
            word =read_word[i].strip('\r\n')                            
            definition = ''
            Chinese_definition = ''
            word_tuple = (word_id, word, definition, Chinese_definition)
            word_list.append(word_tuple)
        
        
        c.executemany('INSERT INTO dictionary(id, word, definition, Chinese_definition) VALUES (?,?,?,?)', word_list)
        conn.commit()           # 由于没有提交 commit() 耽误了1个小时

        c.close()

    # experimental code for manipulate sqlite3
    def create(self):
        # create a dictionary for store initial word
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE dictionary
                    (id, word, definition, Chinese_definition)''')
        # Insert a row of data
        c.execute("INSERT INTO dictionary VALUES (1,'aha','express feeling','顿悟时的情绪表达词语')")
        # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
       
        

    def insert(self, insert_definition):
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()
        insert_word = (self.word, insert_definition)
        c.execute('INSERT INTO dictionary (word, definition) VALUES(?, ?)', insert_word)
        conn.commit()
        print('INSERT SUCCESSFUL')
        c.close()
    
    def delete(self):
        print('This is delete method')
       

    def update(self, update_def_cn=None, update_def_en=None):
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()
        update_def_cn = (update_def_cn, self.word)
        update_def_en = (update_def_en, self.word)

        c.execute('UPDATE dictionary SET definition=? WHERE word=?', update_def_en)
        conn.commit()
        # print('UPDATE English definition SUCCESSFUL')
        c.execute('UPDATE dictionary SET Chinese_definition=? WHERE word=?', update_def_cn)
        conn.commit()
        # print('更新中文释义成功')
        print("更新成功")
        c.close()

        
    def query(self, query_word):
        
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()
        
        # 开始没有理解完全 fetchone() 这个方法，它取的是sql查询后的集合的下一行序列数据。所以每次执行 c.execute() 语句后，cursor的位置会往下移动一行。因此，在每次需要取值的时候需要重新执行 c.execute() 语句
        c.execute("SELECT * FROM dictionary WHERE word=?", (query_word,))
        retrieve_word = c.fetchone()
        if retrieve_word is not None:
            def_en = retrieve_word[2]
            def_cn = retrieve_word[3]
            
            # 刚开始以为 fetchone()[2] 返回的None这个值，判断语句一直出问题，经过几次print语句的调试后，才发现 fetchone()[2] 返回的是str类型的空字符串 '', 修改后判断正确。
            if def_en != '' and def_cn != '' :
                # get english definition
                print("Enlish: {}".format(def_en))
                print("中  文: {}".format(def_cn))
        
                # get Chinese definition                
                
            elif def_en != '' and def_cn == '': 
                print("没有中文释义，请更新")
                Chinese_definition = input()
                self.update(update_def_cn=Chinese_definition, update_def_en=def_en)

            elif def_en == '' and def_cn != '' :
                print("No English definition, please update")
                definition = input()
                self.update(update_def_en=definition, update_def_cn=def_cn)

            else:
                print("既无中文含义，也无英文含义")
                print("输入中文含义")
                Chinese_definition = input()
                print("Input English definition")
                definition = input()
                self.update(update_def_en=definition, update_def_cn=Chinese_definition)
        else:
            print("词库没有这个单词!")
            
        c.close()

def main():
            
    # 开始时实例对象没有传递参数
    new_dictionary = dictionary(sys.argv[1])
    new_dictionary.query(sys.argv[1])
        
if __name__ == "__main__":
    main()
 
    
    
    
