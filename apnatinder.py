import  mysql.connector,sys,time

class apnatinder:
    def __init__(self):
        
        self.conn=mysql.connector.connect(user="root",password=""
                                          ,host="localhost",database="apnatinder")
        self.mycursor=self.conn.cursor()
        self.program_menu()

    def program_menu(self):
        user_response1=input("""Welcome to ApnaTinder
        1. Enter 1 to Register
        2. Enter 2 to Login
        3. Anything else to exit""")

        if user_response1=="1":
            self.register()
        elif user_response1=="2":
            self.login()
        else:
            self.goodbye()

    def user_menu(self):
        user_response2=input("""1. Enter 1 to see all users
        2. Enter 2 to see your proposals
        3. Enter 3 to see all matches
        4. Enter 4 to see who proposed you
        5. Enter 5 to logout""")

        if user_response2=="1":
            self.view_users()
        elif user_response2=="2":
            self.view_proposals()
        elif user_response2=="3":
            self.view_matches()
        elif user_response2=="4":
            self.view_proposed()
        elif user_response2=="5":
            self.logout()
        else:
            self.user_menu()


    def register(self):
        print("Enter the following credentials to register: ")
        name=input("Name: ")
        email=input("Email: ")
        password=input("Password: ")
        gender=input("Gender: ")
        city=input("City: ")

        # run db query to insert
        self.mycursor.execute("""INSERT INTO `apnatinder`.`users` 
        (`user_id`, `name`, `email`, `password`, `gender`, `city`)
         VALUES (NULL, '%s', '%s', '%s', '%s', '%s')""" %
                              (name,email,password,gender,city))
        self.conn.commit()
        self.is_logged_in=1
        print("Registration Successful")
        self.user_menu()


    def login(self):
        print("Enter the following credentials")
        email_for_login=input("Email: ")
        password_for_login=input("Password: ")

        self.mycursor.execute("SELECT * FROM `users` WHERE `email` "
                              "LIKE '%s' AND `password` LIKE '%s'"
                              % (email_for_login,password_for_login))
        user_list=self.mycursor.fetchall()
        counter=0
        for i in user_list:
            counter=counter+1
            current_user=i


        if counter==1:
            self.is_logged_in=1
            self.current_user_id=current_user[0]
            print("You have logged in successfully")
            self.user_menu()
        else:
            print("Incorrect email/password")
            self.program_menu()


    def view_users(self):
        print("Following is the list of all losers")
        self.mycursor.execute("SELECT * FROM `users` WHERE `user_id` NOT LIKE '%s'" %
                              (self.current_user_id))
        all_user_list=self.mycursor.fetchall()
        print("----------------------------------------------------------------")
        for i in all_user_list:
            print(i[0],"|",i[1],"|",i[2],"|",i[4],"|",i[5])
            print("------------------------------------------------------------")
        whom_to_propose=input("Enter the id of the user whom you want to propose")
        self.propose(whom_to_propose)

    def propose(self,proposed_user_id):
        self.mycursor.execute("""INSERT INTO `apnatinder`.`proposals` 
        (`proposal_id`, `proposed_by`, `proposed_to`) VALUES (NULL, '%s', '%s')"""
                              % (self.current_user_id,proposed_user_id))
        self.conn.commit()
        print("Your proposal was sent successfully.Fingers Crossed!")
        self.user_menu()


    def view_proposals(self):
        self.mycursor.execute("""SELECT * FROM `proposals` p
        JOIN `users` u ON p.`proposed_to`=u.`user_id` WHERE p.`proposed_by` LIKE '%s'"""
                              % (self.current_user_id))
        proposed_user_list=self.mycursor.fetchall()
        print("--------------------------------------------------------")
        for i in proposed_user_list:
            print(i[4],"|",i[5],"|",i[7],"|",i[8])
            print("-----------------------------------------------------------")
        self.user_menu()

    def view_proposed(self):
        self.mycursor.execute("""SELECT * FROM `proposals` p
                JOIN `users` u ON p.`proposed_by`=u.`user_id` WHERE p.`proposed_to` LIKE '%s'"""
                              % (self.current_user_id))
        proposed_user_list = self.mycursor.fetchall()
        print("--------------------------------------------------------")
        for i in proposed_user_list:
            print(i[4], "|", i[5], "|", i[7], "|", i[8])
            print("-----------------------------------------------------------")
        self.user_menu()

    def view_matches(self):
        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN `users` u ON
         p.`proposed_to`=u.`user_id`
         WHERE `proposed_to`
         IN (SELECT `proposed_by` FROM `proposals` WHERE `proposed_to` LIKE '%s')"""
                              % (self.current_user_id))
        matched_user_list=self.mycursor.fetchall()
        print("------------------------------------------------------")
        for i in matched_user_list:
            print(i[4], "|", i[5], "|", i[7], "|", i[8])
            print("-----------------------------------------------------------")
        self.user_menu()

    def logout(self):
        self.is_logged_in=0
        print("You have successfully logged out")
        self.program_menu()


    def goodbye(self):
        print("Thanks for using ApnaTinder! BTW aaye kyu the?")
        print("Closing App...")
        time.sleep(2)
        print("Closed")

obj1=apnatinder()