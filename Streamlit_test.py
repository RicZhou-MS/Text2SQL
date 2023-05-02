import streamlit as st
import streamlit.components.v1 as components
import streamlit_scrollable_textbox as stx
import numpy as np
import time
from streamlit_chat import message as st_message
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

@st.cache_resource
def get_models():
    # it may be necessary for other frameworks to cache the model
    model_name = "facebook/blenderbot-400M-distill"
    # tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    # model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    return  # tokenizer, model

if "GlobalContext" not in st.session_state:
    st.session_state["GlobalContext"] = GlobalContext()

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Hello Text2SQL")

message_placeholder = st.container()
message_placeholder.write("this is first message")

placeholder = st.empty()

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def clear_text():
    st.session_state["text"] = "Hellow world"
    message_placeholder.write(f"this is {time.time} message")

str = st.text_area('Enter text', height=275, disabled=st.session_state.disabled, key="text",on_change=clear_text)

if st.button('display'):
    # if st.session_state.disabled:
    #     st.session_state.disabled = False
    # else:
    #     st.session_state.disabled = True
    st.write(st.session_state.GlobalContext.DB_SERVER)
    


long_text = "Input here"
stx.scrollableTextbox(long_text, height=300)

components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div id="accordion">
      <div class="card">
        <div class="card-header" id="headingOne">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
            Collapsible Group Item #1
            </button>
          </h5>
        </div>
        <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #1 content
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header" id="headingTwo">
          <h5 class="mb-0">
            <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
            Collapsible Group Item #2
            </button>
          </h5>
        </div>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #2 content
          </div>
        </div>
      </div>
    </div>
    """,
    height=200,
    scrolling=True,
)


def generate_answer():
    user_message = st.session_state.input_text
    message_bot = """How are you
    I am a bot""".replace("\n", "\\n")

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": message_bot, "is_user": False})


# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

with st.container():
    for i, chat in enumerate(st.session_state.history):
        st_message(**chat, key=str(i))  # unpacking

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))


st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})
st.area_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write("""
             The chart above shows some numbers I picked for you.
             I rolled actual dice for these, so they're * guaranteed * to
             be random.
             """)
    st.image("https://static.streamlit.io/examples/dice.jpg")


# # Replace the placeholder with some text:
# placeholder.text("Hello")
# time.sleep(1)
# # Replace the text with a chart:
# placeholder.line_chart({"data": [1, 5, 2, 6]})
# time.sleep(1)
# # Replace the chart with several elements:
# for seconds in range(5):
#   placeholder.text_input(f"⏳ {seconds} seconds have passed")
#   time.sleep(1)

with placeholder.container():
  with st.spinner('Wait for it...'):
    if st.session_state.disabled:
        st.session_state.disabled = False
    else:
        st.session_state.disabled = True
    time.sleep(1)
  st.success('Done!')




# with placeholder.container():
#     for seconds in range(5):
#       st.write(f"⏳ {seconds} seconds have passed")
#       time.sleep(1)
#     st.write("✔️ 1 minute over!")
time.sleep(1)
# Clear all those elements:
placeholder.empty()