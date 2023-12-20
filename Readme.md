# Content-Based Image Retrieval (CBIR) Project

## Overview

This project implements a Content-Based Image Retrieval (CBIR) system, allowing users to search for similar images based on content rather than keywords. The project involves scraping images from [Pexels](https://www.pexels.com), a free stock photo and video website, and building a web application using FastAPI for the backend and a combination of JavaScript, HTML, and CSS for the frontend.

## Features

- **Web Scraping:** Utilizes web scraping techniques to fetch images from [Pexels](https://www.pexels.com).
- **FastAPI Backend:** Implements the backend using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **JavaScript/HTML/CSS Frontend:** Subtle frontend for interaction.

![image](https://github.com/AminRane/CBIR/assets/71436342/3e1db202-2263-4d2c-86d4-2cbc62276ce4)

## Setup and Installation
1. Clone the Repository
`git clone https://github.com/AminRane/CBIR.git
cd cbir-project`

2. Install dependencies
`pip install -r requirements.txt`

3. Scrap the data
`python scrap.py`

4. To train the model for image embeddings run the train.ipynb

5. Run the application
`uvicorn main:app --reload`
