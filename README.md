# LWAProj
We have failed to deploy this project. 
Currently, our project can handle userinput. However, the rpc call that retrieves data from the EC2 server is not written. 

The data handeling is completed The RPC that writes back to EC2 is also completed. However, since no data can be read from the EC2 server, it cannot output anything useful.

Summary of our deployment:

We have an AWS server running scalica. Users will input their ranking for each label using that.

We also have a Google Cloud Engine running the latent facotr model algorithm. Some core functionalities of this algorithm
is from the website cited below. We have modified it to suit our needs. The script for starting this GCE is called startGCE.sh

Upon running, the GCE server would request user ranking input from the scalica server via RPC call. Then it will run the algorithm to compute the full ranking matrix. It will then output three recommended user for each user in the matrix. Then, it will store this information in a Redis server, upon the request of an RPC call, it will retrieve these information and send to scalica for display.

Matcher_server also functions as the requester client as it requests stream info from the server
source http://www.albertauyeung.com/post/python-matrix-factorization/ 

