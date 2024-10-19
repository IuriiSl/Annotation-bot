import aiohttp
import asyncio
import pandas as pd
import os

async def get_gene_info(session, gene_id):
    url = f'https://rest.ensembl.org/lookup/id/{gene_id}?content-type=application/json'
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Ошибка при получении информации для гена {gene_id}: {response.status} - {await response.json().get('error')}")
            return None

async def main_ensembl(input_file, file_id):
    output_dir = 'output_dir'
    os.makedirs(output_dir, exist_ok=True)  # Создаем выходную директорию, если ее нет
    file_path = input_file
    gene_ids = []
    
    with open(file_path, 'r') as file:
        gene_ids = [line.strip() for line in file if line.strip()]
    
    gene_data = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_gene_info(session, gene_id) for gene_id in gene_ids]
        results = await asyncio.gather(*tasks)
        
        for info in results:
            if info:
                gene_data.append(info)
    
    df = pd.DataFrame(gene_data)
    
    output_path = os.path.join(output_dir, f"result_{file_id}.csv")
    df.to_csv(output_path, sep='\t', index=False)

if __name__ == "__main__":
    asyncio.run(main_ensembl(input_file, file_id))


