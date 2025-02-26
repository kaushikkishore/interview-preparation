# Tambola Game - Claim Validator

## Overview
Tambola (also known as Housie or Bingo) is a popular game played worldwide. Players receive tickets with numbers, and a dealer announces numbers randomly. Players cross off matching numbers on their tickets. The game consists of multiple rounds, with each round containing several games. Players can claim victory when they complete specific patterns.

## Problem Statement
Create a claim validator that validates whether a player's claim for winning is valid or not.

### Input
- Numbers announced so far
- A valid ticket
- Claim for a specific game

### Output
- Accepted/Rejected

## Game Types
Each round includes multiple games with different winning patterns:
- **Top line**: All numbers in the top row crossed first
- **Middle line**: All numbers in the middle row crossed first
- **Bottom line**: All numbers in the bottom row crossed first
- **Full house**: All 15 numbers crossed first
- **Early five**: First to cross 5 numbers

## Rules
1. System only has to return whether a claim is accepted or rejected
2. A player's claim is only valid if made immediately following the announcement of the number that completes their winning sequence

## Examples

### Example 1: Top Row Win (Accepted)
**Input**
Ticket:
4,16,_,_,48,_,63,76
7,_,23,38,_,52,_,_,80
9,_,25,_,_,56,64,_,83
90, 4, 46, 63, 89, 16, 76, 48

Output Accepted
Explanation Winning pattern: 4, 63, 16, 48, 76

### Example 2: Top Row Win (Rejected)
**Input**  
Ticket:
4,16,_,_,48,_,63,76,_
7,_,23,38,_,52,_,_,80
9,_,25,_,_,56,64,_,83
90, 4, 46, 63, 89, 16, 76, 48  
Claim: Top Row

**Output**: Rejected  
**Explanation**: The last announced number (12) does not complete the top row

## Setup Instructions

### Prerequisites
- Python 3.8 or higher

### Installation & Running

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```