# Attack-classification-of-Iot-Network


## Installation of Tensorflow 


**STEP 1:**    
cat /etc/os-release   
python3 --version  
pip3 --version 


**STEP 2:**   
sudo apt update  
sudo apt dist-upgrade  
sudo apt clean


**STEP 3:**   
sudo pip install --upgrade pip  
sudo pip3 install --upgrade setuptools  
sudo pip3 install numpy==1.19.0  
sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran python-dev libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev  
sudo pip3 install keras_applications==1.0.8 --no-deps  
sudo pip3 install keras_preprocessing==1.1.0 --no-deps  
sudo pip3 install h5py==2.9.0  
sudo pip3 install pybind11  
pip3 install -U --user six wheel mock  


**STEP 4:**   
$ wget "https://raw.githubusercontent.com/PINTO0309/Tensorflow-bin/master/tensorflow-2.3.0-cp37-none-linux_armv7l_download.sh"  
$ sudo chmod +x tensorflow-2.3.0-cp37-none-linux_armv7l_download.sh  
$ ./tensorflow-2.3.0-cp37-none-linux_armv7l_download.sh  
$ sudo pip3 uninstall tensorflow  
$ sudo -H pip3 install tensorflow-2.3.0-cp37-none-linux_armv7l.whl  


(NOTE:  Other versions or architectures can be found in this link (Simply replace 2.3.0 with the desired TF 2 version):   
https://github.com/PINTO0309/Tensorflow-bin/#usage:)  


**STEP 5:**   
$ python3   
>import tensorflow  
>tensorflow.__version__  
'2.3.0'  
>exit()  


## Installation of Keras 

**STEP 1:**     
sudo apt-get install python3-numpy  
sudo apt-get install libblas-dev  
sudo apt-get install liblapack-dev  
sudo apt-get install python3-dev   
sudo apt-get install libatlas-base-dev  
sudo apt-get install gfortran  
sudo apt-get install python3-setuptools  
sudo apt-get install python3-scipy  
sudo apt-get update  
sudo apt-get install python3-h5py  


**STEP 2:**     
workon cv  
pip install --upgrade scipy  
pip install --upgrade cython  
pip install keras   


