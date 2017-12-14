from concurrent import futures
import time

import grpc
import recommender_pb2
import recommender_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Recommender(recommender_pb2_grpc.RecommenderServicer):

  def Recommender(self, request, context):
    	reply = recommender_pb2.UserList()
	reply.userID = request.userID
	for n in range(5):
		reply.commendedID.append(n)
	return recommender_pb2.UserList(reply)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  recommender_pb2_grpc.add_RecommenderServicer_to_server(Recommender(), server)
  server.add_insecure_port('[::]:50021')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
