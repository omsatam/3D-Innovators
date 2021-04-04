import shutil, os
# from models import saveDicomFiles
# import vtk
# def find_files(file, search_path):

#    for root, dir, files in os.walk(search_path ):
#       if file in files:
#          return file.tell()
# print(find_files("folder.stl","F:\\Final year project\\3D!nnovators\\Innovators"))

file = open("F:\\Final year project\\3D!nnovators\\Innovators\\folder.stl",'rb')
file.seek(0, os.SEEK_END)
print(file.tell())
shutil.move("F:\\Final year project\\3D!nnovators\\Innovators\\folder.stl",'F:\\Final year project\\3D!nnovators\\Innovators\\dicom\\stlFiles')