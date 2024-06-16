from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from apps.users import keyboards as u_keyboard
from apps.users.states import RefillState
from apps.users.services import TransactionService
from apps.users.handlers.start import start

from loader import bot


router = Router()

REFILL_MESSAGE = "Введите сумму пополнения: "


async def ask_amount(callback: CallbackQuery, state: FSMContext):
    new_message = await callback.message.answer(
        REFILL_MESSAGE, reply_markup=u_keyboard.ask_amount()
    )
    await state.set_state(RefillState.amount)
    await state.set_data({"last_message_id": new_message.message_id, "attempt": 1})


@router.message(state=RefillState.amount)
async def input_amount(message: Message, state: FSMContext):
    state_data = await state.get_data()
    amount = message.text
    await message.delete()
    last_message_id = state_data["last_message_id"]
    attempt = state_data["attempt"]
    if not amount.isdigit():
        new_message = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"{REFILL_MESSAGE}\n\n<b>Неверно введена сумма, попробуйте ещё раз.\nПопытка ввода: {attempt}</b>",
            message_id=last_message_id,
        )
        await state.set_data(
            {"last_message_id": new_message.message_id, "attempt": attempt + 1}
        )
    else:
        reply_markup = u_keyboard.confirm_refill()
        await state.clear()
        new_message = await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=last_message_id,
            text=f"Вы уверены, что хотите пополнить баланс на {amount}₽?",
            reply_markup=reply_markup,
        )
        await state.set_state(RefillState.confirm)
        await state.set_data(
            {
                "last_message_id": new_message.message_id,
                "attempt": attempt,
                "amount": amount,
            }
        )


@router.callback_query(state=RefillState.confirm)
async def confirm_refill(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    amount = state_data["amount"]
    transaction = TransactionService.create_transaction(
        {"amount": amount, "user_id": callback.from_user.id}
    )
    # send to admin channel, wait refill


@router.callback_query(u_keyboard.RefillCallback.filter())
async def navigate_refill(
    callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    current_level = callback_data.level
    tid = callback_data.tid

    levels = {0: start, 1: ask_amount}

    await levels[current_level](callback=callback, tid=tid, state=state)
