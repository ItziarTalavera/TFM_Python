#Función que pasa un fichero en formato PPM con 4 colores a una memoria vhdl
 
import xlrd #Para usar archivos de excel

#Función para crear la memoria
def memoria (Nombrebase, imagen, columnas, filas):

	nombre_archivo = Nombrebase + ".vhd"
	file_out = open(nombre_archivo, "w")

	file_out.write ("--Memoria creada a partir de una imagen PPM de 4 colores\n\n")
	file_out.write ("library IEEE;\n")
	file_out.write ("use IEEE.STD_LOGIC_1164.ALL;\n")
	file_out.write ("use IEEE.NUMERIC_STD.ALL;\n")
	file_out.write ("library WORK;\n")
	file_out.write ("use WORK.VGA_PKG.ALL;\n\n")
	file_out.write ("entity ")
	file_out.write (Nombrebase)
	file_out.write (" is\n")
	file_out.write ("	port (\n")
	file_out.write ("	--Puertos de entrada\n")
	file_out.write ("	clk : in std_logic;\n")
	file_out.write ("	dir_img_")
	file_out.write (Nombrebase)
	file_out.write (" : in std_logic_vector (12-1 downto 0);\n")
	file_out.write (" 	--Puertos de salida\n")
	file_out.write ("	dato_img_")
	file_out.write (Nombrebase)
	file_out.write (" : out std_logic_vector (8-1 downto 0)\n")
	file_out.write (");\n")
	file_out.write ("end ")
	file_out.write (Nombrebase)
	file_out.write (";\n\n")
	file_out.write ("architecture behavioral of ")
	file_out.write (Nombrebase)
	file_out.write (" is\n\n")
	file_out.write ("signal dir_int_img : natural range 0 to 2**12;\n")
	file_out.write ("type img is array (natural range<>) of std_logic_vector (8-1 downto 0);\n")
	file_out.write ("constant title : img := (\n")
	for fila in range(filas): #Bucle que crea la memoria de la imagen en vhdl
		file_out.write ('	"')
		for columna in range(columnas):
			if columna == 0:
				file_out.write (str(imagen[fila][7]))
			elif columna == 1:
				file_out.write (str(imagen[fila][6]))
			elif columna == 2:
				file_out.write (str(imagen[fila][5]))
			elif columna == 3:
				file_out.write (str(imagen[fila][4]))
			elif columna == 4:
				file_out.write (str(imagen[fila][3]))
			elif columna == 5:
				file_out.write (str(imagen[fila][2]))
			elif columna == 6:
				file_out.write (str(imagen[fila][1]))
			else:
				file_out.write (str(imagen[fila][0]))
		if fila == (filas - 1) and columna == (7):
			file_out.write('"\n') 
		else:			
			file_out.write('",\n') 
	file_out.write (");\n\n")
	file_out.write ("begin\n\n")
	file_out.write ("dir_int_img <= to_integer(unsigned(dir_img_")
	file_out.write (Nombrebase)
	file_out.write ("));\n\n")
	file_out.write ("P_img: process (clk)\n")
	file_out.write ("begin\n")
	file_out.write ("	if clk'event and clk='1' then\n")
	file_out.write ("		dato_img_")
	file_out.write (Nombrebase)
	file_out.write (" <= title(dir_int_img);\n")
	file_out.write ("	end if;\n")
	file_out.write ("end process;\n\n")
	file_out.write ("end behavioral;\n")

	file_out.close()

	print("Imagen convertida")


#Función que convierte la imagen
def conver_img_vhdl(Hoja_trabajo):
	
	filePath = "C:\\Users\\itzia\\Desktop\\Mosaicos_256.xlsx"

	openFile = xlrd.open_workbook(filePath)

	sheet = openFile.sheet_by_name(Hoja_trabajo)

	filas_excel = sheet.nrows

	columnas_excel = sheet.ncols

	filas = filas_excel*16

	columnas = columnas_excel//16

	imagen_PPM_ord = [ [0 for columna in range(0,columnas)] for fila in range (0,filas)]
	
	fil = 0
	m = 0
	for i in range(filas_excel):
		col = 0
		for j in range(columnas_excel):
			if j % 8 == 0 and j != 0: #Si es múltiplo de 8, comienzo de cada mosaico
				fil = fil + 8
				col = 0
			elif i % 8 == 0 and j == 0 and i != 0:
				fil = i*16
				m = m + 15
			elif j == 0 and i != 0:
				fil = i + m*8
				col = 0

			imagen_PPM_ord[fil][col] = sheet.cell_value(i,j)
			col = col + 1

	#print(imagen_PPM_ord)

	#Matriz en vhdl

	imagen_vhdl = [ [0 for columna in range(0,columnas)] for fila in range (0,filas*2)]
	color_vhdl = [0,0]
	fila_vhdl = 0

	for fila in range(filas):
		if fila % 8 == 0: #Si es múltiplo de 8, comienzo de cada mosaico
			fila_vhdl = fila*2
		else:
			fila_vhdl = fila_vhdl+1
		for columna in range(columnas):			
			if imagen_PPM_ord[fila][columna] == "92 148 252":
				color_vhdl = [0,0]
			elif imagen_PPM_ord[fila][columna] == "252 188 176":
				color_vhdl = [0,1]
			elif imagen_PPM_ord[fila][columna] == "200 76 12":
				color_vhdl = [1,0]
			else:
				color_vhdl = [1,1]
		

			imagen_vhdl[fila_vhdl][columna] = color_vhdl[0]
			imagen_vhdl[fila_vhdl+8][columna] = color_vhdl[1]

	return(imagen_vhdl, filas*2, columnas)


#Direccion_arvhico = input("Introducir la direccion del archivo: ")

Hoja_imagen = input("Introducir el nombre de la hoja del archivo: ")

[imagen, filas, columnas] = conver_img_vhdl(Hoja_imagen)

nombre_mem_vhdl = input("Introducir el nombre de la memoria de vhdl: ")

memoria(nombre_mem_vhdl, imagen, columnas, filas)