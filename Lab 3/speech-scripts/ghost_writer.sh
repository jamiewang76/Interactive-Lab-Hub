
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "Welcome to Ghost Writer" | aplay
 
python ghost_writer.py -m en