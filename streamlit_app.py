from st_weaviate_connection import WeaviateConnection
import streamlit as st
import time
import sys
import os
from streamlit_modal import Modal
from dotenv import load_dotenv
# Set the sidebar background color to dark
st.markdown(
    """
    <style>
    [data-testid="stSidebarUserContent"] button[data-testid="baseButton-secondary"] {
                background: none;
                width: 100%;
                border: 0 !important;
                justify-content: start;
            }
    p, h1, h2, h3, h4, h5, h6, div, body {
            color: #fff !important;
        }
        h1, h2, h3, h4, h5, h6 {
            padding-top: 0;
        }
    [data-testid="stSidebar"], .stApp[data-testid="stApp"] {
        background: #09241f;
        color: #fff;
    }
    [data-testid="stSidebarUserContent"] label[data-baseweb="radio"] > div:last-child p,
    [data-testid="stSidebarUserContent"] h1, [data-testid="stSidebar"] + section.main h1 {
        color: #fff;
    }
    [data-testid="stSidebarUserContent"] label[data-baseweb="radio"] > div:first-child {
        display: none;
    }
    [data-testid="stSidebarUserContent"] label[data-baseweb="radio"] > div:last-child {
        padding: 10px;
        width: 100%;
        border-radius: 10px;
    }
    [data-testid="stAppViewBlockContainer"] {
        max-width: 1000px;
        padding-inline: 40px;
    }
    [data-testid="stSidebar"] + section.main h1 {
        padding-top: 0;
    }
    [data-testid="stSidebarUserContent"] label[data-baseweb="radio"] {
        width: 100%;
        margin-right: 0;
    }
    [data-testid="stSidebarUserContent"] [data-testid="stWidgetLabel"] {
        display: none;
    }
    [data-testid="stSidebar"] + section.main {
        background: #0f352e;
    }
    header[data-testid="stHeader"] {
        background: #09241f;
    }
    [data-testid="baseButton-headerNoPadding"] {
        background-color: rgb(255 255 255 / 85%) !important;
        color: #000 !important
    }
    [data-testid="baseButton-headerNoPadding"]:hover {
        background-color: rgb(255 255 255 / 100%) !important;
    }
    [data-testid="stSidebarUserContent"] label[data-baseweb="radio"] [tabindex="0"] + div:last-child, 
    [data-testid="stSidebarUserContent"] label[data-baseweb="radio"] [tabindex="-1"] + div:last-child:hover {
        background: #307f71;
    }
    [data-testid="stSidebarUserContent"] [role="radiogroup"] {
        gap: 5px;
    }
    hr {
        background-color: #ffffff40;
    }
    [key="data-modal"] [data-testid="stVerticalBlock"] {
        margin: 0 !important;
        border-radius: 20px !important;
    }
    [data-testid="stHeadingWithActionElements"] h2 {
        padding-bottom: 0 !important;
    }
    div[data-modal-container='true'][key='data-modal'] [data-testid="stMarkdownContainer"] hr {
        margin-block: 10px 30px;
    }
        [key='data-modal'] .stRadio > div {
            display: flex;
            justify-content: space-around;
        }
        [key="data-modal"] [data-testid="baseButton-secondary"] {
            background-color: #307f71 !important;
            color: white;
            width: auto !important;
            padding: 10px 30px;
            border-radius: 10px;
            margin-left: auto;
            display: block;
            justify-content: center;
            cursor: pointer;
            transition: background-color 0.3s ease;
            flex-grow: 1;
            text-align: center;
            border: 0;
        }
        .element-container.st-emotion-cache-shybcl button.st-emotion-cache-15hul6a.ef3psqc13:hover {
            background-color: #0f352e;
        }
        .element-container.st-emotion-cache-oertxx.e1f1d6gn4 button.st-emotion-cache-15hul6a.ef3psqc13 {
            background: #fff0;
            width: 40px;
            display: block;
            margin-left: auto;
        }
        .element-container.st-emotion-cache-oertxx.e1f1d6gn4 button.st-emotion-cache-15hul6a.ef3psqc13:hover {
            background: #307f71;
            border-color: #307f71;
        }
        [key='data-modal'] .stRadio > div > label { width: 100%; }
        [key='data-modal'] .stRadio > div > label > div:last-child {
            background-color: #0f352e;
            color: white;
            padding: 20px 20px;
            border-radius: 10px;
            justify-content: center;
            cursor: pointer;
            transition: background-color 0.3s ease;
            flex-grow: 1;
            text-align: center;
            margin: 5px;
        }
        [key='data-modal'] .stRadio > div > label > div:last-child:hover,
         [key='data-modal'] .stRadio > div > label > input[tabindex="0"] + div:last-child {
            background-color: #307f71;
        }
        [key='data-modal'] .stRadio > div > label > div:first-child {
            display: none;
        }
        [key='data-modal'] .stRadio > div > label[aria-checked="true"] {
            background-color: #2196F3;
        }
        div[data-modal-container='true'][key='data-modal'] > div:first-child > div:first-child {
            background: #09241f !important;
        }
        [key='data-modal'] .stRadio > div[role="radiogroup"] {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            margin-inline: -5px;
        }
        .footer-hr {
            margin-block: 20px 20px !important;
        }
        [key="data-modal"] [data-testid="column"] [data-test-scroll-behavior="normal"] [data-testid="baseButton-secondary"] {
            width: 45px;
            padding-inline: 14px;
        }
        [data-testid="stExpander"] summary {
                background: #09241f;
                border-radius: 10px;
                align-items: center;
                outline: none !important;
            }
            [data-testid="stExpander"] summary:hover {
                color: #fff;
            }
            [data-testid="stExpander"] summary:hover svg {
                fill: #fff;
            }
            [data-testid="stExpander"] summary p {
                font-size: 18px;
            }
            [data-testid="stExpanderDetails"] {
                padding-top: 20px;
                margin-top: -10px;
                background: #09241f;
                border-radius: 0px 0 10px 10px;
            }
            .flex-center {
                display: flex;
                gap: 15px;
                align-items: center;
            }
            p:last-child {
                margin-bottom:0;
            }
            .m-n10 {
                margin-inline: -10px;
            }
            .col-33 {
                padding-inline: 10px;
                width: 33.33%;
            }
            .flex-wrap {
                display: flex;
                flex-wrap: wrap;
            }
            hr {
                background-color: #ffffff40;
            }
            .card-border {
                padding: 15px;
                text-align: center;
                background: #09241f;
                border-radius: 10px;
                margin-bottom: 20px !important;
            }
            [data-testid="stChatInputSubmitButton"] {
                color: #307f71 !important;
            }
            [data-testid="stChatInput"] {
                background: none;
            }
            [data-testid="stChatInput"] [data-baseweb="textarea"] {
                border-color: #307f71;
            }
            [data-testid="stChatInput"] [data-baseweb="textarea"] textarea {
                color: #fff !important;
            }
            .ai-default-text {
                margin-bottom: 25px;
            }
            .user-command {
                justify-content: end;
                flex-direction: row-reverse;
                padding: 10px;
                margin-bottom: 30px;
                background: #09241f;
                border-radius: 10px;
            }
            .ai-generated {
                padding-bottom: 30px;
            }
            [data-testid="stChatMessage"] {
                background: #09241f;
                border-radius: 10px;
            }
            [data-testid="stBottom"] > div {
                background: #0f352e;
            }
            [data-testid="stBottom"] [data-testid="stBottomBlockContainer"] {
                max-width: 1000px;
                padding-inline: 40px;
            }
            .ai-default-text > div {
                display: flex;
                width: 3rem;
                height: 3rem;
                flex-shrink: 0;
                border-radius: 0.5rem;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                background-color: rgb(255, 189, 69);
            }
            .ai-default-text > div > svg {
                width: 2rem;
                height: 2rem;
            }
            [data-testid="stTooltipIcon"] > div, [data-testid="stTooltipIcon"] > div > button {
                width: 100% !important;
            }
            [data-testid="stTooltipIcon"] > div > button {
                background: #09241f;
                border-radius: 10px;
            }
            [data-testid="stTooltipIcon"] > div > button {
                background: #09241f !important;
                border-radius: 10px !important;
                padding: 25px 10px;
                border: 0 !important;
            }
            
            [data-testid="stSidebarUserContent"] button[data-testid="baseButton-secondary"]:hover {
                background: #307f71;
            }
            div[data-modal-container='true'][key='data-modal'] {
                height: 100%;
                top: 0;
                display: flex;
                align-items: center;
                justify-content: center;
            }
    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()

# Constants
ENV_VARS = ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_KEY"]
NUM_IMAGES_PER_ROW = 3

# Functions
def get_env_vars(env_vars: list) -> dict:
    """Retrieve environment variables
    @parameter env_vars : list - List containing keys of environment variables
    @returns dict - A dictionary of environment variables
    """

    env_vars = {}
    for var in ENV_VARS:
        value = os.environ.get(var, "")
        if value == "":
            st.error(f"{var} not set", icon="🚨")
            sys.exit(f"{var} not set")
        env_vars[var] = value

    return env_vars


def display_chat_messages() -> None:
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for i in range(0, len(message["images"]), NUM_IMAGES_PER_ROW):
                    cols = st.columns(NUM_IMAGES_PER_ROW)
                    for j in range(NUM_IMAGES_PER_ROW):
                        if i + j < len(message["images"]):
                            cols[j].image(message["images"][i + j], width=200)


# Environment variables
env_vars = get_env_vars(ENV_VARS)
url = env_vars["WEAVIATE_URL"]
api_key = env_vars["WEAVIATE_API_KEY"]
openai_key = os.getenv("OPENAI_KEY")

# Check keys
if url == "" or api_key == "" or openai_key == "":
    st.error(f"Environment variables not set", icon="🚨")
    sys.exit("Environment variables not set")

# Title
st.title("🔮 Magic Chat")

# Connection to Weaviate thorugh Connector
conn = st.connection(
    "weaviate",
    type=WeaviateConnection,
    url=os.getenv("WEAVIATE_URL"),
    api_key=os.getenv("WEAVIATE_API_KEY"),
    additional_headers={"X-OpenAI-Api-Key": openai_key},
)

with st.sidebar:
    st.title("Streamlit Chat")
    # st.subheader("The Generative Gathering")
    st.markdown(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""
    )
    # st.header("Settings")
    # st.success("Connected to Weaviate client", icon="💚")
    # Navigation
    menu = st.radio(
        "Go to",
        [
            "🏠 Home",
            "📄 FAQ",
            "📑 Contact",
            "📊 About Us",
            "📊 Signin"
        ]
    )
    # Show the "Open" button in the sidebar directly
    modal = Modal(
        "Lorem Ipsum", 
        key="data-modal",
        
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )
    open_modal = st.sidebar.button("📊 Pop Up")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            # Streamlit radio buttons as buttons
            option = st.radio("Select an Template:", ["Image + Text", "Text + Data Table", "Data Table + Image"], index=0)
            st.markdown ("""<hr class="footer-hr">""", unsafe_allow_html=True)
            st.button("Generate", key="hidden-generate-button")
            # Display selected option
            # st.write(f"Selected: {option}")

    # Map menu items to functions
    pages = {
        "🏠 Home": "home",
        "📄 FAQ": "faq",
        "📑 Contact": "contact",
        "📊 About Us": "about",
        "📊 Signin": "signin"
    }
# Search Mode descriptions

bm25_gql = """
        {{
            Get {{
                MagicChat_Card(limit: {limit_card}, bm25: {{ query: "{input}" }}) 
                {{
                    name
                    card_id
                    img
                    mana_cost
                    type
                    mana_produced
                    power
                    toughness
                    color
                    keyword
                    set
                    rarity
                    description
                    _additional {{
                        id
                        distance
                        vector
                    }}
                }}
            }}
        }}"""

vector_gql = """
        {{
            Get {{
                MagicChat_Card(limit: {limit_card}, nearText: {{ concepts: ["{input}"] }}) 
                {{
                    name
                    card_id
                    img
                    mana_cost
                    type
                    mana_produced
                    power
                    toughness
                    color
                    keyword
                    set
                    rarity
                    description
                    _additional {{
                        id
                        distance
                        vector
                    }}
                }}
            }}
        }}"""

hybrid_gql = """
        {{
            Get {{
                MagicChat_Card(limit: {limit_card}, hybrid: {{ query: "{input}" alpha:0.5 }}) 
                {{
                    name
                    card_id
                    img
                    mana_cost
                    type
                    mana_produced
                    power
                    toughness
                    color
                    keyword
                    set
                    rarity
                    description
                    _additional {{
                        id
                        distance
                        vector
                    }}
                }}
            }}
        }}"""

generative_gql = """
        {{
            Get {{
                MagicChat_Card(limit: {limit_card}, nearText: {{ concepts: ["{input}"] }})
                {{
                    name
                    card_id
                    img
                    mana_cost
                    type
                    mana_produced
                    power
                    toughness
                    color
                    keyword
                    set
                    rarity
                    description
                    _additional {{
                        generate(
                            groupedResult: {{
                                task: "Based on the Magic The Gathering Cards, which one would you recommend and why. Use the context of the user query: {input}"
                            }}
                        ) {{
                        groupedResult
                        error
                        }}
                        id
                        distance
                        vector
                    }}
                }}
            }}
        }}"""

mode_descriptions = {
    "BM25": [
        "BM25 is a method used by search engines to rank documents based on their relevance to a given query, factoring in both the frequency of keywords and the length of the document.",
        bm25_gql,
        30,
    ],
    "Vector": [
        "Vector search is a method used by search engines to find and rank results based on their similarity to your search query. Instead of just matching keywords, it understands the context and meaning behind your search, offering more relevant and nuanced results.",
        vector_gql,
        15,
    ],
    "Hybrid": [
        "Hybrid search combines vector and BM25 methods to offer better search results. It leverages the precision of BM25's keyword-based ranking with vector search's ability to understand context and semantic meaning. Providing results that are both directly relevant to the query and contextually related.",
        hybrid_gql,
        15,
    ],
    "Generative": [
        "Generative search is an advanced method that combines information retrieval with AI language models. After finding relevant documents using search techniques like vector and BM25, the found information is used as an input to a language model, which generates further contextually related information.",
        generative_gql,
        9,
    ],
}

# Information
with st.expander("Built with Weaviate for the Streamlit Hackathon 2023"):
    st.subheader("Streamlit Hackathon 2023")
    st.markdown(
        """
        This project is a submission for the [Streamlit Connections Hackathon 2023](https://discuss.streamlit.io/t/connections-hackathon/47574).
        It delivers a Streamlit connector for the open-source vector database, [Weaviate](https://weaviate.io/). 
        Magic Chat uses the Weaviate connector to search through [Magic The Gathering](https://magic.wizards.com/en) cards with various search options, such as BM25, Semantic Search, Hybrid Search and Generative Search. 
        You can find the submission in this [GitHub repo](https://github.com/weaviate/st-weaviate-connection/tree/main)
        """
    )
    st.subheader("Data")
    st.markdown(
        """The database contains around 27k cards from the [Scryfall API](https://scryfall.com/). We used the following attributes to index the cards:
- Name, Type, Keywords
- Mana cost, Mana produced, Color
- Power, Toughness, Rarity
- Set name and Card description """
    )
    st.subheader("How the demo works")
    st.markdown(
        """The demo offers four search options with defined GraphQL queries, which you can use to search for various Magic cards. 
        You can search for card types such as "Vampires", "Humans", "Wizards", or you can search for abilities, mana color, descriptions, and more.
        If you're interested you can read more about the anatomy of a Magic card in this [documentation from the Magic Academy](https://magic.wizards.com/en/news/feature/anatomy-magic-card-2006-10-21).
"""
    )
    st.markdown(
        """The first is the **BM25 search**, 
        it's a method used by search engines to rank documents based on their relevance to a given query, 
        factoring in both the frequency of keywords and the length of the document. In simple terms, we're conducting keyword matching.
        We can simply pass a query to the `query` parameter ([see docs](https://weaviate.io/developers/weaviate/search/bm25))"""
    )
    st.code(
        """
        {
            Get {
                MagicChat_Card(limit: {card_limit}, bm25: { query: "Vampires with flying ability" }) 
                {
                    ...
                }
            }
        }""",
        language="graphql",
    )
    st.markdown(
        """The second option is **Vector search**, a method used to find and rank results based on their similarity to a given search query. 
        Instead of matching keywords, it understands the context and meaning behind the query, offering relevant and more semantic related results. For example, when we search for "Vampires" we might also get cards like a "Bat" or "Undead" because they are semantically related.
        We use the `nearText` function in which we pass our query to the `concepts` parameter ([see docs](https://weaviate.io/developers/weaviate/api/graphql/search-operators#neartext))"""
    )
    st.code(
        """
        {
            Get {
                MagicChat_Card(limit: {card_limit}, nearText: { concepts: ["Vampires with flying ability"] }) 
                {
                    ...
                }
            }
        }""",
        language="graphql",
    )
    st.markdown(
        """With **Hybrid search** we combine both methods and use a ranking alogrithm to combine their results. 
        It leverages the precision of BM25's keyword-based ranking with vector search's ability to understand context and semantic meaning. 
        We can pass our query to the `query` parameter and set the `alpha` that determines the weighting for each search ([see docs](https://weaviate.io/developers/weaviate/api/graphql/search-operators#hybrid))"""
    )
    st.code(
        """
        {
            Get {
                MagicChat_Card(limit: {card_limit}, hybrid: { query: "Vampires with flying ability" alpha:0.5 }) 
                {
                    ...
                }
            }
        }""",
        language="graphql",
    )
    st.markdown(
        """The last option is **Generative search** which is an advanced method that combines information retrieval with AI language models. 
        In our configuration, it retrieves results with a **Vector search** and passes them to a `gpt-3.5-turbo model` to determine the best Magic card based on the user query. For this, we rely on its knowledge about Magic The Gathering, but this model could be easily exchanged. 
        We use the `generate` module and `groupedResult` task which uses the data of the result as context for the given prompt and query. ([see docs](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai))"""
    )
    st.code(
        """
        {
            Get {
                MagicChat_Card(limit: {card_limit}, nearText: { concepts: ["Vampires with flying ability"] }) 
                {
                    _additional {
                        generate(
                            groupedResult: {
                                task: "Based on the Magic The Gathering Cards, which one would you recommend and why. Use the context of the user query: {input}"
                            }
                        ) {
                        groupedResult
                        error
                        }
                    }
                }
            }
        }""",
        language="graphql",
    )
    st.subheader("Future ideas")
    st.markdown(
        """Magic The Gathering is a very complex and exciting game, and there were many ideas we got when building this demo. 
        We thought about an actual deck builder interface, where you could search for similar cards or predict the next card based on your already established deck. 
        Or even a meta-finder that simulates battles between two sets of cards, trying out different combinations and more. With Magic, the possibilities for an exciting demo are endless, and we hope to enhance the demo further!
"""
    )

col1, col2, col3 = st.columns([0.2, 0.5, 0.2])

col2.image("./img/anim.gif")

# User Configuration Sidebar
with st.sidebar:
    mode = st.radio(
        "Search Mode", options=["BM25", "Vector", "Hybrid", "Generative"], index=3
    )
    limit = st.slider(
        label="Number of cards",
        min_value=1,
        max_value=mode_descriptions[mode][2],
        value=6,
    )
    st.info(mode_descriptions[mode][0])

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False

# Display chat messages from history on app rerun
display_chat_messages()

# Greet user
if not st.session_state.greetings:
    with st.chat_message("assistant"):
        intro = "Hey! I am Magic Chat, your assistant for finding the best Magic The Gathering cards to build your dream deck. Let's get started!"
        st.markdown(intro)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True

# Example prompts
example_prompts = [
    "You gain life and enemy loses life",
    "Vampires cards with flying ability",
    "Blue and green colored sorcery cards",
    "White card with protection from black",
    "The famous 'Black Lotus' card",
    "Wizard card with Vigiliance ability",
]

example_prompts_help = [
    "Look for a specific card effect",
    "Search for card type: 'Vampires', card color: 'black', and ability: 'flying'",
    "Color cards and card type",
    "Specifc card effect to another mana color",
    "Search for card names",
    "Search for card types with specific abilities",
]

button_cols = st.columns(3)
button_cols_2 = st.columns(3)

button_pressed = ""

if button_cols[0].button(example_prompts[0], help=example_prompts_help[0]):
    button_pressed = example_prompts[0]
elif button_cols[1].button(example_prompts[1], help=example_prompts_help[1]):
    button_pressed = example_prompts[1]
elif button_cols[2].button(example_prompts[2], help=example_prompts_help[2]):
    button_pressed = example_prompts[2]

elif button_cols_2[0].button(example_prompts[3], help=example_prompts_help[3]):
    button_pressed = example_prompts[3]
elif button_cols_2[1].button(example_prompts[4], help=example_prompts_help[4]):
    button_pressed = example_prompts[4]
elif button_cols_2[2].button(example_prompts[5], help=example_prompts_help[5]):
    button_pressed = example_prompts[5]


if prompt := (st.chat_input("What cards are you looking for?")):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt = prompt.replace('"', "").replace("'", "")

    images = []
    if prompt != "":
        query = prompt.strip().lower()
        gql = mode_descriptions[mode][1].format(input=query, limit_card=limit)

        df = conn.query(gql, ttl=None)

        response = ""
        with st.chat_message("assistant"):
            for index, row in df.iterrows():
                if index == 0:
                    if "_additional.generate.groupedResult" in row:
                        first_response = row["_additional.generate.groupedResult"]
                    else:
                        first_response = f"Here are the results from the {mode} search:"

                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in first_response.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    response += full_response + " "

                # Create a new row of columns for every NUM_IMAGES_PER_ROW images
                if index % NUM_IMAGES_PER_ROW == 0:
                    cols = st.columns(NUM_IMAGES_PER_ROW)

                if row["img"]:
                    # Display image in the column
                    cols[index % NUM_IMAGES_PER_ROW].image(row["img"], width=200)
                    images.append(row["img"])
                else:
                    cols[index % NUM_IMAGES_PER_ROW].write(
                        f"No Image Available for: {row['type']}"
                    )

            st.session_state.messages.append(
                {"role": "assistant", "content": response, "images": images}
            )
            st.experimental_rerun()
