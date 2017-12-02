#! /bin/bash
sudo apt-get update
sudo apt-get -y install g++
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
sudo pip install Django 
