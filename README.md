![Image of Nebula](https://i.imgur.com/HjSw4Cv.jpeg)

# What is Nebula?

It's for viewing a large amount of websites and taking screenshots of them automatically. This is a very early alpha. Use at your own frustration.

## Why?
 
Imagine you're on a red team engagement and there are hundreds, perhaps thousands of hosts. You have limited time to get a quick overview of the juiciest targets. 

Enter Nebula. This script generates screenshots of each page, port and protocol, then displays them in an html file that allows you to sort between protocols and ports. 

You are then free to pick the most likely targets of opportunity.
 
# Usage

## Inputfile
 
Your input file must be formatted like so:
 
 ```
 https://website.com
 http://website.com
 https://website.com:8080
 http://website.com:8080
 ```
## Example Use

 ```
$ python3 nebula.py -i websites.txt
 ```

## Parameters

```
$ python3 nebula.py --help
usage: nebula.py [-h] [-i INPUTFILE] [-r]

Nebula

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        Specify a text file with line-separated domains
  -r, --report          Regenerate the report instead of running another long-winded scan.
 ```
