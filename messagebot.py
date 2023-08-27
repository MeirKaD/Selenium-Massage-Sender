import pandas as pd
from tkinter import filedialog, Tk, Label, Button, messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import chromedriver_autoinstaller  # Import the chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By  # Add this import statement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import phonenumbers

df = None  # Define df in the global scope

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path, dtype={'phone number': str})
        return df
    return None

def send_whatsapp_message(df, message_format):
    chromedriver_autoinstaller.install(cwd=True) # Ensure the latest version of ChromeDriver is installed
    driver = webdriver.Chrome()  # No need to specify 'executable_path' here
    driver.get('https://web.whatsapp.com/')
    input('Press Enter after scanning QR code from WhatsApp Web...')

    for _, row in df.iterrows():
        phone_number = row['phone number']
        message = message_format.format(row['name'], row['hour'], row['number of orders'])
        send_message(driver, phone_number, message)
        time.sleep(2)  # Add a delay to prevent WhatsApp Web from blocking the script

    driver.quit()

# Rest of the code remains the same...


def send_message(driver, phone_number, message):
    parsed_number = phonenumbers.parse(phone_number, "IL")  # Assuming numbers are from Israel (IL)
    phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    driver.get(f'https://web.whatsapp.com/send?phone={phone_number}&text={message}')
    try:
        # Add a wait of 10 seconds for the "send" button to become clickable
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_button.click()
    except Exception as e:
        print(f"Error sending message to {phone_number}: {str(e)}")
if __name__ == "__main__":
    root = Tk()
    root.title("WhatsApp Message Sender")

    label = Label(root, text="Select CSV file:")
    label.pack()

    def select_csv():
        global df  # Use the global keyword to indicate that you are modifying the global df variable
        df = load_csv()
        if df is not None:
            messagebox.showinfo("CSV Loaded", "CSV file loaded successfully!")

    button = Button(root, text="Browse", command=select_csv)
    button.pack()

    def send_messages():
        if df is not None: #{0}- name {2} number of orders {1} hour 
            message_format ="ערב טוב חברים , מתזכר אתכם על ההזמנה על שם :{0} מחר בשעה : {1} של :{2} מנות של קציצות דג בפרנה מזכיר שכרגע התשלום הוא במזומן בלבד והאיסוף יתבצע מרחוב דיצה 8 בשכונת הרצוג , ברנע , אשקלון אשמח שתחייגו 5 דקות לפני שתהיו בחוץ תודה ושבת שלום אוהב מלא !"
            send_whatsapp_message(df, message_format)
            messagebox.showinfo("Messages Sent", "WhatsApp messages sent successfully!")
        else:
            messagebox.showerror("Error", "Please select a CSV file first.")

    send_button = Button(root, text="Send WhatsApp Messages", command=send_messages)
    send_button.pack()

    root.mainloop()
#1:35:45 