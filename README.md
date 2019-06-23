 # :rocket: Google Summer Of Code 2019 Project - Creation of an online Greek mail dictation system

Welcome to the home repository of "Creation of an online Greek mail dictation system using Sphinx and personalized acoustic/language model training".

This project is implemented as a Google Summer of Code 2019 Project, under the auspices of Open Technologies Aliance - GFOSS.

## About the project

With over 2.6 billion active users and over 4.6 billion email accounts in operation, email is the most important and widely used communication medium on the Internet. In the last fifteen years, the huge rise of social networks and chat applications changed the role of emails, that nowadays are mainly used for business purposes rather than chatting. The email inbox is the first thing that anyone checks after entering their respective workplace. Seeing that this kind of communication has become an important part for businesses, convenience, speed and accuracy are necessary. All these benefits can be provided by enabling people to dictate their emails rather than writing them. More specifically, through email dictation users can move from one place to another while getting their work done faster than writing them and more accurately, since the computer is responsible for the correct spelling.

In the modern era of Big Data, many dictation systems have already been implemented reaching high accuracy in the proposed metrics. However,  each system concerns a certain language because of the huge diversity of spoken languages. As a result, the implementation of a Greek mail dictation system should be done from scratch based on the Greek language and its unique characteristics. A basic problem is the fact that the training part requires a large set of human transcribed recordings, while very small Greek speech datasets are available. So, the project’s purpose is the implementation of a personalized Greek mail dictation system, that will be trained in the speech of each user (speaker dependent). By this way, we solve the above problem by asking the user for some dictations at the start and train the system using these recordings. Ιt is worth noting, that this restriction of the system doesn’t pose a problem, since each email address corresponds to a single user. In addition, the system’s performance will be enhanced by adapting the language model to the user's existing emails. Extra utilities, such as special dictation commands and email replay, will facilitate the user interaction and make the whole procedure faster and more practical.


## Timeline

A detailed timeline follows, organized by [GSoC timeline](https://developers.google.com/open-source/gsoc/timeline). More details can be found in [Project](https://github.com/eellak/gsoc2019-sphinx/projects/1) and [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki).

- __Student application work (Mar 25 - Apr 09)__
  
  Get familiar with all the concepts of the project, read documentation and think about possible extensions. Some useful links follow:
  - [Sphinx](https://cmusphinx.github.io/wiki/)
  - [SRILM](http://www.speech.sri.com/projects/srilm/)
  - [g2p-seq2seq](https://github.com/cmusphinx/g2p-seq2seq)
  - [WebSocket](https://blog.teamtreehouse.com/an-introduction-to-websockets)
  - [Spacy](https://spacy.io/)
  - [scikit-learn](https://scikit-learn.org/)
  - [React](https://reactjs.org/tutorial/tutorial.html)

- __Community Bonding Period (May 6 - May 26)__
  - Get to know my mentors better and discuss the project more extensively.
  - Implementation of the baseline part of the ASR system based on the default acoustic and language model, that can be found [here](https://www.dropbox.com/sh/fl6698yfuam54ch/AABx4hHs4P5kFVBGJQQZN_Voa?dl=0).
  - Search for speech datasets (recordings along with their transcriptions) and organize them in order to be in Sphinx standard form.
  - Implementation of a domain specific and a merged (specific + default) language model for each dataset.
  - Evaluation of these models in both datasets. Using the default acoustic model and dictionary, the results are [here](https://github.com/eellak/gsoc2019-sphinx/wiki/Datasets-and-Adaptation).


- __Phase 1 (May 27 - Jun 28)__
  - Extension of the the default dictionary using [Phonetisaurus](https://github.com/AdolfVonKleist/Phonetisaurus).
  - Adaptation of the acoustic model in all datasets and evaluation.
  - Implementation of a system that extracts the emails from a user's account.
  - Email classification.
  - Email clustering.
  - Create a personal email dataset for evaluation.

- __Phase 2 (Jun 29 - Jul 26)__
  - Implementation of domain-specific language models.
  - Implementation of the correction system.
  - Integration of special dictation commands.
 
- __Phase 3 (Jul 27 - Aug 26)__
  - Implementation of the UI.
  - Playback of the email to the user.
 

## People
- Google Summer of Code 2019 Student: Panagiotis Antoniadis ([PanosAntoniadis](https://github.com/PanosAntoniadis))
- Mentor: Andreas Symeonidis ([asymeon](https://github.com/asymeon))
- Mentor: Manos Tsardoulias ([etsardou](https://github.com/etsardou))
