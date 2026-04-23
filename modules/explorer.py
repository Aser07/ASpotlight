import ctypes
import datetime
import struct

#defines
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
EVERYTHING_REQUEST_DATE_RUN = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000

# 파일 정렬 상수
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING = 6  # 최신 수정순

#dll imports
everything_dll = ctypes.WinDLL ("C:/Users/gitdm/Documents/project/utilitys/spotlight/EverythingSDK/dll/Everything64.dll")
everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p



#convert a windows FILETIME to a python datetime
#https://stackoverflow.com/questions/39481221/convert-datetime-back-to-windows-64-bit-filetime
WINDOWS_TICKS = int(1/10**-7)  # 10,000,000 (100 nanoseconds or .1 microseconds)
WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00',
                                           '%Y-%m-%d %H:%M:%S')
POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00',
                                         '%Y-%m-%d %H:%M:%S')
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0

def get_time(filetime):
    """Convert windows filetime winticks to python datetime.datetime."""
    winticks = struct.unpack('<Q', filetime)[0]
    microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
    return datetime.datetime.fromtimestamp(microsecs)


#setup search --- 검색 함수 정의
def file_search(query:str,
                REQUEST_FILE_NAME=EVERYTHING_REQUEST_FILE_NAME,
                REQUEST_PATH=EVERYTHING_REQUEST_PATH, 
                REQUEST_SIZE=EVERYTHING_REQUEST_SIZE, 
                REQUEST_DATE_MODIFIED=EVERYTHING_REQUEST_DATE_MODIFIED, 
                dll=everything_dll):
    # file data save
    file_data = {
        "name": [],
        "path": [],
        "date_modified": [],
        "size": []
    }
    dll.Everything_SetSearchW(query)
    dll.Everything_SetRequestFlags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE | EVERYTHING_REQUEST_DATE_MODIFIED)
    # 1. 정렬 기준 설정 (예: 최신 수정일 순서)
    everything_dll.Everything_SetSort(EVERYTHING_SORT_DATE_MODIFIED_DESCENDING)
    #execute the query
    dll.Everything_QueryW(1)

    #get the number of results
    num_results = dll.Everything_GetNumResults()
    filename = ctypes.create_unicode_buffer(260)
    date_modified_filetime = ctypes.c_ulonglong(1)
    file_size = ctypes.c_ulonglong(1)
    if num_results !=0:
        #show results
        for i in range(num_results):
            dll.Everything_GetResultFullPathNameW(i,filename,260)
            dll.Everything_GetResultDateModified(i,date_modified_filetime)
            dll.Everything_GetResultSize(i,file_size)
            
            full_path = ctypes.wstring_at(filename).replace('\\', '/')
            file_name = full_path[full_path.rfind('/')+1:]
            file_path = full_path[:full_path.rfind('/')+1]
            date_modified = get_time(date_modified_filetime).strftime('%Y-%m-%d %H:%M:%S')
            
            file_data["name"].append(file_name)
            file_data["path"].append(file_path)
            file_data["date_modified"].append(date_modified)
            file_data["size"].append(file_size.value)
            
        return file_data
    else:
        return 0