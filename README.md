# Background
Immersion learning is a method of foreign language learning (also called acquisition) which emphasizes the learning of a foreign language using native content in the language as the primary study material.
For Japanese, one source of content for use in immersion learning is anime.
Different methods and approaches for using anime to learn the Japanese language have been presented on different internet sites and platforms, one example being AJATT (All Japanese All The Time) [1] and its various adaptations and modifications.

One source of information relating to tips, strategies, and tools for applying an AJATT style approach to Japanese learning using Anime is a YouTube channel called Matt vs Japan [2].
One idea that has been presented by MattvsJapan, as well as on the Refold language learning guide is the idea of language "domains", or genres of content which have a specific subset of language that is commonly used (e.g. fantasy vs. crime drama vs. slice-of-life) [3].
By focusing on a single domain, words unique to a domain can be encountered more frequency, thus increasing the chance of acquiring them for long term retention.
The aquisition of words has been deemed as highly important for learning a language, such as by Steve Kaufmann (one of the founders of LingQ) [4] [5].
Therefore, focusing on a single domain when immersing is an attractive strategy for quickly aquiring foreign language vocabulary.

One idea to determine the domain of a show/piece of content is by the genre of the media (e.g. slice-of-life).
While this seems to be a sensible categorization of media into language domains, the question remains (at least to me) whether shows within a single genre quantitatively have a higher language similarity than shows across different tagged genres.

The aim of this repo is to provide an analysis of the language content from different anime shows to quantify the degree of similarity in the language used.
The objectives are as follows:
- Develope criteria for comparing the similarity of the language present between any two shows.
- Identify and differentiate between "core language" and "domain language".
- Compare the degree of similarity of the language of shows in a single genre compared to shows across genres.

References:
[1] https://tatsumoto-ren.github.io/blog/whats-ajatt.html
[2] https://www.youtube.com/@mattvsjapan
[3] https://refold.la/simplified/stage-2/b/immersion-guide
[4] https://www.youtube.com/@Thelinguist
[5] https://www.lingq.com/en/

# Repo Contents
data - subtitle files for shows analyzed, separated as one folder for each show.

jupyter_writeup - Jupyter Notebook file and associated scripts for a more "article" style writeup.

# Setting up environment
To run the scripts and code in this repo, the python environment was set up as follows:

Note: if 'pip install package' can't find the path to pip, try 'python -m pip install package'.

## Installing fugashi 
For obtaining the lemma's of the words.
Cython wrapper for the Mecab tool (https://pypi.org/project/fugashi/).

```shell
pip install fugashi
```

## Installing Unidic 
Dictionary tool (https://pypi.org/project/unidic/).

```shell
pip install unidic
```
followed by
```shell
python -m unidic download
```
to download the dictionary files.
Takes up 1GB of disk space (according to pypi readme).

## Installing Mecab
Japanese language tokenizer and morphological analysis (https://github.com/ikegami-yukino/mecab/releases).

For python 64-bit on Windows, the MeCab 64-bit binary is required (according to the pypi site).
https://github.com/ikegami-yukino/mecab/releases

Install using the UTF-8 character set option.

Following installing of the above binary if needed, run
```shell
pip install mecab
```
