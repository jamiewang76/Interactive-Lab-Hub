import digitalio
import board

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

while True:
    if not buttonA.value:
        print("button A")
    if not buttonB.value:
        print("button B")