# Chatterboxes
Jamie Wang zw448<br />Yunfei Jiao yj497
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

**Please note:** connect the webcam/speaker/microphone while the pi is *off*. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Setup 

*DO NOT* forget to work on your virtual environment! 

Run the setup script
```chmod u+x setup.sh && sudo ./setup.sh  ```

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the directory is a folder called `speech-scripts` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/speech-scripts $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files `.sh` by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/speech-scripts $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech
```
You can test the commands by running
```
echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? 
Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

See [saymyname.sh](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%203/speech-scripts/saymyname.sh)

---
Bonus:
[Piper](https://github.com/rhasspy/piper) is another fast neural based text to speech package for raspberry pi which can be installed easily through python with:
```
pip install piper-tts
```
and used from the command line. Running the command below the first time will download the model, concurrent runs will be faster. 
```
echo 'Welcome to the world of speech synthesis!' | piper \
  --model en_US-lessac-medium \
  --output_file welcome.wav
```
Check the file that was created by running `aplay welcome.wav`. Many more languages are supported and audio can be streamed dirctly to an audio output, rather than into an file by:

```
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  piper --model en_US-lessac-medium --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -
```
  
### Speech to Text

Next setup speech to text. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 
```
pip install vosk
pip install sounddevice
```

Test if vosk works by transcribing text:

```
vosk-transcriber -i recorded_mono.wav -o test.txt
```

You can use vosk with the microphone by running 
```
python test_microphone.py -m en
```

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

See [asknmber.sh](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%203/speech-scripts/asknumber.sh)
See [changes made in test_microphone.py](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%203/speech-scripts/test_microphone.py)

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

![ghost-writer](https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/ce14de03-75cb-4843-af7e-52b82a99a241)


Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

Our device “ghostwriter” allows users to write paragraphs with just speech input. It could convert the user’s speech to text and recognize user’s commands regarding how to edit the recorded text. 
Ghostwriter provides the following arguments:
PI Write - Activate the ghostwriter
PI Backspace - Delete the last digit
PI Delete Sentence - Delete the last sentence
PI Rewrite Sentence [number] - Replace sentence [number] with the next detected sentence
PI Continue - Continue from the end of last sentence
If not detecting any argument, Ghostwriter writes whatever the user speaks into the text document.


\*\***Please describe and document your process.**\*\*

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

[![Ghost Writer Video](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/12070eeba135b1a959b313894b3e0e01c8aad311/Lab%203/Screen%20Shot%202023-09-25%20at%209.11.58%20PM.png)](https://drive.google.com/file/d/11blehYVYfhxLKzXz3orZX7QOAvMtI3zH/view?usp=drive_link)

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

There are some unnatural interactions that users might need time to get used to. E.g. Saying aloud “Rewrite Sentence [number]” directly followed by the new sentence feels weird. It may be more natural to change the argument to “Rewrite Sentence [number] TO”.
But overall, the dialogue and the logic of Ghostwriter are working quite well.

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
Better speech recognition, more comprehensive functionality.
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
The device gives a brief walkthrough of how the program can be interacted with. It explains what each commands it supports can do. 
3. Make a new storyboard, diagram and/or script based on these reflections.
![commands](https://github.com/Yunfei-J/Interactive-Lab-Hub/assets/142849884/73d85462-4643-4574-badb-436e0023d8b3)

![Storyboard](https://github.com/Yunfei-J/Interactive-Lab-Hub/assets/142849884/2d385d91-3533-48d3-80aa-241a2303bdbb)


## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works* <br />
Our device “ghostwriter” allows users to write paragraphs with just speech input. It could convert the user’s speech to text and recognize user’s commands regarding how to edit the recorded text.  <br />
Here are the updated commands that the user can interact with ghostwriter: <br />
Back - Delete the last word from the last sentence <br />
Delete - Delete the last sentence <br />
Delete <i> - Delete the sentence with index i <br />
Rewrite <i> - Replace sentence <i> with the next detected sentence <br />
Show me everything - Print everything ghostwriter has recorded <br />
If not detecting any argument, Ghostwriter writes whatever the user speaks into the text document. <br />

The improvements we've made based on feedback: <br />
Delete the "pi"s in the commands to reduce recognition error. <br />
Delete the "Activate" and "Continue" features <br />
Using a sentence as a command argument sometimes yields higher recognition accuracy because the voice-to-text system can make sense of it more than a single word. <br />

*Include videos or screencaptures of both the system and the controller.* <br />
[![Ghost Writer Video](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%203/Screen%20Shot%202023-10-02%20at%2012.12.42%20AM.png)](https://drive.google.com/file/d/1JAwP47VQ_4JaSbzOmN7hVksMjzpjYVJa/view?usp=drive_link)

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\**The ghostwriter has a good coverage of functions meeting the basic need for typing and editing texts with voice input.
    It still lacks flexibility and doesn't have a good UI because it's run in the terminal.
  *\*\*

### What worked well about the controller and what didn't?

\*\** The accuracy of speech recognition is really low even if the users pronounce the words clearly. It would thus be very frustrating to match every single word to the user's expectation. *\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

1. The user may not feel relaxed when they have to remain silent when they don't want the system to write down anything.
2. Showing the index of each sentence at the beginning of them could help the user to use the commands that target at a specific sentence without having to count the position of the target sentence.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

A button or any haptic sensor could be used for signaling when and when not to take the user's voice as input.
