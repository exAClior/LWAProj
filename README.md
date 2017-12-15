# LWAProj
The project which we deployed on server only achieves partial functionalities as proposed in our project design.

What we have achieved:

1. Currently, our project can handle userinput (as specified in part 1 in our project design) and stores the input in the related databases. The logics and views of asking users random questions and store the answers in a database is completed and deployed. The implementation of the RPC to reply to Part 2 is also completed. However, we failed to deploy RPC on server.
Access http://ec2-54-183-149-48.us-west-1.compute.amazonaws.com/micro to first register as an user.
Access http://ec2-54-183-149-48.us-west-1.compute.amazonaws.com/question while logged in to answer the questions on perference.

2. The latent factor model algorithm is completed and can be deployed on GCE. The code is in ~/LWAProj/backend/matcher_server.py
The RPC that writes back to EC2 is also completed Yusheng Zhao has grouped them together into the matcher_server.py file. However, since no data can be read from the EC2 server via RPC call, the algorithm cannot output anything useful.
Since no data can be retrieved from the GCE server, no matching data can be displayed from Wentao Zou.

3. 

What we failed to achieve:
1. Deploy the RPCs connecting the user input and output with the latent factor model.

2. 

Summary of our deployment:

We have an AWS server running scalica. Users will input their ranking for each label using that.

We also have a Google Cloud Engine running the latent facotr model algorithm. Some core functionalities of this algorithm
is from the website cited below. We have modified it to suit our needs. The script for starting this GCE is called startGCE.sh. It is located under ~/LWAProj

Upon running, the GCE server would request user ranking input from the scalica server via RPC call. Then it will run the algorithm to compute the full ranking matrix. It will then output three recommended user for each user in the matrix. Then, it will store this information in a Redis server, upon the request of an RPC call, it will retrieve these information and send to scalica for display.

Matcher_server also functions as the requester client as it requests stream info from the server

source http://www.albertauyeung.com/post/python-matrix-factorization/ 

