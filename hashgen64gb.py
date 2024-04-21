import os
from blake3 import blake3
import logging
import time

# Constants based on the assignment
#values for my reference
#2**26 1gb
#2^27 2gb
#2^28 4gb
#2^29 8gb
#2^30 16gb
#2^31 32gb
#2^32 64gb
NUM_HASHES_SMALL = 2**32
HASH_SIZE = 10
NONCE_SIZE = 6
RECORD_SIZE = HASH_SIZE + NONCE_SIZE

# Setup logging
logging.basicConfig(filename='hashgen.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_record(nonce_size, hash_size):
    """Generate a single hash record consisting of a BLAKE3 hash and a random nonce."""
    nonce = os.urandom(nonce_size)
    hash_value = blake3(nonce).digest()[:hash_size]
    return hash_value + nonce

def generate_and_sort_records(num_records, nonce_size, hash_size):
    """Generate the specified number of records and sort them with detailed logging."""
    logging.info("Starting record generation.")
    start_time = time.time()
    records = []
    for i in range(num_records):
        if i % (num_records // 100) == 0:  # Update every 1%
            percent_complete = (i / num_records) * 100
            logging.info(f"[{i}][HASHGEN]: {percent_complete:.2f}% completed")
        records.append(generate_record(nonce_size, hash_size))
    gen_time = time.time() - start_time
    logging.info(f"Completed record generation in {gen_time:.2f} seconds.")

    logging.info("Starting record sorting.")
    start_time = time.time()
    records.sort(key=lambda record: record[:hash_size])
    sort_time = time.time() - start_time
    logging.info(f"Completed record sorting in {sort_time:.2f} seconds.")
    return records, gen_time, sort_time

def write_records(file_path, records):
    """Write the sorted records to a binary file with detailed logging."""
    logging.info("Starting record writing to disk.")
    start_time = time.time()
    with open(file_path, 'wb') as file:
        for i, record in enumerate(records):
            if i % (len(records) // 100) == 0:  # Update every 1%
                percent_complete = (i / len(records)) * 100
                logging.info(f"[{i}][IO]: {percent_complete:.2f}% completed")
            file.write(record)
    write_time = time.time() - start_time
    logging.info(f"Completed record writing in {write_time:.2f} seconds.")
    return write_time

def main():
    start_time = time.time()
    total_records = NUM_HASHES_SMALL
    sorted_records, gen_time, sort_time = generate_and_sort_records(total_records, NONCE_SIZE, HASH_SIZE)
    write_time = write_records('sorted_hashes_small.bin', sorted_records)
    total_time = time.time() - start_time
    logging.info(f"Total execution time: {total_time:.2f} seconds")
    print(f"Generated and stored {total_records} sorted records in 'sorted_hashes_small.bin'")
    print(f"Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
