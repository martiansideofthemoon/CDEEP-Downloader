import os,re
from subprocess import Popen
course = raw_input("Please enter your course ")
type1 = ['A','S']
year = ['02','03','04','05','06','07','08','09','10','11','12','13','14','15']
settings = []
for m in ['','-A']:
	for k in ['mp4','flv']:
		for i in type1:
			for j in year:
				if (os.system("rtmpdump -r rtmp://epay.cdeep.iitb.ac.in:1935/vod/Videos/"+i+j+"/"+course+"/"+course+"-L1"+m+"."+k+" -o civil."+k))==256:
					continue
				else:
					settings.append({"semester":i,"year":j,"filetype":k});
print "The following courses were found :- "					
for i in settings:
	print i["semester"]+" "+i["year"]
choice = input("Enter the course you would like (please enter a number :P ) ");
active = settings[choice-1]
base_url = "rtmp://epay.cdeep.iitb.ac.in:1935/vod/Videos/"+active["semester"]+active["year"]+"/"+course+"/"+course+"-L";
downloaded = []
for i in range(1,50):
	for j in ['','-A','-B','-C','-D']:
		code = os.system("rtmpdump -r "+base_url+str(i)+j+"."+active["filetype"]+" -o "+course+"-"+str(i)+"."+active["filetype"])
		if (code==256):
			os.system("rm "+course+"-"+str(i)+"."+active["filetype"]);
			continue;
		downloaded.append({"number":i,"type":j});
print downloaded
