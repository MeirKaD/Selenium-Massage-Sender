import phonenumbers
phonenum="528728774"
parsed_number = phonenumbers.parse(phonenum, "IL")  # Assuming numbers are from Israel (IL)
phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
print (phone_number)