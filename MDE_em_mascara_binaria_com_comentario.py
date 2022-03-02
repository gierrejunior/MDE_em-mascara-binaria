from osgeo import gdal, gdal_array
import numpy as np
import matplotlib.pyplot as plt
import os


pastaDEM =  (r'C:\Users\Gierre\Desktop\Rasters\MDEs')
os.chdir(pastaDEM)

dados = gdal.Open('AP_05061_FBS_F7150_RT1.dem.tif')
geotransform = dados.GetGeoTransform() # Armazena informações sobre a origem do arquivo raster e sua resolução e X e Y
projecao = dados.GetProjection() # Armazena informações sobre a projeção geográfica do raster
#print(dados.RasterCount) # Verifica o número de bandas raster que estão armazenadas nos dados, No caso só há um

banda = dados.GetRasterBand(1) # Cria uma variável Gdal com o Raster
array=banda.ReadAsArray() # Converte em Array, para poder manipular

#plt.figure
#plt.imshow(array) # plota o array na tela.

"""    
A função numpy.where() retorna os índices dos elementos em um array de entrada onde a condição dada é satisfeita
numpy.mean(arr, axis = None): Calcula a média aritmética (média) dos dados fornecidos (elementos da matriz) ao longo do eixo especificado
"""
mascara_binaria = np.where((array >= np.mean(array)),1,0)

"""
filtra os pixels que armazenam alturas acima de um determinado limite de elevação e 
criar uma massa binária para que todos os pixels acima do limite recebam o valor 1 
e tudo que tiver abaixo do valor receba 0.
"""

#plt.figure()
#plt.imshow(mascara_binaria)

"""
Exportar para GeoTiff
"""

driver = gdal.GetDriverByName("GTiff")
driver.Register()
saida_dados = driver.Create("mascara_binaria.tif", xsize = mascara_binaria.shape[1],
                      ysize = mascara_binaria.shape[0], bands = 1, 
                      eType = gdal.GDT_Int16)
saida_dados.SetGeoTransform(geotransform) # Como não houve alteração na resolução, ela continua a mesma de quando os dados entraram, logo podemos utilizar os dados armazenados anteriormente
saida_dados.SetProjection(projecao) # O mesmo acontece com a projeção, ela não foi alterada
saida_banda = saida_dados.GetRasterBand(1)
saida_banda.WriteArray(mascara_binaria)
saida_banda.SetNoDataValue(np.nan)
saida_banda.FlushCache() # Passa todas as mudanças que estão armazenadas no cache para o disco

"""
Fechando
"""

saida_banda = None
saida_dados = None


