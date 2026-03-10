Setup Python Environment
# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies 
pip install -r requirements.txt




# Install Ollama: https://ollama.ai
# Start Ollama server
ollama serve

# In another terminal, pull a model
ollama pull llama2

# Run analysis (in another terminal)
python analyze_java_codebase.py ./project --llm --provider ollama --model llama2


# For Open API
export OPENAI_API_KEY=sk-your-key-here
python analyze_java_codebase.py ./project --llm




# Running a program
# Below command will clasify all the classes kile DTO, mapper controller
python analyze_java_codebase.py <Project analysis path>

python analyze_java_codebase.py <Project analysis path> --llm --provider ollama -j report.json

# If we Run with OpenAI
python analyze_java_codebase.py ./project --llm -j report.json%         


python analyze_java_codebase.py /Users/gauravagnihotri/code/ai/interview/spring-rest-sakila --llm --provider ollama --convert-ts