# Annotation bot

The module contains a code for launching a bot that can assist colleagues in the **annotation of genes or proteins**, should they lack the requisite programming skills.

## Overview:

All of the code can be divided into two main parts: the bot and the annotation.

### The bot

The bot was developed using the **Aiogram** library. This affords the possibility of asynchronous processing of commands and parallel operation with multiple users. The **Pydantic** library will help you take care of your token security.

### The annotation

The current version lets you annotate proteins and genes using **Uniprot** and **Ensembl**, respectively. The protein annotation is based on the protein ID, for example, **P51587** for human *BRCA2*. The gene annotation is based on the Ensembl ID, for example, **ENSG00000142192** for human *APP*. The plan is to add the ability to annotate by gene names. Code for Uniprot database annotation was created using [Roberts Lab Handbook](https://roberts-lab-resources.readthedocs.io/en/latest/bio-Annotation/).

## Launch 

1. **Clone the repository**                      
2. **Install dependencies from**   `requirements.txt`                         
3. **Creating a Bot Account in Telegram:**                             
3.1. Open Telegram and find the bot @BotFather                               
3.2. Use the command `/newbot` to create a new bot                                      
3.3. Follow the instructions                      
3.4. After creating the bot, you will receive an API token. Save it, as you will need it for configuration   
4. **Setting Up the Token:**                             
4.1. Create a .env file in the root directory                                  
4.2. Add the following text to the .env file, replacing YOUR_BOT_TOKEN with the token you received from BotFather: `BOT_TOKEN=YOUR_BOT_TOKEN`                                                             
5. **After setting up the token, you can start the bot using the following command:**   `python3 bot.py`                 

## Usage

Briefly, find your bot and use the command `/start`. Then select database in the reply keyboard.

### Input

Upload a file containing IDs in `.txt` format. Each ID must be on a new line.

### Output

The resulting file is sent in csv format with `\t` as the separator.

## Troubleshooting

One of the most common causes of errors is incorrect file IDs. This can be checked in the `downloads` folder, where files are not deleted in the event of an error.
