from st_weaviate_connection import WeaviateConnection
import streamlit as st
import time
import sys
import os
from streamlit_modal import Modal
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import requests
from urllib.parse import urlparse, parse_qs

# Load external CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call the function to load CSS
load_css()
# Get query parameters from the URL
query_params = st.query_params
user_email_list = query_params.get("user_email", [])
user_email = user_email_list if user_email_list else None
st.markdown(
    
    """
    <style>
     
    # MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
       .header {
        text-align: center;
        color: darkblue;
        font-size: 36px;
        margin-bottom: 20px;
    }
   .header {
    background-color: #09241f;
    border-bottom: 2px solid #333;
    padding: 10px;
    text-align: center;
    position: fixed;
    top: 0;
    width: 100%;
    left: 0;
}
    .header h1 {
        color: #333;
        font-family: 'Arial', sans-serif;
        font-size: 36px;
        margin: 0;
    }
   
    </style>
     
    """,
    
    unsafe_allow_html=True
    
    
)
# If user is authenticated, display their email
if user_email:
    st.markdown(
        f"""
        <div class="header">
            <button class="sign-btn" disabled>Signed in as: {user_email}</button>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="header">
            <a class="sign-btn" href="https://streamlit.devexhub.com/" target="_blank" onclick="window.open(this.href, '_blank'); window.close(); return false;">Sign in with Google</a>
        </div>
        """,
        unsafe_allow_html=True)

# Define your functions or content for each page
def render_home_page():
    # Title
    st.title("🔮 Magic Chat")
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


    if prompt := (st.chat_input("What cards are you looking for?") or button_pressed):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        prompt = prompt.replace('"', "").replace("'", "")

        images = []
        if prompt != "":
            query = prompt.strip().lower()
           

            df = conn.query(query,ttl=None)

            response = ""
            with st.chat_message("assistant"):
                for index, row in df.iterrows():
                    if index == 0:
                        
                        first_response = row["_additional.generate.groupedResult"]
                      
                           

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

def render_faq_page():
    st.write=st.markdown ("""<h1><svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="35" height="35" x="0" y="0" viewBox="0 0 64 64" style="enable-background:new 0 0 512 512;margin-right:5px;" xml:space="preserve" class=""><g><path d="M59.11 48.992c8.408-13.378 5.979-31.614-7.328-42.163-11.536-9.138-28.187-9.097-39.672.103-15.18 12.144-16.085 34.352-2.737 47.71 10.764 10.754 27.26 12.226 39.62 4.466l9.85 2.8c1.872.535 3.601-1.194 3.066-3.067zm-27.107 4.92a3.285 3.285 0 0 1-3.283-3.284 3.287 3.287 0 0 1 3.283-3.293 3.287 3.287 0 0 1 3.283 3.293 3.285 3.285 0 0 1-3.283 3.283zm7.389-22.065c-2.614 2.007-4.106 4.827-4.106 7.739v.216a3.287 3.287 0 0 1-3.283 3.293 3.287 3.287 0 0 1-3.283-3.293v-.216c0-4.97 2.429-9.684 6.669-12.946a5.543 5.543 0 0 0 2.171-4.487c-.041-2.933-2.552-5.444-5.485-5.485h-.072a5.479 5.479 0 0 0-3.9 1.605 5.502 5.502 0 0 0-1.657 3.952 3.279 3.279 0 0 1-3.283 3.283 3.272 3.272 0 0 1-3.283-3.283 12.04 12.04 0 0 1 3.612-8.634c2.326-2.295 5.454-3.5 8.675-3.49 6.504.093 11.866 5.455 11.959 11.96a12.206 12.206 0 0 1-4.734 9.786z" fill="#307f71" opacity="1" data-original="#000000" class=""></path></g></svg> Frequently Asked Questions</h1>""",
        unsafe_allow_html=True)
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")

    # Adding an FAQ section with collapsible accordion
    st.markdown(
        """
        <style>
        p, h1, h2, h3, h4, h5, h6, div, body {
            color: #fff !important;
        }
        h1, h2, h3, h4, h5, h6 {
            padding-top: 0;
        }
        .faq-section {
            margin-top: 20px;
        }
        .faq-title {
            font-size: 20px;
            color: #0099ff;
            font-weight: bold;
        }
        .faq-answer {
            font-size: 16px;
            color: #333;
        }
        hr {
            background-color: #ffffff40;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <h4>What does LOREM mean? <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="30" height="30" x="0" y="0" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;margin-top: -15px;" xml:space="preserve" class=""><g><g fill="#1d1d1b"><path d="M267.446 174.934c4.822 1.192 9.702 3.207 14.07 6.314 4.371 3.076 8.114 7.36 10.54 12.27 2.453 4.922 3.56 10.352 3.575 15.603h-14.298c.013-6.653-2.852-12.539-8.114-16.228-5.25-3.772-12.652-5.349-20.257-5.334v-14.283c4.755.012 9.604.452 14.484 1.658zM202.862 459.409h90.741c0 25.065-20.314 45.377-45.364 45.377-25.062 0-45.377-20.311-45.377-45.377zM446.672 72.208c3.474 3.476 7.488 5.476 10.382 5.447l.2.184c-2.924-.425-7.362 1.604-11.15 5.405-3.276 3.262-5.235 7.008-5.418 9.859-.355-2.795-2.286-6.37-5.418-9.505-2.71-2.71-5.748-4.525-8.313-5.178 2.71-.481 6.058-2.368 9.007-5.319 3.205-3.205 5.149-6.865 5.419-9.688.537 2.667 2.411 5.916 5.291 8.795zM377.065 58.463c-10.381-1.545-26.112 5.674-39.576 19.15-11.602 11.602-18.566 24.894-19.275 34.993-1.178-9.93-8.042-22.597-19.162-33.718-9.619-9.616-20.372-16.043-29.535-18.383 9.66-1.717 21.491-8.411 31.974-18.895 11.389-11.376 18.313-24.369 19.248-34.397 1.93 9.503 8.555 21.008 18.769 31.221 12.338 12.354 26.594 19.462 36.88 19.348z" fill="#f1cf32" opacity="1" data-original="#1d1d1b" class=""></path><path d="M265.163 349.89c0-12.356-10.017-22.37-22.369-22.37-12.371 0-22.385 10.014-22.385 22.37 0 12.37 10.014 22.381 22.385 22.381 12.352 0 22.369-10.011 22.369-22.381zM312.2 210.95c0-27.532-20.242-51.746-64.018-51.746-23.561 0-43.136 6.623-55.405 13.59l11.276 36.17c8.625-5.974 21.888-9.956 32.838-9.956 16.598.326 24.227 8.296 24.227 19.898 0 10.95-8.637 21.903-19.233 34.84-14.936 17.573-20.581 34.824-19.588 51.745l.339 8.625h44.116v-5.974c-.326-14.923 4.979-27.859 16.922-41.461 12.596-13.929 28.526-30.524 28.526-55.731zm-211.454 38.598c0-81.451 66.03-147.495 147.493-147.495 81.451 0 147.479 66.044 147.479 147.495 0 22.453-5.021 43.73-13.986 62.779-8.979 19.05-21.914 35.859-37.744 49.393l-13.363 26.596H165.842l-13.363-26.596c-31.646-27.053-51.733-67.266-51.733-112.172zM404.499 119.897c6.697 6.695 14.427 10.539 20.016 10.483l.354.368c-5.631-.837-14.155 3.078-21.445 10.383-6.3 6.298-10.072 13.49-10.456 18.965-.638-5.376-4.354-12.241-10.396-18.27-5.206-5.221-11.037-8.695-16-9.958 5.22-.937 11.645-4.567 17.334-10.256 6.17-6.17 9.915-13.206 10.424-18.639 1.049 5.152 4.638 11.393 10.169 16.924zM170.339 397.253h155.792l-10.923 21.728v35.777H181.259v-35.777z" fill="#f1cf32" opacity="1" data-original="#1d1d1b" class=""></path></g></g></svg></h4>
        <p>‘Lorem ipsum dolor sit amet, consectetur adipisici elit…’ (complete text) is dummy text that is not meant to mean anything. It is used as a placeholder in magazine layouts, for example, in order to give an impression of the finished document. The text is intentionally unintelligible so that the viewer is not distracted by the content. The language is not real Latin and even the first word ‘Lorem’ does not exist. It is said that the lorem ipsum text has been common among typesetters since the 16th century. (Source: Wikipedia.com).</p>
        """, 
    unsafe_allow_html=True)
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown("""
        <h4>Where can I edit my billing and shipping address? <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="30" height="30" x="0" y="0" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;margin-top: -15px;" xml:space="preserve" class=""><g><g fill="#1d1d1b"><path d="M267.446 174.934c4.822 1.192 9.702 3.207 14.07 6.314 4.371 3.076 8.114 7.36 10.54 12.27 2.453 4.922 3.56 10.352 3.575 15.603h-14.298c.013-6.653-2.852-12.539-8.114-16.228-5.25-3.772-12.652-5.349-20.257-5.334v-14.283c4.755.012 9.604.452 14.484 1.658zM202.862 459.409h90.741c0 25.065-20.314 45.377-45.364 45.377-25.062 0-45.377-20.311-45.377-45.377zM446.672 72.208c3.474 3.476 7.488 5.476 10.382 5.447l.2.184c-2.924-.425-7.362 1.604-11.15 5.405-3.276 3.262-5.235 7.008-5.418 9.859-.355-2.795-2.286-6.37-5.418-9.505-2.71-2.71-5.748-4.525-8.313-5.178 2.71-.481 6.058-2.368 9.007-5.319 3.205-3.205 5.149-6.865 5.419-9.688.537 2.667 2.411 5.916 5.291 8.795zM377.065 58.463c-10.381-1.545-26.112 5.674-39.576 19.15-11.602 11.602-18.566 24.894-19.275 34.993-1.178-9.93-8.042-22.597-19.162-33.718-9.619-9.616-20.372-16.043-29.535-18.383 9.66-1.717 21.491-8.411 31.974-18.895 11.389-11.376 18.313-24.369 19.248-34.397 1.93 9.503 8.555 21.008 18.769 31.221 12.338 12.354 26.594 19.462 36.88 19.348z" fill="#f1cf32" opacity="1" data-original="#1d1d1b" class=""></path><path d="M265.163 349.89c0-12.356-10.017-22.37-22.369-22.37-12.371 0-22.385 10.014-22.385 22.37 0 12.37 10.014 22.381 22.385 22.381 12.352 0 22.369-10.011 22.369-22.381zM312.2 210.95c0-27.532-20.242-51.746-64.018-51.746-23.561 0-43.136 6.623-55.405 13.59l11.276 36.17c8.625-5.974 21.888-9.956 32.838-9.956 16.598.326 24.227 8.296 24.227 19.898 0 10.95-8.637 21.903-19.233 34.84-14.936 17.573-20.581 34.824-19.588 51.745l.339 8.625h44.116v-5.974c-.326-14.923 4.979-27.859 16.922-41.461 12.596-13.929 28.526-30.524 28.526-55.731zm-211.454 38.598c0-81.451 66.03-147.495 147.493-147.495 81.451 0 147.479 66.044 147.479 147.495 0 22.453-5.021 43.73-13.986 62.779-8.979 19.05-21.914 35.859-37.744 49.393l-13.363 26.596H165.842l-13.363-26.596c-31.646-27.053-51.733-67.266-51.733-112.172zM404.499 119.897c6.697 6.695 14.427 10.539 20.016 10.483l.354.368c-5.631-.837-14.155 3.078-21.445 10.383-6.3 6.298-10.072 13.49-10.456 18.965-.638-5.376-4.354-12.241-10.396-18.27-5.206-5.221-11.037-8.695-16-9.958 5.22-.937 11.645-4.567 17.334-10.256 6.17-6.17 9.915-13.206 10.424-18.639 1.049 5.152 4.638 11.393 10.169 16.924zM170.339 397.253h155.792l-10.923 21.728v35.777H181.259v-35.777z" fill="#f1cf32" opacity="1" data-original="#1d1d1b" class=""></path></g></g></svg></h4>
        <ul>
            <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
            <li>Nullam vehicula justo eu lacinia mollis.</li>
            <li>Vestibulum placerat lorem quis leo accumsan laoreet.</li>
            <li>Proin sed nulla venenatis, finibus elit non, cursus elit.</li>
            <li>Mauris euismod tellus a mi pharetra rhoncus.</li>
            <li>Fusce rutrum lacus nec mauris aliquet, vitae volutpat risus lacinia.</li>
            <li>Fusce eget diam aliquam, tempor augue vel, placerat lacus.</li>
        </ul>
        """, 
    unsafe_allow_html=True)
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown("""
        <h4>What does LOREM mean? <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="30" height="30" x="0" y="0" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;margin-top: -15px;" xml:space="preserve" class=""><g><g fill="#1d1d1b"><path d="M267.446 174.934c4.822 1.192 9.702 3.207 14.07 6.314 4.371 3.076 8.114 7.36 10.54 12.27 2.453 4.922 3.56 10.352 3.575 15.603h-14.298c.013-6.653-2.852-12.539-8.114-16.228-5.25-3.772-12.652-5.349-20.257-5.334v-14.283c4.755.012 9.604.452 14.484 1.658zM202.862 459.409h90.741c0 25.065-20.314 45.377-45.364 45.377-25.062 0-45.377-20.311-45.377-45.377zM446.672 72.208c3.474 3.476 7.488 5.476 10.382 5.447l.2.184c-2.924-.425-7.362 1.604-11.15 5.405-3.276 3.262-5.235 7.008-5.418 9.859-.355-2.795-2.286-6.37-5.418-9.505-2.71-2.71-5.748-4.525-8.313-5.178 2.71-.481 6.058-2.368 9.007-5.319 3.205-3.205 5.149-6.865 5.419-9.688.537 2.667 2.411 5.916 5.291 8.795zM377.065 58.463c-10.381-1.545-26.112 5.674-39.576 19.15-11.602 11.602-18.566 24.894-19.275 34.993-1.178-9.93-8.042-22.597-19.162-33.718-9.619-9.616-20.372-16.043-29.535-18.383 9.66-1.717 21.491-8.411 31.974-18.895 11.389-11.376 18.313-24.369 19.248-34.397 1.93 9.503 8.555 21.008 18.769 31.221 12.338 12.354 26.594 19.462 36.88 19.348z" fill="#f1cf32" opacity="1" data-original="#1d1d1b" class=""></path><path d="M265.163 349.89c0-12.356-10.017-22.37-22.369-22.37-12.371 0-22.385 10.014-22.385 22.37 0 12.37 10.014 22.381 22.385 22.381 12.352 0 22.369-10.011 22.369-22.381zM312.2 210.95c0-27.532-20.242-51.746-64.018-51.746-23.561 0-43.136 6.623-55.405 13.59l11.276 36.17c8.625-5.974 21.888-9.956 32.838-9.956 16.598.326 24.227 8.296 24.227 19.898 0 10.95-8.637 21.903-19.233 34.84-14.936 17.573-20.581 34.824-19.588 51.745l.339 8.625h44.116v-5.974c-.326-14.923 4.979-27.859 16.922-41.461 12.596-13.929 28.526-30.524 28.526-55.731zm-211.454 38.598c0-81.451 66.03-147.495 147.493-147.495 81.451 0 147.479 66.044 147.479 147.495 0 22.453-5.021 43.73-13.986 62.779-8.979 19.05-21.914 35.859-37.744 49.393l-13.363 26.596H165.842l-13.363-26.596c-31.646-27.053-51.733-67.266-51.733-112.172zM404.499 119.897c6.697 6.695 14.427 10.539 20.016 10.483l.354.368c-5.631-.837-14.155 3.078-21.445 10.383-6.3 6.298-10.072 13.49-10.456 18.965-.638-5.376-4.354-12.241-10.396-18.27-5.206-5.221-11.037-8.695-16-9.958 5.22-.937 11.645-4.567 17.334-10.256 6.17-6.17 9.915-13.206 10.424-18.639 1.049 5.152 4.638 11.393 10.169 16.924zM170.339 397.253h155.792l-10.923 21.728v35.777H181.259v-35.777z" fill="#f1cf32" opacity="1" data-original="#1d1d1b" class=""></path></g></g></svg></h4>
        <p>‘Lorem ipsum dolor sit amet, consectetur adipisici elit…’ (complete text) is dummy text that is not meant to mean anything. It is used as a placeholder in magazine layouts, for example, in order to give an impression of the finished document. The text is intentionally unintelligible so that the viewer is not distracted by the content. The language is not real Latin and even the first word ‘Lorem’ does not exist. It is said that the lorem ipsum text has been common among typesetters since the 16th century. (Source: Wikipedia.com).</p>
        """, 
    unsafe_allow_html=True)

def render_contact_page():
    # Header with SVG icon
    st.markdown(
        """
        <h1>
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="35" height="35" x="0" y="0" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512" xml:space="preserve" class="">
                <g>
                    <path fill-rule="evenodd" d="M189.279 107.079h284.235L304.693 222.812l-114.834-78.723c4.372-11.707 4.409-24.94-.58-37.01zm-74.337 67.172 41.43-25.226c12.295-7.486 16.376-23.458 9.178-35.925l-37.403-64.784c-3.837-6.647-9.645-10.923-17.131-12.613-7.487-1.691-14.567-.326-20.889 4.027L21.915 86.694C-10.554 201.098 135.355 448.778 247.259 477l74.778-35.591c6.93-3.298 11.653-8.748 13.932-16.077s1.48-14.496-2.358-21.143l-37.403-64.784c-7.197-12.467-23.07-16.919-35.701-10.014l-42.561 23.266c-42.09-37.433-91.63-123.238-103.004-178.406zm379.216-52.288L311.443 247.221c-4.275 2.918-9.768 2.69-13.741-.165l-121.3-83.155a50.509 50.509 0 0 1-7.549 5.624l-26.204 15.954c13.767 44.43 47.832 103.432 79.426 137.569l26.919-14.716c24.052-13.148 54.292-4.666 67.997 19.073l23.196 40.176h135.108c10.668 0 19.396-8.728 19.396-19.396v-221.71a19.25 19.25 0 0 0-.533-4.512z" clip-rule="evenodd" fill="#307f71" opacity="1" data-original="#000000" class=""></path>
                </g>
            </svg> Get in Touch With Us
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Custom styles
    st.markdown(
        """
        <style>
            [data-testid="stForm"] input, [data-testid="stForm"] [data-baseweb="base-input"], [data-baseweb="input"], [type="textarea"], [data-baseweb="textarea"] {
                background: none;
            }
            [data-testid="stFileUploaderDropzone"] {
                background: rgb(88 88 88 / 0%) !important;
                border: 1px solid #307f71;
            }
            [data-testid="stFileUploaderDropzoneInstructions"] * {
                color: #fff;
            }
            [data-testid="stFileUploaderDropzone"] button {
                background: #09241f !important;
                border-color: #09241f !important;
                color: #fff !important;
            }
            button[kind="secondaryFormSubmit"] {
                border-color: rgb(48 127 113) !important;
                color: #fff !important;
                background: #307f71 !important;
                padding: 10px 30px;
            }
            [data-baseweb="input"], [data-baseweb="textarea"] {
                border-color: #307f71;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Information text
    st.markdown(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
    )

    # Form container
    with st.form(key='contact_form'):
        # Name field
        name = st.text_input("Name")

        # Subject field
        subject = st.text_input("Subject")

        # Email field
        email = st.text_input("Email")

        # Message field
        message = st.text_area("Message")

        # Upload image
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        # Submit button
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if name and subject and email and message:
                # Prepare form data
                form_data = {
                    'name': name,
                    'subject': subject,
                    'email': email,
                    'message': message
                }

                # Prepare file data if available
                files = {}
                if uploaded_file is not None:
                    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}

                # Send data to API
                try:
                    response = requests.post('http://streamlit.devexhub.com/contact', data=form_data, files=files)
                    response.raise_for_status()  # Raise an error for bad status codes

                    if response.status_code == 200:
                        st.success("Form submitted successfully!")
                    else:
                        st.error(f"Failed to submit form. Status code: {response.status_code}")

                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")

                # Display uploaded image if any
                if uploaded_file is not None:
                    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

                # Display form data
                st.write(f"Name: {name}")
                st.write(f"Subject: {subject}")
                st.write(f"Email: {email}")
                st.write(f"Message: {message}")
            else:
                st.error("Please fill out all fields.")
def render_about_page():
    st.write=st.markdown ("""<h1><svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="35" height="35" x="0" y="0" viewBox="0 0 25 25" style="enable-background:new 0 0 512 512" xml:space="preserve" class=""><g><path d="M21.1.5H3.9C2 .5.5 2 .5 3.9V21c0 1.9 1.5 3.4 3.4 3.4H21c1.9 0 3.4-1.5 3.4-3.4V3.9C24.5 2 23 .5 21.1.5zm-12.3 3c1.6 0 2.8 1.3 2.8 2.8 0 1.6-1.3 2.8-2.8 2.8S6 7.9 6 6.3c0-1.5 1.3-2.8 2.8-2.8zM6 20.6h-.7c-.5 0-1-.5-1-1s.5-1 1-1H6c.5 0 1 .5 1 1s-.5 1-1 1zm4.6 0h-.7c-.5 0-1-.5-1-1s.5-1 1-1h.7c.6 0 1 .5 1 1s-.5 1-1 1zm-5.8-4.9c-.7 0-1.2-.7-1-1.4.4-1.6 1.7-3 3.3-3.5.5.2 1.1.3 1.7.3s1.2-.1 1.7-.3c.8.2 1.4.7 2 1.2.6.6 1.1 1.4 1.3 2.3.2.7-.3 1.4-1 1.4zm10.3 4.9h-.7c-.5 0-1-.5-1-1s.5-1 1-1h.7c.5 0 1 .5 1 1s-.4 1-1 1zm4.6 0H19c-.5 0-1-.5-1-1s.5-1 1-1h.7c.5 0 1 .5 1 1s-.4 1-1 1zm1-8.5h-4c-.5 0-1-.5-1-1 0-.6.5-1 1-1h4c.6 0 1 .4 1 1 0 .5-.5 1-1 1zm0-4h-4c-.5 0-1-.4-1-1 0-.5.5-1 1-1h4c.6 0 1 .5 1 1 0 .6-.5 1-1 1z" fill="#307f71" opacity="1" data-original="#000000" class=""></path></g></svg> About Us</h1>""",
        unsafe_allow_html=True)
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    st.image("img/about-ai.jpg", caption="")
    st.markdown ("""<h2>Overview</h2>""", 
                 unsafe_allow_html=True)
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    st.markdown ("""<h2>Tools Features</h2>""", 
                 unsafe_allow_html=True)
    st.markdown("""<ul>
        <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
        <li>Nullam vehicula justo eu lacinia mollis.</li>
        <li>Vestibulum placerat lorem quis leo accumsan laoreet.</li>
        <li>Proin sed nulla venenatis, finibus elit non, cursus elit.</li>
        <li>Mauris euismod tellus a mi pharetra rhoncus.</li>
        <li>Fusce rutrum lacus nec mauris aliquet, vitae volutpat risus lacinia.</li>
        <li>Fusce eget diam aliquam, tempor augue vel, placerat lacus.</li>
    </ul>""", unsafe_allow_html=True)

# def render_signin_page():
#     # Inject custom CSS
#     st.markdown(
#         """
#         <style>
#         [data-testid="stVerticalBlock"] {
#             max-width: 600px;
#             margin: auto;
#         }
#         p, h1, h2, h3, h4, h5, h6, div, body {
#             color: #fff;
#         }
#         .google-signin-btn {
#             border: 0;
#             padding: 10px 20px;
#             border-radius: 10px;
#             display: flex;
#             align-items: center;
#             margin-inline: auto;
#             background: #fff;
#             color: #000;
#             cursor: pointer;
#             font-size: 16px;
#         }
#         .google-signin-btn svg {
#             fill: #000;
#             margin-right: 8px;
#         }
#         .signin-content {
#         text-align:center;}
#         [data-testid="stMarkdownContainer"] {
#             margin-bottom:0;
#         }
#         [data-testid="stForm"] {
#             background: #09241f;
#             border-radius: 20px;
#             padding: 25px;
#         }
#         .term-privacy-links {
#             margin-top: 30px
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     # st.title("Sign In")

#     # Create a placeholder for the button
#     placeholder = st.empty()

#     # Insert a form in the container
#     with placeholder.form("login"):
#         # Add the SVG directly to the button
#         st.markdown (
#             """
#             <div class="signin-content">
#                 <h2>Welcome to Stramlit</h2>
#                 <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
#             </div>

#             """
#         , unsafe_allow_html=True)
#         st.markdown(
#             """
#             <button type="submit" class="google-signin-btn">
#                 <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" x="0" y="0" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512" xml:space="preserve" class="icon">
#                     <g>
#                         <path d="m492.668 211.489-208.84-.01c-9.222 0-16.697 7.474-16.697 16.696v66.715c0 9.22 7.475 16.696 16.696 16.696h117.606c-12.878 33.421-36.914 61.41-67.58 79.194L384 477.589c80.442-46.523 128-128.152 128-219.53 0-13.011-.959-22.312-2.877-32.785-1.458-7.957-8.366-13.785-16.455-13.785z" style="" fill="#167ee6" data-original="#167ee6" class=""></path>
#                         <path d="M256 411.826c-57.554 0-107.798-31.446-134.783-77.979l-86.806 50.034C78.586 460.443 161.34 512 256 512c46.437 0 90.254-12.503 128-34.292v-.119l-50.147-86.81c-22.938 13.304-49.482 21.047-77.853 21.047z" style="" fill="#12b347" data-original="#12b347"></path>
#                         <path d="M384 477.708v-.119l-50.147-86.81c-22.938 13.303-49.48 21.047-77.853 21.047V512c46.437 0 90.256-12.503 128-34.292z" style="" fill="#0f993e" data-original="#0f993e"></path>
#                         <path d="M100.174 256c0-28.369 7.742-54.91 21.043-77.847l-86.806-50.034C12.502 165.746 0 209.444 0 256s12.502 90.254 34.411 127.881l86.806-50.034c-13.301-22.937-21.043-49.478-21.043-77.847z" style="" fill="#ffd500" data-original="#ffd500"></path>
#                         <path d="M256 100.174c37.531 0 72.005 13.336 98.932 35.519 6.643 5.472 16.298 5.077 22.383-1.008l47.27-47.27c6.904-6.904 6.412-18.205-.963-24.603C378.507 23.673 319.807 0 256 0 161.34 0 78.586 51.557 34.411 128.119l86.806 50.034c26.985-46.533 77.229-77.979 134.783-77.979z" style="" fill="#ff4b26" data-original="#ff4b26"></path>
#                         <path d="M354.932 135.693c6.643 5.472 16.299 5.077 22.383-1.008l47.27-47.27c6.903-6.904 6.411-18.205-.963-24.603C378.507 23.672 319.807 0 256 0v100.174c37.53 0 72.005 13.336 98.932 35.519z" style="" fill="#d93f21" data-original="#d93f21"></path>
#                     </g>
#                 </svg>
#                 <span>Sign in with Google</span>
#             </button>
#             <div class="signin-content term-privacy-links">
#                 <p>By registration you agree to <a href="#">Term of Use</a> and <a href="#">Privacy Policy</a>.</p>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
#         st.markdown (
#             """
            

#             """
#         , unsafe_allow_html=True)
#         # Handle form submission
#         # submit = st.form_submit_button("Sign in with Google")
#         # if submit:
#         #     st.warning("Google sign-in is not yet implemented.")


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
    st.markdown(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""
    )
    menu = st.radio(
        "Go to",
        [
            "🏠 Home",
            "📄 FAQ",
            "📑 Contact",
            "📊 About Us",
            
        ]
    )


    # Show the Template text+image in the sidebar directly
    modal = Modal(
        "Image & Text", 
        key="image-text",
        
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )
    open_modal = st.sidebar.button("📊 Image & Text")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            # Streamlit radio buttons as buttons
            st.markdown("""<p style="margin-bottom: 20px">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>""", unsafe_allow_html=True)
            st.image("img/about-ai.jpg")
            st.markdown("""<p style="margin-bottom: 20px">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>""", unsafe_allow_html=True)

    # Show the Template Image+dataGrid in the sidebar directly
    modal = Modal(
        "Image & DataGrid", 
        key="Image-DataGrid",
        
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )
    open_modal = st.sidebar.button("📊 Image & DataGrid")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            # Streamlit radio buttons as buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("img/about-ai.jpg", caption="Sunrise by the mountains")
            with col2:
                st.image("img/about-ai.jpg", caption="Sunrise by the mountains")
            with col3:
                st.image("img/about-ai.jpg", caption="Sunrise by the mountains")
            df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
            st.dataframe(df)  # Same as st.write(df)
            

    # Show the Template Text+dataGrid in the sidebar directly
    modal = Modal(
        "Text & DataGrid", 
        key="Text-DataGrid",
        
        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )
    open_modal = st.sidebar.button("📊 Text & DataGrid")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            # Streamlit radio buttons as buttons
            st.markdown("""<p style="margin-bottom: 20px">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>""", unsafe_allow_html=True)
            df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
            st.dataframe(df)  # Same as st.write(df)
           


# Map menu items to functions
pages = {
    "📄 FAQ": render_faq_page,
    "📑 Contact": render_contact_page,
    "📊 About Us": render_about_page,
  
}
# Content rendering based on the selected menu item
if menu == "🏠 Home":
    render_home_page()
elif menu == "📄 FAQ":
    render_faq_page()
elif menu == "📑 Contact":
    render_contact_page()
elif menu == "📊 About Us":
    render_about_page()

st.divider()

