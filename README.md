# Plagiarism Detector using ML and NLP 

A machine learning-based plagiarism detection system built using Natural Language Processing (NLP) techniques to ensure the integrity of academic work. This tool helps  promote academic honesty by identifying potential plagiarism.

This project is ideal for anyone interested in AI and ML and is looking to gain experience practically. This is also for ideal for anyone trying to figure out if AI or ML is something the want to pursue.
A lot of time and effort was taking into this, that being said, it is not perfect and may contain some errors.

## Features:
- **Plagiarism Detection**: Detects plagiarism by comparing submitted text with the original text using NLP and machine learning algorithms.
- **Real-time Feedback**: Provides feedback on content originality as soon as it's submitted.
- **Preprocessing**: Removes stopwords, punctuation, and converts text to lowercase before processing for accuracy.
- **Lemmatization and POS Tagging**: Uses lemmatization to reduce words to their base forms and POS (Part of Speech) tagging to identify word types, ensuring the analysis is more accurate.
- **User-friendly Interface**: The Flask application makes it easy to interact with the system. The interface is simple, intuitive, and easy to navigate, designed with user experience in mind.
- **Memes and Educational Content**: The system incorporates memes and relatable content that aim to educate users about plagiarism and promote academic integrity in a lighthearted, engaging way.
- **Login Functionality**: Allows users to securely log in to the system and access their profiles.
- **Admin Functionality**: Admins can manage user accounts, monitor submissions, and control access to the system.
- **User Profiles**: Each user (student/instructor) has a personal profile with submission history and plagiarism check results.
- **Easy Registration**: Users can easily register for an account and get started with submitting their work for plagiarism checks.
- **Database Connection**: The system connects to a MySQL database to store user data, submissions, and results, ensuring secure and efficient data management.

## Inspiration:
This project was inspired by the [Plagiarism Detector using Machine Learning](https://github.com/611noorsaeed/Plagiarism-detector-using-machine-learning) repository. I utilized their dataset, making slight modifications to better suit my implementation. I highly appreciate the work done by the original author, and this project builds on their efforts to improve plagiarism detection.

## Dataset:
The dataset used in this project is based on the one from the above-mentioned repository. I modified the dataset slightly by cleaning it and ensuring that it fits the requirements for the machine learning model in this plagiarism detector system. The dataset was preprocessed with techniques like lemmatization and POS tagging to improve the accuracy of text comparisons.

## Preprocessing:
The dataset underwent a series of preprocessing steps to prepare it for the plagiarism detection model:
- **Lowercasing**: All text was converted to lowercase to ensure uniformity and reduce false positives.
- **Stopword Removal**: Commonly used words (stopwords) like "the", "and", "is", etc., were removed using the NLTK library. This helps focus on the content-specific words.
- **Punctuation Removal**: All punctuation marks were stripped from the text to avoid unnecessary distractions for the algorithm.
- **Removing common words**: I removed specific common words from the text, such as name.
- **Lemmatization**: Words were reduced to their base or dictionary form using NLTK's lemmatizer. This ensures that variations of words are treated as the same word (e.g., "running" becomes "run").
- **POS Tagging**: Part of Speech tagging was used to identify the word types (nouns, verbs, adjectives, etc.) to ensure the system better understands the structure of the text.
- **TF-IDF Vectorization**: The processed texts were converted into numerical vectors using Term Frequency-Inverse Document Frequency (TF-IDF) to capture important word features.

## Training and testing the ML 
I used svm and 80% of the preprossed and vectorized data was to train the model and 20% used to test theaccuracy of the system. 


## Flask Application 
I used Flask and used it to connect my trained model and database to my user interface. This application will allow ; 
- Users to submit text for plagiarism, If plagiarism is detected then the specific text will be highlighted.
- Users to access previous submissions and Plagiaraism results.
- Admins to manage the users ie delete or update user roles.

The Flask application provides customized interfaces for different user roles (Student and Instructor, Admin). Each role has access to specific functionalities and views, ensuring that users have a streamlined and tailored experience based on their needs and responsibilities

## Database
I used Mysql Workbench.
