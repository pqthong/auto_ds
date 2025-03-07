

# Automated Data Science Platform

This project is an automated data science platform designed to streamline data cleaning, statistical analysis, and visualization using advanced machine learning models and tools. The platform leverages LangGraph, LangChain, and other libraries to provide a comprehensive solution for data analysis.

## Features

- **Data Cleaning**: Automatically handle missing values, detect and remove duplicates, normalize text columns, convert date columns, and handle outliers.
![image](./doc/1.png)
- **Statistical Analysis**: Generate detailed statistical summaries, including descriptive statistics, correlation matrices, skewness, kurtosis, and outlier detection.
![image](./doc/3.png)

- **Data Visualization**: Suggest and generate various chart types to visualize the dataset effectively.
![image](./doc/4.png)
- **Entity Relationship Diagram (ERD)**: Generate ERDs from SQL schema.
![image](./doc/2.png)
- **Interactive Chat**: Ask questions about your dataset and get insights through an interactive chat interface.
![image](./doc/5.png)

## Setup

### Prerequisites

- Python 3.11 or higher
- Google gemini key ( because it is cheap , dont ask)


### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/data_analyzer.git
    cd data_analyzer/auto_ds
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    
    Not done write requiremnt.txt 

    ```bash
    pip install -e .
    ```
    When run any thing missing install it 
4. Create a `.env` file and add your API keys:
    
    need GOOGLE_API_KEY

### Running the Application

1. Start the FastAPI server:

    ```bash
    python3 app.py
    ```

2. Start streamlit
    
    ```bash
    streamlit run streamlit.py
    ```

go to streamlit ui and mess around
## Usage

### Uploading a Dataset

1. Go to the upload section and choose a CSV  to upload or use test.csv data.
2. The platform will process the data, clean it, and provide a preview of the cleaned data.
3. It will also generate a statistical summary, ERD, and various visualizations.
4. That shit take time be peition
### Interactive Chat

1. Use the chat interface to ask questions about your dataset.
2. The platform will analyze your query and provide insights based on the data.
3. Use after uloaded file

## Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Tavily](https://tavily.com/)
- [Anthropic](https://console.anthropic.com/)
- [OpenAI](https://platform.openai.com/)

