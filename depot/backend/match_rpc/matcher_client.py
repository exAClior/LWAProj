import grpc
//from __future__ import print_function

import grpc

import matcher_pb2
import matcher_pb2_grpc


def run(userID, userName):
  //The channel need to update to the server IP 
  channel = grpc.insecure_channel('localhost:50051')
  stub = matcher_pb2_grpc.MatcherStub(channel)
  user = matcher_pb2.WhichUser()
  user.userID = userID
  user.userName = userName
  response = stub.Match(matcher_pb2.Match(user))
  return response.matchID

if __name__ == '__main__':
  run()
