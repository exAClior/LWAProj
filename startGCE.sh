#! /bin/bash
sudo apt-get update
sudo apt-get -y install g++
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
sudo pip install Django
sudo apt-get install make

wget http://downloads.sourceforge.net/tcl/tcl8.6.1-src.tar.gz
sudo tar xzvf tcl8.6.1-src.tar.gz  -C /usr/local/
cd  /usr/local/tcl8.6.1/unix/
sudo ./configure
sudo make
sudo make install
cd
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make test
sudo make install

sudo apt-get install bzip2

//install the rest manually
wget http://repo.continuum.io/archive/Anaconda2-5.0.1-Linux-x86_64.sh
bash ~/Anaconda2-5.0.1-Linux-x86_64.sh -yes
source ~/.bashrc


conda install -c conda-forge redis-py

python -m pip install --upgrade pip
python -m pip install grpcio
python -m pip install grpcio-tools
