import nltk
import json
from time import gmtime, strftime
from name import getName,current_names
from qaNew import find_answer
from nltk import download
from smalltalk_new import process_user_input,find_matching_intent,generate_response
from random import choice
from feedback import store_feedback, get_feedback
#from ticket_booking import book_movie_ticket
from threading import Thread
import time
import random
#download("stopwords")
#download("punkt")
#download("averaged_perceptron_tagger")
#download("maxent_ne_chunker")
#download("words")

global transaction_id

def user_transaction(user_input):
  global current_transaction, transaction_id

  if "book ticket" in user_input:
    current_transaction = "movie_booking"
    transaction_id = str(random.randint(10000, 99999))
    print(f"=> Bot: Your booking ID is {transaction_id}")
    book_movie_ticket()
  else:
    # Process other types of user input
    pass



def main():
  global user_name, chatbot_name, flag

  user_name = '(User)'
  chatbot_name = current_names()["chatbot_name"]
  flag = True

  print("=> Bot: Hi my name is Bot,May I have know your name please?")
  print('=> %s: ' %user_name, end=" ")
  user_input = input()
  if user_input == 'bye':
    flag = False
  else:
    user_name = getName('PERSON',user_input)
    print(f"=> {chatbot_name}: Hi {user_name},how can i help you?")

  while(flag == True):
    print('=> %s: '%user_name, end=" ")
    user_input = input()
    user_input = user_input.lower()

    if(user_input != 'bye'):

      # name management
      user_qname = ["what is my name?", "Tell me my name","Who are you talking to?"]
      if user_input in user_qname:
        #if response != 'NOT FOUND':
        print("=> Bot: you're name is %s" %(user_name))
        continue

      chatbot_qname = ["what is your name?","What do you call me?","What name do you call me by?"]
      if user_input in chatbot_qname:
        print("=> Bot: I am %s"%(chatbot_name))
        continue

      # time and date
      if 'time' in user_input or 'date' in user_input:
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print("=> Bot: The date and Time at this moment is - ",(time))
        continue

      # qa
      response = find_answer(user_input)
      if response != 'NO RECORD FOUND':
          print("=> Bot: "+ response)
          continue

      # small talk
      user_input_processed = process_user_input(user_input)
      matching_intent = find_matching_intent(user_input_processed)
      response = generate_response(matching_intent)
      if response != "Sorry, I couldn't find a matching intent.":
        print("=> Bot: "+ response)
        continue
      # movie ticket booking
      if "book ticket" in user_input:
        user_transaction(user_input)
      else:
        print("=> Bot: I'm sorry. can you please reprhase it and try again.")

    else:
      print("=> Bot: Please provide feedback for the chatbot ") 
      print('=> %s: '%user_name, end=" ")
      #feedback of user
      user_feedback = input()
      response = get_feedback(user_feedback)
      store_feedback(user_name, user_feedback)
      flag = False
  print("=> Bot: Bye, ",response)
  
  
def book_movie_ticket():
    global transaction_id
    global selected_movie_title
    global selected_timing

    # confitmation of user to start the booking transaction
    print("=> Bot: Do you want to book a movie ticket? (yes/no) ")
    print('=> %s: '%user_name, end=" ")
    user_input = input()
    
    user_input = user_input.lower()
    if user_input == "yes":
        # loading the data
        with open('dataset/movie_time.json',"r") as f:
            movies_data = json.load(f)

        # Displaying all the available movies
        print("=> Bot: Available movies:")
        for movie in movies_data['movies']:
            print(movie['title'])

        # Selection of a movie title
        while True:
            print("=> Bot: Enter the title of the movie you want to book. ")
            print('=> %s: '%user_name, end=" ")
            user_movie_selection = input().lower()

            # Find the index of the selected movie in the available_movies list
            selected_movie_index = None
            for i, movie in enumerate(movies_data['movies']):
                if movie['title'].lower() == user_movie_selection.lower():
                    selected_movie_index = i
                    break
                #selected_movie_title = movies_data['movies'][selected_movie_index]['title']
            # Checking if the selected movie exists in the available_movies list
            if selected_movie_index is None:
                print("=> Bot: Invalid movie selection. Please choose from the available movies.")
                continue
            else:
                break
            
        selected_movie_title = movies_data['movies'][selected_movie_index]['title']
        # retrieving the showtimes for the selected movie
        showtimes = movies_data['movies'][selected_movie_index]['showtimes']
            # Displaying available showtimes for the selected movie
        print("=> Bot: Available showtimes for", movies_data['movies'][selected_movie_index]['title'] + ":")
        for showtime in showtimes:
                print(showtime)
            
        # Selection of showtime for the selected movie
        while True:
            print("=> Bot: Enter the showtime you want to book for "+selected_movie_title+" movie")
            print('=> %s: '%user_name, end=" ")
            user_timing_input = input().lower()
            
            # Converting all showtimes to lowercase to match user input
            lowercase_showtimes = [showtime.lower() for showtime in showtimes]
            if user_timing_input.lower() not in lowercase_showtimes:
                    print("=> Bot: Please enter a valid timing from the available timings list.")
                    continue
            else:
                break
            
        selected_timing = user_timing_input.lower()
        # Selection of number of tickets for the selected movie
        while True:
            print("=> Bot: Enter the number of tickets you want to book for "+selected_movie_title+" movie")
            print('=> %s: '%user_name, end=" ")
            user_input = input()

            try:
                number_of_tickets = int(user_input)
                if number_of_tickets > 20:
                    print("=> Bot: please enter below 20 ticket because it exceeds seat available in threatre")
                    continue
                if number_of_tickets > 0 and number_of_tickets <20:
                    break
            except ValueError:
                print("=> Bot: Please enter a valid integer value for the number of tickets.")

        # Display available theater seats
        theater_seats = {
            "A": [1, 2, 3, 4],
            "B": [1, 2, 3, 4],
            "C": [1, 2, 3, 4],
            "D": [1, 2, 3, 4],
            "E": [1, 2, 3, 4],
        }
        print("=> Bot: Available seats:")
        for row, seats in theater_seats.items():
            print(f"Row {row}: {', '.join(str(seat) for seat in seats)}")
        selected_seats = []
        count = 1
        # iterating as number of the ticket till user selects row and seat number for each ticket
        while count <= number_of_tickets:
            while True:
                # inputting the selected seat numbers
                print(f"=> Bot: For ticket {count}, select the row (A, B, C, D, E) ")
                print('=> %s: '%user_name, end=" ")
                row = input().upper()

                # Checking if the selected row is available in threatre seat map
                if row in theater_seats:
                    break
                else:
                    print(f"=> Bot: Invalid row selection. Please choose from the available rows (A, B, C, D, E).")

            # inputting the selected seat number
            while True:
                print(f"=> Bot: For ticket {count}, select a seat number from 1 to 4 ")
                print('=> %s: '%user_name, end=" ")
                seat_number = input()
                if seat_number.isdigit():
                    if 1 <= int(seat_number) <= 4:
                        # Checking if the selected seat already exists in the selected_seats list
                        for selected_seat in selected_seats:
                            if row == selected_seat[0] and int(seat_number) == selected_seat[1]:
                                print(
                                    f"=> Bot: The seat {row}-{seat_number} has already been selected. Please choose another seat."
                                )
                                continue

                        # Storing the selected seats
                        selected_seat = [row, int(seat_number)]

                        # Removing the selected seat from the available seats
                        theater_seats[row].remove(int(seat_number))
                        break
                    else:
                        print(
                            f"=> Bot: Invalid seat number. Please choose a valid seat number from 1 to 4."
                        )
                else:
                    print(
                        f"=> Bot: Invalid seat selection format. Please enter a row (A, B, C, D, E) followed by a seat number (1, 2, 3, or 4)."
                    )

            # Adding the selected seat to the list of selected seats
            selected_seats.append(selected_seat)
            count += 1
        # Confirming the booking of movie ticket with user to proceed with the transaction
        print("=> Bot: Are you sure you want to confirm "+str(selected_seats)+ " movie ticket booking for "+selected_movie_title+ " at "+ selected_timing+ "? (yes/no) ")
        print('=> %s: '%user_name, end=" ")
        user_input = input()
        user_input = user_input.lower()

        if user_input == "yes":
            # Generating transaction ID
            #transaction_id = str(random.randint(10000, 99999))
            print(f"=> Bot: Booking successful! Here is your Transaction ID: {transaction_id}")

            # Storing the booking details in the json file
            with open("bookings.json", "a") as f:
                booking_data = {
                    "transaction_id": transaction_id,
                    "userName": user_name,
                    "movie_title": selected_movie_title,
                    "showtime": selected_timing,
                    "seats": selected_seats,
                }
                json.dump(booking_data, f)
                f.write("\n")

                print(f"=> Bot: Booking details saved in our database. Don't worry your seats are safe with us.")

        else:
            print("=> Bot: Booking canceled.")

    else:
        print("=> Bot: Okay, come back if you decide to book a movie ticket.") 



if __name__ == "__main__":
  main()



'''def process_user_feedback(user_feedback):
  response1 = get_feedback(user_feedback)
  store_feedback(user_name, user_feedback)'''