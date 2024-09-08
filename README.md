# LLAMA Chat+RAG App for CPU

These are the following instructions for running a local chat and RAG application to communicate with Llama for CPU-based inference.

# Step 1: 
Open terminal and install the nicegui, llama-cpp, langchain, langchain_community, langchain_core, torch, and pywebview packages. 
```
pip install nicegui
pip install llama-cpp
pip install langchain
pip install langchain_community
pip install langchain_core
pip install torch
pip install pywebview
```
# Step 2: 
Navigate to [Hugging Face]([url](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main)) to download the [llama-2–7b-chat.Q2_K.gguf]([url](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main)) file: 
[https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main](url). Other model versions also work, as long as they are llama-cpp supported.

# Step 3: 
Clone this github repo into a folder. Move the downloaded Llama model into the same folder.

# Step 4: 
Go to file explorer and open the designated folder. Open the runapp.py file.

# Step 5: 
Ensure that the model_path parameter is set to correct path to the model file (just the file name if all steps have been followed properly).

```
model_path = [file name]
```

# Step 6: 
Open terminal and navigate to the designated folder. Then run the runapp.py file.

``` 
python runapp.py
```

# Step 7: 
The app should popup in your desktop. Enjoy chatting with Llama!

<img width="444" alt="image" src="https://github.com/user-attachments/assets/ec432c2f-977f-4355-94c1-cc2def292ce2">

# Step 8:
To use the RAG capability, navigate to the upload tab on the app and upload your file. You can now chat with Llama about your uploaded content.

<img width="430" alt="image" src="https://github.com/user-attachments/assets/ef92399b-1246-4f7a-a0d6-622ad5b54d37">

<img width="430" alt="image" src="https://github.com/user-attachments/assets/9bb3bb7f-8236-4b4d-a84a-e3ae49985d5d">


