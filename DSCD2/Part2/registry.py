import disc_pb2
import disc_pb2_grpc
import grpc
 
from concurrent import futures

class RegisterReplicaServiceServicer(disc_pb2_grpc.RegisterReplicaServiceServicer):
    primary_server = None
    replica_list = []
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


def main():
    print("registry server started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    disc_pb2_grpc.add_RegisterReplicaServiceServicer_to_server(RegisterReplicaServiceServicer(),server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()
main()    
