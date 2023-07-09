import grpc 
import disc_pb2_grpc
import disc_pb2
import uuid
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

local_replica_list=[]
unique_id = str(uuid.uuid1())
def write(file_name,file_content,client_uuid):
    channel =grpc.insecure_channel('localhost:50051')
    stub=disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    req_type='write'
    send=disc_pb2.list_request(type=req_type,uuid=unique_id)
    result=stub.registryList(send)
    print(result)
    write_list=result.server_list
    print(write_list)
    # file_name= input("Enter file name")
    # file_content = input("Enter content of the file")
    # client_uuid = input("Enter uuid of the file")
    result=""
    for server in write_list:
        addr=server.server_address
        channel = grpc.insecure_channel('localhost:'+ str(addr))
        stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
        send =disc_pb2.write(name=file_name,content= file_content,uuid=client_uuid)
        result =stub.writeRequest(send)
        timestamp=result.version
        seconds = timestamp.seconds
        nanos = timestamp.nanos 
        dt = datetime.datetime.fromtimestamp(seconds + nanos/1e9)
        formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(formatted_timestamp) 
    return result
def read(file_uuid):
    channel =grpc.insecure_channel('localhost:50051')
    stub=disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    req_type='read'
    send=disc_pb2.list_request(type=req_type,uuid=unique_id)
    result=stub.registryList(send)
    write_list=result.server_list
    # file_uuid = input("Enter uuid of the file")
    ret="SUCCESSFUL"
    final_name=''
    final_content=''
    final_timestamp=None
    for server in write_list:
        addr=server.server_address
        channel = grpc.insecure_channel('localhost:'+ str(addr))
        stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
        send =disc_pb2.uuidData(uuid=str(file_uuid))
        result =stub.readFile(send)
        cur_timestamp=result.version.seconds
        print(result)
        print("File name: ", result.name)
        print("File content: ", result.content)
        print("File timestamp: ", result.version.seconds)
        if final_timestamp is None or cur_timestamp > final_timestamp.seconds:
            ret=result.status
            final_name = result.name
            final_content = result.content
            final_timestamp = result.version

    print("File name: ", final_name)
    print("File content: ", final_content)
    print("File timestamp: ", final_timestamp)
    print("status: ", ret)
    return ret
def delete(client_uuid):
    channel =grpc.insecure_channel('localhost:50051')
    stub=disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    req_type='delete'
    send=disc_pb2.list_request(type=req_type,uuid=unique_id)
    result=stub.registryList(send)
    write_list=result.server_list
    # client_uuid = input("enter unique id")
    for server in write_list:
        addr=server.server_address
        channel = grpc.insecure_channel('localhost:'+ str(addr))
        stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)       
        send =disc_pb2.uuidData(uuid=client_uuid)
        result =stub.deleteRequest(send)
        print(result)
    
    print(result)
    return result
def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub =disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    register_request = disc_pb2.void()
    register_response =stub.getReplicaList(register_request)
    local_replica_list=register_response.server_list
    for value in local_replica_list:
            print(value.server_address)

    print("Welcome to the registry client!")
    print("1. Write File")
    print("2. Read File ")
    print("3. Delete File")
  

    

    while True:
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            # channel =grpc.insecure_channel('localhost:50051')
            # stub=disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            # req_type='write'
            # send=disc_pb2.list_request(type=req_type,uuid=unique_id)
            # result=stub.registryList(send)
            # print(result)
            # write_list=result.server_list
            # print(write_list)
            file_name= input("Enter file name")
            file_content = input("Enter content of the file")
            client_uuid = input("Enter uuid of the file")
            # for server in write_list:
            #     addr=server.server_address
            #     channel = grpc.insecure_channel('localhost:'+ str(addr))
            #     stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            #     send =disc_pb2.write(name=file_name,content= file_content,uuid=client_uuid)
            #     result =stub.writeRequest(send)
            #     timestamp=result.version
            #     seconds = timestamp.seconds
            #     nanos = timestamp.nanos 
            #     dt = datetime.datetime.fromtimestamp(seconds + nanos/1e9)
            #     formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
            #     print(formatted_timestamp)
            write(file_name,file_content,client_uuid)    
                


        elif choice == "2":
            # channel =grpc.insecure_channel('localhost:50051')
            # stub=disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            # req_type='read'
            # send=disc_pb2.list_request(type=req_type,uuid=unique_id)
            # result=stub.registryList(send)
            # write_list=result.server_list
            file_uuid = input("Enter uuid of the file")
            # final_name=''
            # final_content=''
            # final_timestamp=None
            # for server in write_list:
            #     addr=server.server_address
            #     channel = grpc.insecure_channel('localhost:'+ str(addr))
            #     stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            #     send =disc_pb2.uuidData(uuid=str(file_uuid))
            #     result =stub.readFile(send)
            #     cur_timestamp=result.version.seconds
            #     print(result)
            #     print("File name: ", result.name)
            #     print("File content: ", result.content)
            #     print("File timestamp: ", result.version.seconds)
            #     if final_timestamp is None or cur_timestamp > final_timestamp.seconds:
            #         final_name = result.name
            #         final_content = result.content
            #         final_timestamp = result.version

            # print("File name: ", final_name)
            # print("File content: ", final_content)
            # print("File timestamp: ", final_timestamp)
            read(file_uuid)

        elif choice == "3":
            # channel =grpc.insecure_channel('localhost:50051')
            # stub=disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            # req_type='delete'
            # send=disc_pb2.list_request(type=req_type,uuid=unique_id)
            # result=stub.registryList(send)
            # write_list=result.server_list
            client_uuid = input("enter unique id")
            # for server in write_list:
            #     addr=server.server_address
            #     channel = grpc.insecure_channel('localhost:'+ str(addr))
            #     stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)       
            #     send =disc_pb2.uuidData(uuid=client_uuid)
            #     result =stub.deleteRequest(send)
            #     print(result)
            
            # print(result)
            delete(client_uuid)
        elif choice == "4":
           break 
        else:
            # Handle invalid input
            print("Invalid choice, try again.")   

       
if __name__ == '__main__':
    run()        
