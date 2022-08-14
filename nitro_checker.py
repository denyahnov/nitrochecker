try:
	import os
	import requests
	from plyer import notification
except:
	exit("[!] ERROR Install 'plyer'")

class settings:
	nitro_only = False
	notify = False

def nitro_code(nitro):
	if nitro == 0: return 'None'
	if nitro == 1: return 'Classic'
	if nitro == 2: return 'Nitro'

def check_token(token,url):
	response = requests.get(url, headers={"Authorization" : token})
	return response.text if response.status_code != 401 else False

def read_data(data):
	username, tag, email, phone, nitro = False, False, False, False, False

	for line in data.split(','):
		if 'username' in line:
			line = line.replace('"username": ','')
			username = line.replace('"','')[1:]
		elif 'discriminator' in line:
			line = line.replace('"discriminator": ','')
			tag = line.replace('"','')[1:]
		elif 'email' in line:
			line = line.replace('"email": ','')
			email = line.replace('"','')[1:]
		elif 'phone' in line:
			line = line.replace('"phone": ','')
			phone = line.replace('"','').replace('}','')[1:]
		elif 'premium_type' in line:
			line = line.replace('"premium_type": ','')
			nitro = line.replace('"','')[1:]
			nitro = nitro_code(int(nitro))

	return username, tag, email, phone, nitro

def read_tokens(filedir):
	f=open(filedir,'r')
	lines=f.readlines()
	f.close()

	return lines

def create_files(names):
	if "output" not in os.listdir(os.getcwd()): 
		try:
			os.mkdir("output")
		except:
			exit('[!] ERROR Missing Permissions to create folder')

	directory = os.getcwd() + "\\output\\"

	f1=open(directory + names[0],"w+")
	f2=open(directory + names[1],"w+")

	return f1,f2

def get_settings():
	if "settings.txt" not in os.listdir(os.getcwd()):
		settings.nitro_only = True if 'y' in input("[?] Only save nitro users? y/n\n   > ") else False
		settings.notify = True if 'y' in input("[?] Notification on finish checking? y/n\n   > ") else False

		settings_file = open("settings.txt","w+")

		settings_file.write(f"nitro : {settings.nitro_only}\nnotify : {settings.notify}")

		settings_file.close()
	else:
		for line in open("settings.txt","r").readlines():
			if 'nitro' in line:
				settings.nitro_only = True if 'true' in line.strip('\n').lower() else False
			elif 'notify' in line:
				settings.notify = True if 'true' in line.strip('\n').lower() else False

	print(f"[>] Nitro Check = {settings.nitro_only}\n[>] Notification = {settings.notify}")
def main():
	print('[+] Reading Tokens File')

	try:
		tokens = read_tokens("tokens.txt")
	except FileNotFoundError:
		open("tokens.txt","w+")

	final_tokens = []

	print('[+] Creating Output File')

	get_settings()

	userdata, tokens_file = create_files(["userdata.txt","tokens.txt"])
	print('[+] Searching {} Tokens'.format(len(tokens)))

	for tkn in tokens:
		tkn = tkn.strip('\n')

		data = check_token(tkn,'https://discordapp.com/api/users/@me')

		if not data: continue

		username, tag, email, phone, nitro = read_data(data)

		if nitro == False and settings.nitro_only == True: 
			print(f"[-] {tkn}")
			continue

		formatted = f"{'{'}\n\tuser:     {username}#{tag}\n\ttoken:    {tkn}\n\temail:    {email}\n\tphone:    {phone}\n\tpremium:  {nitro}\n{'}'}"

		print(formatted)
		userdata.write(formatted + '\n\n')
		tokens_file.write(tkn + '\n')
		final_tokens.append(tkn)

	print('[+] Finished with {} valid tokens'.format(len(final_tokens)))

	tokens_file.close()
	userdata.close()

if __name__ == "__main__":
	main()

	if settings.notify: notification.notify(title="Discord Nitro Checker", message="Finished checking tokens!", app_icon=None, timeout=5)
	input('[?] Press ENTER to close script')