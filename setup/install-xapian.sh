# *****************************************************
# ***************** Install xapian Core ***************
# *****************************************************

sudo apt-get install zlib1g-dev
sudo apt-get install g++
sudo apt-get install uuid-dev

curl -O http://oligarchy.co.uk/xapian/1.2.18/xapian-core-1.2.18.tar.xz
curl -O http://oligarchy.co.uk/xapian/1.2.18/xapian-bindings-1.2.18.tar.xz

unxz xapian-core-1.2.18.tar.xz
unxz xapian-bindings-1.2.18.tar.xz

tar xvf xapian-core-1.2.18.tar
tar xvf xapian-bindings-1.2.18.tar

cd xapian-core-1.2.18
mkdir -p $HOME/local
./configure --prefix=$HOME/local
./configure
make
sudo make install

# *****************************************************
# **** Install Xapian bindings with Python support ****
# *****************************************************

cd ..
cd xapian-bindings-1.2.18
sudo apt-get install python-sphinx
./configure --with-python --prefix=$HOME/local/
make
sudo make install

# *****************************************************
# ********************* Check it **********************
# *****************************************************
python -c "import xapian"
