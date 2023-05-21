import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import h5py, png, PIL
import numpy as np
import os, json

EUMETSAT_SAMPLE_PATH = "/ims_archive/Operational/MSG/images/HRIT_RSS/{img_type}/{year}/{month}/{day}/{year}{month}{day}{hour}{minute}.{img_format}"
H5_FILE_NAME = "IMS_{img_type}_{year}_{start_month}{start_day}_{end_month}{end_day}.h5"
IMG_TYPES = ["MIDDLE_EAST_VIS", "MIDDLE_EAST_DAY_CLOUDS", "MIDDLE_EAST_COLORED", "MIDDLE_EAST_IR"]
IMG_FORMATS = ["png", "jpeg"]
CATALOG_PATH = "/ims_projects/Research/Oren/Lia_Ofir/earthformer-inference-experiments/ims_data/CATALOG.csv"
H5_FILES_PATH = "/ims_projects/Research/Oren/Lia_Ofir/earthformer-inference-experiments/ims_data/data"
CFG_FILE_PATH = "/ims_projects/Research/Oren/Lia_Ofir/earthformer-inference-experiments/ims_data/cfg.json"

# png
PNG_SIZE_Z = 4
PNG_SIZE_X = 600
PNG_SIZE_Y = 600

def create_h5_file(catalog_df, img_type, time_delta, year, start_date, end_date, img_format='png', sunrise=(2,40), sunset=(16,40)):
    # extract parameters of h5 file
    h5_year = str(year)
    h5_start_month = start_date.strftime("%m")
    h5_end_month = end_date.strftime("%m")
    h5_start_day = start_date.strftime("%d")
    h5_end_day = end_date.strftime("%d")
    h5_file_name = H5_FILE_NAME.format(img_type=img_type, year=h5_year, start_month=h5_start_month, start_day=h5_start_day, end_month=h5_end_month, end_day=h5_end_day)

    # create directory for h5 file
    h5_output_dir = Path(os.path.join(H5_FILES_PATH, img_type, h5_year))
    if not h5_output_dir.exists():
        h5_output_dir.mkdir(parents=True)
    
    # open h5 file
    hf = h5py.File(os.path.join(str(h5_output_dir), h5_file_name), "w")
    ids = []
    images = []

    # file index init
    file_index = 0

    # go over all days on between start_date and end_date, insert them to catalog and to the h5 file
    curr_date = start_date
    day_time_delta = timedelta(days=1)
    while curr_date <= end_date:
        # init empty frames list
        frames = []

        start_event_time = datetime(*(curr_date.year, curr_date.month, curr_date.day, sunrise[0], sunrise[1])) # time_utc in CATALOG
        end_event_time = datetime(*(curr_date.year, curr_date.month, curr_date.day, sunset[0], sunset[1]))
        day_full = True

        # open all images of this day
        curr_frame_time = start_event_time
        while curr_frame_time <= end_event_time and day_full:
            img_year = curr_frame_time.strftime("%Y")
            img_month = curr_frame_time.strftime("%m")
            img_day = curr_frame_time.strftime("%d")
            img_hour = curr_frame_time.strftime("%H")
            img_minute = curr_frame_time.strftime("%M")
        
            img_full_path = EUMETSAT_SAMPLE_PATH.format(year=img_year, month=img_month, day=img_day, hour=img_hour, minute=img_minute, img_format=img_format, img_type=img_type)
            if Path(img_full_path).exists():
                if img_format == 'png':
                    raw_img = png.Reader(file=open(img_full_path, "rb")).asRGBA8()
                    channels = raw_img[3]['planes']
                    raw_pixels = raw_img[2]
                    pixels = np.array([list(row) for row in raw_pixels], dtype="uint8").reshape(PNG_SIZE_X, PNG_SIZE_Y, PNG_SIZE_Z)
                    frames.append(pixels)
            else:
                day_full = False

            curr_frame_time += time_delta

        # append event frames and id
        event_id = curr_date.strftime("%Y%m%d")
        if day_full:
            ids.append(event_id)
            images.append(frames)

            # append event to CATALOG
            catalog_df = catalog_df._append({'id': event_id, 'file_name': h5_file_name, 'file_index': file_index , 'time_utc': start_event_time ,'img_type': img_type, 'min_delta': time_delta.seconds/60, 'size_x': PNG_SIZE_X, 'size_y': PNG_SIZE_Y, 'size_z': PNG_SIZE_Z}, ignore_index=True)
        
            print(f"appended event {event_id} to catalog.")
        else:
            print(f"event {event_id} was not full.")

        # move on to the next day
        curr_date += day_time_delta
        file_index += 1
    
    # insert data to h5 file
    hf.create_dataset('id', data=ids)
    hf.create_dataset(img_type, data=images)
    hf.close()

    return catalog_df

def main():
    # extract config
    cfg = json.load(open(CFG_FILE_PATH, "r"))
    catalog_df = pd.DataFrame(columns=['id', 'file_name', 'file_index', 'img_type', 'time_utc', 'min_delta', 'size_x', 'size_y', 'size_z'])
    
    for key in cfg.keys():
        year = int(key)
        img_format = cfg[key]['img_format']
        for img_type in cfg[key]['img_types']:
            for date_range in cfg[key]['ranges']:
                start_date_range = date_range[0]
                end_date_range = date_range[1]
                start_date =  datetime(*(year, start_date_range[0], start_date_range[1]))
                end_date = datetime(*(year, end_date_range[0], end_date_range[1]))
                time_delta = timedelta(minutes=5) 
    
                catalog_df = create_h5_file(catalog_df, img_type, time_delta, year, start_date, end_date)
    
    catalog_df.to_csv("/ims_projects/Research/Oren/Lia_Ofir/earthformer-inference-experiments/ims_data/CATALOG.csv", index=False)

if __name__ == '__main__':
    main()


