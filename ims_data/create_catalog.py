import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

EUMETSAT_SAMPLE_PATH = "/ims_archive/Operational/MSG/images/HRIT_RSS/{img_type}/{year}/{month}/{day}/{year}{month}{day}{hour}{minute}.{img_format}"
H5_FILE_NAME = "IMS_{img_type}_{year}_{start_month}_{end_month}.h5"
IMG_TYPES = ["MIDDLE_EAST_VIS", "MIDDLE_EAST_DAY_CLOUDS", "MIDDLE_EAST_COLORED", "MIDDLE_EAST_IR"]
IMG_FORMATS = ["png", "jpeg"]
CATALOG_PATH = "/ims_projects/Research/Oren/Lia_Ofir/earthformer-inference-experiments/ims_data/CATALOG.csv"

def insert_to_catalog(df, start_time, end_time, time_delta, img_type, h5_year, h5_start_month, h5_end_month):
    curr_time = start_time
    while curr_time <= end_time:
        year = curr_time.strftime("%Y")
        month = curr_time.strftime("%m")
        day = curr_time.strftime("%d")
        hour = curr_time.strftime("%H")
        minute = curr_time.strftime("%M")
        for img_format in IMG_FORMATS:
            img_full_path = EUMETSAT_SAMPLE_PATH.format(year=year, month=month, day=day, hour=hour, minute=minute, img_format=img_format, img_type=img_type)
            img_id = f"{year}{month}{day}"
            h5_file_name = H5_FILE_NAME.format(img_type=img_type, year=h5_year, start_month=f'{h5_start_month:02d}', end_month=f'{h5_end_month:02d}')
            if Path(img_full_path).exists():
                df = df._append({'id': img_id, 'file_name': h5_file_name, 'img_type': img_type, 'img_full_path': img_full_path}, ignore_index=True)
            curr_time += time_delta
    return df

def main():
    df = pd.DataFrame(columns=['id', 'file_name', 'file_index', 'img_type', 'time_utc', 'size_x', 'size_y', 'min_offsets', 'img_full_path'])
    start_time = datetime(*(2023, 1, 1, 4, 0))
    print(start_time)
    end_time = datetime(*(2023, 1, 1, 20, 0))
    print(end_time)
    time_delta = timedelta(minutes=5)    
    df = insert_to_catalog(df, start_time, end_time, time_delta, "MIDDLE_EAST_VIS", 2023, 1, 2)
    print(df)

if __name__ == '__main__':
    main()


