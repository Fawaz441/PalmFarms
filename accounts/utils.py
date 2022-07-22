import os
import africastalking

username = os.getenv("AFRICAS_TALKING_USERNAME")
api_key = os.getenv("AFRICAS_TALKING_API_KEY")

africastalking.initialize(username, api_key)

sms = africastalking.SMS


def on_sending_finish(error, response):
    if error is not None:
        raise error
    print(response)


def send_welcome_sms(user, password):
    first_name = user.first_name
    print(user.phone_number, type(user.phone_number))
    phone_number = str(user.phone_number)

    message = f"Hello {first_name}, Welcome to PalmFarms. This is to confirm that you have successfully " \
              f"registered an account with us using your phone number and your password is : {password}. " \
              f"You are advised to keep your password secure.\n" \
              f"Now, login to the app to add in your other information and enjoy the experience of having a " \
              f"farm in the palm of your hands."

    # Add on_sending_finish method above as 3rd argument below for asynchronous sending perhaps?
    sms.send(message, [phone_number, ])
