def decide_motion(distance):
    if distance < 0.5:
        return "STOP"
    elif distance < 1:
        return "SLOW"
    else:
        return "GO"


distance = float(input("Enter distance in meters: "))
print(distance, decide_motion(distance))
