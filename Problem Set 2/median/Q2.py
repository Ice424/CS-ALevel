holidays = {
    ("Jan", 1): "New Year's Day",
    ("July", 1): "Canada Day",
    ("Dec", 25): "Christmas Day"
}


month = input("Enter the month (e.g., Jan, July, Dec): ").capitalize()
day = int(input("Enter the day: "))


if (month, day) in holidays:
    print(f"{month} {day} is {holidays[(month, day)]}.")
else:
    print(f"{month} {day} does not correspond to a f holiday.")