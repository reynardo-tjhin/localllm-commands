import time

def test_index(client):
    """Testing the index link"""
    
    # send a get request
    response = client.get("/")
    
    # test script no 1
    assert b"Test Script 1" in response.data
    assert b"Script for Testing No 1" in response.data
    assert b"0e6a19cc157941e0b56b6a272c6eec71" in response.data
    
    # test script no 2
    assert b"Test Script 2" in response.data
    assert b"Script for Testing No 2" in response.data
    assert b"c66d9421757f4051aa2f99b5305cb037" in response.data
    
    # test script no 3
    assert b"Test Script 3" in response.data
    assert b"Script for Testing No 3" in response.data
    assert b"6b84f067aaf34649a5a9a161395b504c" in response.data
    
def test_worker_status(client):
    """Test the worker-status API"""
    
    # script IDs
    script_1 = "0e6a19cc157941e0b56b6a272c6eec71"
    script_2 = "c66d9421757f4051aa2f99b5305cb037"
    script_3 = "6b84f067aaf34649a5a9a161395b504c"
    
    # send a get request
    response = client.get("/worker-status/" + script_1)
    assert b"1" in response.data
    
    # send a get request
    response = client.get("/worker-status/" + script_2)
    assert b"1" in response.data
    
    # send a get request
    response = client.get("/worker-status/" + script_3)
    assert b"1" in response.data
    
    # start the first script via a post request
    response = client.post("/start-worker/" + script_1)
    time.sleep(0.2)
    assert b"ok" in response.data
    
    # get the script status
    response = client.get("/worker-status/" + script_1)
    assert b"0" in response.data
    
    # end the first script via a post request
    response = client.post("/stop-worker/" + script_1)
    time.sleep(0.2)
    assert b"ok" in response.data
    
def test_incorrect_script_id_worker_status(client):
    """Test getting the worker status of script with incorrect script IDs"""
    
    # Test 1: script_id is None
    empty_script_id = ""
    response = client.get("/worker-status/" + empty_script_id)
    assert b"404 Not Found" in response.data
    
    # Test 2: script_id is not exactly 32 characters
    incorrect_length_script_id = "1234"
    response = client.get("/worker-status/" + incorrect_length_script_id)
    assert b"error" in response.data
    assert b"Script '1234' is not exactly 32 characters." in response.data
    
    # Test 3: script_id contains unacceptable characters (not 0-9 or a-e)
    incorrect_script_id = "0zza19cc157941e0b56b6a272c6eec71"
    response = client.get("/worker-status/" + incorrect_script_id)
    assert b"error" in response.data
    assert b"Script '0zza19cc157941e0b56b6a272c6eec71' contains characters that are not 0-9 or a-f." in response.data
    
    # Test 4: script_id does not exist
    not_exist_script_id = "e7c25d6cbb6b4b60ab557a3cf868f9c0"
    response = client.get("/worker-status/" + not_exist_script_id)
    assert b"error" in response.data
    assert b"Script 'e7c25d6cbb6b4b60ab557a3cf868f9c0' not found." in response.data

def test_start_stop_worker(client, mock_redis):
    """Test starting and stopping scripts via API"""
    
    # script IDs
    script_1 = "0e6a19cc157941e0b56b6a272c6eec71"
    script_2 = "c66d9421757f4051aa2f99b5305cb037"
    script_3 = "6b84f067aaf34649a5a9a161395b504c"
    script_4 = "1a4d538a50c24cff9958fd16de1c5efd"
    script_5 = "70a142eed7a0430588ddb9bc96c567a9"
    
    # start the first script via a post request
    response = client.post("/start-worker/" + script_1)
    time.sleep(0.2)
    assert b"ok" in response.data
    assert b"Script '0e6a19cc157941e0b56b6a272c6eec71' started" in response.data

    # start the first script again via a post request
    response = client.post("/start-worker/" + script_1)
    time.sleep(0.1)
    assert b"error" in response.data
    assert b"Script '0e6a19cc157941e0b56b6a272c6eec71' is currently running. Refresh the events if you are confident it has finished running." in response.data
    
    # start the rest of the scripts
    response = client.post("/start-worker/" + script_4)
    time.sleep(0.2)
    assert b"ok" in response.data
    assert b"Script '1a4d538a50c24cff9958fd16de1c5efd' started" in response.data
    
    response = client.post("/start-worker/" + script_3)
    time.sleep(0.2)
    assert b"ok" in response.data
    assert b"Script '6b84f067aaf34649a5a9a161395b504c' started" in response.data
    
    response = client.post("/start-worker/" + script_2)
    time.sleep(0.2)
    assert b"ok" in response.data
    assert b"Script 'c66d9421757f4051aa2f99b5305cb037' started" in response.data
    
    # starting script 5 will give the Script Limit Error
    response = client.post("/start-worker/" + script_5)
    time.sleep(0.2)
    assert b"error" in response.data
    assert b"Number of script running has reached the maximum, i.e. 4." in response.data
    
    # let all other scripts end
    time.sleep(2)
    response = client.post("/stop-worker/" + script_2)
    assert b"error" in response.data
    assert b"Script 'c66d9421757f4051aa2f99b5305cb037' process is not alive" in response.data
    
    response = client.get("/worker-status/" + script_2)
    assert b"1" in response.data
    
    response = client.post("/stop-worker/" + script_2)
    assert b"error" in response.data
    assert b"Script 'c66d9421757f4051aa2f99b5305cb037' is not in running processes" in response.data
    
    # end the first script via a post request
    response = client.post("/stop-worker/" + script_1)
    time.sleep(0.2)
    assert b"ok" in response.data
    assert b"script terminated successfully" in response.data

def test_incorrect_script_start_stop_worker(client):
    """Test starting and stopping scripts with incorrect script IDs"""
    
    # Test 1: script_id is None
    empty_script_id = ""
    response = client.post("/start-worker/" + empty_script_id)
    assert b"404 Not Found" in response.data
    response = client.post("/stop-worker/" + empty_script_id)
    assert b"404 Not Found" in response.data
    
    # Test 2: script_id is not exactly 32 characters
    incorrect_length_script_id = "1234"
    response = client.post("/start-worker/" + incorrect_length_script_id)
    assert b"Script '1234' is not exactly 32 characters." in response.data
    response = client.post("/stop-worker/" + incorrect_length_script_id)
    assert b"Script '1234' is not exactly 32 characters." in response.data
    
    # Test 3: script_id contains unacceptable characters (not 0-9 or a-e)
    incorrect_script_id = "0zza19cc157941e0b56b6a272c6eec71"
    response = client.post("/start-worker/" + incorrect_script_id)
    assert b"Script '0zza19cc157941e0b56b6a272c6eec71' contains characters that are not 0-9 or a-f." in response.data
    response = client.post("/stop-worker/" + incorrect_script_id)
    assert b"Script '0zza19cc157941e0b56b6a272c6eec71' contains characters that are not 0-9 or a-f." in response.data
    
    # Test 4: script_id does not exist
    not_exist_script_id = "e7c25d6cbb6b4b60ab557a3cf868f9c0"
    response = client.post("/start-worker/" + not_exist_script_id)
    assert b"error" in response.data
    assert b"Script 'e7c25d6cbb6b4b60ab557a3cf868f9c0' not found." in response.data
    response = client.post("/stop-worker/" + not_exist_script_id)
    assert b"error" in response.data
    assert b"Script 'e7c25d6cbb6b4b60ab557a3cf868f9c0' not found." in response.data
    
def test_poll(script_1_logger, mock_redis, client):
    """Testing on poll API"""
    
    script_1 = "0e6a19cc157941e0b56b6a272c6eec71"
    script_2 = "c66d9421757f4051aa2f99b5305cb037"
    
    # Test 1: script_id is None
    empty_script_id = ""
    response = client.get("/poll/" + empty_script_id)
    assert b"404 Not Found" in response.data
    
    # Test 2: incorrect length script id
    incorrect_length_script_id = "1234"
    response = client.get("/poll/" + incorrect_length_script_id)
    assert b"{\"end\":0,\"events\":[]}" in response.data
    
    # Test 3: incorrect script id
    incorrect_script_id = "0zza19cc157941e0b56b6a272c6eec71"
    response = client.get("/poll/" + incorrect_script_id)
    assert b"{\"end\":0,\"events\":[]}" in response.data
    
    # Test 4: non-existent script id
    not_exist_script_id = "e7c25d6cbb6b4b60ab557a3cf868f9c0"
    response = client.get("/poll/" + not_exist_script_id)
    assert b"{\"end\":0,\"events\":[]}" in response.data
    
    # Test 5: no start query parameter
    response = client.get("/poll/" + script_2)
    assert b"{\"end\":0,\"events\":[]}" in response.data
    
    # create some events
    script_1_logger.log("2026-04-13 20:00:00|Hello, World!")
    script_1_logger.log("2026-04-13 20:10:00|Another Hello, World!")
    script_1_logger.log("2026-04-13 20:20:00|Another Another Hello, World!")
    script_1_logger.log("2026-04-13 20:30:00|Ending, World!")
    
    # Test 6: good test
    response = client.get("/poll/" + script_1 + "?start=0")
    assert b"2026-04-13 20:00:00|Hello, World!" in response.data
    assert b"2026-04-13 20:10:00|Another Hello, World!" in response.data
    assert b"2026-04-13 20:20:00|Another Another Hello, World!" in response.data
    assert b"2026-04-13 20:30:00|Ending, World!" in response.data
    
    # clean up
    mock_redis.delete("script:0e6a19cc157941e0b56b6a272c6eec71")