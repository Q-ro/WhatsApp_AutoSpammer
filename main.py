"""
Author: Andres Mrad (Q-ro)
Creation Date : [ 2020/06 (Jun)/30 (Tue) ] @[ 15:03 ]
Description :  A very shitty attempt to automate WhatsApp contacting of potential students using PyAutoGUI
"""

# importing AutoGUI so we can do fun stuff in the desktop
import pyautogui
import re
import simpleaudio as sa
import pyperclip


# Loads txt files as strings
def loadFileArray(file):
    sanitizedDB = []
    with open(file, "r", encoding='utf-8') as text_file:
        for dirtyDB in text_file.readlines():
            tempEntry = []
            for info in dirtyDB.split(','):
                tempEntry.append(re.sub('[^A-Za-z0-9]+', ' ', info).strip())
            sanitizedDB.append(tempEntry)
    return sanitizedDB

# Loads txt files as strings


def loadFileStr(file):
    with open(file, "r", encoding='utf-8') as text_file:
        return text_file.read()

# Saves a the result from the opperations as a new file


def saveResultToFile(result, filename):
    with open(filename, "w", encoding='utf-8') as txt_file:
        for line in result:
            txt_file.write(", ".join(line) + "\n")
    pass

# The main thread of our program


def main():

    print('Hello fellow hooman !\nInitializing Spam')

    # pyautogui.PAUSE = 1

    #   Step 1
    # Load the message template
    messageTemplate = loadFileStr('UNAB_Spam_Template.txt')
    sender = 'Andres Mrad.'
    senderTitle = 'M.Sc. Multimedia Applications'

    #   Step 2
    # Load and clean the DB (remove extra spaces and identify the list of humans and their phone numbers)
    spamDB = loadFileArray('spamDB.txt')

    #   Step 3
    # For each one of those humans,
    for human in spamDB:
        # Open the URL using chrome (api-endpoint: https://api.whatsapp.com/send?phone=[PhoneDestino]&text=[Message])
        # Go to chome window and make it active
        pyautogui.click(pyautogui.locateCenterOnScreen(
            'Img_Recognition/WA_Web_Window_2.png'))
        # Open the searchbar
        pyautogui.press('f6')
        waURL = 'https://api.whatsapp.com/send?phone=+57[PhoneDestino]'.replace(
            '[PhoneDestino]', human[1])
        pyautogui.write(waURL)
        pyautogui.press('enter')
        pyautogui.click(pyautogui.locateCenterOnScreen(
            'Img_Recognition/WA_Web_TextPerson_btn_1.png'))
        pyautogui.click(pyautogui.locateCenterOnScreen(
            'Img_Recognition/WA_Web_TextPerson_btn_2.png'))

        # Determine if the phone is valid
        # if valid
        if pyautogui.locateOnScreen(
                'Img_Recognition/WA_FailDialog_Close_btn.png') == None:
            # If so, click to open the whatsapp desktop app
            print('trying to type templated message')
            finalMessage = messageTemplate.replace('[Destino]', human[0])
            finalMessage = finalMessage.replace('[Remitente]', sender)
            finalMessage = finalMessage.replace(
                '[TituloRemitente]', senderTitle)
            # Paste the template message replacing the fields accordingly

            pyperclip.copy(finalMessage)
            # pyautogui.click(pyautogui.locateCenterOnScreen(
            #     'Img_Recognition/WA_TextField.png'))
            # pyperclip.paste()
            pyautogui.hotkey('ctrl', 'v')
            print('typing message')
            pyautogui.press('enter')
            human.append(
                'El telefono de contacto es usuario de WhatsApp, El mensaje se ha enviado con exito')
            print('message sent')
        else:
            print('F, el humano no tiene WA')
            print(pyautogui.locateOnScreen(
                'Img_Recognition/WA_FailDialog_Close_btn.png'))
            # add a marker indicating the phone is invalid (no WP user), including the time stamp for the message
            human.append(
                'El telefono de contacto no es usuario de WhatsApp, no ha sido posible contactarlo')
            # Close the dialog and move to the next human
            pyautogui.click(pyautogui.locateCenterOnScreen(
                'Img_Recognition/WA_FailDialog_Close_btn.png'))

    # Step 4
    # Save the final state of the list as a csv file
    saveResultToFile(spamDB, "output.txt")

    # Step 5
    # Play some music or something that lets uf know we are done and close the script
    filename = 'done.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing
    print('job done')

    pass

# Return just the last colums (which should bge the test result info) for each human contacted


def excelReport():
    file = loadFileArray("output.txt")
    return [row[2:] for row in file]


if __name__ == "__main__":
    # the main task, which automates the mause usage and message sending through the set-up
    main()
    # Trims and outputs just the test results on a line by line basis (useful for the purpose of copiying and pasting to excel)
    saveResultToFile(excelReport(), "output_excel.txt")
    pass
