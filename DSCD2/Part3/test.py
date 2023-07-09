import unittest
import os
from multiprocessing import Process
import time
# import utils
from client import *


def run_registry():
    os.system('python3 registry_test.py')


def run_server1():
    os.system('python3 Server.py 50001')

def run_server2():
    os.system('python3 Server.py 50002')

def run_server3():
    os.system('python3 Server.py 50003')
class TestWrite(unittest.TestCase):
    def test1(self):
        response = write("yuganshu","yuganshu","123456yug")
        self.assertEqual(response.status, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test2(self):
        response = read("123456yug")
        self.assertEqual(response, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test3(self):
        response = write("aditi","aditi","1234aditi")
        self.assertEqual(response.status, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test4(self):
        response = read("1234aditi")
        self.assertEqual(response, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test5(self):
        response = delete("1234aditi")
        self.assertEqual(response.reply, 'SUCCESSFUL', "WRITE OPERATION FAILED")
    def test6(self):
        response = read("1234aditi")
        self.assertEqual(response, 'FILE ALREADY DELETED', "SUCCESSFUL")
    
    # def test1(self):
    #     response = write("yuganshu","yuganshu","123456yug")
    #     self.assertEqual(response.status, 'SUCCESSFUL', "WRITE OPERATION FAILED")

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
    # p3 = Process(target=run_server3)
    # p3.start()

    # p3 = Process(target=run_server3)
    # p3.start()

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