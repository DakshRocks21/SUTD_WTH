# What The Hack 2024!!
## Who are we?
Hello! We are team The Undefined (yeah, that's our team name) participating in What the Hack 2024, presenting a solution to make finding seats at food courts seamless and hassle-free.
All people in our team have experienced this frustration - our school, Ngee Ann Poly, only has ***THREE*** food courts despite its humongous student population. For comparison, Singapore Poly has 6 of them!

I (Richard) once had to walk to all 3 food courts to get food cause the first two were completely full. Took me 30+ minutes before I managed to grab my food, and it was a really unpleasant experience. Hence, we set out to fix this problem for good!

## Our Solution
introducing... SEATTECT
(seat and detect, get it)

SeatTect's role is simple: To detect empty seats at a food court and display it out on a screen at the food court's entrance. That way, you don't even need to step into the food court to know if there's space for you and your friends.

Through the CCTV that have been installed in the food courts, we monitor and analyse all the tables within using Computer Vision (#AI #BigData #MachineLearning #Givememy2Krnplease) to spot empty seats. Every space on the table will also have an LDR (Light Dependant Resistor) installed to track if the person is physically at the table, as the tray/plate would be sufficient to block light from entering it.

Why use LDRs when we already have CV? This is a second measure to register the table being taken in case the person decides to "chope" the table (Singaporean context, ikr). To make this easier, the tables will have markers on them (on top of the LDR) for people to dump their "choping" items on.

All this data is passed to our website, which will display a topdown view of the entire food court. Similar to a movie theatre booking system, occupied areas will be shaded so people can easily tell if there's free seats.

Lastly, we wanted to implement a Admin Setup Editor for landowners to setup the system, which basically allows them to connect tables and identify tables for the CV model to work with. Due to a lack of time, we decided to make a Figma proof of concept :)

## Tech Stack!!!
We used quite the variety of tech here! 

Firstly, we modified an existing Computer Vision model (owlv2-base-patch16-ensemble) to detect empty seats around tables. For the LDR setup, we used small circuits consisting of a ESP-01S microcontroller, a potentiometer, a LM339 Comparator, and the LDRs we've been talking about. We're pretty proud of this one - the entire setup costs less than $4, pretty cheap considering a microcontroller is involved!

Our physical prototype consists of 2 tables of 4 seats each, and we decided to laser cut them out and attach the wiring below. We could have used 3D printing, but we wanted size for our tables and laser cutting is undoubtably the faster option. To create the SVG needed I decided to use Adobe Illustrator, which the FabLab staff were more than happy to help with.

All data from the CV model and the LDR (and other electronics) bit were passed to our Firebase server, which was then used to change the stuff displayed on our website which was made using React JS.

And the Admin Setup Editor was made solely using Figma.

## Challenges we ran into
Many of the technologies here were stuff that we've barely worked with, but we were able to tap on each others strengths and make it in the end. We faced a bug on the CV model where it wasn't able to show the bounding boxes it placed on video, so we decided to revert to photos in order to show bounding boxes during our demonstrations.

Having a really short time to work with stressed us out a bit, and it took teamwork and mutual support to get us through.

## Accomplishments that we're proud of, and what we learned
All of us have quite diverse skillsets, and we took different roles during the project:\
Daksh - Server setup and Website Coding\
Jing Shun - Computer Vision guy\
Chin Ray - Website Coding\
Samuel - Insane Electronics carry\
Richard - Chief yapper, also the guy who wrote this bedtime story of an essay

Our roles overlapped often during the project, so we were able to learn lots from each other. In these two days, we discussed about CV, to Machine Learning, to obscure electronic manuals from the 80s, to the argument that XML > React (??)

The biggest takeaway within our team was the experience of locking in for such a long period. Most of us (maybe Daksh excluded) have not taken part in a hackathon like this before.
Making to the end made us really proud :)

## What's next for SeatTect
If we continued this project, we would probably improve the reliability of the system and create the Admin Setup Editor (which is stuck in Figma hell for now). But realistically, we won't continue this beyond this competition. It was a really cool concept, and we would be really happy to see such an idea adopted in our daily lives.
