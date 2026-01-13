msgs = int(input("How many msgs have you sent?\t"))
call_time = int(input("For how long have you been on a phone call?\t"))

msgs_cost = 0.0
call_cost = 0.0
for i in range(msgs):
    if i >= 50:
        msgs_cost = 0
    else:
        msgs_cost += 0.15

print(f"Additional msg cost is {msgs_cost}")

for i in range(call_time):
    if i >= 50:
        call_cost = 0
    else:
        call_cost += 0.25
        
print(f"Additional call cost is {call_cost}")

print(f"total is {call_cost + msgs_cost + 15.0}")