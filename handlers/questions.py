from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from keyboard.for_question import get_yes_no_kb
import os

router = Router()  
class OrderDatabase(StatesGroup):
    choosing_database_name = State()

available_databases = ['Uniprot', 'Ensembl']
    
@router.message(Command("start"))  
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text="Which database would you like to use?",
        reply_markup=get_yes_no_kb()
    )
    await state.set_state(OrderDatabase.choosing_database_name)

@router.message(OrderDatabase.choosing_database_name, F.text.in_(available_databases))
async def database_chosen(message: Message, state: FSMContext):
    await state.update_data(database=message.text.lower())
    picture_path = os.path.join("pictures", "example.jpg")
    image_from_pc = FSInputFile(picture_path)
    await message.answer_photo(
        image_from_pc,
        caption=(
            "<b>Upload a file containing IDs in .txt format.</b> Each ID must be on a new line. Remember that a Uniprot identifier looks like <b>P05067</b>, while an Ensembl identifier looks like <b>ENSG00000142192</b>. \n<b>Example file structure:</b>"
        ),
        show_caption_above_media=True,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(OrderDatabase.choosing_database_name)
