'''
Created on Apr 2, 2019

@author: cch2owater
'''

#This function returns classes in 2 programs
def processProgramFile(path):
    import os
    
    program1path = os.path.join(path,'program1.txt');program2path = os.path.join(path,'program2.txt')
    program1 = open(program1path,'r');program2 = open(program2path,'r')#read the files 
    
    pname1 = program1.readline().rstrip('\n');pname2 = program2.readline().rstrip('\n')#obtain the first line string as the program name and move the read point to next line
    
    dict_1 = {};dict_2 = {} #create 2 empty dictionaries
    for line in program1:
        line = line.replace('.','')#replace the dot with empty string
        courselist1 = line.rstrip('\n').split(' ',1)#I only want the line to split once, so that the first is number and rest is the name
        
        dict_1[courselist1[0]] = courselist1[1]#assign the number as key and coursename as string
    #do the same thing for program 2
    for line in program2:
        line = line.replace('.','')
        courselist2 = line.rstrip('\n').split(' ',1)#split the remaining text into list
        
        dict_2[courselist2[0]] = courselist2[1]
    finaltuple = (pname1,dict_1,pname2,dict_2) #put all the necessary elements into a tuple
    program1.close();program2.close();

    return finaltuple; #return the tuple

#This function returns a dictionary of classes that have prereqs
def processPrereqFile(path):  
    import os.path
    prereqs = os.path.join(path,'prereqs.txt')
    file = open(prereqs,'r') #open the file and read it
    
    prelist = file.read().split('\n')#split the text using linebreaks
   
    courselist =[]; requirelist = [] #create two empty list for later 
    
    for item in prelist:
        course,require = item.split(':') #for every string in the prereqs text list, split the string using colons
        require = require.strip() #get rid of spaces on both sides if any
        courselist.append(course);requirelist.append(require) #build a list with course number only and prereqs only
    
    dict_prereqs = {}
    for index in range(len(courselist)):#courselist and requirelist should have the same length
        dict_prereqs.update({courselist[index]:requirelist[index]}) #for the fist element in courselist it is the key, the first element in requirelist is the 
                                                            #value of the first key 
    
    file.close();
    return dict_prereqs;#return the dictionary

#this function returns a dictionary of students in every class
def processClassFiles(subfolder):
    import os.path
    txtlist = os.listdir(subfolder)

    dict_class = {}
    unwantedfile = ('program1.txt','program2.txt','prereqs.txt')# those files are not needed
    
    #for files that are not in the unwantedfiles,open them, split the text so that the index 0 is the coursenumber, 
    # and index 1 will be the student name by taking an incremental step of 2
    for file in txtlist:
        if file in unwantedfile:
            continue;
        else:
            text = open(os.path.join(subfolder,file),'r')
            textlist= text.read().split()
            
            coursenum = textlist[0][1:]
            
            student = textlist[1::2]
    
            if coursenum in dict_class.keys():#if the course already exists, we want to update the values for this course;otherwise, assign a new key
                dict_class[coursenum] += student
            else:
                dict_class.update({coursenum:student})  
            text.close();  
     
    return  dict_class;

def initFromFiles(subfolder):
    #just call the previous 3 functions and construct a tuple that contains the output from them
    course = processProgramFile(subfolder)
    classlist = processClassFiles(subfolder)
    prereqs = processPrereqFile(subfolder)
    
    finaltuple = (course,classlist,prereqs)
    return finaltuple;


#this function does the calculation of how many students are eligible to take the class  
def estimateClass(coursenum,tuplelist):    #can add multiple parameters if needed
    #I choose to the tuplelist from the initFromFiles() functions as it contains the info I need.
    classlist = tuplelist[1]
    prereqs = tuplelist[2]
    program1 = tuplelist[0][1];program2 = tuplelist[0][3]
    studentlist = []
    
    #construct a student list that will have all student names in the school
    for classes,student in classlist.items():
        for studentname in student:
            if studentname in studentlist:
                continue;
            else:
                studentlist.append(studentname)
    
         
    estudentlist = []   
    #if this is a real course:

    if coursenum in classlist.keys():  
        #remaining students: remove the students that took or are currently in the class， I just need to take the difference between all students 
        #and the students that are already in the class or was in the class.
        Rstudent = set(studentlist).difference(set(classlist[coursenum]))
        if coursenum in program1:
            coursename = program1[coursenum]
        else:
            coursename = program2[coursenum] 
        # if this is a class that needs prerequisites, we want to sum all the students 
        #who took the prereq classes and put it into a new list for return purpose
        if coursenum in prereqs.keys():
            pre_course = prereqs[coursenum]
            
            for course in pre_course.split():
                student = classlist[course]
                estudentlist.append(Rstudent.intersection(set(classlist[course])))#use intersection to collect students who took the prereq class before.
        else:   #the class does not need prerequisites
            estudentlist = list(Rstudent)
    else:  #if the coursenum does not exist     
        coursename = "None"
        estudentlist = []       
    print(coursename)
    estudentlist = sorted(tuple(estudentlist))#provide a sorted list of students
    
    return coursename,estudentlist;

def main():
    import os
    file = input('Please enter the name of the subfolder with files:')
    i = 0
    while i == 0:
        coursenum = input('Enter course number or press enter to stop:')
        if coursenum == '':
            i = 1;#if the user does not enter any value, stop the loop.
        else:
            folderpath = os.path.join(os.getcwd(),file)
            classinfo = initFromFiles(folderpath)    
            courselabel,studentlist= estimateClass(coursenum, classinfo)     
            if courselabel != 'None':# if the courselabel is not None, it means this class is existent
                print('There are ',len(studentlist),' students who could take course',coursenum,courselabel+'.')
            else:
                print('There are ',len(studentlist),' students who could take course',coursenum,courselabel)
  
main()
    
    
    
    
    