import grpc 
import  disc_pb2_grpc
import   disc_pb2
import socket
import sys
import os 
from concurrent import futures
import time
import os
from os.path import exists
from google.protobuf.timestamp_pb2 import Timestamp

    
curr_addr=0
primary_server =0
fileDict={}
fileTime={}
path = "/Users/yuganshukajla/Downloads/DSCD2/Part3"

class RegisterReplicaServiceServicer(disc_pb2_grpc.RegisterReplicaServiceServicer):
    replica_list=[]
    def updatePrimary(self, request, context):
        self.replica_list=request.server_list
        print(self.replica_list)
        return disc_pb2.void()

    def writeRequest(self, request, context):
        global curr_addr
        global fileDict
        global path
        global fileTime
        print("func working")
            #implement function with dictionary
        ans=""
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        if request.uuid in fileDict.keys():
        #  print("searching")
            if(fileDict[request.uuid]==request.name):
                # file update    
                fileTime[request.uuid]=timestamp
               
                parent_dir = path
                directory = str(curr_addr)
                path1 = os.path.join(parent_dir,directory)
                file_path=os.path.join(path1,request.name)
                file1 = open(file_path,"w")
                file1.write(request.content)
                file1.close()
                ans="SUCCESSFUL"

            else:
                ans="DELETED FILE CANNOT BE UPDATED"
        else:
            # print(" also searching")
            if(request.name in fileDict.values()):
                ans="FILE WITH THE SAME NAME ALREADY EXISTS"
            else:
            # file create
                # print("creating")
                fileTime[request.uuid]=timestamp
                fileDict[request.uuid]=request.name
                parent_dir = path
                directory = str(curr_addr)
                path1 = os.path.join(parent_dir,directory)
                file_path=os.path.join(path1,request.name)
                file1 = open(file_path,"w")
                file1.write(request.content)
                file1.close()
                ans="SUCCESSFUL"
            print(request)

        response=disc_pb2.writeResponse(status=ans,uuid=request.uuid,version=timestamp )#add version here    
        return response    
    
    
    def readFile(self, request, context):
        global path
        global curr_addr
        global fileTime
        global fileDict
        ans=""
        name=""
        content=""
        print("in read")
        if request.uuid in fileDict.keys():
            print("uuid exist")
            name=fileDict[request.uuid]    
            parent_dir = path
            if(name==""):
                 print("deleted")
                 ans="FILE ALREADY DELETED"   
            else:
                directory = str(curr_addr)
                path1 = os.path.join(parent_dir,directory)
                file_path=os.path.join(path1,name)
                print(os.path.isfile(file_path))
                if(os.path.isfile(file_path)):
                    file1 = open(file_path,"r")
                    content=file1.read()
                    print(content)
                    ans="SUCCESSFUL"
                else:
                    ans="FILE ALREADY DELETED"
        else:
            ans="FILE DOES NOT EXIST"
        print("func done")
        print(name)
        print(ans)
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        if(request.uuid in fileTime.keys()):
                timestamp=fileTime[request.uuid]
        response = disc_pb2.file(status=ans,name=name,content=content,version=timestamp)#add version here
        return response
    
    def deleteRequest(self, request, context):
        global curr_addr
        global path
        global fileDict
        global fileTime
            #implement function with dictionary
        ans=""
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        if request.uuid in fileDict.keys():
            print("in delete")
            name=fileDict[request.uuid]    
            parent_dir = path
            directory = str(curr_addr)
            path1 = os.path.join(parent_dir,directory)
            file_path=os.path.join(path1,name)
            if(os.path.isfile(file_path)):
                os.remove(file_path)
                fileDict[request.uuid]=""
                fileTime[request.uuid]=timestamp
                ans="SUCCESSFUL"
            else:
                ans="FILE ALREADY DELETED"
        else:
            ans="FILE DOES NOT EXIST"
            
        response=disc_pb2.result(reply=ans)    
        return response 
    

def run(port):
    global primary_server 
    global path
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
        register_request = disc_pb2.Server(server_address=str(port))
        register_response = stub.replicaRegister(register_request)
        primary_server = register_response.server_address
        print(register_response)
        print(primary_server)
        directory = str(port)
        parent_dir = path #add file source from terminal
        path1 = os.path.join(parent_dir,directory)
        if(not os.path.exists(path1)):
            os.mkdir(path1)

def main(port):
    global curr_addr
    print("server started")
    curr_addr=port
    run(port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    disc_pb2_grpc.add_RegisterReplicaServiceServicer_to_server(RegisterReplicaServiceServicer(),server)
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python server.py <port>')
        sys.exit(1)
    main(int(sys.argv[1]))
