from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
import os
from annotation_function.uniprot_retrieval import main
from annotation_function.ensembl_anno import main_ensembl
from aiogram.fsm.context import FSMContext

router = Router()  

@router.message(F.document)
async def download_document(message: Message, bot: Bot, state: FSMContext):
    user_data = await state.get_data()  
    database = user_data.get('database')
    
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    directory = "downloads"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"ID_list_{file_id}.txt")

    await bot.download_file(file.file_path, file_path)
    await message.reply("Файл успешно загружен.")

    if database == 'uniprot':
        await main(file_path, file_id)
    elif database == 'ensembl':
        await main_ensembl(file_path, file_id)

    result_path = os.path.join("output_dir", f"result_{file_id}.csv")
    result_file = FSInputFile(result_path)
    await message.answer_document(
        document=result_file,
        caption=(
            "<b>Обращаем ваше внимание:</b> в качестве разделителя колонок используется знак табуляции.\n\n"
            "Для чтения таких файлов можно использовать как <b>Excel</b>, так и <b>Google Таблицы</b>.\n\n"
            "<b>Для Google Таблиц последовательность действий следующая:</b>\n"
            "1. Создайте новый документ.\n"
            "2. Перейдите в меню <b>Файл</b>.\n"
            "3. Выберите <b>Импортировать</b>.\n"
            "4. Добавьте файл.\n"
            "5. В выпадающем окне <b>'Тип разделителя'</b> выберите <b>'Табуляция'</b>."
        ),
        parse_mode="HTML"
    )
    await state.clear()
    os.remove(result_path)
    os.remove(file_path)