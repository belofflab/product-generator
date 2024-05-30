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
    asyncio.run(main())
