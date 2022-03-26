# Test Repo for DevRev Hackathon

# Usage
- `pip install -r requirements.txt`
- Create `.env` file  containing your OpenAI secret key as follows
`OPENAI_API_KEY=`
- Add `embeddings.pt` file for intent classification
## Start Server
uvicorn server:app --reload --port 8080

