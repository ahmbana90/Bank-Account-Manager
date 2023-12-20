
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
class Bank_account:        #a class to get bank accounts
    def __init__(self,name,age,sex,balance):   #attrib. of each account
        self.name=name
        self.age=age
        self.sex=sex
        self.balance=balance 
        self.withd_status="False"  #statuse of withdrowal
        #self.all=self.name,self.age,self.sex,self.balance  #all info. of each account
    def withdraw(self,a):   #withdraw method
        if (a>self.balance):     #first cheak balance and the wanted amount
            print("Max. Allowed Withdraw :",self.balance)
        elif a<=0:
            raise NameError("Error Withdrawal Input")
        else:
            self.balance-=a      #if amount is acceptable then subtract
            self.withd_status="True"    #from balance
            print("Withdrawal :\n",a,
            "\nRemaining Amount :",self.balance,) #show remaining amount
    def deposit(self,a):  #deposit method 
        if a<=0:      #amount should not be under zero!!
            raise NameError("Error Deposit Input")
        self.balance+=a      #add the saved amount to balance if above zero
        print("Deposit :\n",a,
        "\nCurrent Amount :",self.balance)  #show final balance
    def update_det(self):     #update account info. after withdraw or deposit
        self.all=self.name,self.age,self.sex,self.balance,self.withd_status
    def get_details(self):  #show final ditails when called
        self.update_det()
        #return ("Account details :\n",self.all)
        return("Name: {0},\nSex: {1},\nAge: {2},\nBalance: {3:.2f}\n"\
                .format(self.name,self.sex,str(self.age),self.balance))
class Bank():   #class as Bank to save bank accounts also add\remove...
    def __init__(self):
        self.name="N&D Bank"    #attrib of each bank
        self.adress="Berlin-Mitte"
        self.nu_account=0
        self.all_acc=[]
        self.sum_withd=0
        self.w=0
        self.age=0
    def add_acc(self,account:Bank_account):  #method to add singel account
        (self.all_acc).append(account)
        self.nu_account+=1
    def add_multi_acc(self,AccList):  #method to add multi. accounts
        for acc in AccList:
            self.add_acc(acc)
    def remov_acc(self,account:Bank_account):  #remove an account
        (self.all_acc).remove(account)
        self.nu_account-=1
    def get_info(self):   #details of bank with total nu. of accounts
        print("Name of Bank :",self.name)
        print("Adress :",self.adress)
        print("Nu. of Accounts",self.nu_account)
    def get_acc(self,a):   #method to get ditails of a specific account
        if a<=self.nu_account-1:
            return self.all_acc[a].get_details()
        else:
            raise ValueError
        #return self.all_acc[a].get_details()
    def read_acc_list(self,filename,a): #method to read accounts data from a file
        f=open(filename,"r") #read file
        k=0
        while k!=a: #read out unneeded lines
            f.readline()
            k+=1
        i=0 #list starts at 0
        Namelist=[] #list for each variable
        Sexlist=[]
        Agelist=[]
        Balancelist=[]
        tmp_acc_list=[]
       #extract coulumns in each line & add each coulumn
                        #to its variable list
        a=True
        while a:
            line=f.readline()
            if line=="":
                a=False
                break
            line=line.strip() 
            coulumn=line.split()
            Namelist.append(coulumn[0])
            Sexlist.append(coulumn[1].strip(",")) #stripping unneeded str.(",")
            Agelist.append(int(coulumn[2].strip(",")))
            Balancelist.append(float(coulumn[3].strip(",")))
            tmp_acc_list.append(Bank_account(Namelist[i],Agelist[i],Sexlist[i],Balancelist[i]))
            i+=1
        return tmp_acc_list #return a list with all acounts details saved in
    def sub_from_acc(self,w,age): #method to subtract fees from all acount
        self.w=w
        self.age=age #age of holders to start subtracting
        self.sum_withd=0
        a=0
        while a!=self.nu_account:
            if (self.all_acc[a].balance > w) and (self.all_acc[a].age > age):
                self.all_acc[a].withdraw(w)
                self.sum_withd+=1
            a+=1
    def write_infile(self,filename): #method to print the final data of all accounts intto a file
        f=open(filename,"w")
        #up headers to tell details of the data saved
        f.write("=======================================================\
            ================================\n")##another way??!!
        f.write("************************** Confidential **************************\n")##another way??!!
        f.write("This is a File contanins the first {} Accounts in our Bank\n".format(self.nu_account)) #nu. of accounts
        #fees/age to start subtracting
        f.write("(-{0:0}$ from each Account when holder is over {1:0} years old)\
            \nsubtracted accounts : {2:0}\nSignature: Ahmed\n"
            .format(self.w,self.age,self.sum_withd)) 
        f.write("=============================================\
            ==========================================\n")
        #info. of each coulumn in data list
        f.write("{0:16},{1:16},{2:16},{3:16},{4:16}\n"\
            .format(str("Name"),str("Sex"),str("Age"),str("Balance"),str("Withdraw Status")))
        f.write("---------------------------------------------------------------------------------------\n")
        #printing data of the bank accounts in the after headers
        i=0
        while i<self.nu_account:
            f.write("{0:16},{1:16},{2:16},{3:.2f} \t{4:10},{5:10}\n".
                format(self.all_acc[i].name,self.all_acc[i].sex,str(self.all_acc[i].age),
                    self.all_acc[i].balance,str(""),self.all_acc[i].withd_status))
            i+=1
        f.close()
##################################################################
###################### GUI #######################################
##################################################################
class GUI_QT(QWidget):
    def __init__(self):
        super().__init__()
        self.bank=Bank()
        self.setGeometry(150,100,600,500)
        self.setWindowTitle("Bank Demo")     
        self.gui()
        self.show()
    def add_account(self):
        name,n=QInputDialog.getText(self,"account input",\
            "Enter name:")
        l=["Male","Female"]
        sex,s=QInputDialog.getItem(self,"account input",\
            "Enter sex:",l)
        age,a=QInputDialog.getInt(self,"account input",\
            "Enter age:")
        balance,b=QInputDialog.getDouble(self,"account input",\
            "Enter balance:")
        #h=self.bank_accou(name,age,sex,balance)
        if n and s and a and b:
            self.bank_acc=Bank_account(str(name),str(age),str(sex),str(balance))
            self.bank.add_acc(self.bank_acc)
            self.label1.setText(" 1 Account was added:\nName: {0} , Age: {1} , Sex: {2} , Balance: {3}\n\nNu. of Accounts: {4}"\
                .format(self.bank_acc.name,self.bank_acc.age,self.bank_acc.sex,self.bank_acc.balance,self.bank.nu_account))
            self.label1.setFont(QFont("Arial",14,QFont.Bold))
            self.label1.setAlignment(Qt.AlignCenter)
            print(self.bank_acc.get_details)

    def add_list(self):
        reply = QMessageBox.question(self,"Message","Choose list file?",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            file,c=QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",\
                "","Text Files (*.dat *.txt)")
            if c:
                l=self.bank.read_acc_list(file,7)
                self.bank.add_multi_acc(l)
                self.label1.setText(" {} Accounts were added".format(self.bank.nu_account))
                self.label1.setFont(QFont("Arial",24,QFont.Bold))
                self.label1.setAlignment(Qt.AlignCenter)
                print(self.bank.get_info())
    def new_window(self):
        self.new=win(self.bank)
        self.new.show()
 
    def gui(self):
        grid=QGridLayout()
        label=QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Arial', 22))
        self.setLayout(grid)
        grid.addWidget(label,1,0,1,4)
        label.setText("Welcome to\n"+self.bank.name+" in "+self.bank.adress)       
        bt1=QPushButton("Add Account",self)
        bt1.setMinimumWidth(100)
        bt1.setMinimumHeight(60)
        grid.addWidget(bt1,2,0,0,1)
        bt1.clicked.connect(self.add_account)
        bt2=QPushButton("Add Account List",self)
        bt2.setMinimumWidth(100)
        bt2.setMinimumHeight(60)
        bt2.clicked.connect(self.add_list)
        grid.addWidget(bt2,2,1,0,1)
        bt3=QPushButton("Get Info.",self)
        bt3.setMinimumWidth(100)
        bt3.setMaximumWidth(120)
        bt3.setMinimumHeight(60)
        bt3.clicked.connect(self.new_window)
        grid.addWidget(bt3,2,3,1,1)
        self.label1=QLabel(self)
        #self.label1.setStyleSheet("QLabel""{""border : 2px solid black;\
         #   ""background : white;""}")
        #self.label1.setStyleSheet("QLabel {color : blue; }")
        grid.addWidget(self.label1,3,0,1,0)
class win(QMainWindow):
    def __init__(self,myBank):
        super().__init__()
        self.setGeometry(350,50,700,600)
        self.setWindowTitle("Bank info.") 
        self.tabs=QTabWidget(self)
        self.tabs.setStyleSheet("QTabBar::tab{height:100px;width:30px}")
        self.tabs.setTabPosition(QTabWidget.West)
        self.tab1=QWidget(self)
        self.tab2=QWidget(self)
        self.tabs.addTab(self.tab1,"List") 
        self.tabs.addTab(self.tab2,"info.")  
        #**********
    
        if myBank.nu_account>0:
            self.tab1.layout=QVBoxLayout(self)
            self.l=QTableWidget(self)
            self.l.setColumnCount(4)
            #self.l.setFont(QFont('Arial', 12))
        #self.l.setStyleSheet("QLabel {color:red; }")
            
            self.tab1.layout.addWidget(self.l)
            self.tab1.setLayout(self.tab1.layout)
            #self.l.setAlignment(Qt.AlignLeft)
            i=0
            self.l.setRowCount(0)
            #self.l.setItem(1,2, QTableWidgetItem("Test"))
            self.l.setHorizontalHeaderLabels(["Name","Sex","Age","Balance"])
            #self.l.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
            #self.l.setHorizontalHeaderItem(1,QTableWidgetItem("Sex"))
            #self.l.setHorizontalHeaderItem(2,QTableWidgetItem("Age"))
            #self.l.setHorizontalHeaderItem(3,QTableWidgetItem("Balance"))
            print(self.l.horizontalHeaderItem(0))
            #self.l.setColumnWidth(0,120)
            #self.l.setColumnWidth(1,120)
            #self.l.setColumnWidth(2,120)
            #self.l.setColumnWidth(3,120)
          
            while i<myBank.nu_account:
                self.l.insertRow(i)

                self.l.setItem(i,0, QTableWidgetItem(myBank.all_acc[i].name))
                self.l.setItem(i,1, QTableWidgetItem(myBank.all_acc[i].sex))
                self.l.setItem(i,2, QTableWidgetItem(str(myBank.all_acc[i].age)))
                self.l.setItem(i,3, QTableWidgetItem("{0:.2f}".format(myBank.all_acc[i].balance)))
                
                #self.l.setItem(i,2, QTableWidgetItem("Test"))
                i+=1
            ########
            #change coulumn size
            for i in range(4):
                self.l.setColumnWidth(i,130)
            #######
            #desabil edit and table fit page
            self.l.horizontalHeader().setStyleSheet("::section{Background-color:white}")
            self.l.setEditTriggers(QTableWidget.NoEditTriggers)
            self.l.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.l.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            header=self.l.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)       
            
            
        else:
            self.tab1.layout=QVBoxLayout(self)
            self.l=QLabel()
            self.l.setFont(QFont('Arial', 22))
            self.l.setStyleSheet("QLabel {color:red; }")
            self.l.setAlignment(Qt.AlignCenter)
            self.l.setText("------------------------------------\n\
ACCOUNT LIST IS EMPTY\n\
------------------------------------")
            self.tab1.layout.addWidget(self.l)
            self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout=QGridLayout(self)
        self.namel=QLabel(self)
        self.namel.setText("Bank name: {0}\nBank adress: {1}\nAccounts: {2} Accounts"
            .format(myBank.name,myBank.adress,myBank.nu_account))
        self.namel.setFont(QFont('Arial', 15))
        self.namel.setMaximumHeight(150)
        self.tab2.layout.addWidget(self.namel,1,0,1,4)
        self.l1=QLabel(self)
        self.l1.setText("*Search Account (with Name or Account nu.):")
        self.l1.setFont(QFont("Arial",15))
        self.l1.setMaximumHeight(50)
        
        self.tab2.layout.addWidget(self.l1,2,0,1,1)
        self.l2=QLabel(self)
        self.l2.setText("Name:")
        self.l2.setFont(QFont("Arial",12))
        
        self.tab2.layout.addWidget(self.l2,3,0,1,1) 
        self.l3=QLabel(self)
        self.l3.setText("Account nu.:")
        self.l3.setFont(QFont("Arial",12))
      
        self.tab2.layout.addWidget(self.l3,4,0,1,1)
        self.ql1=QLineEdit(self)
        self.ql1.setMaximumWidth(150)
        self.ql1.setMaximumHeight(30)
        ##?????
        regex=QRegExp("[a-z-A-Z_]+")
        validator=QRegExpValidator(regex)
        self.ql1.setValidator(validator)
        #********
        self.ql1.returnPressed.connect(self.enter_name)
        self.tab2.layout.addWidget(self.ql1,3,1,1,2)
        self.ql2=QLineEdit(self)
        self.ql2.setMaximumWidth(150)
        self.ql2.setMaximumHeight(30)
        self.ql2.returnPressed.connect(self.enter_acc)
        self.ql2.setValidator(QIntValidator())
        self.ql2.setMaxLength(5)
        self.tab2.layout.addWidget(self.ql2,4,1,1,2)
        self.res=QLabel(self)
        self.res.setStyleSheet("QLabel""{""border : 2px solid black;\
           ""background : white;""}")
        self.tab2.layout.addWidget(self.res,5,0,1,4)
        
        self.tab2.setLayout(self.tab2.layout)

        #************
        self.setCentralWidget(self.tabs) 

        self.show()
    def enter_name(self):
        print("hi")    
    def enter_acc(self):
        print("hallo")
        
        

app=QApplication(sys.argv)
window= GUI_QT()
sys.exit(app.exec_())