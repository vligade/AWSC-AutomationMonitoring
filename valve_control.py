'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times, 
introduce substance at a specific ratio based on flow data, recording 
and saving flow data, and actuating a flush at a specified time.

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen. 
daily flow rate data
'''
from valve_schedule import Schedule
import datetime
import time

workingSchedule = Schedule()
midnight = datetime.time()
nextStartTime = datetime.time()
nextEndTime = datetime.time()
counter = 1
nextEventTag = ""

while True:
    print "\n1: Run Schedule"
    print "2: Manage Schedules"
    print "3: Exit"
    option = int(raw_input("\nPlease select an option.\n"))

    #run schedule: set midnight time, set flow enable to high (off). 
    #Import a schedule or sort and use current schedule
    if option == 1:
        currentTime = datetime.datetime.time(datetime.datetime.now()).replace(microsecond = 0)
        midnight = currentTime.replace(hour = 23, minute = 59, second = 59)
        
        print "\n\nCtrl + Pause/Break at any time to stop operation.\n"
        
        if not workingSchedule.eventCount:#if no objects ask for a schedule to import
            workingSchedule.importSchedule()
            workingSchedule.displaySchedule()
        else:#sort and run
            workingSchedule.eventList.sort(key = lambda event: event.startTime)
            workingSchedule.displaySchedule()
            print ""
        
        nextEvent = workingSchedule.eventList[0]#grab first event
        nextStartTime = nextEvent.startTime
        nextEndTime = nextEvent.endTime
        nextEventTag = nextEvent.eventTag
        print nextEvent.displayEvent() + " loaded."
        
        while True:# infinite loop
            currentTime = datetime.datetime.time(datetime.datetime.now())
            currentTime = currentTime.replace(microsecond = 0)#current time ignore microseconds

            if (nextEndTime < currentTime and counter < (len(workingSchedule.eventList))):
                print "Event is in the past, loading next event.\n"
                nextEvent = workingSchedule.eventList[counter]
                nextStartTime = nextEvent.startTime
                nextEndTime = nextEvent.endTime
                nextEventTag = nextEvent.eventTag
                counter += 1
                print nextEvent.displayEvent() + " loaded."

            elif nextStartTime == currentTime:
                nextEvent.valveTrigger(nextEventTag)
                time.sleep(1)#hold a second so that the event isn't triggered multiple times

            elif nextEndTime == currentTime:
                nextEvent.valveStop(nextEventTag)
                if (counter == len(workingSchedule.eventList)):
                    print "Last event of the day, waiting until midnight to reset.\n"
                time.sleep(1)#hold a second so event isn't triggered multiple times

            elif currentTime == midnight:
                    counter = 0
                    nextEvent = workingSchedule.eventList[0]
                    nextStartTime = nextEvent.startTime
                    nextEndTime = nextEvent.endTime
                    nextEventTag = nextEvent.eventTag
                    print "\nMidnight! Resetting.\n"
                    workingSchedule.displaySchedule()
                    time.sleep(1)
                    print nextEvent.displayEvent() + " loaded."

#Import, save, edit a schedule or create a new one.
    elif option == 2:
        selection = 0
        while selection != 7:
            workingSchedule.displayMenu()
            selection = int(raw_input("\nPlease select an option.\n"))
            
            if selection == 1:
                workingSchedule.importSchedule()
                workingSchedule.displaySchedule()
            elif selection == 2:
                workingSchedule.addEvent()
            elif selection == 3:
                if not workingSchedule.eventCount:
                    print "There are no events to remove."
                else:
                    print ""
                    workingSchedule.displaySchedule()
                    item = int(raw_input(("\nSelect an event to remove.\n"))) - 1
                    workingSchedule.eventList.pop(item)
                    workingSchedule.eventCount -= 1
            elif selection == 4:
                if not workingSchedule.eventCount:
                    print "The current schedule has no events."
                else:
                    print "\nEvents in this schedule are:"
                    workingSchedule.displaySchedule()
            elif selection == 5:
                workingSchedule.saveSchedule()
            elif selection == 6:
                option = 0
                break
            else:
                print "\nThat is not a valid option please make another selection.\n"
    elif option == 3:
        print("Exiting...\n")
        break
    else:
        print("You did not enter a valid option please try again.\n")