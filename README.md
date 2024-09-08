# LLAMA Chat+RAG App for CPU

These are the following instructions for running a local chat and RAG application to communicate with Llama for CPU-based inference.

# Step 1: 
Open terminal and install nicegui, llama-cpp, langchain, langchain_community, langchain_core, and torch.

# Step 2: 
Navigate to [Hugging Face]([url](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main)) to download the [llama-2–7b-chat.Q2_K.gguf]([url](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main)) file: 
[https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main](url). Other model versions also work, as long as they are llama-cpp supported.

# Step 3: 
Clone this github repo into a folder. Move the downloaded Llama model into the same folder.

# Step 4: 
Go to file explorer and open the designated folder. Open the mainpy.py file.

<img width="581" alt="image" src="https://github.com/user-attachments/assets/aa56f778-36e6-42b2-9415-6120105aa6d6">

# Step 5: 
Ensure that the model_path parameter is set to correct path to the model file (just the file name if all steps have been followed properly).

```

```

# Step 6: 
Open terminal and navigate to the designated folder. Then run the runapp.py file.

``` 
python mainpy.py

```

# Step 7: 
The app should popup in your desktop. Enjoy chatting with Llama!

# Step 8:
To use the RAG capability, navigate to the upload tab on the app and upload your file. You can now chat with Llama about your uploaded content.



