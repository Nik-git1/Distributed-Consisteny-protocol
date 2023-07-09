import grpc 
import disc_pb2_grpc
import disc_pb2
import uuid

local_replica_list=[]

def write(server_address,file_name,file_content,client_uuid):
    
    channel = grpc.insecure_channel('localhost:'+ str(server_address))
    stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
   
    send =disc_pb2.write(name=file_name,content= file_content,uuid=client_uuid)
    result =stub.writeRequest(send)
    print(result)
    return result

def read(server_address,client_uuid):
    # server_address = input("Enter replica address: ")
    channel = grpc.insecure_channel('localhost:'+ str(server_address))
    stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    # client_uuid = input("enter unique id")
    send =disc_pb2.uuidData(uuid=client_uuid)
    result =stub.readFile(send)
    print(result)
    return result

def delete(server_address,client_uuid):
    # server_address = input("Enter replica address: ")
    channel = grpc.insecure_channel('localhost:'+ str(server_address))
    stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    # client_uuid = input("enter unique id")# send unique id everytime
    send =disc_pb2.uuidData(uuid=client_uuid)
    result =stub.deleteRequest(send)
    print(result)
    return result

    
    print(result)
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
  

    unique_id = str(uuid.uuid1())

    while True:
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            server_address = input("Enter replica address: ")
            # server_address = input("Enter replica address: ")
            # channel = grpc.insecure_channel('localhost:'+ str(server_address))
            # stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            # file_name= input("Enter file name")
            # file_content = input("Enter content of the file")
            # client_uuid = input("Enter uuid of the file")# send unique id everytime
            # send =disc_pb2.write(name=file_name,content= file_content,uuid=client_uuid)
            # result =stub.writeRequest(send)
            # print(result)
            file_name= input("Enter file name")
            file_content = input("Enter content of the file")
            client_uuid = input("Enter uuid of the file")# send unique id everytime
            write(server_address,file_name,file_content,client_uuid)

        elif choice == "2":
            
            server_address = input("Enter replica address: ")
            # channel = grpc.insecure_channel('localhost:'+ str(server_address))
            # stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            client_uuid = input("enter unique id")
            # send =disc_pb2.uuidData(uuid=client_uuid)
            # result =stub.readFile(send)
            # print(result)
            read(server_address,client_uuid)

        elif choice == "3":
            server_address = input("Enter replica address: ")
            # channel = grpc.insecure_channel('localhost:'+ str(server_address))
            # stub = disc_pb2_grpc.RegisterReplicaServiceStub(channel)
    
            client_uuid = input("enter unique id")# send unique id everytime
            # send =disc_pb2.uuidData(uuid=client_uuid)
            # result =stub.deleteRequest(send)
            # print(result)
            
            # print(result)
            delete(server_address,client_uuid)

        elif choice == "4":
           break 
        else:
            # Handle invalid input
            print("Invalid choice, try again.")   

       
if __name__ == '__main__':
    run()        
