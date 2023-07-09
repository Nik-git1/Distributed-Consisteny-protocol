import grpc 
import  disc_pb2_grpc
import  disc_pb2
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
path="/Users/yuganshukajla/Downloads/DSCD2/Part1"

class RegisterReplicaServiceServicer(disc_pb2_grpc.RegisterReplicaServiceServicer):
    replica_list=[]
    def updatePrimary(self, request, context):
        self.replica_list=request.server_list
        print(self.replica_list)
        return disc_pb2.void()

    def writeRequest(self, request, context):
        global curr_addr
        global primary_server
        global fileDict
        global path
        global fileTime

        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        ans=""
        if str(curr_addr) == primary_server:
            print("value printed in primary")
           
            if request.uuid in fileDict.keys():
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
                    ans="DELETED FILE CANNOT BE UPDATED" # ye waala run hora hia hamesha
            else:
                if(request.name in fileDict.values()):
                    ans="FILE WITH THE SAME NAME ALREADY EXISTS"
                else:
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

            print(request)
            for server in self.replica_list:
                addr = server.server_address
                if addr != primary_server:
                    channel = grpc.insecure_channel('localhost:'+ addr)
                    stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
                    send = disc_pb2.write(name=request.name, content=request.content, uuid=request.uuid)
                    result = stub.writeReplica(send)
                    ans=result.reply
        else:
            channel = grpc.insecure_channel("localhost:" + primary_server)
            stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            file_name = request.name
            file_content = request.content
            client_uuid = request.uuid
            send = disc_pb2.write(name=file_name, content=file_content, uuid=client_uuid)
            result = stub.writeRequest(send)
            timestamp=result.version
            ans=result.status
            print(result)

        print(timestamp)    

        response=disc_pb2.writeResponse(status=ans,uuid=request.uuid,version=timestamp)    
        return response    
    
    def writeReplica(self, request, context):
        #implement function with dictionary

        global curr_addr
        global fileDict
        global path
        global fileTime

        print(curr_addr)
        print("running in replica")
        ans="UNSUCCESSFUL"
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
        
        return disc_pb2.result(reply=ans)
    
    def readFile(self, request, context):
        global path
        global curr_addr
        global fileTime
        global fileDict
        ans=""
        name=""
        content=""
        if request.uuid in fileDict.keys():
            name=fileDict[request.uuid]    
            parent_dir = path
             
            directory = str(curr_addr)
            path1 = os.path.join(parent_dir,directory)
            file_path=os.path.join(path1,name)
            print(os.path.isfile(file_path))
            if(os.path.isfile(file_path)):
                file1 = open(file_path,"r")
                content=file1.read()
                print(content)
                ans="SUCCESSFUL"
            elif(name==""):
                ans="FILE ALREADY DELETED"
        else:
            ans="FILE DOES NOT EXIST"

        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        if(request.uuid in fileTime.keys()):
                timestamp=fileTime[request.uuid]
        
        response = disc_pb2.file(status=ans,name=name,content=content,version=timestamp)#add version here
        return response
    
    def deleteRequest(self, request, context):
        global curr_addr
        global primary_server
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        if str(curr_addr) == primary_server:
            #implement function with dictionary
            ans=""
            if request.uuid in fileDict.keys():
                print("in delete")
                name=fileDict[request.uuid]    
                parent_dir = "/Users/yuganshukajla/Downloads/DSCD2/Part1" 
                directory = str(curr_addr)
                path = os.path.join(parent_dir,directory)
                file_path=os.path.join(path,name)
                print(os.path.isfile(file_path))
                if(os.path.isfile(file_path)):
                    
                    os.remove(file_path)
                    fileDict[request.uuid]=""
                    fileTime[request.uuid]=timestamp
                    print(os.path.isfile(file_path))
                    ans="SUCCESSFUL"

                else:
                    ans="FILE ALREADY DELETED"
            else:
                ans="FILE DOES NOT EXIST"
                
            # reply stored in ans

            for server in self.replica_list:
                addr = server.server_address
                if addr != primary_server:
                    channel = grpc.insecure_channel('localhost:'+ addr)
                    stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
                    send = disc_pb2.uuidData(uuid=request.uuid)
                    result = stub.deleteReplica(send)
                    ans=result.reply
                    print(result)
        else:
            print("value printed in replica"+ str(curr_addr))
            channel = grpc.insecure_channel("localhost:" + primary_server)
            stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            send = disc_pb2.uuidData(uuid=request.uuid)
            result = stub.deleteRequest(send)
            print(result)

        response=disc_pb2.result(reply=ans)    
        return response 
    
    def deleteReplica(self, request, context):
        ans=""
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        if request.uuid in fileDict.keys():
            print("in delete")
            name=fileDict[request.uuid]    
            parent_dir =path
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
            
        return disc_pb2.result(reply=ans)        
            

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
