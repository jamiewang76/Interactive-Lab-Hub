# Observant Systems

**Jamie Wang zw448 Yunfei Jiao yj497**


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/-/Lab%202/prep.md#using-vnc-to-see-your-pi-desktop).
2.  Install the dependencies as described in the [prep document](prep.md). 
3.  Read about [OpenCV](https://opencv.org/about/),[Pytorch](https://pytorch.org/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### Pytorch for object recognition

For this first demo, you will be using PyTorch and running a MobileNet v2 classification model in real time (30 fps+) on the CPU. We will be following steps adapted from [this tutorial](https://pytorch.org/tutorials/intermediate/realtime_rpi.html).

![torch](Readme_files/pyt.gif)


To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md).

Make sure your webcam is connected.

You can check the installation by running:

```
python -c "import torch; print(torch.__version__)"
```

If everything is ok, you should be able to start doing object recognition. For this default example, we use [MobileNet_v2](https://arxiv.org/abs/1801.04381). This model is able to perform object recognition for 1000 object classes (check [classes.json](classes.json) to see which ones.

Start detection by running  

```
python infer.py
```

The first 2 inferences will be slower. Now, you can try placing several objects in front of the camera.

Read the `infer.py` script, and get familiar with the code. You can change the video resolution and frames per second (fps). You can also easily use the weights of other pre-trained models. You can see examples of other models [here](https://pytorch.org/tutorials/intermediate/realtime_rpi.html#model-choices). 


### Machine Vision With Other Tools
The following sections describe tools ([MediaPipe](#mediapipe) and [Teachable Machines](#teachable-machines)).

[![Model 1](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%205/%20model1.png)](https://drive.google.com/file/d/1yMBy1bN1cNWW--kKmLknIa8U9Y3hGyB-/view?usp=drive_link)

#### MediaPipe

A recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Media pipe](Readme_files/mp.gif)

To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md):

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(venv-ml) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(venv-ml) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py`. 

Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)

[![Hand Pose](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%205/Screen%20Shot%202023-10-30%20at%208.55.18%20PM.png)](https://drive.google.com/file/d/12qoKBLof523LlRxaCP21arJSXL0QkpEL/view?usp=sharing)

#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) is very useful for prototyping with the capabilities of machine learning. We are using [a python package](https://github.com/MeqdadDev/teachable-machine-lite) with tensorflow lite to simplify the deployment process.

![Tachable Machines Pi](Readme_files/tml_pi.gif)

To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md):

After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)


```
(venv-tml) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tml_example.py
```


Next train your own model. Visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. The raspberry pi 4 is capable to run not just the low resource models. Second, use the webcam on your computer to train a model. *Note: It might be advisable to use the pi webcam in a similar setting you want to deploy it to improve performance.*  For each class try to have over 150 samples, and consider adding a background or default class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate. Finally export your model as a 'Tensorflow lite' model. You will find an '.tflite' file and a 'labels.txt' file. Upload these to your pi (through one of the many ways such as [scp](https://www.raspberrypi.com/documentation/computers/remote-access.html#using-secure-copy), sftp, [vnc](https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#transferring-files-to-and-from-your-raspberry-pi-0-6), or a connected visual studio code remote explorer).
![Teachable Machines Browser](Readme_files/tml_browser.gif)
![Tensorflow Lite Download](Readme_files/tml_download-model.png)

Include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.

[![Teaching Model](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%205/teaching.png)](https://drive.google.com/file/d/1yMBy1bN1cNWW--kKmLknIa8U9Y3hGyB-/view?usp=drive_link)

#### (Optional) Legacy audio and computer vision observation approaches
In an earlier version of this class students experimented with observing through audio cues. Find the material here:
[Audio_optional/audio.md](Audio_optional/audio.md). 
Teachable machines provides an audio classifier too. If you want to use audio classification this is our suggested method. 

In an earlier version of this class students experimented with foundational computer vision techniques such as face and flow detection. Techniques like these can be sufficient, more performant, and allow non discrete classification. Find the material here:
[CV_optional/cv.md](CV_optional/cv.md).

### Part B
### Construct a simple interaction.

* Pick one of the models you have tried, and experiment with prototyping an interaction.
* This can be as simple as the boat detector showen in a previous lecture from Nikolas Matelaro.
* Try out different interaction outputs and inputs.

We have used Mediapipe to implement the interaction of using the distance between the user’s thumb and index finger to control pitches of music notes. We compared the distance detection between different fingers to find out the pair with highest detection accuracy. We also tried out using different pitches and timbers of notes.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

[![Hand Pose Pitch](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%205/hand_pose_pitch.png)](https://drive.google.com/file/d/1BCuWeMrrcgJ__scZ08_litG5JkSk54pH/view?usp=sharing)

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
2. When does it fail?
3. When it fails, why does it fail?
4. Based on the behavior you have seen, what other scenarios could cause problems?

As the user places their thumb and index finger closer by acting the “pinch” gesture, the pitch of the note goes down. The minimum it can go is 400hz and the maximum is 1000hz.
The prototype failed at first because we wrongly set m.setVolume as zero, so the webcam wasn’t able to play any sound.
While now it seems clear of technical problems, other problems may arise such as when the hand structure cannot be captured clearly by the camera. For instance, when the palm is almost 90 degrees to the camera so the fingers are too close to each other.


**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
2. How bad would they be impacted by a miss classification?
3. How could change your interactive system to address this?
4. Are there optimizations you can try to do on your sense-making algorithm.

Uncertainty 1: The detection can be inaccurate. When the system fails to detect the expected finger input, it will generate notes that are off the right pitch. To avoid this uncertainty, we may have to instruct the user to make more salient and exaggerated gestures.
Uncertainty 2: The system may not be intuitive enough. We should display instructions such as the relationship between the finger placement and the note pitch.
Regarding the visual feedback, users should be able to have a clear understanding of the system's status as they can observe the video and real-time display of detected mesh points on the screen. 



### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?

Interactive Music or Sound Generation: Interactive Music Controller can be used for creating interactive music or sound effects based on hand gestures. It allows users to control the pitch of the generated sound by changing the distance between their thumb and index finger. This can be used for creative musical performances or sound manipulation. <br>

Educational Tools: Interactive Music Controller can serve as an educational tool for teaching concepts related to sound and music. It provides a hands-on way for users to understand the relationship between pitch and physical gestures. <br>

Entertainment and Art Installations: Interactive Music Controller can be part of interactive art installations or entertainment experiences, where users can experiment with sound and music in a playful and engaging manner. <br>

* What is a good environment for X?

Evenly Lit Spaces: Well-lit spaces with uniform lighting can enhance the accuracy of hand detection and tracking. Avoid areas with strong shadows, as they can interfere with gesture recognition. <br>

Appropriate Color Contrast: Background color should be selected to provide clear contrast with the color of the user's hands. For example, a brightly lit room with a darker background can work well, while a dark room with dark walls may confuse the algorithm. <br>

Physical Space: Ensure that there is enough physical space for users to perform hand gestures comfortably. This allows for natural and unobstructed interaction with the Interactive Music Controller. <br>

* What is a bad environment for X?

High-Noise Environments: Interactive Music Controller may not perform well in noisy environments as background noise can interfere with hand gesture detection and audio perception. <br>

Critical Audio Applications: Interactive Music Controller may not be suitable for critical audio applications where precise and consistent sound quality is required, as it relies on hand gestures that may not always provide precise control. <br>

* When will X break?

Interactive Music Controller may break if: <br>
- Insufficient Lighting: Poor lighting conditions may affect the accuracy of hand detection. <br>
- Unfamiliar Gestures: Users making gestures that the program doesn't recognize. Or having both hands in the camera frame. <br>
- Hardware or Software Failures: Issues with the camera, audio hardware, or software can disrupt the functionality of Interactive Music Controller. <br>

* When it breaks how will X break?

Inaccurate Pitch Control: Users may not be able to control the pitch as expected due to hand detection inaccuracies. <br>
Audio Disturbances: Unexpected audio glitches or distortions could occur if there are issues with audio processing. <br>

* What are other properties/behaviors of X?

Interactive Music Controller provides real-time interaction between physical gestures and sound, allowing users to have immediate control over the generated audio.<br>
Interactive Music Controller promotes interactivity, engagement, and experimentation, making it suitable for interactive art and educational purposes.<br>
The program can be customized to control various audio parameters beyond just pitch, it can control the timbre, and volume.<br>

* How does X feel?

Interactive Music Controller feels interactive, engaging, and creative. It provides users with a tactile and visually appealing way to influence sound and music. It may also be frustrating at times, especially if hand detection is not accurate or if users struggle to achieve the desired sound.

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***

[![Hand Pose Pitch](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Lab%205/hand_pose_misrecoognize.png)](https://drive.google.com/file/d/15IBIEf09rMQx024zpiXvtc-FH9x08_7Q/view?usp=sharing)

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***
