
<h1 align="center">

  Split-Facewise
  <br>
</h1>

<h4 align="center">A minimal implementation of splitwise using Face-Recognition </h4>



<p align="center">
  <a href="#problem-statement">Problem Statement</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#pre-requisites">Pre-Requisites</a> •
  <a href="#installation">Installation</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#user-interface">User Interface</a> •
  <a href="#license">Downfalls</a>
</p>

![akhil](https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.gif)

## Problem Statement
Ever had to face the difficulty of splitting bills while at dinner?
<br>
Worry no more, on the Split-Facewise webapp, you and your friends can signup for free and split bills on the go.
<br>
Upload a profile picture, to verify yourself
<br>
To split a bill, just add a group picture. We automatically scan and recognise all faces present and correctly split the amount.


## Key Features
* Login Logout authentication
  - Secured account using password hashing
  - Add a profile pic which will be stored on firebase as well as locally
  - Credentials are stored in a sqlite3 database
* Detects all faces and recognises people who are registered on the webapp using face_recognition library
* The Multi-user system is able to handle as many users and transactions
* Each Transaction has a unique id and timestamp, every user is able to see his/her balances
* Search feature for transactions
* Update feature to revise the balance for people who have paid you back either partially or entirely
* Settle Feature to reduce number of redundant payments amongst your friend circles



## Pre-Requisites

> **Note**
>For Windows insallation only
<br>

To clone and run this application, you'll need [Git](https://git-scm.com) and python installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/amitmerchant1990/electron-markdownify

# Install Python
$ cd electron-markdownify

# Create a Virtual Env
$ npm install

# Install cmake
$ pip install cmake

# Install Dlib
$ pip install dlib
Dlib package is present in the repository
$ pip install [DIR_NAME]

# Install all other Requirements
$pip install requirements.txt


```

## Installation

Markdownify is an [emailware](https://en.wiktionary.org/wiki/emailware). Meaning, if you liked using this app or it has helped you in any way, I'd like you send me an email at <bullredeyes@gmail.com> about anything you'd want to say about this software. I'd really appreciate it!

## Tech Stack

This software uses the following open source packages:

- [Django](https://www.djangoproject.com/)
- [Firebase](https://firebase.google.com/)
- [Dlib](http://dlib.net/)
- [TensorFlow](https://www.tensorflow.org/)


## User Interface

Screenshots

## Downfalls

Heroku deployment


---


> GitHub [AkhilNagar](https://github.com/AkhilNagar/) &nbsp;&middot;&nbsp;
> Linkedin [AkhilNagar](https://www.linkedin.com/in/akhil-nagar/)

