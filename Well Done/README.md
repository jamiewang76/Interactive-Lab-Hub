# Final Project - Well Done

Using the tools and techniques you learned in this class, design, prototype and test an interactive device.

## Project plan

Big Idea: The user can set timers,by physical knobs,to control multiple stoves to turn on, turn off, or adjust power

Specific Application: A control panel comprising four rotary encoders or joysticks and some LED signal lights is used to set time for individual stove’s action such as turning on, off, or changing power level. To physically rotate the stove knobs, we want to provide the option of remotely controlling a servo motor to do the job for the user.

Well Done is a stove add-on system that offers an individual timer for each stove to save users from the trouble of keeping track of the cooking time themselves.

Timeline: 
Nov 14: Set proposal
Nov 21: Scout for suitable rotary encoders, buttons,  joystick, and LED signal lights. Envision its final appearance on actual stove
Nov 28 & 30: Code timer-setting program and alert-sending system with MQTT
Dec 5 & 7: Design and produce costumes for “Well Done”. 
Dec 14: User-testing and finish write-up

Expected Challenges:
May not find four rotary encoders
Servo motor may not be powerful enough to turn the knob and if it could do precise turns
Fall-back plan: 
use joysticks as substitute for rotary encoders
Discard the remote knob-turning feature

Contribution Overview:
Together: Scout resources, design costumes
Jamie: Develop timer-setting program and alert-sending system
Fei: Develop LED feedback program and produce costume
 
## Documentation

### Storyboards
Richard is cooking. He is cooking two pots of food at the same time.
![DALL·E 2023-12-09 18 08 27 - A cheerful house-husband in a modern kitchen, turning on the stove  He's placing two pots on two separate burners  The kitchen is well-lit and spaciou](https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/4e719c21-4458-4c15-b0b4-9df7c1ae6826)

He needs to set separate timers to time the duration of cooking. Setting up different timers for different pots is troublesome for Richard.
![DALL·E 2023-12-09 18 08 25 - A house-husband in a modern kitchen, looking slightly troubled as he sets separate timers on his phone for two different pots cooking on the stove  Th](https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/eda53b25-d81d-484c-a1f9-ee9e20874004)

He learned about WellDone, a stovetop add-on that can help him time different stove’s cooking time independently.
![DALL·E 2023-12-09 18 08 22 - A close-up view of a modern stovetop in a kitchen, showing only two fire level knobs and two smaller, differently colored knobs for timers, each pair ](https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/7f323318-72f7-4e89-87ee-cc07226f2790)

When the stove is complete cooking, Richard receives a text message informing him that stove No.X is done cooking!
![DALL·E 2023-12-09 18 08 12 - A scene in a cozy living room where the house-husband is sitting on a sofa chair, looking happy and relaxed as he reads a text message on his phone  T](https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/33565b41-8706-41cb-b335-463621858582)

### Executions
#### Program
Drafted the preliminary design plan: use rotary encoders to register the cooking time that the user wants to assign each of the stoves with. Once the time is up for a stove, a text message will be sent to the user’s phone.
Implemented individually working count-down timers.
Applied multi-threading to enable timers working concurrently.
Tried display with ST7735 screen but ended up paralyzing both Raspberry Pis we owned.
Replaced with a new Pi.
Wrote script to show real-time positions of the rotary encoders, start counting down once the encoder knob is pressed, and display “Done” when the time left hits zero. 
Improved message readability by adjust their alignment and color .

#### Device Costume
Drafted a rough layout of the stovetop in Adobe Illustrator
<img width="731" alt="Screen Shot 2023-12-09 at 6 26 01 PM" src="https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/206fa67b-3629-42ca-a42f-fd240acc63a7">

Measured the dimensions of needed components (e.g. Pi, Pi screen, rotary encoder platform, etc.)
Changed from horizontal to portrait layout design.
<img width="849" alt="Screen Shot 2023-12-09 at 6 26 52 PM" src="https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/7aaeae9e-5e7a-4568-b532-746f94a051e0">

Laser cut steps:
Cut out the box structure
Vector cut holes for screen, fake cooking power knobs, and rotary encoders
Vector cut “add-ons”: stoves, knobs 
Raster cut our Logo and names
Embellished the box surface with reflective silver material

#### Hardware

Soldered the back of Adafruit rotary encoders to modify each’s i2C address
Connected all parts to MiniPi TFT screen with jumpers as following:

<img width="513" alt="Screen Shot 2023-12-09 at 6 27 59 PM" src="https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/0a77c947-ef30-4ce3-bd90-068e5c7c8e3e">

Final Product

<img width="1189" alt="Screen Shot 2023-12-09 at 6 15 57 PM" src="https://github.com/jamiewang76/Interactive-Lab-Hub/assets/57398429/24601b78-d8b3-47d5-b9e4-8824f80943f7">
[![Well Done Video](https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Well%20Done/Screen%20Shot%202023-12-09%20at%206.15.57%20PM.png)](https://drive.google.com/file/d/1V_nF6uEfMx32FJ5AoiEJPgi34Yzn_owL/view?usp=sharing)

## Archive of Code and Design

Link to all design files: https://drive.google.com/drive/folders/1yzNtHQX90HGxako8HVQdgNbBtZvix6DH?usp=sharing
Product Code: https://github.com/jamiewang76/Interactive-Lab-Hub/blob/Fall2023/Well%20Done/multiple_rotary_timer.py

## Reflection on Process

More research and thorough initial planning: 
Screen for display
Eyespi couldn’t function
Mini OLED doesn’t light up
Testing for screens wasted time for laser cut planning

Conducting screen tests before laser cut planning proved to be a time-consuming detour. Future projects should prioritize comprehensive planning to ensure a more efficient and purposeful prototyping process. Encountering difficulties with the Mini OLED not lighting up highlighted the necessity of thorough pre-research on component compatibility. A deeper understanding of each component's specifications during the planning phase could prevent unforeseen issues during the prototyping process. 

Battery case needed for PI to run
Specific power banks that PI can run on

A battery case was necessary for the Raspberry Pi's functionality. It shows us the importance of early consideration of power requirements. Identifying specific power banks compatible with the Raspberry Pi in the early stages would optimize testing efforts and resource allocation.

3D printing of knobs
Failed because model can’t be glued to printer surface
Laser cut
Originally used a thicker board, and the rotary encoder couldn’t be fixed to the board
With Pi’s raised interface (ports), it is difficult to have only the screen popping out and the rest of the interface hidden

Challenges in 3D printing and fixing the rotary encoder to the board emphasized the critical role of material selection and manufacturing techniques. Early experimentation with materials and prototyping methods could mitigate complications in later stages.The unique architecture of the Raspberry Pi, particularly its raised interface (ports), posed unexpected design challenges. Awareness of device architecture at the project's outset would enable more thoughtful and innovative design solutions, avoiding complexities during implementation.

## Team Contribution

### Jamie
Timer logic programming
Laser Cut
Device Design
Hardware assembly
### Yunfei
Timer logic programming
Laser Cut
Device Design
Hardware assembly
