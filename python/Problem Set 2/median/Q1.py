sounds = {
    "Jackhammer": 130,
    "Gas lawnmower": 106,
    "Alarm clock": 70,
    "Quiet room": 40
}

level = int(input("Enter the sound level in decibels: "))

sorted_sounds = sorted(sounds.items(), key=lambda x: x[1])

for name, db in sorted_sounds:
    if level == db:
        print(f"The sound level matches a {name}.")
        break
    else:
        # Check range
        if level < sorted_sounds[0][1]:
            print("The sound level is quieter than a Quiet room.")
        elif level > sorted_sounds[-1][1]:
            print("The sound level is louder than a Jackhammer.")
        else:
            for i in range(len(sorted_sounds) - 1):
                low_name, low_db = sorted_sounds[i]
                high_name, high_db = sorted_sounds[i + 1]
                if low_db < level < high_db:
                    print(f"The sound level is between a {low_name} and a {high_name}.")
                    break
