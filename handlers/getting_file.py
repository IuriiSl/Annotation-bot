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
    output_dir = "output_dir"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(directory, f"ID_list_{file_id}.txt")

    await bot.download_file(file.file_path, file_path)
    await message.reply("The file was successfully uploaded.")

    if database == 'uniprot':
        await main(file_path, file_id)
    elif database == 'ensembl':
        await main_ensembl(file_path, file_id)

    result_path = os.path.join("output_dir", f"result_{file_id}.csv")
    result_file = FSInputFile(result_path)
    await message.answer_document(
        document=result_file,
        caption=(
            "<b>Please note:</b> the tab character is used as a column separator.\n\n"
            "You can use either <b>Excel</b> or <b>Google Sheets</b> to read such files.\n\n"
            "<b>For Google Sheets, the sequence of actions is as follows:</b>\n"
            "1. Create a new document.\n"
            "2. Go to the <b>File</b> menu.\n"
            "3. Select <b>Import</b>.\n"
            "4. Add the file.\n"
            "5. In the dropdown menu <b>'Separator type'</b>, select <b>'Tab'</b>."
        ),
        parse_mode="HTML"
    )
    await state.clear()
    os.remove(result_path)
    os.remove(file_path)
