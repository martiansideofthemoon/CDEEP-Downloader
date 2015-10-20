import os,re,subprocess,itertools,time,sys,thread

base_url = "rtmp://epay.cdeep.iitb.ac.in:1935/vod/Videos/"

def base_thread(threadName,url,course,file_number,filetype):
	command = ["rtmpdump","-r "+url,"-o "+course+file_number+"."+filetype]
	process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	while(process.poll()==None):
		pass

def validate_input(course):
	courseRegex = re.compile(r'^([A-Z][A-Z])\s?(\d\d\d)$',re.VERBOSE)
	result = courseRegex.search(course)
	if result==None:
		return 0
	else:
		return result.group(1)+result.group(2)

def print_progress(message, count, total):
	sys.stdout.flush()
	percent = count*100/total
	progress = message+" "+str(percent)+"% "
	print "\r"+progress,

def generate_urls(course, choice):
	urls=[]
	filestyles = ['','-A','-B','-C','-D']
	count=1
	for i,j in itertools.product(range(1,50),filestyles):
		url = base_url+choice["semester"]+choice["year"]+"/"+course+"/"+course+"-L"+str(i)+j+"."+choice["filetype"]
		command = ["rtmpdump","-r "+url,"-o test."+j]
		print_progress("Generating URLs...",count,245)
		count+=1
		start=time.clock()
		process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		while (process.poll()==None):
			if (time.clock()-start>1):
				process.kill()
				urls.append(url)
				break
	return urls



course = raw_input("Please enter your course :- ")
course = validate_input(course)

# 'A' represents Autumn and 'S' represents Spring
semester = ['A','S']
# Courses on CDEEP vary from 2002 to 2015
year = ['02','03','04','05','06','07','08',
		'09','10','11','12','13','14','15']
# Filetype added for two possible course files
filetype = ['mp4','flv']
# Type of file (complete or part A to look for during brute force
brute_types = ['','-A']
courses_found = []
count=1
for i,j,k,l in itertools.product(brute_types,filetype,semester,year):
	
	url = base_url+k+l+"/"+course+"/"+course+"-L1"+i+"."+j
	command = ["rtmpdump","-r "+url,"-o test."+j]

	print_progress("Brute Forcing...",count,112)
	count+=1

	start=time.clock()
	process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	while (process.poll()==None):
		if (time.clock()-start>1):
			process.kill()
			courses_found.append({"semester":k,"year":l,"filetype":j});
			break

if len(courses_found)==0:
	print "\nNo courses found. Check CDEEP / internet connection"
	sys.exit()
print "\nWe found the following courses. Choose one. "
num = 1
for c in courses_found:
	if (c["semester"]=="S"):
		print str(num)+". Spring 20"+c["year"]
	else:
		print str(num)+". Autumn 20"+c["year"]
	num+=1
select = input("Enter your choice. 0 to quit. ")
if (select==0):
	sys.exit()
choice = courses_found[select-1]
urls = generate_urls(course, choice)
print urls

k=1
proc = []
for url in urls:
	command = ["rtmpdump","-r "+url,"-o "+course+str(k)+"."+choice["filetype"]]
	proc.append(subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE))
	k+=1
for p in proc:
	p.wait()