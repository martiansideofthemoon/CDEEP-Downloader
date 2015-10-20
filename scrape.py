import os,re,subprocess,itertools,time,sys

def validate_input(course):
	courseRegex = re.compile(r'^([A-Z][A-Z])\s?(\d\d\d)$',re.VERBOSE)
	result = courseRegex.search(course)
	if result==None:
		return 0
	else:
		return result.group(1)+result.group(2)

def print_progress(count):
	sys.stdout.flush()
	percent = count*100/112
	progress = "Running..."+str(percent)+"% "
	print "\r"+progress,

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
base_url = "rtmp://epay.cdeep.iitb.ac.in:1935/vod/Videos/"
courses_found = []
count=1
for i,j,k,l in itertools.product(brute_types,filetype,semester,year):
	url = base_url+k+l+"/"+course+"/"+course+"-L1"+i+"."+j
	command = ["rtmpdump","-r "+url,"-o test."+j]

	print_progress(count)
	count+=1
	start=time.clock()
	process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	while (process.poll()==None):
		if (time.clock()-start>1):
			process.kill()
			courses_found.append({"semester":k,"year":l,"filetype":j});
			break

print "\nWe found the following courses. Choose one. "
num = 1
for course in courses_found:
	if (course["semester"]=="S"):
		print str(num)+". Spring 20"+course["year"]
	else:
		print str(num)+". Autumn 20"+course["year"]
	num+=1

"""
for m in ['','-A']:
	for k in ['mp4','flv']:
		for i in type1:
			for j in year:
				if (os.system("rtmpdump -r rtmp://epay.cdeep.iitb.ac.in:1935/vod/Videos/"+i+j+"/"+course+"/"+course+"-L1"+m+"."+k+" -o civil."+k))==256:
					continue
				else:
					
print "The following courses were found :- "					
for i in settings:
	print i["semester"]+" "+i["year"]
choice = input("Enter the course you would like (please enter a number :P ) ");
active = settings[choice-1]
base_url = "rtmp://epay.cdeep.iitb.ac.in:1935/vod/Videos/"+active["semester"]+active["year"]+"/"+course+"/"+course+"-L";
downloaded = []
for i in range(1,50):
	for j in ['','-A','-B','-C','-D']:
		code = os.system("rtmpdump -r "+base_url+str(i)+j+"."+active["filetype"]+" -o "+course+"-"+str(i)+j+"."+active["filetype"])
		print code
		if (code==256):
			os.system("rm "+course+"-"+str(i)+j+"."+active["filetype"]);
			continue;
		downloaded.append({"number":i,"type":j});
print downloaded
"""
