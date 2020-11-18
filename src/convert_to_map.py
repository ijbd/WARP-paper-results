
from netCDF4 import Dataset 
import numpy as np 
import pandas as pd


raw_results_folder = '../raw_results'
map_results_folder = '../map_results'


def extract_results(results_filename):
    results = pd.read_csv(results_filename,index_col=0)

    latitude = results['latitude'].values.astype(float)
    longitude = results['longitude'].values.astype(float)
    elcc = results['ELCC'].values.astype(int)

    # make map 

    lats = np.unique(latitude)
    lons = np.unique(longitude)

    elcc_map = np.zeros((len(lats),len(lons)))

    # fill map

    for i in range(len(elcc)):
        
        elcc_map[np.argwhere(lats == latitude[i])[0,0], np.argwhere(lons == longitude[i])[0,0]] = elcc[i]

    return lats, lons, elcc_map

def write_to_map(region, year, nameplate, technology, add_on=''):
    
    results_filename = '%s_%d_%d_MW_%s%s_results.csv' % (region,year,nameplate,technology,'' if add_on is None else '_'+add_on)
    lats, lons, elcc = extract_results('%s/%s' % (raw_results_folder, results_filename))
    elcc_map = pd.DataFrame(index=lats, columns=lons, data=elcc)
    elcc_map.to_csv('%s/%s' % (map_results_folder,results_filename.replace('.csv','_map.csv')))

# Base cases
capacity = 500
for region in ['basin','california','mountains','northwest','southwest']:
    for year in [2016, 2017, 2018, 2019]:
        for technology in ['solar', 'wind']:
                for ff in [True, False]:
                    try: 
                        write_to_map(region,year,capacity,technology,'FF' if ff else '')
                    except:
                        pass

# Sensitivities
year = 2019
for region in ['basin','california','mountains','northwest','southwest']:
    for technology in ['solar','wind']:
        for capacity in [100,500,2000]:
            # storage
            if capacity == 500:
                try: 
                    write_to_map(region,year,capacity,technology,'storage')
                except:
                    pass
            # variable size
            else: 
                try: 
                    write_to_map(region,year,capacity,technology)
                except:
                    pass