import asyncio


# Testing modules 
from apps.generator_base.modules.cards.wb import WB


# from apps.generator_base.modules.cards import Generator
from apps.generator_base.modules.cards.exceptions import CardGenFailed
from apps.generator_base.modules.cards.saver import Saver
from apps.generator_base.modules.cards.ai import AI


# DatabaseManager().load()


async def main():
    # product = await wb().get_product(209695275)
    # print(product)
    # try:
    #     new_card = await Generator(875044476).make_card("image.jpg")
    #     print(new_card)
    # except CardGenFailed as ex:
    #     print(ex.message, ex.card_id)
    # Saver(875044476).make_report()
    result = await AI().generate_card(open("image.jpg", "rb"))
    print(result)

if __name__ == "__main__":
    # asyncio.run(main())
    import re

    pattern = re.compile(r'(\d*\.?\d+)\s*x\s*(\d*\.?\d+)\s*x\s*(\d*\.?\d+)')

    # Examples to test
    test_strings = [
        "3 x 4 x 5",
        "3.5 x 4.2 x 5.1",
        "3 x 4.2 x 5",
        "3.5 x 4 x 5.1",
    ]

    for s in test_strings:
        match = pattern.match(s)
        if match:
            print(f"Matched: {s} -> {match.groups()}")
        else:
            print(f"No match: {s}")

