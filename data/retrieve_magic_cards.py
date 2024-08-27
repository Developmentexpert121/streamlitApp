import weaviate  # type: ignore[import]
import typer
import os
import json
import requests
import random
import streamlit as st
from wasabi import msg  # type: ignore[import]

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


def get_card_details(card_name) -> dict:
    """Retrieve information from the Scryfall API about a card through its name.
    @parameter card_name : str - Card name
    @returns dict - A dictionary with the card information formatted to the correct Weaviate schema
    """
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        card_data = response.json()

        mana_dict = {"W": "White", "B": "Black", "R": "Red", "G": "Green", "U": "Blue"}

        weaviate_object = {
            "name": card_data.get("name", "Unknown"),
            "card_id": str(card_data.get("arena_id", "0")),
            "img": card_data.get("image_uris", {"normal": ""}).get("normal", ""),
            "mana_cost": card_data.get("mana_cost", "0"),
            "type": card_data.get("type_line", ""),
            "mana_produced": str(card_data.get("produced_mana", "")),
            "power": card_data.get("power", "0"),
            "toughness": card_data.get("toughness", "0"),
            "color": str(card_data.get("colors", "")),
            "keyword": str(card_data.get("keywords", "")),
            "set": card_data.get("set_name", ""),
            "rarity": card_data.get("rarity", ""),
            "description": card_data.get("oracle_text", ""),
        }

        for color_code in mana_dict:
            weaviate_object["mana_produced"] = weaviate_object["mana_produced"].replace(
                color_code, mana_dict[color_code]
            )
            weaviate_object["mana_cost"] = weaviate_object["mana_cost"].replace(
                color_code, mana_dict[color_code]
            )
            weaviate_object["color"] = weaviate_object["color"].replace(
                color_code, mana_dict[color_code]
            )
        return weaviate_object

    except requests.RequestException as e:
        msg.fail(f"Error retrieving card details: {e}")
        return None


def add_card_to_weaviate(weaviate_obj: dict, client: weaviate.Client) -> None:
    """Import a card object to Weaviate.
    @parameter weaviate_obj : dict - Formatted dict with the same keys as the schema
    @parameter client : weaviate.Client - Weaviate Client
    @returns None
    """
    try:
        with client.batch as batch:
            batch.batch_size = 10  # Adjust batch size as needed
            batch.add_data_object(weaviate_obj, "MagicChat_Card")
            msg.good(f"Imported {weaviate_obj['name']} to database")
    except Exception as e:
        msg.fail(f"Error adding card to Weaviate: {e}")


def main() -> None:
    msg.divider("Starting card retrieval")

    # Connect to Weaviate
    url = st.secrets.get("WEAVIATE_URL", "").strip()
    api_key = st.secrets.get("WEAVIATE_API_KEY", "").strip()
    openai_key = st.secrets.get("OPENAI_KEY", "").strip()

    if not url or not api_key or not openai_key:
        msg.fail("Environment Variables not set properly.")
        return

    client = weaviate.Client(
        url=url,
        additional_headers={"X-OpenAI-Api-Key": openai_key},
        auth_client_secret=api_key,
    )

    msg.good("Client connected to Weaviate Server")

    query_results = (
        client.query.get(
            "MagicChat_Card",
            ["name"],
        )
        .with_limit(30000)
        .do()
    )

    unique_cards = set(
        [
            str(card["name"]).lower().strip()
            for card in query_results["data"]["Get"]["MagicChat_Card"]
        ]
    )

    msg.info(f"Loaded {len(query_results['data']['Get']['MagicChat_Card'])} cards")

    with open("all_cards.json", "r") as reader:
        all_cards = json.load(reader)["data"]

    msg.info(f"{len(all_cards) - len(unique_cards)} Cards left to fetch")

    random.shuffle(all_cards)

    for card_name in tqdm(all_cards):
        if card_name.lower().strip() not in unique_cards:
            card = get_card_details(card_name)
            if card is not None:
                add_card_to_weaviate(card, client)
        else:
            msg.info(f"Skipping {card_name}")


if __name__ == "__main__":
    typer.run(main)
