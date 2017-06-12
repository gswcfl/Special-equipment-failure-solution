# Create your views here.
#!/usr/bin/env python
#-*- codeing:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
import re,time,telnetlib
import xlrd,os,IPy

def index(request):
	return render_to_response('index.html')
def top(request):
	return render_to_response('top.html')
def left(request):
	return render_to_response('left.html')
def right(request):
	return render_to_response('right.html')
def buttom(request):
	return render_to_response('buttom.html')
def manage_host(request):
	return render_to_response('manage_host.html')

def upload_file(request):
	if request.method == "POST":
		myFile = request.FILES.get('file_name',None)
		if not myFile:
			result_upload="No files for upload"
			return HttpResponse(result_upload)
		dest = open(os.path.join("/xtyw/Site/site_project/check_site",myFile.name),"wb+")
		for chunk in myFile.chunks():
			dest.write(chunk)
			dest.close()
		result_upload="Upload OK"
	return HttpResponse(result_upload)

def query_passwd(request):
	query_ip_address = request.GET['query_ip_address']
	try:
		IPy.IP(str(query_ip_address))
		pass
	except Exception as e:
		alart = "Notice:IP address is invalid syntax"
		return render_to_response('manage_host.html',{'alart':alart})
	G_date = xlrd.open_workbook('/xtyw/Site/site_project/check_site/G_info.xls')
	G_sheet = G_date.sheet_names()[0]
	table = G_date.sheet_by_name(G_sheet)
	nrows = table.nrows
	ncols = table.ncols
	g_ip = table.col_values(3)
	ip_str = str(g_ip)
	ip_test = ip_str.find(query_ip_address)
	if ip_str.find(query_ip_address) < 0:
		alart = "Notice:IP address does not exist!"
		return render_to_response('manage_host.html',{'alart':alart})
	for i in range(nrows):
		cell_D = table.cell(i,3).value
		if str(query_ip_address) == cell_D:
			query_address = table.cell(i,0).value
			query_IP = cell_D
			query_username = table.cell(i,5).value
			query_passwd1 = table.cell(i,6).value
			query_passwd2 = table.cell(i,7).value
	return render_to_response('manage_host.html',{'query_address':query_address,'query_IP':query_IP,'query_username':query_username,'query_passwd1':query_passwd1,'query_passwd2':query_passwd2})


def query(request):
	global address
	address = ''
	address = request.GET['address']
	try:
		IPy.IP(str(address))
		pass
	except Exception as e:
		alart = "Notice:IP address is invalid syntax"
		return render_to_response('right.html',{'alart':alart})

	global G_address,G_nu,G_info,G_IP,G_mf,G_username,G_passwd1,G_passwd2
	G_date = xlrd.open_workbook('/xtyw/Site/site_project/check_site/G_info.xls')
	G_sheet = G_date.sheet_names()[0]
	table = G_date.sheet_by_name(G_sheet)
	nrows = table.nrows #
	ncols = table.ncols #
	g_ip = table.col_values(3)
	ip_str = str(g_ip)
	ip_test = ip_str.find(address)
	if ip_str.find(address) < 0:
		alart = "Notice:IP address does not exist!"
		return render_to_response('right.html',{'alart':alart})
	for i in range(nrows):
		cell_D = table.cell(i,3).value
		if str(address) == cell_D:
			G_address = table.cell(i,0).value
			G_nu = table.cell(i,1).value
			G_info = table.cell(i,2).value
			G_IP = cell_D
			G_mf = table.cell(i,4).value
			G_username = table.cell(i,5).value
			G_passwd1 = table.cell(i,6).value
			G_passwd2 = table.cell(i,7).value
	get_G_status(address,G_mf,G_username,G_passwd1,G_passwd2)
	get_D_info(G_info,G_nu)
	return render_to_response('right.html',{'G_address':G_address,'address':address,'G_mf':G_mf,'text':text,'result':result,'interface':interface,'port_bandwidth':port_bandwidth,'real_time_rate':real_time_rate,'description':description,'ip_d_list':ip_d_list,'result_sugon':result_sugon})


def get_D_info(G_info,G_nu):
	global D_ip_list,D_user_list,D_password1,D_password2,D_int,D_G,ip_d_list
	ip_d_list = ''
	D_ip_list = ''
	D_user_list = ''
	D_password1 = ''
	D_password2 = ''
	D_int = ''
	D_G = ''
	D_date = xlrd.open_workbook('/xtyw/Site/site_project/check_site/D_info.xls')
	D_sheet = D_date.sheet_names()[0]
	table = D_date.sheet_by_name(D_sheet)
	d_nrows = table.nrows
	d_ncols = table.ncols
	ip_list = []
	mf_list = []
	user_list = []
	password1 = []
	password2 = []
	D_int_list = []
	D_G_list = []
	for d in range(d_nrows):
		if (str(G_info) == str(table.cell(d,1).value)) and (str(G_nu) == str(table.cell(d,8).value)):
			ip_list.append(table.cell(d,2).value)
			mf_list.append(table.cell(d,3).value)
			user_list.append(table.cell(d,4).value)
			password1.append(table.cell(d,5).value)
			password2.append(table.cell(d,6).value)
			D_int_list.append(table.cell(d,7).value)
			D_G_list.append(table.cell(d,8).value)
	commands = []
	if str(mf_list[0]) == 'HUAWEI':
		for j in range(len(D_int_list)):
			c = D_int_list[j]
			commands.append(str('display interface ') + str(c))
	elif str(mf_list[0]) == 'ZXR10':
		for j in range(len(D_int_list)):
			c = D_int_list[j]
			commands.append(str('show interface ') + str(c))
	elif str(mf_list[0]) == 'DP':
		for j in range(len(D_int_list)):
			c = D_int_list[j]
			commands.append(str('show interface ') + str(c))
	elif str(mf_list[0]) == 'SUGON':
		for j in range(len(D_int_list)):
			c = D_int_list[j]
			commands.append(str('show interface ') + str(c))
	elif str(mf_list[0]) == 'SHENMA':
		for j in range(len(D_int_list)):
			c = D_int_list[j]
			commands.append(str('show interface ') + str(c))
	ip_d_list = ip_list[0]
	u = user_list[0]
	p1 = password1[0]
	p2 = password2[0]
	dg = D_G_list[0]
	if str(mf_list[0]) == 'HUAWEI':
		get_HUAWEI_D_result(ip_d_list,u,p1,p2,dg,commands)
	elif str(mf_list[0]) == 'ZXR10':
		get_ZXR10_D_result(ip_d_list,u,p1,p2,dg,commands)
	elif str(mf_list[0]) == 'DP':
		get_DP_D_result(ip_d_list,u,p1,p2,dg,commands)
	elif str(mf_list[0]) == 'SUGON':
		get_SUGON_D_result(ip_d_list,u,p1,p2,dg,commands)
	elif str(mf_list[0]) == 'SHENMA':
		get_SHENMA_D_result(ip_d_list,u,p1,p2,dg,commands)

def get_HUAWEI_D_result(ip_d_list,u,p1,p2,dg,commands):
	global interface,port_bandwidth,real_time_rate,description
	interface = []
	port_bandwidth = []
	real_time_rate = []
	description = []
	tn = telnetlib.Telnet(ip_d_list)
	tn.read_until('Username:')
	tn.write(str(u) + '\n')
	tn.read_until('Password:')
	tn.write(str(p1) + '\n')
	tn.read_until('>')
	tn.write('super\n')
	tn.read_until('Password:')
	tn.write(str(p2) + '\n')
	time.sleep(1)
	test = tn.read_very_eager()
	for command in commands:
		tn.write(command + '\n')
		for m in range(10):
			tn.write('\n')
		time.sleep(2)
		test1 = tn.read_very_eager()
		test2 = test1.split('\n')
		for line in range(len((test2))):
			l = test2[line]
			if str(l).find(dg) >= 0:
				interface.append('Interface:' + test2[line - 2].split()[0])
			if str(l).find('Port BW') >= 0 or str(l).find('BW') >= 0:
				port_bandwidth.append(l.split(',')[0])
			if str(l).find('input rate') >= 0:
				dk = l.split('rate')[1].split()[0]
				d_k = round(int(dk) / 1000.00 / 1000.00,2)
				real_time_rate.append('Real-time rate:' + str(d_k) + 'Mbps')
			if str(l).find('Description') >= 0:
				description.append(l.split(',')[0])
	tn.write('quit\n')
	return interface,port_bandwidth,real_time_rate,description,ip_d_list


def get_ZXR10_D_result(ip_d_list,u,p1,p2,dg,commands):
	global interface,port_bandwidth,real_time_rate,description
	interface = []
	port_bandwidth = []
	real_time_rate = []
	description = []
	if str(p2) != 'none':
		tn = telnetlib.Telnet(ip_d_list)
		time.sleep(1)
		tn.read_until('Username:')
		tn.write(str(u) + '\n')
		tn.read_until('Password:')
		tn.write(str(p1) + '\n')
		tn.read_until('>')
		tn.write('enable\n')
		tn.read_until('Password:')
		tn.write(str(p2) + '\n')
		time.sleep(1)
		test = tn.read_very_eager()
	else:
		tn = telnetlib.Telnet(ip_d_list)
		time.sleep(1)
		tn.read_until('Username:')
		tn.write(str(u) + '\n')
		tn.read_until('Password:')
		tn.write(str(p1) + '\n')
		tn.read_until('>')
		tn.write('enable\n')
		time.sleep(1)
		test = tn.read_very_eager()
	for command in commands:
		tn.write(command + '\n')
		time.sleep(1)
		for m in range(10):
			tn.write('\n')
		time.sleep(1)
		test1 = tn.read_very_eager()
		time.sleep(1)
		test2 = test1.split('\n')
		for line in range(len(test2)):
			l = test2[line]
			if str(l).find(dg) >= 0:
				a = test2[line - 1]
				interface.append('Interface:' + str(a).split()[0])
				description.append('Description:' + l.strip().split('is')[1].strip())
			if str(l).find('input  rate') >= 0:
				b = l.strip().split()[4]
				real_time_rate.append('Real_time_rate:' + str(round(int(b) * 8.00 / 1000.00 / 1000.00,2)) + 'Mbps')
			if str(l).find('BW') >= 0:
				port_bandwidth.append('Port BW:' + str(l).strip().split()[4] + 'Kbits')
	tn.write('exit\n')
	return interface,port_bandwidth,real_time_rate,description,ip_d_list


def get_DP_D_result(ip_d_list,u,p1,p2,dg,commands):
	global interface,port_bandwidth,real_time_rate,description
	interface = []
	port_bandwidth = []
	real_time_rate = []
	description = []
	space = '\n' * 10
	tn = telnetlib.Telnet(ip_d_list)
	time.sleep(1)
	tn.read_until('Login:')
	tn.write(str(u) + '\n')
	tn.read_until('Password:')
	tn.write(str(p1) + '\n')
	test = tn.read_very_eager()
	for command in commands:
		tn.write(command + '\n')
		time.sleep(1)
		for i in space:
			tn.write(i + '\n')
			time.sleep(1)
		test1 = tn.read_very_eager()
		test2 = test1.split('\n')
		for line in range(len(test2)):
			l = test2[line]
			if str(l).find(dg) >= 0:
				interface.append('Interface:' + test2[line - 12].split()[1])
				a = test2[line + 6].split('M')[0]
				port_bandwidth.append('Port BW:' + str(int(a) / 1000) + 'G')
				description.append(l.strip())
			if str(l).find('rxbytes') >= 0:
				b = l.split()[5]
				real_time_rate.append('Real_time_rate:' + str(round(int(b) / 1000.00 / 1000.00,2)) + 'Mbps')
	return interface,port_bandwidth,real_time_rate,description,ip_d_list


def get_SUGON_D_result(ip_d_list,u,p1,p2,dg,commands):
	global interface,port_bandwidth,real_time_rate,description
	interface = []
	port_bandwidth = []
	real_time_rate = []
	description = []
	tn = telnetlib.Telnet(ip_d_list)
	time.sleep(2)
	tn.read_until('name:')
	tn.write(str(u) + '\n')
	tn.read_until('password:')
	tn.write(str(p1) + '\n')
	time.sleep(1)
	for command in commands:
		tn.write(command + '\n')
		time.sleep(1)
		test1 = tn.read_very_eager()
		test2 = test1.split('\n')
		for line in range(len(test2)):
			l = test2[line]
			if str(l).find(dg) >= 0:
				interface.append('Interface:' + test2[line - 1].strip().split(':')[1])
				port_bandwidth.append('Port BW:' + test2[line + 11].split(':')[1].strip())
				description.append(l.strip().split()[1] + l.strip().split()[2])
			if (str(l).find('input rate') >= 0) and (str(l).find('kbps')     >= 0):
				ir = int(str(l).strip().split()[3]) / 1000.00
				real_time_rate.append('Real_time_rate:' + str(round(ir,2)) + 'Mbps')
	return	interface,port_bandwidth,real_time_rate,description,ip_d_list

def get_SHENMA_D_result(ip_d_list,u,p1,p2,dg,commands):
	global interface,port_bandwidth,description,real_time_rate
	interface = []
	port_bandwidth = []
	description = []
	real_time_rate = []
	tn = telnetlib.Telnet(ip_d_list)
	time.sleep(2)
	tn.read_until('login:')
	tn.write(str(u) + '\n')
	tn.read_until('Password:')
	tn.write(str(p1) + '\n')
	time.sleep(2)
	test1 = tn.read_very_eager()
	for command in commands:
		tn.write(command + '\n')
		time.sleep(1)
		test2 = tn.read_very_eager()
		test3 = test2.split('\n')
		for line in range(len(test3)):
			l = test3[line]
			if str(l).find(dg) >= 0:
				interface.append('Interface:' + test3[line - 9].strip().split(':')[1])
				real_time_rate.append('Real_time_rate:' + test3[line + 11].split()[3] + 'Mbps')
				description.append(l.split()[4])
			if str(l).find('input rate') >= 0 and str(l).find('kbps') >= 0:
				port_bandwidth = round(int(str(l).strip().split[3]) / 1000.00,2)
				port_bandwidth.append(port_bandwidth + 'Mbps')
	return interface,port_bandwidth,description,real_time_rate,ip_d_list


def DP_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	commands = 'show link port-rate-probe'
	tn = telnetlib.Telnet(str(address))
	time.sleep(2)
	tn.read_until('Login:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	tn.read_until('>')
	tn.write(commands + '\n')
	tn.write('exit\n')
	text1 = tn.read_all()
	tn.close()
	text2 = text1.split('\n')
	for i in range(len(text2)):
		text.append(str(text2[i]))
	check_result(text,G_mf)
	return text

def DP_U_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	tn = telnetlib.Telnet(str(address))
	time.sleep(1)
	tn.read_until('Username:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	tn.read_until('>')
	time.sleep(1)
	test1 = tn.read_very_eager()
	tn.write('show link port-rate-probe\n')
	time.sleep(1)
	text1 = tn.read_very_eager()
	tn.close()
	text2 = text1.split('\n')
	for i in range(len(text2)):
		text.append(str(text2[i]))
	check_result(text,G_mf)
	return text

def ZXR10_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	command1 = 'show security line-protect interface bind'
	tn = telnetlib.Telnet(str(address))
	time.sleep(2)
	tn.read_until('Username:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	tn.read_until('>')
	tn.write('en\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd2) + '\n')
	tn.write(command1 + '\n')
	tn.write('exit\n')
	text_int = tn.read_all()
	tn.close()
	text_l = str(text_int).split('\n')
	for i in range(len(text_l)):
		if text_l[i].strip().startswith('Interface'):
			break
	text_l = text_l[i+2]
	int_l = text_l.split()
	int = int_l[0]
	command2 = 'show security line-protect interface state ' + str(int)
	tn = telnetlib.Telnet(str(address))
	time.sleep(2)
	tn.read_until('Username:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	tn.read_until('>')
	tn.write('en\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd2) + '\n')
	tn.write(command2 + '\n')
	tn.write('exit\n')
	text1 = tn.read_all()
	tn.close()
	text2 = text1.split('\n')
	for i in range(len(text2)):
		if str(text2[i]).strip().startswith('Interface') or re.match('^[d-z]',str(text2[i]    )):
			text.append(str(text2[i]))
	check_result(text,G_mf)
	return text

def ZXR10_9005_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	tn = telnetlib.Telnet(address)
	time.sleep(1)
	tn.read_until('Username:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	tn.read_until('>')
	tn.write('enable\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd2) + '\n')
	time.sleep(1)
	test1 = tn.read_very_eager()
	tn.write('show protect-policy line-protect state\n')
	time.sleep(1)
	text = tn.read_very_eager()
	check_result(text,G_mf)
	return text

def HUAWEI_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	commands = 'display system status'
	tn = telnetlib.Telnet(str(address))
	time.sleep(1)
	tn.read_until('Username:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	tn.read_until('>')
	tn.write('super\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd2) + '\n')
	test_huawei = tn.read_very_eager()
	time.sleep(1)
	tn.write(commands + '\n')
	time.sleep(1)
	text1 = tn.read_very_eager()
	time.sleep(1)
	tn.write('quit\n')
	text2 = text1.split('\n')
	for i in  range(len(text2)):
		text.append(str(text2[i]))
	check_result(text,G_mf)
	return text

def SUGON_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	tn = telnetlib.Telnet(address)
	time.sleep(1)
	tn.read_until('name:')
	tn.write(str(G_username) + '\n')
	tn.read_until('password:')
	tn.write(str(G_passwd1) + '\n')
	time.sleep(1)
	tn.read_until('>')
	tn.write('show link\n')
	time.sleep(1)
	text1 = tn.read_very_eager()
	text2 = text1.split('\n')
	for i in range(len(text2)):
		if re.match('^\d',str(text2[i]).strip()):
			int1 = str(text2[i].strip().split()[0]) + str(text2[i].strip().split()[1])
			break
	command1 = 'link-protection ' + str(int1)
	tn.write(command1 + '\n')
	tn.read_until('>')
	tn.write('show optical-protection\n')
	time.sleep(1)
	text3 = tn.read_very_eager()
	text4 = text3.split('\n')
	for i in range(len(text4)):
		text.append(str(text4[i]))
	check_result(text,G_mf)
	return text

def SUGON_S214_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	tn = telnetlib.Telnet(address)
	time.sleep(1)
	tn.read_until('name:')
	tn.write(str(G_username) + '\n')
	tn.read_until('password:')
	tn.write(str(G_passwd1) + '\n')
	time.sleep(1)
	tn.read_until('>')
	tn.write('show link\n')
	time.sleep(1)
	text1 = tn.read_very_eager()
	text2 = text1.split('\n')
	for i in range(len(text2)):
		if re.match('^\d',str(text2[i]).strip()):
			int1 = str(text2[i].strip().split()[0])
			break
	command1 = 'link-protection ' + str(int1)
	tn.write(command1 + '\n')
	tn.read_until('>')
	tn.write('show optical-protection\n')
	time.sleep(1)
	text3 = tn.read_very_eager()
	text4 = text3.split('\n')
	for i in range(len(text4)):
		text.append(str(text4[i]))
	check_result(text,G_mf)
	return text

def SHENMA_status(address,G_username,G_passwd1,G_passwd2):
	global text
	text = []
	tn = telnetlib.Telnet(address)
	time.sleep(1)
	tn.read_until('login:')
	tn.write(str(G_username) + '\n')
	tn.read_until('Password:')
	tn.write(str(G_passwd1) + '\n')
	time.sleep(2)
	test1 = tn.read_very_eager()
	tn.write('show opm\n')
	time.sleep(1)
	test = tn.read_very_eager()
	test1 = test.split('\n')
	a = 'opt'
	b = 'pass'
	c = 'bypass'
	for i in range(len(test1)):
		p = str(test1[i]).strip()
		if re.findall('slot|opt\d',p):
			text.append(str(re.findall('slot|opt\d',p)))
		if re.findall('^\d|pass|bypass',p):
			text.append(str(re.findall('^\d|pass|bypass',p)))
	check_result(text,G_mf)
	return text

def get_G_status(address,G_mf,G_username,G_passwd1,G_passwd2):
	if str(G_mf) == 'DP':
		DP_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'DP_U':
		DP_U_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'ZXR10':
		ZXR10_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'ZXR10:9005':
		ZXR10_9005_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'HUAWEI':
		HUAWEI_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'SUGON':
		SUGON_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'SUGON:S214':
		SUGON_S214_status(address,G_username,G_passwd1,G_passwd2)
	elif str(G_mf) == 'SHENMA':
		SHENMA_status(address,G_username,G_passwd1,G_passwd2)

def sugon_change(request):
	global link
	link = ''
	link = request.GET['link']
	tn = telnetlib.Telnet(address)
	time.sleep(1)
	tn.read_until('name:')
	tn.write(str(G_username) + '\n')
	tn.read_until('password:')
	tn.write(str(G_passwd1) + '\n')
	time.sleep(1)
	tn.read_until('>')
	command1 = 'link-protection ' + str(link)
	if G_mf == 'SUGON':
		command2 = 'optical-protection pass'
	elif G_mf == 'SUGON:S214':
		command2 = 'optical-protection interdict'
	command3 = 'show optical-protection'
	tn.write(command1 + '\r\n')
	tn.read_until('>')
	tn.write(command2 + '\r\n')
	time.sleep(1)
	tn.write(command3 + '\r\n')
	time.sleep(1)
	text2 = tn.read_very_eager()	

	print G_mf
	return render_to_response('right.html',{'G_address':G_address,'address':address,'G_mf':G_mf,'text':text,'result':result,'interface':interface,'port_bandwidth':port_bandwidth,'real_time_rate':real_time_rate,'description':description,'ip_d_list':ip_d_list,'result_sugon':result_sugon,'text2':text2})




		


def change(request):
	if str(G_mf) == 'DP':
		link = []
		for i in range(len(text)):
			if text[i].find('bypass') >= 0:
				link.append(text[i].strip().split()[0])
		tn = telnetlib.Telnet(address)
		tn.read_until('Login:')
		tn.write(str(G_username) + '\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd1) + '\n')
		tn.read_until('>')
		tn.write('conf-mode\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd2) + '\n')
		for k in link:
			command = 'set ' + str(k) + ' optical pass'
			tn.write(command + '\n')
		tn.write('exit\n')
		tn.read_until('>')
		tn.write('show link\n')
		time.sleep(1)
		text2 = tn.read_very_eager()
	elif str(G_mf) == 'DP_U':
		tn = telnetlib.Telnet(address)
		tn.read_until('Username:')
		tn.write(str(G_username) + '\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd1) + '\n')
		tn.read_until('>')
		tn.write('conf-mode\n')
		tn.write('set 1 optical-protect pass\n')
		test1 = tn.read_very_eager()
		tn.write('show link port-rate-probe\n')
		time.sleep(1)
		text2 = tn.read_very_eager()
	elif str(G_mf) == 'ZXR10':
		text2 = []
		command1 = 'show security line-protect interface bind'
		tn = telnetlib.Telnet(address)
		time.sleep(1)
		tn.read_until('Username:')
		tn.write(str(G_username) + '\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd1) + '\n')
		tn.read_until('>')
		tn.write('enable\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd2) + '\n')
		test1 = tn.read_very_eager()
		tn.write(command1 + '\n')
		time.sleep(1)
		test2 = tn.read_very_eager()
		test3 = test2.split('\n')
		for i in range(len(test3)):
			if re.match('^[a-z]',str(test3[i])):
				int = str(test3[i]).strip().split()[0]
		int_l = [0,1,2]
		int_l[0] = 'configure terminal'
		int_l[1] = 'interface ' + str(int)
		int_l[2] = 'security line-protect switch pass'
		for l in int_l:
			tn.write(l + '\n')
			time.sleep(1)
		command2 = 'show security line-protect interface state ' + str(int)
		time.sleep(1)
		test4 = tn.read_very_eager()
		tn.write(command2 + '\r\n')
		time.sleep(1)
		test5 = tn.read_very_eager()
		tn.close()
		test6 = test5.split('\n')
		for i in range(len(test6)):
			if str(test6[i]).strip().startswith('Interface') or re.    match('^[d-z]',str(test6[i])):
				text2.append(test6[i])
	elif str(G_mf) == 'HUAWEI':
		tn = telnetlib.Telnet(address)
		time.sleep(1)
		tn.read_until('Username:')
		tn.write(str(G_username) + '\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd1) + '\n')
		tn.read_until('>')
		tn.write('super\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd2) + '\n')
		time.sleep(1)
		test1 = tn.read_very_eager()
		tn.write('display device\n')
		time.sleep(1)
		test2 = tn.read_very_eager()
		test3 = str(test2).split('\n')
		command2 = ''
		for i in range(len(test3)):
			l = str(test3[i]).strip()
			if l.find('OPM') >= 0:
				command1 = l.split()[0]
				command2 = 'opm ' + str(command1) + ' mode ' + 'pass'
				break
		if command2 == '':
			command_opm = 'opm-pic slot 1 card 0 mode pass'
		else:
			command_opm = command2
		tn.write('display epm\n')
		time.sleep(1)
		test4 = tn.read_very_eager()
		test5 = test4.split('\n')
		for i in range(len(test5)):
			line = str(test3[i]).strip()
			if re.match('^\d',line):
				command_epm =  'epm slot ' + line.split()[0] + ' mode pass'
		tn.write('system-view\n')
		tn.write('security-block\n')
		for i in range(len(text)):
			if (text[i].strip().find('OPM') >= 0) and (text[i].strip().find('bypass') >= 0):
				tn.write(command_opm + '\n')
				tn.write('quit\n')
				tn.write('quit\n')
				time.sleep(1)
				test6 = tn.read_very_eager()
				tn.write('display system status\n')
				time.sleep(1)
				text2 = tn.read_very_eager()
			if (text[i].strip().find('EPM') >= 0) and (text[i].strip().find('bypass') >= 0):
				tn.write(command_epm + '\n')
				tn.write('quit\n')
				tn.write('quit\n')
				time.sleep(1)
				test6 = tn.read_very_eager()
				tn.write('display system status\n')
				time.sleep(1)
				text2 = tn.read_very_eager()
		tn.close()
	elif str(G_mf) == 'SHENMA':
		tn = telnetlib.Telnet(address)
		time.sleep(1)
		tn.read_until('login:')
		tn.write(str(G_username) + '\n')
		tn.read_until('Password:')
		tn.write(str(G_passwd1) + '\n')
		time.sleep(2)
		tn.write('configure\n')
		command = ['opt slot-9 first pass','opt slot-9 second pass','opt slot-9 third pass','opt slot-9 forth pass']
		for i in range(len(command)):
			tn.write(str(command[i]) + '\n')
			time.sleep(1)
		tn.write('exit\n')
		time.sleep(2)
		test1 = tn.read_very_eager()
		tn.write('show opm\n')
		time.sleep(1)
		test2 = tn.read_very_eager()
		text2 = []
		test3 = test2.split('\n')
		for i in range(len(test3)):
			p = str(test3[i]).strip()
			if re.findall('slot|opt\d',p):
				text2.append(str(re.findall('slot|opt\d',p)))
			if re.findall('^\d|pass|bypass',p):
				text2.append(str(re.findall('^\d|pass|bypass',p)))
			
	return render_to_response('right.html',{'G_address':G_address,'address':address,'G_mf':G_mf,'text':text,'result':result,'interface':interface,'port_bandwidth':port_bandwidth,'real_time_rate':real_time_rate,'description':description,'ip_d_list':ip_d_list,'result_sugon':result_sugon,'text2':text2})

def check_result(text,G_mf):
	global result,result_sugon
	result = []
	result_sugon = ''
	for i in range(len(text)):
		if text[i].find('bypass') >= 0:
			result.append('bypass')
		elif text[i].find('interdict') >= 0:
			result.append('interdict')
		elif text[i].find('pass') >= 0:
			result.append('pass')
	if G_mf == 'SUGON' or G_mf == 'SUGON:S214':
		result_sugon = 'check links'
	return result,result_sugon



