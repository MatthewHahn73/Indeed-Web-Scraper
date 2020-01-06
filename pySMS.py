import smtplib

class pySMS():
	phoneNumber = ""
	hostEmail = ("","")
	carrier = {
		"at@t": "@mms.att.net",
		"tmob": "@tmomail.net",
		"verizon": "@vtext.net",
		"sprint": "@page.nextel.com"
	}

	def __init__(self, Num, Host):
		self.phoneNumber = Num + "{}".format(self.carrier["at@t"])
		self.hostEmail = Host
	
	def send(self, Data):
		try:
			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.starttls()
			server.login(self.hostEmail[0], self.hostEmail[1])
			server.sendmail(self.hostEmail[0], self.phoneNumber, Data[:Data.rfind("\n")])
		except Exception as e:
			print(e)
