#### important
talk is cheap, send commit

# Automated Data Science Platform

This project is an automated data science platform designed to streamline data cleaning, statistical analysis, and visualization using advanced machine learning models and tools. The platform leverages LangGraph, LangChain, and other libraries to provide a comprehensive solution for data analysis.

## Features

- **Data Cleaning**: Automatically handle missing values, detect and remove duplicates, normalize text columns, convert date columns, and handle outliers.
- **Statistical Analysis**: Generate detailed statistical summaries, including descriptive statistics, correlation matrices, skewness, kurtosis, and outlier detection.
- **Data Visualization**: Suggest and generate various chart types to visualize the dataset effectively.
- **Entity Relationship Diagram (ERD)**: Generate ERDs from SQL schema.
- **Interactive Chat**: Ask questions about your dataset and get insights through an interactive chat interface.

## Setup

### Prerequisites

- Python 3.11 or higher
- [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio)
- [Tavily API Key](https://tavily.com/)
- [Anthropic API Key](https://console.anthropic.com/) or [OpenAI API Key](https://platform.openai.com/signup)

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

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your API keys:

    ```bash
    cp .env.example .env
    ```

    Update the `.env` file with your API keys.

### Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn app:app --reload
    ```

2. Open your browser and navigate to `http://localhost:5000`.

## Usage

### Uploading a Dataset

1. Go to the upload section and choose a CSV or Excel file to upload.
2. The platform will process the data, clean it, and provide a preview of the cleaned data.
3. It will also generate a statistical summary, ERD, and various visualizations.

### Interactive Chat

1. Use the chat interface to ask questions about your dataset.
2. The platform will analyze your query and provide insights based on the data.

## Project Structure

- `app.py`: Main FastAPI application file.
- `src/react_agent`: Contains the core logic for data cleaning, statistical analysis, and visualization.
- `src/react_agent/state.py`: Defines the state structures for the agent.
- `src/react_agent/prompts.py`: Contains prompt templates for various tasks.
- `src/react_agent/graph.py`: Defines the custom Reasoning and Action agent.
- `src/react_agent/node`: Contains the nodes for different tasks like data cleaning, statistical analysis, etc.
- `llm`: Contains additional logic for language model interactions.
- `Makefile`: Contains commands for testing, linting, and formatting.
- `pyproject.toml`: Project configuration file.
- `.env.example`: Example environment file.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Tavily](https://tavily.com/)
- [Anthropic](https://console.anthropic.com/)
- [OpenAI](https://platform.openai.com/)

