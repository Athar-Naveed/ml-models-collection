# ML models collection

## Overview

The purpose of this project is not just to add it into our portfolio but, to learn new technologies while building it.
Every model contains a complete new world in them.

## Current Features in my mind

1. Weather prediction
2. Shortest path finder (using tracker of your device).
3. Image Segmentation
4. Facial Recognition
5. Rubik's cube solver

## What I have done till yet

-> Task 1:
I am getting the user's IP address, from it, I have fetched its city, and loaded his/her area's 1 year rain data, into pandas tables. (Make sure to cross-verify the tables, they should have to be async, you can try PyArrow or asyncio whichever feels suitable).

## What You have to do

Take this table, train an AI model using PyTorch, and return the results to the frontend.

### Folder Structure

"-" <- This represents the root

"--" <- This represents the folder in the root

"---" <- This represents a file/folder

```
─ src
-- backend
--- routers
---- weather.py (it is where I am receiving the ip from the frontend)
--- models
---- weather_prediction.py (your work starts from here)
--- server.py (Main code file)
--- .env (make sure to add your own RAPID_API_KEY, like this: RAPID_API_KEY="key_here")
─ .gitignore
─ README.md
─ Makefile
─ pyproject.toml
─ requirements.txt
- uv.lock
- vercel.json
```

### weather_prediction.py

This file contains a class and it has 2 functions:

1. get_weather_history(): From name you know it is getting that specific area's 1 year weather history.
2. weather_prediction_model(): Here you have to start making the pytorch model, and pass the previous year's data for your model to get trained on, you can temporarily store the data (upto you). Or you can just train you model and store that trained model in a **_.h5_** file
