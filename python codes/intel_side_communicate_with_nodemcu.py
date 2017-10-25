import socket
import time
import threading


def recvdata(cobj):
	while(1):

		data = "";
		char = "";

		while(char!="\n"):
			char = cobj.recv(1).decode() ;
			data+=char ;

		print(data);
		if not len(data):break;
		data="" ;







s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) ; 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(("10.255.255.255" , 0)) ;
ref = s.getsockname()[0]
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM) ;
s.bind((ref , 9876)) ;

print("Server ip : {}\nPort : {}\n\n".format(ref , 9876)) ;

s.listen(100)
cobj , addr = s.accept();
print("\nConnected to client : " , addr) ;

threading.Thread(target=recvdata , args=[cobj]).start() ;

while(1):
	msg = input("\n\n>> ").encode(); 
	cobj.send(msg) ;
	
	



