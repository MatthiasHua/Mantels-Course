import qrcode

def get_qr_string(data):
	qr = qrcode.QRCode(
	    version=1,
	    error_correction=qrcode.constants.ERROR_CORRECT_L,
	    box_size=10,
	    border=0,
	)
	qr.add_data(data)
	#print(qr.get_matrix())
	s = ""
	t = 0
	tmp = 0
	for i in qr.get_matrix():
		for j in i:
			t = (t + 1) % 8
			tmp = tmp * 2 + (1 if (j) else 0);
			if t == 0:
				#print(tmp)
				s += chr(tmp)
				tmp = 0
	for i in range(8 - t):
		tmp *= 2
	s += chr(tmp)
	#print(s)
	return s;
