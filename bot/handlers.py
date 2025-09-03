from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink, hbold

from bot.config import TG_ID
from bot import keyboards as kbs
from bot.states import Output
from scrapper.headers import HEADERS
from scrapper.discount_parser import get_data, post_process_data


router = Router()


async def include_notification(dp, bot):

    @router.message(CommandStart())
    async def cmd_start(message: Message, state: FSMContext = None):
        if state:
            if state:
                await state.clear()

        # Псевдостатистика - оповещение о пользовании ботом
        await bot.send_message(chat_id=TG_ID,
                               text=f"Пользователь только что начал использовать меня!")
        
        await message.answer(text=f"Здравствуй, {message.from_user.first_name}!\n"
                                "Для кого будем искать кроссовки?",
                             reply_markup=kbs.gender_kb)


@router.message(F.text == 'Сбросить 🔙')
async def canceled(message: Message, state: FSMContext = None):
    if state:
        await state.clear()

    await message.answer(text='Надеюсь я смог помочь!',
                         reply_markup=kbs.gender_kb)


@router.message(F.text.startswith('Ищем'))
async def get_man_sneakers(message: Message, state: FSMContext):
    required_gender = message.text.split(' ')
    if required_gender[-2] == 'мужские': 
        await message.answer(text="Ищу все мужские кроссовки со скидками\n"\
                                  "Пожалуйста, ожидай 🤔\n"\
                                  "Это может занять около минуты...",
                             reply_markup=ReplyKeyboardRemove())
        
        data = get_data(headers=HEADERS, gender='man')
        proceced_data = post_process_data(data)
   
    if required_gender[-2] == 'женские': 
        await message.answer(text="Ищу все женские кроссовки со скидками\n"\
                                  "Пожалуйста, ожидай 🤔\n"\
                                  "Это может занять около минуты...",
                             reply_markup=ReplyKeyboardRemove())
        
        data = get_data(headers=HEADERS, gender='woman')
        proceced_data = post_process_data(data)
    
    await state.update_data(stack=0)
    await state.update_data(sneakers_data=proceced_data)
    await state.set_state(Output.stack)

    await message.answer(text=f"Спасибо за ожидание!\n"\
                              f"Я нашел {len(data)} позиций со скидками 🔥\n"\
                              "Давай посмотрим что там?\n"\
                              "Нажми кнопку, и я покажу первые 5 позиций",
                         reply_markup=kbs.output_kb)
    

@router.message(Output.stack)
async def researching_sales(message: Message, state: FSMContext):
    state_data = await state.get_data()
    current_stack_index = state_data.get('stack')
    data = state_data.get('sneakers_data')

    for item in data[current_stack_index]:
        card = f"{hlink(title=item.get('model'), url=item.get('url'))}\n"\
               f"{hbold('Бренд: ')}{(item.get('brand'))}\n"\
               f"{hbold('Старая цена: ')}{(item.get('old_price'))}\n"\
               f"🔥{hbold('Цена по скидке: ')}{item.get('new_price')}🔥\n"\
               f"{hbold(item.get('type'))}\n"\
               f"{hbold('Цвет: ')}{item.get('color')}\n"\
               f"{hbold('Доступные размеры: ')}{item.get('sizes')}"
    
        await message.answer(text=card, reply_markup=kbs.output_kb)

    next_stack_index = int(current_stack_index) + 1
    await state.update_data(stack=next_stack_index)

    if next_stack_index == len(data):
        await state.clear()
        await message.answer('Это все!',
                             reply_markup=ReplyKeyboardRemove())
        
