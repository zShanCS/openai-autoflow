
# Autoflow Server

# Setup
Ensure you have `python 3.8` installed.

1.  `pip install -r requirements.txt`
2. Create `.env` file  containing your OpenAI secret key as follows
`OPENAI_API_KEY=`
3. Download the [intent embeddings](https://drive.google.com/file/d/1a0e3m8TyyxRaPi73gdsSXSHjfWPbnRo_/view?usp=sharing) to use `classify_intent.py`
4. Download the following models and place them in the mentioned folder:
	- [models/search](https://drive.google.com/file/d/1v3uXuPCpK4V5cnx5C0Q0zEteKgRV5B7B/view?usp=sharing)
	-  [models/defect](https://storage.googleapis.com/sfr-codet5-data-research/finetuned_models/defect_codet5_base.bin)
	- [models/refine](https://storage.googleapis.com/sfr-codet5-data-research/finetuned_models/refine_medium_codet5_base.bin)
	- Rename the defect and refine models as `pytorch_model.bin`
5. Download the [CommitBERT weights](https://drive.google.com/drive/folders/153brGoeSqpCyYSZi2OMmEs25crcsi4WU) folder, place it in `./commit_bert`, and rename it as `weight`
## Start Server
	in root folder:
           `python main.py`
