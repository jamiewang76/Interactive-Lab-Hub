
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "Welcome to Ghost Writer" | aplay
 
python ghost_writer.py -m en

# output_str ="$1"
# echo "Received string: $output_str"
# espeak -ven+f2 -k5 -s150 --stdout  $output_str | aplay
my_string=$(<ghostwriter.txt)
# echo "Received string: $my_string"
espeak -vmb-en1 < ghostwriter.txt