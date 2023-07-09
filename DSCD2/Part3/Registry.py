import disc_pb2
import disc_pb2_grpc
import grpc
import random
from random import sample
 
from concurrent import futures

N_r=0
N_w=0
N=0


class RegisterReplicaServiceServicer(disc_pb2_grpc.RegisterReplicaServiceServicer):
    primary_server = None
    replica_list = []
    #optimize function
    def random(self, start_range, end_range, n):
        return random.sample(range(start_range, end_range+1), n)

    # RegistryList function
    def registryList(self, request, context):
        global N
        global N_r
        global N_w
        print("registry list demand")
        print(self.replica_list)
        req_type = request.type
        replica_len = len(self.replica_list)
        sending = []
        if req_type == 'write':
            server_indexes = self.random(0, replica_len-1, N_w)
            for i in server_indexes:
                sending.append(self.replica_list[i])
        elif req_type == 'read':
            server_indexes = self.random(0, replica_len-1, N_r)
            for i in server_indexes:
                sending.append(self.replica_list[i])
        elif req_type == 'delete':
            server_indexes = self.random(0, replica_len-1, N_w)
            for i in server_indexes:
                sending.append(self.replica_list[i])
        else:
            print("Invalid choice")
        print(sending)
        return disc_pb2.Server_list(server_list=sending)





    def replicaRegister(self, request, context):
        print("JOIN REQUEST FROM LOCAL HOST:"+request.server_address)
        register_reply = disc_pb2.Server()    
        self.replica_list.append(request)
        if(len(self.replica_list)>1):
            channel = grpc.insecure_channel('localhost:'+self.primary_server)
            stub =disc_pb2_grpc.RegisterReplicaServiceStub(channel)
            register_request = disc_pb2.Server_list(server_list=self.replica_list)
            result =stub.updatePrimary(register_request)
            print(result)

        if not self.primary_server:
            self.primary_server = request.server_address
            register_reply.server_address = self.primary_server
        else:
            register_reply.server_address = self.primary_server
        return register_reply
    
    def getReplicaList(self, request, context):
        print("list requested by client")
        return disc_pb2.Server_list(server_list= self.replica_list)

    
    

def run():
    global N_r,N_w,N
    condition=1
    while(condition==1): 
        N_r=int(input("Enter values for read quarom") )
        N_w=int(input("Enter values for write quarom") )
        N=int (input("Enter values for read quarom") )
        if(N_r+N_w>N and N_r>0 and N_w>0):
            condition= 0
        else:
            print("Re-enter values") 
    print("server intialized")             

def main():
    print("server started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    disc_pb2_grpc.add_RegisterReplicaServiceServicer_to_server(RegisterReplicaServiceServicer(),server)
    server.add_insecure_port('localhost:50051')
    server.start()
    run()
    server.wait_for_termination()
main()    
