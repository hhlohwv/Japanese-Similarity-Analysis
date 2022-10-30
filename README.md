# Scope and aim
Aim is to analyze subtitle files from anime series and compile a database/list of the frequently occuring words outside of the 'core language', i.e. the domain language of each show.
- core language being those words that are common to all media (i.e. 私, はい, other ubiquitous words
- domain language being those words common to the type of media (setting, theme, genre), but maybe not common outside of that area.

Motivation is from a number of sources, such as MattVsJapan (Focus on a single domain to increase comprehension of language in that area) and Steve Kaufmann (Words are king, learn a lot of words).


# Python Virtual Environment
Using the python 'venv' module for managing the virtual environment.

Create using 'python -m venv venv'

## Notes regarding usage, mostly for myself
- Start the virtual environment in the terminal (in the folder) using venv\scripts\activate
- Open up the idle in the virtual environment using python -m idlelib.idle
- Deactivate the virtual environment using deactivate
- While in the virtual environment, install packages as normal using pip.


# Environment setup and package installation

Note: if 'pip install package' can't find the path to pip, use 'python -m pip install package' instead.

## Using 'fugashi' for the Japanese language analysis module
For obtaining the lemma's of the words.
Install using 'pip install fugashi'

## Using Unidic as the dictionary
Install using 'pip install unidic' followed by 'python -m unidic download'

## Using Mecab as binding for Mecab (? still not exactly sure what that functions as)
Install using 'pip install mecab'

## Plotting and additional calculations via Matplotlib
Install using 'pip install matplotlib'.
This also handles the installation of the numpy package.

For easy copying of figures with ctrl+c, can use addcopyfighandler
Install using 'pip install addcopyfighandler'

For saving installed packages to requirements.txt, run 'pip freeze > requirements.txt'
For installing packages from requirements file into virtual environment, run 'pip install -r requirements.txt'


# Script usage and analysis workflow


# Proposed study workflow (to refine)
Note: This approach may be best after one has some familiarity with the core vocabular/structure of Japanese.
For me, I've been using an immersion focused study approach for the last 2 years, and am at the point where I can get a sense of the meaning of many things in a relatively simple context, I am able to read/work through some manga, and regularly listen to japanese conversation through podcasts such as YUYUの日本語PODCAST and streams on YouTube, primarily Japanese VTubers, focusing on Zatsudan content but simply watching what I find entertaining.

A study workflow which utilizes these scripts may be in the following form:

Requirements/software needed:
Python
Subtitle files for a show
Slideshow/presentation software (e.g. LibreOffice Impress (free), Powerpoint)

Watch a show that you enjoy/are familiar with the story and possibly have watched once in English.

Extract the domain language using the scripts, with the subtitles for the entire show/season as the input.

Take the top # of domain language words (however many # is) and make sentence cards in the presentation software, perhaps 2-3 sentences per domain language word.
Include a screen shot of the scene and an audio recording that can play when the slide is shown.
- for choosing sentences, probably go with 1T mentality, choosing sentences that have this word as one of the only unknown elements, and also including sentences before/after if they help with understanding the context that the sentece occurs is.
- Goal is for the sentence slide to be understandable by itself.

Each day when immersing, quickly review the slides by clicking through them while listening and reading to the sentence.
When finished watching the series, review the slides again and store away. These slides can then be quickly reviewed then at any point.
