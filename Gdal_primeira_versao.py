from osgeo import gdal, gdal_array
import numpy as np
import matplotlib.pyplot as plt
import os


pastaDEM =  (r'C:\Users\Gierre\Desktop\Rasters\MDEs')
os.chdir(pastaDEM)


dados = gdal.Open('AP_05061_FBS_F7150_RT1.dem.tif')
geotransform = dados.GetGeoTransform()
projecao = dados.GetProjection()
banda = dados.GetRasterBand(1)
array=banda.ReadAsArray()

#array = gdal_array.LoadFile('AP_05061_FBS_F7150_RT1.dem.tif')  
#plt.figure
#plt.imshow(array)

"""    
A função numpy.where() retorna os índices dos elementos em um array de entrada onde a condição dada é satisfeita
numpy.mean(arr, axis = None): Calcula a média aritmética (média) dos dados fornecidos (elementos da matriz) ao longo do eixo especificado
"""

#filtrar todo os pixels que armazenam alturas acima de um determinado limite de elevação e 
# criar uma massa binária para que todos os pixels acima do limite recebam o valor 1 
# e tudo que tiver abaixo do valor receba 0
#array maior ou igual a média de todos os valores de elevação, tudo que for maior ou igual a média receberá o valor 1

mascara_binaria = np.where((array >= np.mean(array)),1,0)
#plt.figure()
#plt.imshow(mascara_binaria)

#Exportar para GeoTiff

driver = gdal.GetDriverByName("GTiff")
driver.Register()
outds = driver.Create("mascara_binaria.tif", xsize = mascara_binaria.shape[1],
                      ysize = mascara_binaria.shape[0], bands = 1, 
                      eType = gdal.GDT_Int16)
outds.SetGeoTransform(geotransform)
outds.SetProjection(projecao)
outband = outds.GetRasterBand(1)
outband.WriteArray(mascara_binaria)
outband.SetNoDataValue(np.nan)
outband.FlushCache()


outband = None
outds = None


