from time import strftime # this allows the program to get the current time
from playsound import playsound # allows program to play sounds, it is used for the alarm sounds
import sys # used to allow the user to close the program
from threading import Timer # used to create new threads that track the time so they know when to alarm
import random # used to display a random quote
import codecs # used to read all file as unicode so quotes display all characters properly in the terminal

# class that is responsible for getting the input for alarms, setting alarms, and playing sounds when a alarm goes off
class Alarm:
    def __init__(self):
        self.alarmHour # stores the user inputted alarm hour
        self.alarmMinute # stores the user inputted alarm minute
        self.alarmAmPm # stores whether the alarm is for am or pm
        self.secondsTillAlarm # stores how many seconds it will be until the alarm should go off

    def alarm():
        """is called when the alarm goes off"""
        print ("TIme Alarm Went Off: " + strftime('%I:%M %p')) # print the time the alarm went off
        # play the alarm sounds
        playsound('C:/Users/knigh/Documents/2021 Fall Semester/Applied Programming/project 1/alarm/alarm.wav')

    def getAlarm(self):
        """is called when the program needs to get all the inputs for a alarm"""
        hour = True # variable used to create a while loop so the user has to input a valid hour time
        while hour: # while hour is true, the program asks for the hour time until the user inputs a number between 1-12
            self.alarmHour = input("Enter your alarm hour time: ") # get input
            if len(self.alarmHour) == 1: # if a single number do this
                self.alarmHour = '0' + str(self.alarmHour) # this adds a zero in front of single numbers for formatting
            if self.alarmHour.isdecimal() == True and len(self.alarmHour) == 2 and int(self.alarmHour) <= 12 and int(self.alarmHour) >= 1:
                hour = False # this stops the while loop because we have a valid hour
        minute = True # variable used to create a while loop so the user has to input a valid minute time
        while minute: # while minute is true, the program asks for the minute time until the user inputs a number between 0-59
            self.alarmMinute = input("Enter your alarm minute time: ") # get input
            if len(self.alarmMinute) == 1: # if a single number do this
                self.alarmMinute = '0' + str(self.alarmMinute) # this adds a zero in front of single numbers for formatting
            if self.alarmMinute.isdecimal() == True and len(self.alarmMinute) == 2 and int(self.alarmMinute) < 60 and int(self.alarmMinute) >= 0:
                minute = False # this stops the while loop because the program recieved a valid number
        amPm = True # variable used to create a while loop so the user has to input a valid minute time
        while amPm:  # while amPm is true, the program asks for the am or pm until the user inputs 'am' or 'pm'
            self.alarmAmPm = input("Enter am or pm: ") # get input
            if self.alarmAmPm.upper() == 'AM' or self.alarmAmPm.upper() == 'PM': # check if it's 'am' or 'pm'
                amPm = False # stop the while loop because the variable is 'am' or 'pm
        # Tell the user the time that the alarm is set for
        print('Alarm set for ' + str(self.alarmHour) + ':' + str(self.alarmMinute) + ' ' + self.alarmAmPm.upper())

    def calculateSeconds(self):
        """uses the current time and the alarm time to calculate the total seconds until the alarm should go off"""
        currentTimeHour = strftime('%H') # gets the current hour time in military time
        currentTimeMinute = strftime('%M') # gets the current minute time
        # if the alarm is PM and doesn't equal 12 we need to add 12 hours
        if self.alarmAmPm.upper() == 'PM' and self.alarmHour != '12':
            self.alarmHour = int(self.alarmHour) + 12
        # if the alarm is set for AM and equals 12 we need to add 12 hours 
        if self.alarmAmPm.upper() == 'AM' and self.alarmHour == '12':
            self.alarmHour = int(self.alarmHour) + 12
        # if the current time is less than the alarm time then the alarm will go off the same day so we can just subtract to get totalHours
        if int(currentTimeHour) < int(self.alarmHour):
            totalHours = int(self.alarmHour) - int(currentTimeHour)
        # if the current time is more than the alarm time we have to add the alarm and 24 - the current time
        # Example: current time = 3:30pm and alarm = 2:30pm we need to have the alarm wait (24 - 15) = 9 hours till it is midnight plus the 2 hours for it to be 2pm
        if int(currentTimeHour) > int(self.alarmHour):
            totalHours = (24 - int(currentTimeHour)) + int(self.alarmHour)
        # if the set alarm has the same hour as the current time, and is in the future we need +0 hours
        # Example: current time = 3:30pm and alarm = 3:45pm we need the alarm to only wait 15 minutes to go off        
        if int(currentTimeHour) == int(self.alarmHour) and int(self.alarmMinute >= currentTimeMinute):
            totalHours = 0
        # if the set alarm has the same hour as the current time, and is in the past we need +24 hours
        # Example: current time = 3:30pm and alarm = 3:15pm we need the alarm to wait a full 24 hours till it is 3pm again the next day
        if int(currentTimeHour) == int(self.alarmHour) and int(self.alarmMinute < currentTimeMinute):
            totalHours = 24
         # calculate the total minutes then use that to calculate the total number of seconds till the alarm goes off
        totalMinutes = (totalHours * 60) + (int(self.alarmMinute) - int(currentTimeMinute))
        self.secondsTillAlarm = totalMinutes * 60 # We multiple minutes by 60 to get seconds because 60 seconds in a minute

    def setAlarm(self):
        """set the actual alarm and create the thread for that alarm"""
        alarm = Alarm # we need this so we can get the function that will be run when the alarm goes off
        # This sets an alarm as a thread so the user can still operate the clock, after 'secondsTillAlarm' passes, the alarm will go off
        t = Timer(self.secondsTillAlarm, alarm.alarm) 
        t.start() # start alarm

    def time():
        """display the current time"""
        print(strftime('%I:%M %p'))

# class that reads 'quotes.txt' file and display quotes 
class Quote:
    def randomQuote():
        """read the quotes in the 'quotes.txt' file and display a random one."""
        quoteFile = codecs.open("quotes.txt","r", "utf-8") # opens the quotes.txt file and encodes as "utf-8" using codecs
        quoteArray = quoteFile.readlines() # make an array where each line is a item in the array
        print ("Quote: " + random.choice(quoteArray)) # select a random quote from the array and print it
        quoteFile.close() # close the file

    def addQuote():
        """ gets input from user and adds it to the 'quotes.txt' file"""
        quote = input("Enter your quote here: ") # get inputted quote
        quote = quote + "\n" # add a newline to the end of the inputted quote
        quoteFile = open("quotes.txt","a") # open the 'quotes.txt' file
        quoteFile.write((quote)) # write the user inputted quote into the 'quote.txt' file
        quoteFile.close() # close the 'quote.txt' file

# class that is used to display the menu and give options to user to set alarm, get the time, end the program, and add favorite quote
class Menu:
    # def __init__(self):
    #     self = ''

    def menu(self):
        """ The main display and commandline interface for the user """
        print("Alarm Clock by Knighten Cooper")
        # loop through the menu forever
        while True:
            # Tell the user the options for commands and ask for input. If the user input matches a command call those functions
            print("Enter command ( \'d\' displays time & a quote, \'set\' sets alarm, \'add\' adds a quote, and \'end\' ends program")
            val = input("Enter your value: ")
            if val == 'd': # if the user inputs d then display the time and a quote
                quote = Quote # quote class that reads quotes from txt file
                quote.randomQuote() # get a random quote from the "quotes.txt" file
                alarm = Alarm # alarm class
                alarm.time() # display the current time
            if val == 'set': # if the user inputs 'set' then we set a alarm
                alarm = Alarm # alarm class
                alarm.getAlarm(self) # get the user to input desired time for alarm
                alarm.calculateSeconds(self) # calculate the seconds until desired time
                alarm.setAlarm(self) # set the alarm to go off after all the seconds have passed
            if val == 'add': # if the user inputs 'add' then add a quote and write it into the quote.txt file
                quote = Quote
                quote.addQuote()
            if val == 'end': # if the user types 'end' terminate this thread, the alarm thread (if set) will continue
                sys.exit()
            # If the user inputs a incorrect command, display a error message
            if val != 'add' and val != 'd' and val != 'set' and val != 'end':
                print('\nError Command Not Recognized, Please Type \'d\', \'set\', \'add\', or \'end\'\n')

# class called Main class that calls menu() from Menu class
class Main:
    def main1(self):
        """call the menu function"""
        menu = Menu()
        menu.menu()

# call main1 function using Main class
main = Main()
main.main1()


# # Sources Used:
# # https://stackoverflow.com/questions/147741/character-reading-from-file-in-python
# # https://www.keepinspiring.me/famous-quotes/
# # https://stackoverflow.com/questions/43137141/show-command-line-results-in-tkinter-text-widget
# # https://stackoverflow.com/questions/5136611/capture-stdout-from-a-script/5136686#5136686
# # https://docs.python.org/3.5/library/contextlib.html
# # https://stackoverflow.com/questions/42828416/print-output-in-gui-interface-tkinter-python
# # https://k3no.medium.com/command-line-uis-in-python-80af755aa27d
# # https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
# # https://en.wikipedia.org/wiki/Array_data_structure#:~:text=In%20computer%20science%2C%20an%20array,one%20array%20index%20or%20key.&text=Arrays%20are%20among%20the%20oldest,used%20by%20almost%20every%20program.
# # https://www.geeksforgeeks.org/random-numbers-in-python/
# # https://www.w3schools.com/python/gloss_python_array_length.asp
# # https://www.geeksforgeeks.org/reading-writing-text-files-python/
# # https://docs.python.org/3/library/sys.html#sys.exit
# # https://stackoverflow.com/questions/905189/why-does-sys-exit-not-exit-when-called-inside-a-thread-in-python
# # https://docs.python.org/2/library/thread.html#thread.interrupt_main
# # https://stackoverflow.com/questions/1489669/how-to-exit-the-entire-application-from-a-python-thread
# # https://docs.python.org/3/library/os.html#os._exit
# # https://stackoverflow.com/questions/18406165/creating-a-timer-in-python/18406263
# # https://www.tutorialspoint.com/python/python_basic_operators.htm
# # https://unitconverter.fyi/en/86340-s-h/86340-seconds-to-hours
# # https://24hourtime.net/86340-seconds-to-hours
# # https://www.codegrepper.com/code-examples/whatever/vs+code+unident+multiple+lines
# # https://www.geeksforgeeks.org/python-convert-string-to-datetime-and-vice-versa/#:~:text=Program%20to%20convert%20string%20to%20DateTime%20using%20strptime()%20function.&text=strptime()%20is%20available%20in,datetime%20into%20the%20desired%20format.&text=The%20arguments%20date_string%20and%20format%20should%20be%20of%20string%20type.
# # https://docs.python.org/3/library/datetime.html#datetime.timedelta.total_seconds
# # https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings
# # https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
# # https://www.geeksforgeeks.org/timeit-python-examples/
# # https://docs.python.org/3/library/timeit.html
# # https://stackoverflow.com/questions/23698871/cannot-install-timeit-with-pip-how-can-i-fix-this#:~:text=timeit%20is%20part%20of%20the,to%20install%20it%20via%20pip.&text=That%27s%20because%20timeit%20is%20a,to%20use%20pip%20for%20that.
# # https://stackoverflow.com/questions/24210700/nameerror-name-timer-is-not-defined
# # https://github.com/colyseus/timer/issues/20
# # https://docs.python.org/2/library/threading.html#timer-objects
# # https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
# # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjDrsbi8p_zAhWkk2oFHT2lCkkQFnoECAsQAQ&url=https%3A%2F%2Fcodingshiksha.com%2Fpython%2Fpython-tkinter-script-to-make-a-alarm-clock-and-set-alarm-time-full-project-for-beginners%2F&usg=AOvVaw23E9sLSRyWuaWIjbif9CWx
# # https://stackoverflow.com/questions/16325039/python-alarm-clock
# # https://stackoverflow.com/questions/16325039/python-alarm-clock
# # https://discuss.codecademy.com/t/how-to-convert-to-12-hour-clock/3920/2
# # https://stackoverflow.com/questions/13855111/how-can-i-convert-24-hour-time-to-12-hour-time
# # https://www.geeksforgeeks.org/how-to-create-a-new-thread-in-python/
# # https://stackoverflow.com/questions/66074642/variable-not-accessed
# # https://careerkarma.com/blog/python-uppercase/
# # https://www.kite.com/python/answers/how-to-check-if-a-string-contains-only-numbers-in-python#:~:text=Use%20str.,are%20numeric%20digits%20or%20not.
# # https://stackabuse.com/python-check-if-variable-is-a-number/
# # https://www.geeksforgeeks.org/python-string-length-len/
# # https://www.edureka.co/community/21051/how-to-exit-a-python-script-in-an-if-statement
# # https://realpython.com/python-or-operator/#if-statements
# # https://www.openbookproject.net/books/bpp4awd/ch04.html
# # https://www.geeksforgeeks.org/taking-input-in-python/
# # https://pypi.org/project/pynput/
# # https://www.hackerearth.com/practice/python/working-with-data/expressions/tutorial/#:~:text=Python%20Expressions%3A,expressions%20are%20representation%20of%20value.&text=Python%20has%20some%20advanced%20constructs,constructs%20are%20also%20called%20expressions.
# # https://pythonbasics.org/python-play-sound/
# # https://www.geeksforgeeks.org/play-sound-in-python/
# # https://bigsoundbank.com/detail-1616-answering-machine-beep.html
# # https://pypi.org/project/playsound/1.2.2/
# # https://docs.python.org/3/tutorial/introduction.html
# # https://dev.to/mindninjax/alarm-clock-python-project-4jn4
# # https://www.w3schools.com/python/ref_string_lower.asp
# # https://www.geeksforgeeks.org/creat-an-alarm-clock-using-tkinter/
# # https://github.com/microsoft/pylance-release/issues/31
# # https://stackoverflow.com/questions/7712389/copy-paste-into-python-interactive-interpreter-and-indentation
# # https://stackoverflow.com/questions/1016814/what-to-do-with-unexpected-indent-in-python
# # https://stackoverflow.com/questions/31340/how-do-threads-work-in-python-and-what-are-common-python-threading-specific-pit
# # https://www.activestate.com/resources/quick-reads/how-to-use-pack-in-tkinter/
# # https://www.educba.com/tkinter-window-size/?source=leftnav
# # https://www.geeksforgeeks.org/how-to-create-full-screen-window-in-tkinter/
# # https://www.geeksforgeeks.org/python-create-a-digital-clock-using-tkinter/
# # https://www.tutorialspoint.com/python/tk_colors.htm
# # https://www.geeksforgeeks.org/python-geometry-method-in-tkinter/
# # https://www.tutorialspoint.com/python/tk_grid.htm
# # https://www.tutorialspoint.com/how-to-add-padding-to-a-tkinter-widget-only-on-one-side
# # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi855iGtp_zAhVInp4KHdB1AlEQFnoECAUQAQ&url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F4174575%2Fadding-padding-to-a-tkinter-widget-only-on-one-side&usg=AOvVaw3O9WZnEA72nFR2UwPvo30A
# # https://www.w3schools.com/python/python_variables.asp
# # https://stackoverflow.com/questions/16043797/python-passing-variables-between-functions
# # https://github.com/microsoft/pylance-release/issues/757
# # https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md#unresolved-import-warnings
# # https://data-flair.training/blogs/alarm-clock-python/
# # https://gist.github.com/charleyXuTO/edf153da4980e7ea68356a6f1edd3c44
# # https://www.codeitbro.com/how-to-make-digital-clock-in-python/
# # https://www.youtube.com/watch?v=ruohUTTo8Kw
# # https://www.reddit.com/r/learnpython/comments/d2slyc/alarm_clock_tkinter/
# # https://riptutorial.com/tkinter/example/22870/-after--
# # https://www.tutorialspoint.com/python/python_multithreading.htm
# # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwimw6e00Z_zAhXQkmoFHTynAUgQFnoECDUQAw&url=https%3A%2F%2Fwww.geeksforgeeks.org%2Fmultithreading-python-set-1%2F&usg=AOvVaw1zEwsK-nmVWADtD9kVyhRf
# # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwimw6e00Z_zAhXQkmoFHTynAUgQFnoECCkQAw&url=https%3A%2F%2Fen.wikibooks.org%2Fwiki%2FPython_Programming%2FThreading&usg=AOvVaw3iJ8cgmE5gsyEaVq66OaVE
# # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwimw6e00Z_zAhXQkmoFHTynAUgQFnoECAIQAQ&url=https%3A%2F%2Frealpython.com%2Fintro-to-python-threading%2F&usg=AOvVaw3oiOZpTGDtJmj9x7FWIoVx
# # https://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-widget
# # https://docs.python.org/3/tutorial/classes.html
# # https://newbedev.com/python-list-takes-0-positional-arguments-but-1-was-given-code-example
# # https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
