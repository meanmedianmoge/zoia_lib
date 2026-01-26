## Execution
```
python -m unittest discover -s zoia_lib/tests
```

## Overview
The tests cover core functionality including API interactions, binary operations, file management, metadata handling, encoding, searching, sorting, and data export capabilities.

## Test Modules

- **test_api.py** - Tests for API communication and requests
- **test_binary.py** - Tests for binary data handling and operations
- **test_deletion.py** - Tests for file/object deletion functionality
- **test_dir_creation.py** - Tests for directory creation operations
- **test_encode.py** - Tests for encoding/decoding operations
- **test_exporting.py** - Tests for data export functionality
- **test_metadata.py** - Tests for metadata handling and manipulation
- **test_saving.py** - Tests for save operations
- **test_searching.py** - Tests for search functionality
- **test_sorting.py** - Tests for sorting operations

## Sample Data
The `sample_files/` directory contains test fixtures:
- `input_test.bin` - Sample single patch
- `sampleJSON.json` - Sample JSON test data
- `sampleJSONZIP.json` - Sample compressed JSON test data
- `sampleMeta.json` - Sample metadata test data
- `sampleZIPBytes.bin` - Sample zipped patch