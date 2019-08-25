 # :rocket: Google Summer Of Code 2019 Project - Creation of an online Greek mail dictation system

Welcome to the home repository of "Creation of an online Greek mail dictation system using Sphinx and personalized acoustic/language model training".

This project is implemented as a Google Summer of Code 2019 Project, under the auspices of Open Technologies Aliance - GFOSS.

## About the project

With over 2.6 billion active users and over 4.6 billion email accounts in operation, email is the most important and widely used communication medium on the Internet. In the last fifteen years, the huge rise of social networks and chat applications changed the role of emails, that nowadays are mainly used for business purposes rather than chatting. The email inbox is the first thing that anyone checks after entering their respective workplace. Seeing that this kind of communication has become an important part for businesses, convenience, speed and accuracy are necessary. All these benefits can be provided by enabling people to dictate their emails rather than writing them. More specifically, through email dictation users can move from one place to another while getting their work done faster than writing them and more accurately, since the computer is responsible for the correct spelling.

In the modern era of Big Data, many dictation systems have already been implemented reaching high accuracy in the proposed metrics. However,  each system concerns a certain language because of the huge diversity of spoken languages. As a result, the implementation of a Greek mail dictation system should be done from scratch based on the Greek language and its unique characteristics. A basic problem is the fact that the training part requires a large set of human transcribed recordings, while very small Greek speech datasets are available. So, the project’s purpose is the implementation of a personalized Greek mail dictation system, that will be trained in the speech of each user (speaker dependent). By this way, we solve the above problem by asking the user for some dictations at the start and train the system using these recordings. Ιt is worth noting, that this restriction of the system doesn’t pose a problem, since each email address corresponds to a single user. In addition, the system’s performance will be enhanced by adapting the language model to the user's existing emails. Extra utilities, such as special dictation commands and email replay, will facilitate the user interaction and make the whole procedure faster and more practical.

## Demo
The project is hosted at https://snf-870034.vm.okeanos.grnet.gr.

## Timeline and Documentation

- A detailed timeline can be found [here](https://github.com/eellak/gsoc2019-sphinx/wiki/Timeline), organized by [GSoC timeline](https://developers.google.com/open-source/gsoc/timeline). 
- The whole progress of the project was tracked on a daily basis in [Project](https://github.com/eellak/gsoc2019-sphinx/projects/1).
- More details can be found in [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki) and in the [Final Report](https://gist.github.com/PanosAntoniadis/2a056cdbe4eb8556c30e33193e84d1b0).

 
The whole model as a block diagram follows:

<img src="https://github.com/eellak/gsoc2019-sphinx/blob/master/docs/pics/model2.png"/> 

## Overview

- **Getting started**
  - [Home](https://github.com/eellak/gsoc2019-sphinx/wiki)
  - [Installation](https://github.com/eellak/gsoc2019-sphinx/wiki/Installation)
  - [Repository](https://github.com/eellak/gsoc2019-sphinx/wiki/Repository)
  - [Datasets and Adaptation](https://github.com/eellak/gsoc2019-sphinx/wiki/Datasets-and-Adaptation)
- **Tools**
  - [Fetching and Processing Emails](https://github.com/eellak/gsoc2019-sphinx/wiki/Fetching-and-Processing-Emails)
  - [Classify Emails](https://github.com/eellak/gsoc2019-sphinx/wiki/Classify-Emails)
  - [Domain Specific Language Models](https://github.com/eellak/gsoc2019-sphinx/wiki/Domain-Specific-Language-Models)
  - [Post Processing](https://github.com/eellak/gsoc2019-sphinx/wiki/Post-Processing)
  - [Evaluation](https://github.com/eellak/gsoc2019-sphinx/wiki/Evaluation)
- **API and UI**
  - [API Documentation](https://github.com/eellak/gsoc2019-sphinx/wiki/API-Documentation)
  - [Angular UI](https://github.com/eellak/gsoc2019-sphinx/wiki/Angular-UI)
- **Other**
  - [Licensing](https://github.com/eellak/gsoc2019-sphinx/wiki/Licensing)
  - [Future Work](https://github.com/eellak/gsoc2019-sphinx/wiki/Future-Work)

## Technologies used
- The project is written in __Python 3.x__, using all the python packages in the [requirements file](https://github.com/eellak/gsoc2019-sphinx/blob/master/requirements.txt).
- The speech recognition part is done using the __pocketsphinx__ library from [CMUSphinx](https://cmusphinx.github.io/wiki/).
- All language models are created using [SRILM](http://www.speech.sri.com/projects/srilm/).
- All the required user data is stored in a __MongoDB__.
- The UI is based on angular 8.

## Project Deliverables

1. Tool for __extracting and cleaning sent emails__ of a Gmail user. [Code](https://github.com/eellak/gsoc2019-sphinx/tree/master/email_processing) [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki/Fetching-and-Processing-Emails)
2. Tool for __creating adapted language models__ through email clustering. [Code](https://github.com/eellak/gsoc2019-sphinx/tree/master/email_clustering) [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki/Domain-Specific-Language-Models)
3. Tool for __correcting ASR output__. [Code](https://github.com/eellak/gsoc2019-sphinx/tree/master/post_processing) [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki/Post-Processing)
4. Various tools for __preparing and evaluating a speech dataset__. [Code](https://github.com/eellak/gsoc2019-sphinx/tree/master/data/scripts) [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki/Datasets-and-Adaptation) 
5. Simple tool for __creating a speech dataset__. [Code](https://github.com/PanosAntoniadis/fast-recorder)
6. __API__ written in Flask. [Code](https://github.com/eellak/gsoc2019-sphinx/tree/master/api) [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki/API-Documentation)
7. __Online webpage__ using Angular 8. [Code](https://github.com/eellak/gsoc2019-sphinx/tree/master/angular-ui) [Wiki](https://github.com/eellak/gsoc2019-sphinx/wiki/Angular-UI)

## People
- Google Summer of Code 2019 Student: Panagiotis Antoniadis ([PanosAntoniadis](https://github.com/PanosAntoniadis))
- Mentor: Andreas Symeonidis ([asymeon](https://github.com/asymeon))
- Mentor: Manos Tsardoulias ([etsardou](https://github.com/etsardou))
