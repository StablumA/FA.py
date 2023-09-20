import pandas as pd
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import shapely
import numpy as np
import warnings
from shapely.geometry import Point
import pointpats
import time
from multiprocessing import Pool

warnings.filterwarnings('ignore')
def puntosenpoligono(args):
    poligono, n = args
    coor = pointpats.random.poisson(poligono, size=int(n))
    x = coor[0]
    y = coor[1]
    return x, y

def explotar(args):
    x, y = args
    circulo = Point(x, y).buffer(0.003)
    nuevopunto = puntosenpoligono((circulo, 1))
    return nuevopunto

def parallel_explotar(args):
    return explotar(args)

if __name__ == '__main__':
    start = time.time()
    od = pd.read_csv("Venado/Output/OD_MaySepNovFINAL.csv")
    # zona = gpd.read_file("SHP Files/RadiosCensales/RCcortado.shp", crs = "22185")
    # zona = zona.to_crs("EPSG:4326")
    # zona["long"] = zona.geometry.centroid.x
    # zona["lat"] = zona.geometry.centroid.y
    # # zona = zona[["geometry", "long", "lat"]]
    # # zona = zona.to_crs("EPSG:22185")
    # # zona["Area"] = zona.area / 10000
    # zona["long"] = zona["long"] + 0.00001
    odaux = od.copy(deep=True)

    num_processes = 6  # Number of processes to run in parallel
    pool = Pool(num_processes)
    results = pool.map(parallel_explotar, zip(odaux["longitude_Origen"], odaux["latitude_Origen"]))
    pool.close()
    pool.join()

    odaux[['longitude_Origen', 'latitude_Origen']] = pd.DataFrame(results, columns=['long', 'lat'])

    num_processes = 6  # Number of processes to run in parallel
    pool = Pool(num_processes)
    results = pool.map(parallel_explotar, zip(odaux["longitude_Destino"], odaux["latitude_Destino"]))
    pool.close()
    pool.join()

    odaux[['longitude_Destino', 'latitude_Destino']] = pd.DataFrame(results, columns=['long', 'lat'])

    odaux.to_csv("Venado/Output/OD_MNS_E.csv", index=True)
    end = time.time()
    print("Execution time:", ((end - start)/60), "minutos")