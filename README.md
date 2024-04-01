# MAS-Program4

## Echo Chamber Project Overview

This project explores the implementation of two voting methods, Ranked choice and Social network, as part of CS 5110 Program 4.
The goal of this project is to understand how these voting systems operate and thier impact.

## Required packages

Ensure you have python installed on your machine along with 'numpy' a required library used for various numerical calculations.

## Usage

Run the script in any python editor or in the command line with

```bash
python voting.py
```

## Files

No other data files are required for this project

## Functionality

### Ranked Choice Voting

- generates random preferences for voters to canidates
- iterates through all voters first choice canidate and removes the canidate with the lowest number of first choice votes, when a canidate is removed, that canidate is replaced with a voters next choice. This pattern continues until there is only one canidate left

### Social Network

- generates random preferences for voters to canidates
- voters are then allowed to change their votes based on what their neigbors 'influence'
