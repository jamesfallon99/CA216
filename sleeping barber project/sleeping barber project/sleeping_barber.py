import time
import random
from threading import Thread, Event, Lock
event = Event() #The internal flag is initially false.
lock = Lock()

class SleepingBarber:

    def __init__(self, barber, num_seats_in_waiting_room):
        self.barber = barber
        self.num_seats_in_waiting_room = num_seats_in_waiting_room

    def start_day(self):
        print("The barber shop is opening for the day")
        barber_working1 = Thread(target=self.work) #A thread on the work function that will continuously look for new customers in the waiting room, and if none left, will allow the barber to go to sleep.
        barber_working1.start()#Start the thread.
        barber_working2 = Thread(target=self.work)
        barber_working2.start()
        barber_working3 = Thread(target=self.work)
        barber_working3.start()
        #Each thread acts as a different barber. The more threads there are, the more barbers in the shop.
    
    waiting_room = [] #A list used to store the customers waiting for a hair-cut.


    def customer_enters_barbers(self, customer):
        lock.acquire() #Get the lock inorder to protect the waiting room as this is a shared resource between the work() function and the customer_enters_barbers() function.
        print("{} entered the barber shop".format(customer))
        if len(self.waiting_room) != self.num_seats_in_waiting_room: # If there's still seats available in the waiting room:
            print("{} took a seat in the waiting room".format(customer))
            self.waiting_room.append(customer) # append the customer to the waiting room list
            lock.release()#Release the lock so the work() function can then acquire it.
            event.set()#The barber wakes up as a customer walks in. Set the internal flag to true. All threads waiting for it to become true are awakened.
            
        else:
            print("The waiting room is full at the moment. {} leaves the barber shop".format(customer))
            lock.release()#Release the lock so the work() function can then acquire it.


    def work(self):
        while True: #while True means loop forever. True always evaluates to boolean "true" and thus executes the loop body indefinitely.
            lock.acquire() #Get the lock inorder to protect the waiting room as this is a shared resource between the work() function and the customer_enters_barbers() function.
            if len(self.waiting_room) != 0: # If there's someone in the waiting room
                customer = self.waiting_room.pop(0) #Let this person be the next customer and delete this person from the waiting room
                lock.release() #Release the lock so the customer_enters_barbers() function can then acquire it.
                self.barber.hair_cut(customer) #Pass this customer into the haircut function
            
            else:
                lock.release()#Release the lock so the customer_enters_barbers() function can then acquire it.
                print("There is no one left to get a hair cut, the barber goes to sleep")
                event.wait()#The barber goes to sleep. Block until the internal flag is true. If the internal flag is true on entry, return immediately. Otherwise, block until another thread calls set() to set the flag to true, or until the optional timeout occurs

                print("A new customer arrived. The barber wakes up")

class Barber:

    def hair_cut(self, customer):
        event.clear() #Reset the internal flag to false.
        print("{} is getting their hair cut".format(customer))
        time.sleep(random.randint(3, 12)) # The amount of time it takes to get a haircut.
        print("{} is finished getting their hair cut".format(customer))


if __name__ == '__main__':
    arriving_customers = []

    arriving_customers.append('customer26')
    arriving_customers.append('customer25')
    arriving_customers.append('customer24')
    arriving_customers.append('customer23')
    arriving_customers.append('customer22')
    arriving_customers.append('customer21')
    arriving_customers.append('customer20')
    arriving_customers.append('customer19')
    arriving_customers.append('customer18')
    arriving_customers.append('customer17')
    arriving_customers.append('customer16')



    SleepingBarber.waiting_room.append('customer1')
    SleepingBarber.waiting_room.append('customer2')
    SleepingBarber.waiting_room.append('customer3')
    SleepingBarber.waiting_room.append('customer4')
    SleepingBarber.waiting_room.append('customer5')
    SleepingBarber.waiting_room.append('customer6')
    SleepingBarber.waiting_room.append('customer7')
    SleepingBarber.waiting_room.append('customer8')
    SleepingBarber.waiting_room.append('customer9')
    SleepingBarber.waiting_room.append('customer10')
    SleepingBarber.waiting_room.append('customer11')
    SleepingBarber.waiting_room.append('customer12')
    SleepingBarber.waiting_room.append('customer13')
    SleepingBarber.waiting_room.append('customer14')
    SleepingBarber.waiting_room.append('customer15')

    barber = Barber()
    sleeping_barber = SleepingBarber(barber, num_seats_in_waiting_room=15)
    sleeping_barber.start_day() # Call the start of the program
    
    while len(arriving_customers) > 0: # While there are customers in the arriving_customers list:
        customer = arriving_customers.pop()#New customer enters the barbers
        sleeping_barber.customer_enters_barbers(customer)#Pass this customer to the customer_enters_barbers() function.
        time.sleep(random.randint(4, 16)) # The amount of time between each customer walking into the shop.