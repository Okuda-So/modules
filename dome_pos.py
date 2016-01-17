import time
import math
import pyinterface


class domepos_controller(object):
	touchsensor_pos = [-391,-586,-780,-974,-1168,-1363,-1561,-1755,-1948,-2143, 0, -197]
	dome_encoffset = 10000
	dome_enc1loop = 2343
	dome_enc_tel_offset = 1513*360
	dome_enc2arcsec = (3600.0*360/dome_enc1loop)
	dome_position = 0


	def __init__(self, ndev2 = 1):
		self.dio = pyinterface.create_gpg6204(ndev2)
		self.dome_encoder_acq()
		pass
	
	def dome_enc_initialize(self):
		self.dio.ctrl.reset()
		self.dio.ctrl.set_mode(4, 0, 1, 0)
		#self.dio.ctrl.set_counter(self.dome_enc_offset)  ???
		return
		
	def dome_enc_correct(self):
		ret = self.dome_limit()
		while ret == 0:
			ret = self.dome_limit()
		print('ENCODER CORRECT AT LIMIT '+str(ret))
		return
	
	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!')
		return
	
	def dome_encoder_acq(self):
		counter = self.dio.get_position()
		dome_enc_arcsec = -int(((counter-self.dome_encoffset)*self.dome_enc2arcsec)-self.dome_enc_tel_offset)
		while(dome_enc_arcsec>1800.*360):
			dome_enc_arcsec-=3600.*360
		while(dome_enc_arcsec<=-1800.*360):
			dome_enc_arcsec+=3600.*360
		self.dome_position = dome_enc_arcsec
		return dome_enc_arcsec
	
	def read_dome_enc(self):
		return self.dome_position

def domepos_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(domepos_controller, host, port)
	return client

def domepos_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(domepos_controller, host, port)
	return client

def start_domepos_server(port1 = 8005, port2 = 8006):
	domepos = domepos_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(domepos, '', port1, port2)
	server.start()
	return server


