import unittest
import os
from multiprocessing import Process
import time
# import utils
from client import *


def run_registry():
    os.system('python registry.py')

def run_server1():
    os.system('python server.py 50001')

def run_server2():
    os.system('python server.py 50002')

def run_server3():
    os.system('python server.py 50003')

# def client_write():
#     write()
class TestWrite(unittest.TestCase):
    def test1(self):
        response = write("50001","yuganshu","yuganshu","123456yug")
        self.assertEqual(response.status, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test2(self):
        response1=read("50001",'123456yug')
        self.assertEqual(response1.status, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test3(self):
        response1=read("50002",'123456yug')
        self.assertEqual(response1.status, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test4(self):
        response1=read("50003",'123456yug')
        self.assertEqual(response1.status, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test5(self):
        response = write("50002","aditi","aditi","1234aditi")
        self.assertEqual(response.status, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test6(self):
        response1=read("50001",'1234aditi')
        self.assertEqual(response1.status, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test7(self):
        response1=read("50002",'1234aditi')
        self.assertEqual(response1.status, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test8(self):
        response1=read("50003",'1234aditi')
        self.assertEqual(response1.status, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test9(self):
        response1=delete("50001",'1234aditi')
        self.assertEqual(response1.reply, 'SUCCESSFUL','FILE DOES NOT EXIST')
    def test10(self):
        response1=read("50001",'1234aditi')
        self.assertEqual(response1.status, 'FILE DOES NOT EXIST','SUCCESSFUL')
    def test11(self):
        response1=read("50002",'1234aditi')
        self.assertEqual(response1.status,'FILE DOES NOT EXIST','SUCCESSFUL')
    def test12(self):
        response1=read("50003",'1234aditi')
        self.assertEqual(response1.status,'FILE DOES NOT EXIST','SUCCESSFUL')
        



def main():
    p = Process(target=run_registry)
    p.start()
    time.sleep(1)
    p1 = Process(target=run_server1)
    p1.start()
    time.sleep(1)
    p2 = Process(target=run_server2)
    p2.start()
    time.sleep(1)
    p3 = Process(target=run_server3)
    p3.start()

    # p2 = Process(target=run_server,args='15003')
    # p2.start()
    # names = ['Google', 'Facebook', 'Microsoft']
    
    # for i in range(3):
        # p = Process(target=run_server, args=(ports[i]))
        # p.start()
    time.sleep(1)
    unittest.main()
    # os.system('python3 client.py')


if __name__ == '__main__':
    main()