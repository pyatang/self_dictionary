# coding:utf-8
# 自制词典
# 1.存储单词释义
# 2.查询
# 3.添加n
# 4.用SQLite 存储

import sys
import sqlite3

# initial dictionary with 370101 english words with id

    

# manipulate the dictionary which exist
class dictionary:
    
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
        
    def update(self, update_definition):
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()
        update_word = (update_definition, self.word)
        print(self.word)
        print(update_definition)
        c.execute('UPDATE dictionary SET definition=? WHERE word=?', update_word)
        conn.commit()
        print('UPDATE SUCCESSFUL')
        c.close()
        
    def query(self, query_word = 'a'):
        conn = sqlite3.connect('atang_dictionary.db')
        c = conn.cursor()
        # result = c.execute("SELECT Chinese_definition FROM dictionary WHERE word=?", query_word)
        while True:
            # c.execute('SELECT * from dictionary WHERE word=?', query_word)
            if c.fetchone() is not None:
                print(c.fetchone())
                print(c.fetchone()[2])
            else:
                print('Sorry there is no {} definition!'.format(self.word))
                print('*'*99)
                print('Please add the meaning of this word.')
                definition = input()
                self.update(definition)
            break
            
        c.close()
        
        
if __name__ == "__main__":
    # 开始时实例对象没有传递参数
    new_dictionary = dictionary(sys.argv[1])
    
    new_dictionary.query()
 
    
    
    