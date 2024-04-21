import os
import random
import subprocess
import logging
from blake3 import blake3

# Set up basic configuration for logging
logging.basicConfig(filename='hash_generation.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def clear_existing_hdfs_file(file_path):
    """Check if the file exists in HDFS and delete it if it does."""
    result = subprocess.run(['hadoop', 'fs', '-test', '-e', file_path])
    if result.returncode == 0:
        logging.info(f"File {file_path} exists in HDFS. Deleting...")
        subprocess.run(['hadoop', 'fs', '-rm', file_path], check=True)
        logging.info(f"Deleted existing file {file_path}.")

def generate_and_write_data(num_records, output_path):
    # Ensure no existing data file conflicts
    data_file_path = f'{output_path}/data.txt'
    clear_existing_hdfs_file(data_file_path)

    # Open a process to write data directly to HDFS
    hdfs_write = subprocess.Popen(['hadoop', 'fs', '-put', '-', data_file_path], stdin=subprocess.PIPE)

    try:
        for _ in range(num_records):
            nonce = os.urandom(6)  # Generate a random 6-byte NONCE
            hasher = blake3()
            hasher.update(nonce)
            hash_bytes = hasher.digest(length=10)  # Generate a 10-byte hash from the NONCE
            record = hash_bytes + nonce + b'\n'
            hdfs_write.stdin.write(record)
        hdfs_write.stdin.close()
        hdfs_write.wait()
    except Exception as e:
        logging.error(f"Failed while writing data to pipe: {str(e)}")
        hdfs_write.kill()
        hdfs_write.stdin.close()
        raise

    if hdfs_write.returncode != 0:
        logging.error("HDFS write process failed")
    else:
        logging.info(f"All data generated and sent to HDFS at {data_file_path}")

def hadoop_sort(input_path, output_path, num_reducers):
    logging.info("Starting Hadoop sort process")
    try:
        subprocess.run([
            'hadoop', 'jar', '/root/hadoop-3.4.0/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar',
            '-D', f'mapreduce.job.reduces={num_reducers}',
            '-mapper', '/bin/cat',
            '-reducer', '/usr/bin/sort',
            '-input', input_path,
            '-output', output_path
        ], check=True)
        logging.info("Hadoop sort completed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Hadoop sort failed: {str(e)}")

def main():
    num_records = 2**32  # Adjust this number based on estimated average record size to reach ~16 GB
    num_reducers = 6  # Use all resources of the 6-node cluster
    input_path = '/user/hadoop/input'
    output_path = '/user/hadoop/output'

    logging.info("Starting data generation process")
    generate_and_write_data(num_records, input_path)
    hadoop_sort(f'{input_path}/data.txt', output_path, num_reducers)

if __name__ == '__main__':
    main()
                                                                                                                                                                                                    1,9           Top
