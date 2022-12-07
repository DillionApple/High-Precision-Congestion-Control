echo 'deb http://dk.archive.ubuntu.com/ubuntu/ xenial main' >> /etc/apt/sources.list && \
echo 'deb http://dk.archive.ubuntu.com/ubuntu/ xenial universe' >> /etc/apt/sources.list && \
apt update
apt install -y g++-5 gcc-5
pip3 install matplotlib
cd ./analysis && make && cd ../
cd ./simulation/ && CC='gcc-5' CXX='g++-5' ./waf configure && cd ../
