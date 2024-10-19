import re
import zlib
import requests
from requests.adapters import HTTPAdapter, Retry
import os
import shutil
import asyncio

re_next_link = re.compile(r'<(.+)>; rel="next"')
retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

def get_batch(batch_url):
    while batch_url:
        response = session.get(batch_url)
        response.raise_for_status()
        total = response.headers["x-total-results"]
        yield response, total
        batch_url = get_next_link(response.headers)

def process_accessions(accessions):
    accession_batches = [accessions[i:i+500] for i in range(0, len(accessions), 500)]
    all_lines = []

    for accession_batch in accession_batches:
        accession_query = '%29%20OR%20%28accession%3A'.join(accession_batch)
        url = f"https://rest.uniprot.org/uniprotkb/search?compressed=true&fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Cgo_p%2Cgo_c%2Cgo%2Cgo_f%2Cgo_id&format=tsv&query=%28%28accession%3A{accession_query}%29%29&size=500"

        progress = 0
        lines = []
        for batch, total in get_batch(url):
            decompressed = zlib.decompress(batch.content, 16 + zlib.MAX_WBITS)
            batch_lines = [line for line in decompressed.decode("utf-8").split("\n") if line]
            if not progress:
                lines = [batch_lines[0].replace("\t", ",")]  
            lines += [line.replace("\t", ",") for line in batch_lines[1:]]  
            progress = len(lines) - 1
            print(f"{progress} / {total}")

        all_lines.extend(lines)

    return all_lines

async def main(file_path, file_id):
    output_dir = 'output_dir'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    with open(file_path, 'r') as f:
        accessions = f.read().splitlines()

    retrieved_data = await asyncio.to_thread(process_accessions, accessions)

    temp_filename = "uniprot-retrieval-temp.csv"
    with open(temp_filename, "w", newline='', encoding="utf-8") as f:
        f.write('\n'.join(retrieved_data))

    output_path = os.path.join(output_dir, f"result_{file_id}.csv")

    try:
        with open(output_path, "r", encoding="utf-8") as f_existing:
            existing_lines = f_existing.readlines()
        
        with open("uniprot-retrieval-merged.csv", "w", newline='', encoding="utf-8") as f_merged:
            f_merged.writelines(existing_lines)
            f_merged.write('\n'.join(retrieved_data))

        shutil.move("uniprot-retrieval-merged.csv", output_path)
    except FileNotFoundError:
        shutil.move(temp_filename, output_path)

if __name__ == "__main__":
    asyncio.run(main("accession_file.txt", "file_id"))
