# Emotion Sound Project

This project is designed to analyze audio files and predict emotions using various machine learning models available through the Hugging Face API. The system provides functionalities to upload audio files, select prediction settings, and visualize the analysis results.

## Features

- **Upload Audio Files**: Users can upload audio files in WAV format to be analyzed for emotions.
- **Prediction Settings**: Users can adjust prediction settings to select the desired machine learning model for emotion prediction.
- **Analysis Visualization**: The system presents analysis results in a clear and concise format, highlighting emotions detected in the audio file.

## Requirements

Ensure you have the following dependencies installed to run the project:

- `streamlit`
- `pathlib`
- `requests`
- `streamlit`
- `requests`
- `pymongo`
- `bcrypt`
- `pymodm`
- `bson`
- `python-dotenv`

You can install them using `pip`:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Set up a MongoDB database and create .env file and put your connection string in an environment variable called `MONGO_URI`
4. Run the Streamlit app using the following command:

```
streamlit run app.py
```

4. The application will open in your default web browser.

## Usage Guide

- **Analysis Tab**: Upload an audio file to analyze its emotional content. The results will be displayed after the analysis is complete.
- **Prediction Settings Tab**: Adjust prediction settings to customize the analysis process.
  - Select the desired machine learning model for emotion prediction.
  - Adjust the settings according to your preference.

## Development Notes

- The project uses the Hugging Face API to access machine learning models for emotion recognition.
- Ensure a stable internet connection for seamless API communication.
- The codebase is modular and can be extended to incorporate additional features or models.



