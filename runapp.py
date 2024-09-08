from nicegui import app, ui, events
from llama_cpp import Llama
import asyncio
import os
from torch import cuda
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.llms.llamacpp import LlamaCpp
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate

# Change model path to your path.
model_path = "llama-2-7b-chat.Q2_K.gguf"

os.environ['USER_AGENT'] = "llama2chatgui"

vectorstore = None
embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)
n_gpu_layers = 32  
n_batch = 1024 
llm = LlamaCpp(
    model_path="llama-2-7b-chat.Q2_K.gguf",
    f16_kv=True, 
    verbose=True,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
)

# You can change the prompt template to change how LLama responds to you.

template = """Question: {query}

Answer: You are a helpful assistant who is ready to answer the user's questions. Answer each question very well and fully. Make each response a few sentences. Use all the context provided from a document if uploaded. Answer each user very well! Ensure that all your answers ARE COMPLETE. MAKE SURE THEY ARE COMPLETE. shorter answers are fine also"""

prompt = PromptTemplate.from_template(template)

llm_chain = prompt | llm
global rag_pipeline
rag_pipeline = llm_chain
global switchrag
switchrag = False

UPLOAD_FOLDER = './uploads/'

@ui.page('/')
def main_page():
    def refresh():
        ui.run_javascript('location.reload();')

    async def clear_input_box():
        input_box.value = ''
        input_box.update()

    async def load_spinner():
        global loader
        with input_box:
            loader = ui.spinner(type='dots', color="red", size="2em", thickness="10").style('margin-top: 5px; align-self: center; margin-right: 10px')

    async def remove_loader():
        loader.remove(loader)

    async def scrolldown():
        ui.run_javascript('document.getElementById("chat_box").scrollTop = document.getElementById("chat_box").scrollHeight;')
        

    async def print_user_msg(msg):
        with chat_box:
            ui.chat_message(text=msg, name='You').style('font-family: Courier; font-size: 12.5px; color: black; text-align: right; align-self: flex-end; border-radius: 10px; padding: 10px;').props('bg-color=blue-3')
    
    async def print_rbt_msg(msg):
        with chat_box:
            ui.chat_message(name='Model', text=msg).style('font-family: Courier; color: black; font-size: 12.5px; text-align: left; align-self: flex-start; border-radius: 10px; padding: 10px;').props('bg-color=grey-3')

    async def send_message() -> None:
        global user_message
        user_message = input_box.value
        await clear_input_box()
        await asyncio.sleep(0.02)
        if user_message.strip():
            await print_user_msg(user_message)
            await asyncio.sleep(0.02)
            await scrolldown()
            await asyncio.sleep(0.02)
            await load_spinner()
            await asyncio.sleep(0.02)
            response = await generate_response1(user_message)
            if (switchrag):
                response = ""
                response = await generate_response2(user_message)
            await asyncio.sleep(0.02)
            try: 
                await asyncio.sleep(0.02)
                await print_rbt_msg(response)
                await asyncio.sleep(0.02)
                #await print(response)
            except Exception as e:
                await asyncio.sleep(0.02)
                #print("error")
                await asyncio.sleep(0.02)
            await asyncio.sleep(0.02)
            await remove_loader()
            await asyncio.sleep(0.02)
            await scrolldown()
            await asyncio.sleep(0.02)
        else:
            await print_rbt_msg("Sorry, I didn't quite understand ;(")
            await asyncio.sleep(0.02)
            await scrolldown()

    async def generate_response1(user_message):
        output = rag_pipeline.invoke({"query": user_message})
        return output
    
    async def generate_response2(user_message):
        output = rag_pipeline.invoke({"query": user_message})
        result = output['result']
        return result

    def upload_file(e: events.UploadEventArguments):  
        #print("event")
        e.name
        upload_dir = UPLOAD_FOLDER
        os.makedirs(upload_dir, exist_ok=True)
        filename = e.name
        file_path = os.path.join(upload_dir, filename)
        print(file_path)

        with open(file_path, 'wb') as f:
            f.write(e.content.read())
        loader = TextLoader(file_path)

        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        all_splits = text_splitter.split_documents(data)

        vectorstore = Chroma.from_documents(documents=all_splits, embedding=embed_model)
        global rag_pipeline
        rag_pipeline = RetrievalQA.from_chain_type(
            llm=llm, chain_type='stuff',
            retriever=vectorstore.as_retriever()
        )
        #print("rag init finish")
        global switchrag
        switchrag = True

    ui.query('body').style()
    with ui.row().style('position: fixed;top: 0; left: 0; height: 100%; width: 110px; background: #fff; box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1)'):
        with ui.tabs().props('vertical').classes('w-full') as tabs:
            chat = ui.tab('c', label='Chat', icon="chat").style()
            upload = ui.tab('u', label='Upload', icon='upload').style()
    with ui.tab_panels(tabs, value=chat).props('vertical').classes('w-full h-full'):
                with ui.tab_panel(chat):
                    ui.query('body').style('background-color: #f0f4f8; margin-left:120px; width: calc(100% - 130px); align-items: center')
                    with ui.column().style('margin-right: 10px; margin-left: 10px; height: 100%; align-items: center'):
                            global input_box, chat_box, refresh_button
                            with ui.column().style('width: 100%; margin-top: 10px; align-items: center'):
                                chat_box = ui.column().style('width: 100%; height: 400px; overflow-y: auto; border: 2px solid #ccc; padding: 10px; background-color: #fff; border-radius: 15px; display: flex; flex-direction: column; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);').props('id=chat_box')
                                with chat_box:
                                    ui.chat_message(name='Model', sent="True", text="Hello! I am Llama!.How can I help?").style('width: calc(100% - 20px) ;font-family: Courier; font-size: 12.5px; color: black; text-align: left; align-self: flex-start; border-radius: 10px; padding: 10px;').props('bg-color=grey-3')
                                    
                                with ui.row().style('align-items: center; justify-content: center; width: 100%;'):
                                    input_box = ui.input(placeholder='Type your message here...').props('rounded outlined input-class=mx-3').style('width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 15px;').on('keydown.enter', send_message)
                                    refresh_button = ui.button('REFRESH', on_click=refresh).props('rounded outlined input-class=mx-3').style('width: 100%; height: 1%; font-size: 12px ; color: white; border: none; border-radius: 15px; padding: 10px; cursor: pointer;')
                with ui.tab_panel(upload):
                    with ui.column().style('height: 100%; align-items: center'):
                        ui.upload(on_upload=upload_file).style('margin-left: 30px')
                

app.native.window_args['resizable'] = False
app.native.start_args['debug'] = True
app.native.settings['ALLOW_DOWNLOADS'] = True
ui.run(title='Chat with LLAMA 2', native=True, window_size=(600, 700), fullscreen=False)
