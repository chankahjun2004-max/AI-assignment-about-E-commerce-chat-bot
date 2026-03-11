# E-Commerce Chatbot

An AI-powered customer support chatbot designed for E-commerce platforms. This project leverages large language models (LLMs) via Ollama to provide intelligent, context-aware responses to user queries based on a given dataset and predefined intents.

## Features

- **Multi-Model Support**: Choose between cutting-edge LLMs including **Gemma 3**, **Llama 3**, and **Mistral**.
- **Interactive UI**: A sleek, web-based chat interface built with HTML, CSS, and vanilla JavaScript.
- **Dataset Cleaning**: Built-in functionality to clean and preprocess raw E-commerce datasets for better model context.
- **Intent Recognition**: Utilizes predefined intents to handle common customer service scenarios effectively.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI / LLMs**: Ollama (Gemma 3, Llama 3, Mistral)
- **Data Processing**: Pandas

## Project Structure

```
E Commerce Chatbot/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── DataCleaner.py          # Script for cleaning datasets
│   ├── chatbot_Gemma3.py       # Gemma 3 chatbot logic
│   ├── chatbot_Llama3.py       # Llama 3 chatbot logic
│   ├── chatbot_Mistral.py      # Mistral chatbot logic
│   └── requirements.txt        # Python dependencies
├── data/
│   ├── DataSet.csv             # Raw dataset
│   ├── Cleaned_DataSet.csv     # Preprocessed dataset
│   └── intents.json            # Predefined intents for the chatbot
└── frontend/
    ├── templates/
    │   └── index.html          # Main chat interface
    └── static/
        ├── style.css           # Styling
        ├── main.js             # Client-side logic
        └── *.jpeg              # UI Assets
```

## Prerequisites

1. **Python 3.8+** installed on your system.
2. **Ollama** installed and running locally. You will need to pull the models you intend to use:
   ```bash
   ollama run gemma:3  # (or equivalent gemma model name)
   ollama run llama3
   ollama run mistral
   ```

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chankahjun2004-max/AI-assignment-about-E-commerce-chat-bot.git
   cd AI-assignment-about-E-commerce-chat-bot
   ```

2. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the web interface**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

- Upon loading the web interface, you can interact with the chatbot immediately.
- The system automatically loads the cleaned dataset to provide context-aware answers.
- The Flask app runs a dataset cleaning route at `/clean-dataset` to process raw CSV files.

## Contributing

Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is created for educational/assignment purposes.
