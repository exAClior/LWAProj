import grpc
//from __future__ import print_function

import grpc

import recommender_pb2
import recommender_pb2_grpc


def run(id):
  //The channel need to update to the server IP 
  channel = grpc.insecure_channel('localhost:50051')
  stub = recommender_pb2_grpc.RecommenderStub(channel)
  user = recommender_pb2.WhichUser()
  user.userID = id
  user.userName = name
  response = stub.Recommend(recommender_pb2.Recommend(user))
  return response.recommendedID

if __name__ == '__main__':
  run()
