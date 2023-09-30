from tkinter import *
from tkinter import messagebox
#abcdefghijklmnopqrstuvwxyz

#class for login
#init(self)

class Login:
  
  def __init__(self, master):

    self.master = master
    self.master.title("Login window")

    
    self.login_label = Label(master, text="Login")
    self.login_label.config(font=("Courier", 44))
    
    self.username_entry = Entry(master)
    self.password_entry = Entry(master, show='*')
    
    self.username_label = Label(master, text="Username")
    self.usernameR_label = Label(master, text="", fg='red')
    
    self.password_label = Label(master, text="Password")
    self.passwordR_label = Label(master, text ="", fg="red")
    
    self.login_button = Button(master, text="Login", command=self.loginPressed)
    self.signup_button = Button(master, text="Signup", command= self.signupPressed)
    self.quit_button = Button(master, text="Quit", command=self.quitPressed)
    
    self.login_label.grid(row=0,column=1,)
    
    self.username_entry.grid(row=1,column=1)
    self.password_entry.grid(row=2,column=1)
    
    self.username_label.grid(row=1,column=0)
    self.password_label.grid(row=2,column=0)
    
    self.login_button.grid(row=3,column=1, rowspan=2, sticky=W+E+S+N)
    self.signup_button.grid(row=3,column=0)
    
    self.quit_button.grid(row=4,column=0, sticky=W+E)
    
    self.usernameR_label.grid(row=1,column=2)
    self.passwordR_label.grid(row=2,column=2)


  def loginPressed(self):
    reader.updateValues() #update the current username and pass vals
    if reader.missingInfo() and reader.goodLogin(): #if it checks out...
      messagebox.showinfo('Nice', (f"Welcome {self.username_entry.get()}!"))
      self.userc = self.username_entry.get() #were gonna be using this userc to name our file so its unique for every login
      self.startMain() #this starts up the main window
    else:
      messagebox.showinfo('Oh no!', "Incorrect username and/or password") 
  
  def startMain(self): #method to start up the main window and move on from the login window
    self.master.destroy() #desttory this current window we have
    self.master = Tk() #start a new root//undermaster
    self.loginWindow = Mainpage(self.master,self.userc) #kept this as loginWindow just so it didn't messup anything with the sign up
    try: #this try and except is basically checking if there is already a file under this users name..
      save = open(f"{self.userc}.txt") #if I can open the file..
      save.close()
      self.master.mainloop() #start up normally
    except IOError: #if I cant...
      save = open(f"{self.userc}.txt", "w") #make a new file under this usernames name
      save.close()
      self.master.mainloop() #and start up


  def signupPressed(self): 
    self.signupWindow = Toplevel(self.master)
    self.newSignupWindow = Signup(self.signupWindow)

    #open up signupwindow with the class
  def quitPressed(self):
    self.master.destroy()


class Mainpage: #firstclass, the mainpage

  def __init__(self, master,name):

    self.master = master
    self.name = name #pass down this name for the file that well need
    self.master.title("Mainframe")

    self.homescreen_label = Label(master, text = "Homescreen||School IQ")
    self.homescreen_label.config(font=("Courier", 22))
    
    self.welcome_label = Label(master, text = f"Welcome {self.name}")
    self.welcome_label.config(font=("Courier", 12)) 

    self.classes_button = Button(master, text="Classrooms", command=self.classroomsPressed)


    self.homescreen_label.grid(row=0,column=0)
    self.welcome_label.grid(row=1,column=0)
    self.classes_button.grid(row=2,column=0, sticky=W+E)

  def classroomsPressed(self): #when the classrooms buttin is pressed..
    self.newClassroomsWindow = Toplevel(self.master)
    self.classroomsWindow = ClassroomsWindow(self.newClassroomsWindow,self.name) #make a new window and pass down that name that we want

class ClassroomsWindow: #the classrooms window

  def __init__(self, master,name): 

    self.master = master
    self.name = name
    self.master.title("Classrooms")
    
    self.allClasses = [] #this is where we will store all of the classrooms we make
    self.empty_label = Label(master, text="No classes yet, Make some :)") #this label will go away as I explain later

    self.addnew_button = Button(master, text="Create new classroom", command=self.createClassroom)
    self.empty_label.grid(row=1, column=0)
    self.addnew_button.grid(row=0, column = 0)
    self.checkClass() #this checks if there is any classrooms in that file we made under the username, if not, it removes that label and does something else....

    for i in range(len(self.allClasses)): #for however many classes there are..
      self.cur_button = 'button' + str(i) #make a new button..
      self.cur_button = Button(master, text= f"{self.allClasses[i][1]}|{self.allClasses[i][0]}",command = lambda: self.classPick(self.allClasses[i][1],self.allClasses[i][0]))
      #each button will just be button1,2 etc but the text will come from the list we have, giving us different names for our button each iteration
      #also we want to send a lambda if this button is clicked with its respective propties
      self.cur_button.grid(row=i+1,column=0, sticky=W+E)
    
  def classPick(self, subject, grade): #this fucmtoion runs if the button was clicked
    self.newViewClassWindow = Toplevel(self.master) #another window! the masters keep passing down
    self.ViewClassWindow = ViewClass(self.newViewClassWindow,subject,grade) #this time we want the subject and grade to create our class later
    
  def checkClass(self): #this just checks if its empty or not
    classrooms = open(f"{self.name}.txt", "r")
    first = classrooms.read(1)
    if not first:
      classrooms.close() #if its not do nothing
    else:
      self.addClasses() #if it isnt add some of those prior classesi in (load feature)
      self.empty_label.destroy()
      
  def addClasses(self): #load our classes in
    classrooms = open(f"{self.name}.txt", "r") #read the file
    for classroom in classrooms:
        classroom = classroom.rstrip()
        classroom = classroom.split(',')
        self.allClasses.append(classroom) #make a 2d list containing each classroom
        print(self.allClasses)
    classrooms.close() 

  def createClassroom(self):
    self.newCreateClassroomWindow = Toplevel(self.master) #atime to make another window where make our class
    self.createWindow = Create(self.newCreateClassroomWindow, self.name)


class ViewClass: #this is the big one with all the information about your class

  def __init__(self, master, subject, grade):

    self.master = master
    self.subject = subject
    self.grade = grade
    self.master.title(subject)

    self.createRealClass() #will xplain this later

    self.high_label = Label(master, text=f"High:{self.cur_class.high()}")#uses our classes methods
    self.low_label = Label(master, text=f"Low:{self.cur_class.low()}")
    self.average_label = Label(master, text=f"Average:{self.cur_class.classAverage()}")


    self.addStudent_button = Button(master, text="Add a Student", command = self.addedStudent)
    self.removeStudent_button = Button(master, text="Remove a Student", command = self.removeStudent)
   
    self.showClassList_button = Button(master, text="Show Classlist", command = self.showClass)
    self.addGrade_button = Button(master, text="Add a Grade", command = self.addGrade)
    self.showClassGrades_button = Button(master, text="Show Class grades", command = self.showAllGrades)

    self.students_button = Button(master, text="Students", command = self.showStudents)

    self.high_label.grid(row=0,column=0)
    self.low_label.grid(row=0,column=2)
    self.average_label.grid(row=0,column=1)

    self.addStudent_button.grid(row=1,column=0, rowspan = 1, sticky=S)
    self.removeStudent_button.grid(row=1,column=2,sticky=W+E )
    
    self.showClassList_button.grid(row=2,column = 2,sticky=W+E)

    self.addGrade_button.grid(row=3,column=0,sticky=W+E)
    self.showClassGrades_button.grid(row=3,column=2,sticky=W+E)

    self.students_button.grid(row=1,column=1, rowspan = 3, sticky=W+E+S+N)

  def addGrade(self):#if add grade button was pressed...
    self.newAddedGradeWindow = Toplevel(self.master)
    self.AddedGradeWindow = AddGrade(self.newAddedGradeWindow, self.cur_class)

  def createRealClass(self): #this runs when we open up the class
    self.cur_class = Classroom(self.subject,self.grade)#cretae our classroom object
    print(self.cur_class)

    self.allStudents = [] #make a list of all the students (load feauture)
    studentsFile = open("students.txt", "r") #get any students that we may have
    for student in studentsFile:
        student = student.rstrip()
        student = student.split(',') #same idea as loading the classes
        self.allStudents.append(student)
    print(self.allStudents)
    

    if len(self.allStudents) > 0:
      for i in range(len(self.allStudents)): #this one creates the classesusing the 2d list and uses the method from the classroom to add them in
        self.cur_class.addStudentToClass(Student(self.allStudents[i][0], self.allStudents[i][1], self.allStudents[i][2]))

  def addedStudent(self): #if add student was pressed...
    self.newAddedStudentWindow = Toplevel(self.master)
    self.AddedStudentWindow = AddStudent(self.newAddedStudentWindow, self.cur_class)
    
  def showClass(self): #simple popup to show the classlist in alphabetical order
    if not self.cur_class.showClassList():
      messagebox.showinfo('Class list', 'Empty')
    else:
      messagebox.showinfo('Class list', self.cur_class.showClassList())
    

  def showAllGrades(self):#shows all the grades as a dict
    messagebox.showinfo('All grades', f'{self.cur_class.showClassGrades()}')
    self.updateLabels()#also updates those labels at the top
  
  def updateLabels(self):
    self.high_label.config(text=f"High:{self.cur_class.high()}")
    self.low_label.config(text=f"Low:{self.cur_class.low()}")
    self.average_label.config(text=f"Average:{self.cur_class.classAverage()}")

  def removeStudent(self): #if remove student was pressed...
    self.newRemoveStudentWindow = Toplevel(self.master)
    self.removeStudentWindow = removeStudent(self.newRemoveStudentWindow,self.cur_class)

  def showStudents(self): #if show students was pressed...
    self.newStudentsWindow = Toplevel(self.master)
    self.StudentsWindow = StudentsWindow(self.newStudentsWindow,self.cur_class)


class StudentsWindow: #this window shows details on every student

  def __init__(self, master, classe):

    self.master = master
    self.cur_class = classe #get the class object passed down
    self.master.title("Students")

    i = 1 
    for name, student in self.cur_class.students.items(): #for the items in our dict...
      self.cur_button = 'button' + str(i) #make some buttons
      self.cur_button = Button(master, text= f"{student.lastName}", command = lambda: self.studentPressed(student)) #config that button
      print(student)
      self.cur_button.grid(row=i+1,column=0, sticky=W+E)
      i += 1 #and do it until weve moved through every value of the dict

  def studentPressed(self, student): #if we click a certain student..
    student.set_Classroom(self.cur_class) #use the set_classroom method wihtin the student to get the grades from that class
    self.newStudentDetailsWindow = Toplevel(self.master) #make another window
    self.StudentDetailsWindow = StudentDetails(self.newStudentDetailsWindow,self.cur_class,student)


class StudentDetails: #details on each student

  def __init__(self, master, classe, student):

    self.master = master
    self.cur_class = classe
    self.cur_student = student #we passed this down earlier, we can use this object for the use of its methods
    self.master.title("Student Details")

    self.studentlastname_label = Label(master, text=f'Lastname:{self.cur_student.lastName}') #allows us to see some stats
    self.studentgrades_label = Label(master , text=f"Grades:{self.cur_student.studentGrades()}")
    self.studentavg_label = Label(master , text=f"Avg:{self.cur_student.studentAvg()}")

    self.studentlastname_label.grid(row=0,column=0)
    self.studentgrades_label.grid(row=1,column=0)
    self.studentavg_label.grid(row=2,column=0)

class removeStudent: #wanting to remove a student from the class

  def __init__(self,master, classe):

    self.master = master
    self.cur_class = classe
    self.master.title("Remove Student")

    i = 1
    for name, student in self.cur_class.students.items(): #again, makes a list of buttons for us to choose from
      self.cur_button = 'button' + str(i)
      self.cur_button = Button(master, text= f"{student.lastName}",command = lambda: self.removeStudent(student.lastName))
      self.cur_button.grid(row=i+1,column=0, sticky=W+E)
      i += 1

  def removeStudent(self, lastname): #if we click on a student...
    self.cur_class.removeStudent(lastname)#remove it from the classroom object
    messagebox.showinfo('Removed', f'{lastname} was removed from the class')
    oldstudents = open("students.txt", "r") #but also remove it from the file
    students = oldstudents.readlines() #save all the old lines from the file
    oldstudents.close()
    newStudents = open("students.txt", "w")
    for student in students: #rewrite the files in but dont write in if we get the same lastname at the start
      if not student.strip('\n').startswith(lastname):
        newStudents.write(student)
    newStudents.close()

    for name, grade in self.cur_class.classGrades.copy().items(): #have to create temp copy to avoid runtime error when the dictonary changes during the iterations
      if name == lastname: #find that student we want
        self.cur_class.classGrades.pop(name) #remove them from the students dict

    self.master.destroy()
  
class AddGrade: #adding a grade window

  def __init__(self, master, classe):

    self.master = master
    self.cur_class = classe
    self.master.title("Add a grade")

    self.lastname_label = Label(master, text="Lastname")
    self.grade_label = Label(master, text="Grade")

    self.lastname_entry = Entry(master)
    self.grade_entry = Entry(master)

    self.add_button = Button(master, text="Add", command = lambda: self.addGradePress(self.lastname_entry.get(),self.grade_entry.get())) #just simply gets entries and passes it through a lambda

    self.lastname_label.grid(row=0,column=0)
    self.grade_label.grid(row=1,column=0)
    
    self.lastname_entry.grid(row=0,column=1)
    self.grade_entry.grid(row=1,column=1)
    
    self.add_button.grid(row=2,column=1,sticky=W+E)

  def addGradePress(self, last, grade):
    self.cur_class.addGrade(last,int(grade)) #makes it an int so we can calculate averages
    self.master.destroy()

      
class AddStudent: #wanting to add a new student...

  def __init__(self, master, classe):

    self.master = master
    self.cur_class = classe
    self.master.title("New Student")

    self.lastname_label = Label(master, text="Lastname")
    self.firstname_label = Label(master, text="Firstname")
    self.age_label = Label(master, text="Age")

    self.lastname_entry = Entry(master)
    self.firstname_entry = Entry(master)
    self.age_entry = Entry(master)

    self.add_button = Button(master, text="Add", command = lambda: self.addStudentPress(self.lastname_entry.get(),self.firstname_entry.get(),self.age_entry.get()))

    self.lastname_label.grid(row=0,column=0)
    self.firstname_label.grid(row=1,column=0)
    self.age_label.grid(row=2,column=0)

    self.lastname_entry.grid(row=0,column=1)
    self.firstname_entry.grid(row=1,column=1)
    self.age_entry.grid(row=2,column=1) 

    self.add_button.grid(row=3,column=1,sticky=W+E)

  def addStudentPress(self, last, first, age): #after we filled in everything and want to add this student
    self.cur_class.addStudentToClass(Student(last, first, age)) #add it to the classroom object
    students = open("students.txt", "a") #but also add them to the file to save them
    students.write(f"{last},{first},{age}\n")
    students.close()
    messagebox.showinfo('Nice!', f"{last} was added to the class")
    
    self.master.destroy() #destroy afterwards

class Create: #create a new classroom

  def __init__(self, master, name):

    self.master = master
    self.name= name
    self.master.title("Create new")

    self.subject_entry = Entry(master)
    self.subject_label = Label(master, text="Subject")

    self.subject_entry.grid(row=0,column=1)
    self.subject_label.grid(row=0,column=0)

    self.grade_entry = Entry(master)
    self.grade_label = Label(master, text="Grade")#Make so only number

    self.grade_entry.grid(row=1,column=1)
    self.grade_label.grid(row=1,column=0)

    self.create_button = Button(master, text="Create", command=self.createClass)

    self.create_button.grid(row=2,column=1,sticky = W+E)

  def createClass(self): #run this fucntion if we click create
    subjectE = self.subject_entry.get()
    gradeE = self.grade_entry.get()
    classrooms = open(f"{self.name}.txt", "a") #had to \n cause for some reason it wasnt moving down lines
    classrooms.write(f"{gradeE},{subjectE}\n")
    classrooms.close()
    messagebox.showinfo('Congrats!', 'You made a new classroom!')
    self.master.destroy()
    
class Signup:
  
  def __init__(self, master):

    self.master = master
    self.master.title("Signup window")
    
    self.signup_label = Label(master, text="Signup")
    self.signup_label.config(font=("Courier", 44))
    
    self.password_entry = Entry(master, show='*')
    self.passwordConfirm_entry = Entry(master, show='*')
    self.username_entry = Entry(master)
    
    self.password_label = Label(master, text="Password")
    self.passwordConfirm_label = Label(master, text="Confirm password")
    self.username_label = Label(master, text="Username")
    
    self.submit_button = Button(master, text="Submit", command=self.signupPressed)
    self.quit_button = Button(master, text="Exit", command=self.quit)

    self.signup_label.grid(row=0,column=1)
    
    self.password_entry.grid(row=2,column=1)
    self.passwordConfirm_entry.grid(row=3,column=1)
    self.username_entry.grid(row=1,column=1)
    
    self.password_label.grid(row=2,column=0)
    self.passwordConfirm_label.grid(row=3,column=0)
    self.username_label.grid(row=1,column=0)
    
    self.submit_button.grid(row=4,column=1)
    self.quit_button.grid(row=4,column=0)

  def quit(self):
    self.master.destroy()

  def signupPressed(self):
    writer.allCheck()
    
class Read:

  def __init__(self):
    self.self = self
  
  def updateValues(self):
    self.username = loginWindow.username_entry.get()
    self.password = loginWindow.password_entry.get()
  
  def goodLogin(self):
    database = open("database.txt", "r")
    for userpass in database:
      userpass = userpass.rstrip()
      if userpass.startswith(self.username) and userpass.endswith(self.password):
        return True
    return False

  def missingInfo(self):
    if not self.username and not self.password:
      loginWindow.usernameR_label.config(text="*")
      loginWindow.passwordR_label.config(text="*")
      return False
    elif not self.password:
      loginWindow.usernameR_label.config(text="")
      loginWindow.passwordR_label.config(text="*")
      return False
    elif not self.username:
      loginWindow.usernameR_label.config(text="*")
      loginWindow.passwordR_label.config(text="")
      return False
    else:
      return True

class Write:

  def __init__(self):
    self.self = self

  def updateValues(self):
    self.username = loginWindow.newSignupWindow.username_entry.get()
    self.password = loginWindow.newSignupWindow.password_entry.get()
    self.passwordC = loginWindow.newSignupWindow.passwordConfirm_entry.get()
    
  def allCheck(self):
    self.updateValues()
    if self.missingInfo() and self.sameCheck() and self.length() and self.upperSymbolCheck() and self.userTaken():
      self.writeToDatabase()
      messagebox.showinfo('Congrats!', 'You made a new account!')
      loginWindow.newSignupWindow.quit()

  def length(self):
    lucky = 0
    if (6 <= len(self.username) <= 10) and (6 <= len(self.password) <= 10):
      return True
    else:
      messagebox.showinfo('Oh no!','Your username and password must be 6-10 characters long!')
      return False 

    #check username and password lengths and raise error as needed
  def upperSymbolCheck(self):
    lucky = 0
    if not self.password.isalnum():
      if any(x.isupper() for x in self.password):
        return True
         #There is an upper and symbol
      else:
        messagebox.showinfo('Oh no!','You also need an uppercase letter in your password!')
        return False  #Symbol but no upper
    else:
      messagebox.showinfo('Oh no!','You need an uppercase letter and symbol in your password!')
      return False 
      #No upper and no Symbol
    #check for symbol in password
  
  def writeToDatabase(self): #if all info is correct send it to the database
    database = open("database.txt", "a")#a appends
    database.write(f"{self.username},{self.password}")
    database.close()

  def missingInfo(self):
    lucky = 0
    if self.password and self.passwordC and self.username:
      return True
    else:
      messagebox.showinfo('Oh no!','Fill out all fields!')
      return False
    #are we missing any info/are the entries empty

  def sameCheck(self):
    lucky = 0
    if self.password == self.passwordC:
      return True
    else:
      messagebox.showinfo('Oh no!','The two passwords you entered are not the same!')
      return False
      
    #are the pass and passC the same reutrn true or false

  def userTaken(self):
    database = open("database.txt", "r")
    for userpass in database:
      userpass = userpass.rstrip()
      if userpass.startswith(self.username):
        messagebox.showinfo('Oh no!','That username is taken!')
        return False
    return True
      
    #is this username already taken? check it out

def checkInt(request):#Function to check if inputs are getting integers
  while True:
    try:
      number = int(input(request))
      break
    except ValueError:
      print("Please try again! You need to input an integer!")
  return number

class School(): #School class

  def __init__(self, schoolName, location, classrooms = []):
    self.schoolName = schoolName #initlizes with a name given by the user and location
    self.location = location
    self.classrooms = classrooms #school has classrooms, thes can be stored in a ist to be acsessed later form of compostion

  def get_schoolName(self): #returns the schoolName
    return self.schoolName
  
  def addClassroom(self, classroom): #this needs a parametr of the classroom (which will be in the form of a Class(not classroom)) this is stored in the list that we initlized
    self.classrooms.append(classroom)

  def get_schoolLocation(self): #return the location
    return self.location

  def set_schoolName(self, schoolName): #set the school name with provided school name
    self.schoolName = schoolName

  def set_schoolLocation(self, location): #set the school locaiton with the provided school location
    self.location = location

class Person(): #Person class (superclass for students)

  def __init__(self, lastName, firstName): #initlize with a firstname and lastname
    self.lastName = lastName
    self.firstName = firstName

  def get_lastName(self): #return the lastname of the person
    return self.lastName

  def get_firstName(self): #return the firstname of the person
    return self.firstName

class Classroom(): #Classroom class 
   
  
  def __init__(self, subject, grade, students = {}, classGrades = {}, classList = {},  allGrades=[]):#initlize some variables
    self.grade = grade #set the grade (grade 12, 11, etc.)
    self.subject = subject #set the subject (science, math etc)
    self.classList = classList #make an empty classList, this classlist is a dictonary thatwill store key:lastname and value:firstname
    self.classGrades = classGrades #this class grade dict will store key:lastname and value:[grades] (so a dicotary and has values as lists)
    self.students  = students#make a dict where we ill store the student classes in): 
    self.allGrades = allGrades#make a list to store all the grades in a list (this list has all the grades in a 1D list for easy comparisions and acsessabiliy)

  def addGrade(self, lastName, grade): #with this function we can add grades for a student
    self.classGrades.setdefault(lastName, []) #what this does is allows us to add value to the classGrades dict as a list, so we can append grades as lists
    self.classGrades[lastName].append(grade) #add a key:lastname and value:[grade], this way we can add multiple grades to each student as a list
    self.createAllGrades() #call the createAllGrades() which we know just makes a list of grades as a 1D list

  def createAllGrades(self): #with this function we will get the dict of classGrades and convert it to a sorted 1D list

    if not self.classGrades: #check to see if classGrades is empty or not
      print("Add grades using addGrade method first")
    else:
      for i in list(self.classGrades.values()): #for each value in classGrade (remember each value is a list right now so classGrades.values() is basically a 2D list)
        for j in i: #for each element in that 2D list
          if j not in self.allGrades: #this is just so we dont repeat and add the same value because we do call this function everytime we add a new grade
            self.allGrades.append(j) #append that value to allGrades to make a 1D list
    
    #just the bubble sort algoritim to sort the list (didn't have to because the list is probably not going to be that large)
      done = False #to start loop
      while not done:  
        done = True #when theres no more items to sort this will remain true
        for i in range(len(self.allGrades) - 1):
          if self.allGrades[i] > self.allGrades[i+1]:
            done = False #everytime a swap is avaliable the loop will continue
            self.allGrades[i], self.allGrades[i+1] = self.allGrades[i+1], self.allGrades[i]


  def showClassGrades(self): #prints the classGrades which show each students grades
    print(self.allGrades) #shows the entire classes grades anonymously
    return (self.classGrades)
      
  def attendance(self): #we can do the attendance using this funciton
    for name, student in self.students.items(): #for each key, value for the dict students (students dict has values that are objects)
      student.here = checkInt(f"Is {student.lastName} here? (1 for yes, 2 for no) ") #set each students here varible to really any number (we are just going to see if they are here (1 input))

    for name, student in self.students.items(): #iterate through the list again
      if student.here == 1: #if the changed varible of the students self.here is 1..
        print(f"{student.lastName} is here") #print they are here
      else:#if they inputted anything other than 1..
        print(f"{student.lastName} is not here") #say thy arent here

  def high(self): #check the allGrades for the higest value
    if not self.classGrades: #check to see if its empty, (we check the classGrades list because allGrades is made everytime classGrades is changed)
      return("No Grades")
    else:
      return self.allGrades[-1] #since this list is sorted we can just get the top index

  def low(self):#check the allGrades for the lowest value
    if not self.classGrades: #same reason as earlier
      return("No Grades")
    else:
      return self.allGrades[0] #again, since its sorted we just get the first index and return it

  def classAverage(self):#this gets the average of the allGrades list
    if not self.classGrades: #same as earlier
      return("No Grades")
    else: #little algoritim to get the average of the list
      total = 0
      for number in self.allGrades:
        total += number
      return total//len(self.allGrades) #returns a number value (average)
  
  def makeClassList(self): #this creates the classList dict, this is called everytime we add a student to our classroom
    for key, student in self.students.items(): #iterate through our students dict...
      self.classList[student.lastName] = student.firstName #add values to our classList based on the students last and first name

  def addStudentToClass(self, student): #adding students to the class using this funciton 
    self.students[student.firstName] = student #the student in this case will be passed as a class, so we are making a dict using class's as values
    self.makeClassList() #update the classlist each time we add a new student
    return print(f"{student.lastName} was added to the class")
    
  def removeStudent(self, lastName): #remove student by last name
    if not self.classList: #check to see if the classlist is empty or not
      return ("Add students to class first")
    else:
      for name, student in self.students.copy().items(): #have to create temp copy to avoid runtime error when the dictonary changes during the iterations
        if student.lastName == lastName: #find that student we want
          self.students.pop(name) #remove them from the students dict
      return self.classList.pop(lastName) #and remove them from the classList

  def showClassList(self): #print the class list in alphabetical order
    return (sorted(self.classList))
  
  def __str__(self): #easy way to display the classroom and some of its attributes
    return (f"GRADE: {self.grade}\nSUBJECT: {self.subject}\nCLASSSIZE: {len(self.classList)}")
    
class Student(Person): #student class that inheirts from the Person super class

  def __init__(self, lastName, firstName, age, grade=None, subject=None, grades = [], here=0, notes="Empty"):
    Person.__init__(self, lastName, firstName) #get the inherited init from person so we can possibliy utilitze its methods
    self.age = age #set age from provided parameters
    self.classroom = Classroom(subject, grade) #the classroom with be set later using a method,
    self.grades = grades #grades will empty for a new student
    self.here = here #not here by default
    self.notes = notes #notes are also empty
    
  def studentGrades(self): 
    if not self.classroom.classGrades: #check to see if they have set a classroom for the student, and if they have check to see if the classGrades is empty or not
      return("The class has added no grades yet")
    else: #if it has values...
      for name, grades in self.classroom.classGrades.items(): #iterate through that dict
        if name == self.lastName: #if their lastname matches...
          self.grades.append(grades) #append that value to their own grades
      return self.grades #gives us a 2d list
  
  def studentAvg(self): #check the students average
    if not self.grades: #check to see if grades list is empty or not
      print("Use the studentGrades method to get grades for the student first")
    else: #if it has something..
      total = 0
      i = 0
      for grades in self.grades: #for each list in the 2d list of grades...
        for grade in grades: #for each elemtn within that list
          total += grade 
          i += 1 #count the amount of iterations we have so we can divide by that number (amount of values there are within that 2d list)
      self.grade = total//i
      return self.grade #return their grade

  def set_Classroom(self, classroom): #this allows them to set the classroom, this will be passed as a object when it is set 
    self.classroom = classroom #composition will allow us to use methods from classroom and its attributes
  
  def isHere(self): #check self.here to see if the student is here or not
    if self.here == 1:
      return print(f"{self.lastName} is here")
    else:
      return print(f"{self.lastName} is not here")

  def addNotes(self, notes): #add any special notes to each setudent (set_notes) 
    self.notes = notes
    return print (f"{self.firstName}'s notes have been updated to '{self.notes}'")

  def __str__(self): #print lastname,firstname of student everytime object is printed
    return (f"{self.lastName},{self.firstName}")

root = Tk()
writer = Write()
reader = Read()

loginWindow = Login(root)
root.mainloop() 

#