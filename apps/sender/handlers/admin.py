import asyncio
from typing import Optional
from sqlalchemy import select
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import types
from config.database import DatabaseManager
from apps.sender import keyboards as s_keyaboard, states
from apps.admin.keyboards import admin as admin_keyboard
from apps.admin.middlewares import IsAdminMiddleware
from apps.sender.models import Template
from apps.users.models import User
from config.settings import MEDIA_DIR
from aiogram.fsm.context import FSMContext
from apps.core.date_time import DateTime
from loader import bot
from apps.core.utils.misc.extras import download_image, answer_or_edit_message, Paginator

router = Router()
router.message.middleware(IsAdminMiddleware())

STEPS = {
    "img": {
        "direction": {"next": "text", "prev": None},
        "state": states.SenderState.image,
        "desc": "<b>Вы начали создание рассылки...</b>\n\nОтправьте мне фотограцию или жмите пропустить",
        "keyboard": s_keyaboard.sender_skip_or_cancel,
    },
    "text": {
        "direction": {"next": "confirm", "prev": "img"},
        "state": states.SenderState.text,
        "desc": "<b>Отправьте мне текст</b>\n\nили жмите пропустить",
        "keyboard": s_keyaboard.sender_skip_or_cancel,
    },
    "confirm": {
        "direction": {"next": None, "prev": "text"},
        "state": states.SenderState.confirm,
        "desc": "<b>Вы уверены, что хотите начать рассылку?</b>\n\nЕсли кнопка <b>ДА</b> недоступна, проверьте ввод текста или изображения!",
        "keyboard": s_keyaboard.confirm_keyboard,
    },
}
LAST_MESSAGE_ID_TAG = "last_mid"
CURRENT_STEP_TAG = "current_step"
TEMPLATE_TAG = "template"


def get_next_or_previous_step(current_step: str, direction: str):
    return STEPS.get(current_step, {}).get("direction", {}).get(direction)


@router.message(Command("admin"))
async def admin(callback: types.Message, **kwargs):
    await answer_or_edit_message(
        message=callback,
        text=f"Добро пожаловать, {callback.from_user.full_name}",
        reply_markup=admin_keyboard(),
    )


async def choose_option_sender(callback: types.CallbackQuery, **kwargs):
    await callback.message.edit_text(
        text="Выберите нужное меню:", reply_markup=s_keyaboard.sender_options()
    )


@router.callback_query(lambda c: c.data == "delete_myself")
async def delete_myself(callback: types.CallbackQuery):
    await callback.message.delete()


async def setup_sender(callback: types.CallbackQuery, state: FSMContext, tid: int = 0):
    template = Template.get_or_none(tid)
    if template is None:
        await setup_step(callback=callback, state=state)
    else:
        await callback.message.edit_text(
            "Вы уверены, что хотите начать рассылку?",
            reply_markup=s_keyaboard.confirm_keyboard(tid=template.id),
        )


async def send_template(chat_id, template):
    if template.image is not None:
        await bot.send_photo(
            chat_id=chat_id,
            photo=types.FSInputFile(MEDIA_DIR / template.image),
            caption=template.text,
            reply_markup=s_keyaboard.myself_delete(),
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=template.text,
            reply_markup=s_keyaboard.myself_delete(),
        )


async def start_sender(template_id: int, message_id: int, admin_id: int):
    with DatabaseManager.session as session:
        users = session.execute(select(User.id))
    template = Template.get(template_id)
    for user in users:
        await asyncio.sleep(0.03)
        await send_template(chat_id=user.id, template=template)
    await bot.edit_message_text(
        chat_id=admin_id,
        message_id=message_id,
        text="<b>Вы успешно начали рассылку!</b>\n\nРезультат вы увидите здесь:\nТекущий статус: <b>Завершена ✅</b>\n\nЧтобы вернуться в меню, \nжми ➡️ /admin",
    )


async def setup_step(
    callback: types.CallbackQuery,
    state: FSMContext,
    step: Optional[str] = "img",
):

    state_data = await state.get_data()
    if state_data.get(TEMPLATE_TAG) is None:
        template = Template.create()
    else:
        template = state_data.get(TEMPLATE_TAG)
    await state.set_state(state=STEPS[step]["state"])
    if isinstance(callback, types.CallbackQuery):
        new_message = await callback.message.edit_text(
            text=STEPS[step]["desc"],
            reply_markup=STEPS[step]["keyboard"](
                step=step,
                has_skip=True,
                has_previous=(get_next_or_previous_step(step, "prev") is not None),
                has_next=(get_next_or_previous_step(step, "next") is not None),
            ),
        )
    elif isinstance(callback, types.Message):
        new_message = await bot.edit_message_text(
            chat_id=callback.from_user.id,
            text=STEPS[step]["desc"],
            reply_markup=STEPS[step]["keyboard"](
                step=step,
                has_skip=True,
                has_previous=(get_next_or_previous_step(step, "prev") is not None),
                has_next=(get_next_or_previous_step(step, "next") is not None),
            ),
            message_id=state_data[LAST_MESSAGE_ID_TAG],
        )
    await state.set_data(
        {
            LAST_MESSAGE_ID_TAG: new_message.message_id,
            CURRENT_STEP_TAG: step,
            TEMPLATE_TAG: template,
            "attempt": 1,
        }
    )


@router.message(F.photo, StateFilter(states.SenderState.image))
async def load_image(message: types.Message, state: FSMContext):
    CURRENT_STEP = "img"
    state_data = await state.get_data()
    image = await download_image(message)
    await message.delete()
    template = Template.update(state_data["template"].id, image=image)
    await state.set_data(
        {
            LAST_MESSAGE_ID_TAG: state_data[LAST_MESSAGE_ID_TAG],
            CURRENT_STEP_TAG: CURRENT_STEP,
            TEMPLATE_TAG: template,
        }
    )
    await setup_step(
        callback=message,
        state=state,
        step=get_next_or_previous_step(CURRENT_STEP, "next"),
    )


@router.message(F.text, StateFilter(states.SenderState.text))
async def load_text(message: types.Message, state: FSMContext):
    CURRENT_STEP = "text"
    TEXT_LIMIT = 4096
    CAPTION_LIMIT = 1024
    state_data = await state.get_data()
    text = message.html_text
    await message.delete()
    template = state_data[TEMPLATE_TAG]
    if template.image is not None:
        if len(text) > CAPTION_LIMIT:
            attempt = state_data["attempt"]
            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"<b>Отправьте мне текст</b>\n\n<b>Возника ошибка:</b> Текст превышает максимаьную длину {CAPTION_LIMIT}!\n\nПопробуйте ещё раз..{attempt}",
                reply_markup=s_keyaboard.sender_skip_or_cancel(
                    step=CURRENT_STEP, has_skip=True, has_previous=True, has_next=False
                ),
                message_id=state_data["last_mid"],
            )
            return await state.update_data(
                last_mid=new_message.message_id, attempt=attempt + 1
            )
    else:
        if len(text) > TEXT_LIMIT:
            attempt = state_data["attempt"]
            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"<b>Отправьте мне текст</b>\n\n<b>Возника ошибка:</b> Текст превышает максимаьную длину {TEXT_LIMIT}!\n\nПопробуйте ещё раз..{attempt}",
                reply_markup=s_keyaboard.sender_skip_or_cancel(
                    step=CURRENT_STEP, has_skip=True, has_previous=True, has_next=False
                ),
                message_id=state_data["last_mid"],
            )
            return await state.update_data(
                last_mid=new_message.message_id, attempt=attempt + 1
            )
    template = Template.update(state_data["template"].id, text=text)
    await state.set_data(
        {
            LAST_MESSAGE_ID_TAG: state_data[LAST_MESSAGE_ID_TAG],
            CURRENT_STEP_TAG: CURRENT_STEP,
            TEMPLATE_TAG: template,
        }
    )
    await setup_step(
        callback=message,
        state=state,
        step=get_next_or_previous_step(CURRENT_STEP, "next"),
    )


@router.callback_query(
    lambda c: c.data.startswith("sender"), StateFilter(states.SenderState)
)
async def proceed_sender(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.split(":")
    do = callback_data[1]
    step = callback_data[2]
    state_data = await state.get_data()
    if do == "cancel":
        Template.delete(state_data["template"])
        await state.clear()
        await choose_option_sender(callback=callback)
    elif do in {"next", "prev"}:
        next_step = get_next_or_previous_step(step, do)
        if next_step == "confirm" and do == "next":
            if (
                state_data["template"].text is None
                and state_data["template"].image is None
            ):
                attempt = state_data["attempt"]
                new_message = await bot.edit_message_text(
                    chat_id=callback.from_user.id,
                    text=f"<b>Отправьте мне текст</b>\n\n<b>Возника ошибка:</b> в рассылке должен быть текст или изображение!\n\nПопробуйте ещё раз..{attempt}",
                    reply_markup=s_keyaboard.sender_skip_or_cancel(
                        step=step, has_skip=True, has_previous=True, has_next=False
                    ),
                    message_id=state_data["last_mid"],
                )
                return await state.update_data(
                    last_mid=new_message.message_id, attempt=attempt + 1
                )
        if next_step is not None:
            await setup_step(callback=callback, state=state, step=next_step)
    elif do == "show_t":
        await send_template(
            chat_id=callback.from_user.id, template=state_data["template"]
        )
    elif do == "confirm":
        await state.clear()
        new_message = await callback.message.edit_text(
            text="<b>Вы успешно начали рассылку!</b>\n\nРезультат вы увидите здесь:\nТекущий статус: <b>В процессе 🕰️</b>\n\nЧтобы вернуться в меню, \nжми ➡️ /admin"
        )
        # TODO: apscheduler
        asyncio.create_task(
            start_sender(
                state_data["template"].id,
                new_message.message_id,
                callback.from_user.id,
            )
        )
        # scheduler.add_job(
        #     start_sender, args=(state_data["template"].id, new_message.message_id, new_message.from_user.id)
        # )


@router.callback_query(s_keyaboard.SenderCallback.filter())
async def navigate_sender(
    callback: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    current_level = callback_data.level
    tid = callback_data.tid

    levels = {0: admin, 1: choose_option_sender, 2: setup_sender}

    await levels[current_level](callback=callback, tid=tid, state=state)


async def show_history(callback: types.CallbackQuery, page: int, **kwargs):
    paginator = Paginator(query=select(Template), page=page, per_page=10)
    paginator_data = paginator.get_response()
    templates = "\n".join(
        [
            f"<b>{DateTime.string(item.created_at)}</b>\n{item.text[:25]}..."
            for item in paginator_data["items"]
            if item.text is not None
        ]
    )
    await callback.message.edit_text(
        f"<b>История ваших рассылок</b>\nВсего: {paginator_data['count']}\n\n"
        + templates,
        reply_markup=s_keyaboard.sender_hs_paginate(
            has_next=paginator_data["next_page"],
            has_prev=paginator_data["previous_page"],
            page=page,
        ),
    )


@router.callback_query(s_keyaboard.SenderHistoryCallback.filter())
async def navigate_sender_history(
    callback: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    current_level = callback_data.level
    page = callback_data.page

    levels = {0: admin, 1: show_history}

    await levels[current_level](callback=callback, state=state, page=page)
