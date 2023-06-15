import streamlit as st
import pyodbc
import pandas as pd
import openai
from GlobalClasses import *

st.set_page_config(
    page_title="Azure OpenAI Chat2SQL Demo",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.demo.com/help',
        'Report a bug': "https://www.demo.com/bug",
        'About': "# This is an Azure OpenAI Chat2SQL Demo!"
    }
)

# @st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + GlobalContext.DB_SERVER
        + ";DATABASE="
        + GlobalContext.DB_NAME
        + ";UID="
        + GlobalContext.DB_USER
        + ";PWD="
        + GlobalContext.DB_USER_PASS
    )

def run_query(query):
    db_conn = init_connection()
    df = pd.read_sql(query, db_conn)
    db_conn.close()
    return df


# read DBSchema.txt
def Get_system_message_from_file():
    with open("DBSchema.txt", "r") as f:
        return f.read()

def Ask_Azure_OpenAI():
    openai.api_type = "azure"
    openai.api_base = GlobalContext.OPENAI_BASE
    openai.api_version = "2023-03-15-preview"
    openai.api_key = GlobalContext.OPENAI_API_KEY

    response = openai.ChatCompletion.create(
    engine=st.session_state.gpt_engine,
    messages = Get_ChatCompletion_message(),
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)
    return response


def Add_Chat_History(role,message):
    chat_history = None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    chat_history = st.session_state.chat_history
    chat_history.append({"role": role, "content": message})
    st.session_state["chat_history"] = chat_history

def Get_Chat_History():
    if "chat_history" not in st.session_state:
        return []
    return st.session_state.chat_history

def Display_Chat_History(container_element):
    with container_element:
        container_element.empty()
        for item in Get_Chat_History():
            if item["role"] == "user":
                container_element.success(item["content"])
            elif item["role"] == "assistant":
                with container_element.expander("AI return", expanded=False):
                    st.write(item["content"])

def Update_ChatCompletion_message():
    message=[{"role": "system", "content": st.session_state["sidebar_system_msg"].replace("\n", "\\n")}]
    if st.session_state["few_shot_user_msg1"] :
        message.append({"role": "user", "content": st.session_state["few_shot_user_msg1"].replace("\n", "\\n")})
    if st.session_state["few_shot_ai_msg1"] :
        message.append({"role": "assistant", "content": st.session_state["few_shot_ai_msg1"].replace("\n", "\\n")})
    if st.session_state["few_shot_user_msg2"] :
        message.append({"role": "user", "content": st.session_state["few_shot_user_msg2"].replace("\n", "\\n")})
    if st.session_state["few_shot_ai_msg2"] :
        message.append({"role": "assistant", "content": st.session_state["few_shot_ai_msg2"].replace("\n", "\\n")})
    for item in Get_Chat_History():
        message.append(item)
    st.session_state["prompt_message"] = message

def Get_ChatCompletion_message():
    if "prompt_message" not in st.session_state:
        Update_ChatCompletion_message()
    return st.session_state["prompt_message"]

def Clear_Chat_History():
    st.session_state["chat_history"] = []
    Update_ChatCompletion_message()

def Run_SQL():
    if (not st.session_state.SQL_Statement_Generated):
        return
    with container_SQL_Result.container():
        with st.spinner("Running SQL..."):
            st.session_state["SQL_Result_df"] = run_query(st.session_state.SQL_Statement_Generated)
    # container_SQL_Result.write(st.session_state.SQL_Result_df)
    

def Show_Diagram():
    if (st.session_state["show_chart"] ):
        st.session_state["show_chart"] = False
    else:
        st.session_state["show_chart"] = True
    return

def Process_User_Input():
    if (not st.session_state.user_input):
        return
    st.session_state["latest_user_input"] = st.session_state.user_input
    Add_Chat_History("user", st.session_state.latest_user_input)
    st.session_state.user_input = "" # clear user input
    st.session_state["SQL_Statement_Generated"] = "" # clear SQL statement
    st.session_state["SQL_Result_df"] = None # clear SQL result
    st.session_state["show_chart"] = False # clear chart
    container_Chat.success(st.session_state.latest_user_input)
    Update_ChatCompletion_message()
    st.session_state.user_input_disabled = True
    with wait_container.container():
        with st.spinner('Azure...'):
            # perform OpenAI chatgpt query
            response = Ask_Azure_OpenAI()
            st.session_state["gpt_response"] = response
            st.session_state["latest_ai_response"] = response.choices[0].message.content
            Add_Chat_History("assistant", st.session_state["latest_ai_response"])
            with container_Chat.expander("AI return", expanded=True):
                st.code(st.session_state["latest_ai_response"], language='sql')
                st.write(st.session_state["gpt_response"].usage)
            st.session_state["SQL_Statement_Generated"] = st.session_state["latest_ai_response"].replace("\\n", "\n") # update SQL statement
            st.session_state.user_input_disabled = False
    return

def Initialize_SideBar():
    if "sidebar_system_msg" not in st.session_state:
        table_definition = Get_system_message_from_file()
        st.session_state["sidebar_system_msg"] = GlobalContext.System_Prompt.format(tableDefinition=table_definition)
    if "few_shot_user_msg1" not in st.session_state:
        st.session_state["few_shot_user_msg1"] = GlobalContext.few_shot_user_msg1
    if "few_shot_ai_msg1" not in st.session_state:
        st.session_state["few_shot_ai_msg1"] = GlobalContext.few_shot_ai_msg1
    if "few_shot_user_msg2" not in st.session_state:
        st.session_state["few_shot_user_msg2"] = GlobalContext.few_shot_user_msg2
    if "few_shot_ai_msg2" not in st.session_state:
        st.session_state["few_shot_ai_msg2"] = GlobalContext.few_shot_ai_msg2
    # Using "with" notation
    with st.sidebar:
        st.selectbox('ChatGPT engine', ['gpt-4','gpt-4-32k', 'gpt-35-turbo'], key='gpt_engine')
        st.text_area('System message', height=175, key="sidebar_system_msg")
    # Using object notation
    st.sidebar.text_area('few-shot user message', height=30, key="few_shot_user_msg1")
    st.sidebar.text_area('few-shot AI messsage', height=100, key="few_shot_ai_msg1")
    st.sidebar.text_area('few-shot user message', height=30, key="few_shot_user_msg2")
    st.sidebar.text_area('few-shot AI messsage', height=100, key="few_shot_ai_msg2")


def Initialize_MainPage():

    global col_Chat, col_SQL, container_Chat, wait_container, container_SQL, container_SQL_Result, container_Diagram
 
    st.markdown('<h2 style="text-align: center;background-color:SlateBlue;color:White">Azure OpenAI Chat to SQL</h2><p/>', unsafe_allow_html=True)
 
    col_Chat, col_SQL = st.columns([2,3],gap="medium")

    col_Chat.markdown("### :speech_balloon: Chat")
    col_Chat.divider()
    col_Chat.button("Clear Chat History", key="clear_chat_history", on_click=Clear_Chat_History)
    container_Chat = col_Chat.container()
    Display_Chat_History(container_Chat)
    wait_container = col_Chat.empty()
    if "user_input_disabled" not in st.session_state:
        st.session_state["user_input_disabled"] = False
    col_Chat.text_input("User Input", key="user_input",disabled=st.session_state["user_input_disabled"],on_change=Process_User_Input)
    with col_Chat.expander("Prompt", expanded=False):
        st.write(Get_ChatCompletion_message())

    col_SQL.markdown("### :sunglasses: :blue[SQL] ")
    col_SQL.divider()
    container_SQL = col_SQL.empty()
    if "SQL_Statement_Generated" not in st.session_state:
        st.session_state["SQL_Statement_Generated"] = ""
    container_SQL.text_area('SQL Statement Generated', height=30, key="SQL_Statement_Generated")

    col_SQL.divider()
    col_SQL.button("Run SQL", key="run_sql", on_click=Run_SQL)
    container_SQL_Result = col_SQL.empty()
    if "SQL_Result_df" in st.session_state and st.session_state.SQL_Result_df is not None:
        df = st.session_state.SQL_Result_df
        container_SQL_Result.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        #container_SQL_Result.dataframe(st.session_state.SQL_Result_df)

    col_SQL.divider()
    if "chart_type" not in st.session_state:
        st.session_state["chart_type"] = "Bar Chart"
    col_SQL.radio("Chart Type", ("Bar Chart", "Area Chart", "Line Chart"), key="chart_type",horizontal=True)
    col_SQL.button("Diagram", key="show_diagram", on_click=Show_Diagram)
    container_Diagram = col_SQL.empty()
    if "show_chart" in st.session_state and st.session_state["show_chart"]:
        if "SQL_Result_df" in st.session_state and st.session_state.SQL_Result_df is not None:
            with container_Diagram:
                if st.session_state.chart_type == "Bar Chart":
                    #plt.figure()
                    #st.image(st.session_state.SQL_Result_df.plot.bar())
                    st.bar_chart(st.session_state.SQL_Result_df)
                elif st.session_state.chart_type == "Area Chart":
                    st.area_chart(st.session_state.SQL_Result_df)
                elif st.session_state.chart_type == "Line Chart":
                    st.line_chart(st.session_state.SQL_Result_df)

    #container_Diagram.success("Diagram")
    
GlobalContext()  # initialize global context

col_Chat = None
col_SQL = None
container_Chat = None
wait_container = None
container_SQL = None
container_SQL_Result = None
container_Diagram = None

Initialize_SideBar()
Initialize_MainPage()

#if st.button('display'):
    #st.write(st.session_state["gpt_response"])
    #st.write(Get_Chat_History())
    # st.write(Get_ChatCompletion_message())
    # st.write(st.session_state.sidebar_system_msg)
    # st.write(st.session_state.few_shot_user_msg1)
    # st.write(st.session_state.few_shot_ai_msg1)
    # st.write(not st.session_state.few_shot_user_msg2)


