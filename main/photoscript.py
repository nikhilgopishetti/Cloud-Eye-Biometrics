import speech_recognition as sr

# Function to authenticate user based on voice input
def authenticate_user():
    recognizer = sr.Recognizer()

    # Define the audio source (e.g., a microphone)
    with sr.Microphone() as source:
        print("Please say your passphrase for authentication:")
        audio = recognizer.listen(source)

    try:
        # Use Google Speech Recognition to recognize the audio
        recognized_phrase = recognizer.recognize_google(audio)
        print("Recognized phrase:", recognized_phrase)

        # Compare recognized phrase with expected passphrase
        expected_passphrase = "secret"
        if recognized_phrase.lower() == expected_passphrase:
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed. Please try again.")
            return False
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return False

# Example usage
if __name__ == "__main__":
    authenticated = authenticate_user()
    if authenticated:
        print("Access granted.")
    else:
        print("Access denied.")
