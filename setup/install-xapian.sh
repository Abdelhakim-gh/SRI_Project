# *****************************************************
# ***************** Install xapian Core ***************
# *****************************************************

sudo apt-get install zlib1g-dev
sudo apt-get install g++
sudo apt-get install uuid-dev

curl -O https://oligarchy.co.uk/xapian/1.4.26/xapian-core-1.4.26.tar.xz
curl -O https://oligarchy.co.uk/xapian/1.4.26/xapian-bindings-1.4.26.tar.xz

unxz xapian-core-1.4.26.tar.xz
unxz xapian-bindings-1.4.26.tar.xz

tar xvf xapian-core-1.4.26.tar
tar xvf xapian-bindings-1.4.26.tar

cd xapian-core-1.4.26
mkdir -p $HOME/local
./configure --prefix=$HOME/local
./configure
make
sudo make install

# *****************************************************
# **** Install Xapian bindings with Python support ****
# *****************************************************

cd ..
cd xapian-bindings-1.4.26
sudo apt-get install python-sphinx
./configure --with-python --prefix=$HOME/local/
make
sudo make install

# *****************************************************
# ********************* Check it **********************
# *****************************************************
python -c "import xapian"
