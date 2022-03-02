from osgeo import gdal, gdal_array
import numpy as np
import matplotlib.pyplot as plt
import os


pastaDEM =  (r'C:\Users\Gierre\Desktop\Rasters\MDEs')
os.chdir(pastaDEM)

dados = gdal.Open('AP_05061_FBS_F7150_RT1.dem.tif')
geotransform = dados.GetGeoTransform() 
projecao = dados.GetProjection() 
#print(dados.RasterCount) 

banda = dados.GetRasterBand(1) 
array=banda.ReadAsArray() 

#plt.figure
#plt.imshow(array) 

mascara_binaria = np.where((array >= np.mean(array)),1,0)


#plt.figure()
#plt.imshow(mascara_binaria)


driver = gdal.GetDriverByName("GTiff")
driver.Register()
saida_dados = driver.Create("mascara_binaria.tif", xsize = mascara_binaria.shape[1],
                      ysize = mascara_binaria.shape[0], bands = 1, 
                      eType = gdal.GDT_Int16)
saida_dados.SetGeoTransform(geotransform)
saida_dados.SetProjection(projecao) 
saida_banda = saida_dados.GetRasterBand(1)
saida_banda.WriteArray(mascara_binaria)
saida_banda.SetNoDataValue(np.nan)
saida_banda.FlushCache() 

saida_banda = None
saida_dados = None

