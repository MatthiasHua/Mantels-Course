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
	for i in qr.get_matrix():
		for j in i:
			s += "1" if (j) else "0";
	return s;
