from glob import glob
from django.http import HttpResponse
from django.shortcuts import redirect, render
# from stlConverter. models import saveDicomFiles
from stlConverter.models import saveContactData
import time
from django.core.files import File
import shutil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import smtplib
from plotly.graph_objs import *
import vtk
from vtk.util import numpy_support
import os
import numpy
from IPython.display import Image
import chart_studio.plotly as py
#from plotly.graph_objs import *
from glob import glob
from .forms import UploadFileForm


def home(request):
    return render(request, 'home.html')


def about(request):
    # return HttpResponse("You are at about")
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        # get contact parameters
        if request.user.is_authenticated:
            fname = request.user.first_name
            lname = request.user.last_name
            email = request.POST.get('contactEmail')
            feedback = request.POST.get('contactFeedback')
        else:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('contactEmail')
            feedback = request.POST.get('contactFeedback')

        # function for sending email to respective person
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('satamom254@gmail.com', 'ydcpkkzqtdwndcqs')
        subject = "Recieved feedback from " + str(fname) + " " + str(lname)
        body = str(fname) + " " + str(lname) + " says " + str(feedback)
        message = f'subject:{subject} \n\n\n   {body}'
        server.sendmail(
            'satamom254@gmail.com',
            'omsatam1005@gmail.com',
            message
        )
        print('Email has been sent successfully')
        server.quit()

        saveContactData(fname=fname, lname=lname,
                        email=email, feedback=feedback).save()
        messages.success(
            request, "Thanks for the feedback..We will connect with you shortly")
        return redirect(contact)

    return render(request, 'contact.html')


def handleSignup(request):
    if request.method == 'POST':
        # get the user parameters
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(username) > 12:
            messages.error(request, 'Your username is too long')
            return redirect('home')
            # return HttpResponse('Your username is too long')
        if not username.isalnum():
            messages.error(
                request, 'username must contain letters and numbers')
            return redirect('home')
            # return HttpResponse('username must contain letters and numbers')
        if (pass1 != pass2):
            messages.error(request, 'passwords do not match')
            return redirect('home')
            #  return HttpResponse('passwords do not match')
        # create the user
        myUser = User.objects.create_user(
            username=username, email=email, password=pass1, first_name=fname, last_name=lname)
        # User.first_name = fname
        # User.last_name = lname
        # myUser.save()
        messages.success(request, 'your accont has been created successfully')
        return redirect(home)
    return redirect(home)


def handleLogin(request):
    if request.method == "POST":
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        user = authenticate(username=login_username, password=login_password)
        if user is not None:
            login(request, user)
            messages.success(request, 'successfully logged in')
            return redirect(home)
        messages.error(
            request, "Invalid credentials, please enter correct details")
        return redirect(uploader)
    return redirect(home)


def handleLogout(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect(uploader)


def uploader(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            CT_data = request.FILES.getlist('CT_data')
            stlFilename = str(request.POST.get('filename'))
            stlFilename = stlFilename.replace(" ", "")
            username = request.user.username
            userid = request.user.id

            import os
            import shutil
            parentdirDicomfiles = 'F:\\Final year project\\3D Innovators production\\Innovators\\dicom\\dicom\\dicomFiles\\'
            parentdirStlfiles = 'F:\\Final year project\\3D Innovators production\\Innovators\\dicom\\dicom\\stlFiles\\'
            directoryName = str(username) + str(userid)
            try:
                shutil.rmtree(parentdirDicomfiles + directoryName)
                shutil.rmtree(parentdirStlfiles + directoryName)
            except:
                pass
            pathDicomfiles = os.path.join(parentdirDicomfiles, directoryName)
            pathStlfiles = os.path.join(parentdirStlfiles, directoryName)
            os.mkdir(pathDicomfiles)
            os.mkdir(pathStlfiles)
            # saveDicomFiles(username = username).save()
            # print((CT_data))
            # ct_data = []
            import os
            # if not os.path.exists(path):
            #     os.mkdir(path)

            for file in CT_data:
                fn = os.path.join(pathDicomfiles, file.name)

                # open read and write the file into the server
                open(fn, 'wb').write(file.file.read())
                # saveDicomFiles(dicomFiles = file).save()
                # saveDicomFiles(stlFiles = file).save()
            # saveDicomFiles().save()
            # print(ct_data)
            # filePath.close()
        else:
            return HttpResponse("error in uploading")
        import vtk
        from vtk.util import numpy_support
        import os
        import numpy
        from IPython.display import Image
        import chart_studio.plotly as py
        #from plotly.graph_objs import *
        from glob import glob

        def vtkImageToNumPy(image, pixelDims):
            pointData = image.GetPointData()
            arrayData = pointData.GetArray(0)
            ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
            ArrayDicom = ArrayDicom.reshape(pixelDims, order='F')

            return ArrayDicom

        def plotHeatmap(array, name="plot"):
            data = Data([
                Heatmap(
                        z=array,
                        colorscale='Greys'
                        )
            ])
            layout = Layout(
                autosize=False,
                title=name
            )
            fig = Figure(data=data, layout=layout)

            return py.iplot(fig, filename=name)

        def vtk_show(renderer, width=400, height=300):
            """
            Takes vtkRenderer instance and returns an IPython Image with the rendering.
            """
            renderWindow = vtk.vtkRenderWindow()
            renderWindow.SetOffScreenRendering(1)
            renderWindow.AddRenderer(renderer)
            renderWindow.SetSize(width, height)
            renderWindow.Render()

            windowToImageFilter = vtk.vtkWindowToImageFilter()
            windowToImageFilter.SetInput(renderWindow)
            windowToImageFilter.Update()

            writer = vtk.vtkPNGWriter()
            writer.SetWriteToMemory(1)
            writer.SetInputConnection(windowToImageFilter.GetOutputPort())
            writer.Write()
            data = writer.GetResult()

            return Image(data)


        try:
            # CT_data = dict(CT_data)
            # ct_data = glob(str(ct_data) + '/*.dcm')
            reader = vtk.vtkDICOMImageReader()
            reader.SetDirectoryName(pathDicomfiles)
            reader.Update()

            # Load dimensions using `GetDataExtent`
            _extent = reader.GetDataExtent()
            ConstPixelDims = [_extent[1]-_extent[0]+1,_extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]

            # Load spacing values
            ConstPixelSpacing = reader.GetPixelSpacing()

            #shiftScale = vtk.vtkImageShiftScale()
            # shiftScale.SetScale(reader.GetRescaleSlope())
            # shiftScale.SetShift(reader.GetRescaleOffset())
            # shiftScale.SetInputConnection(reader.GetOutputPort())
            # shiftScale.Update()

            # In the next cell you would simply get the output with 'GetOutput' from 'shiftScale' instead of 'reader'

            ArrayDicom = vtkImageToNumPy(reader.GetOutput(), ConstPixelDims)
            # plotHeatmap(numpy.rot90(ArrayDicom[:, 256, :]), name="CT_Original")

            threshold = vtk.vtkImageThreshold()
            threshold.SetInputConnection(reader.GetOutputPort())
            threshold.ThresholdByLower(400)  # remove all soft tissue
            threshold.ReplaceInOn()
            threshold.SetInValue(0)  # set all values below 400 to 0
            threshold.ReplaceOutOn()
            threshold.SetOutValue(1)  # set all values above 400 to 1
            threshold.Update()

            ArrayDicom = vtkImageToNumPy(threshold.GetOutput(), ConstPixelDims)
            # plotHeatmap(numpy.rot90(ArrayDicom[:, 256, :]), name="CT_Thresholded")

            # % % time
            dmc = vtk.vtkDiscreteMarchingCubes()
            dmc.SetInputConnection(threshold.GetOutputPort())
            dmc.GenerateValues(1, 1, 1)
            dmc.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(dmc.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            renderer = vtk.vtkRenderer()
            renderer.AddActor(actor)
            renderer.SetBackground(1.0, 1.0, 1.0)

            camera = renderer.MakeCamera()
            camera.SetPosition(-500.0, 245.5, 122.0)
            camera.SetFocalPoint(301.0, 245.5, 122.0)
            camera.SetViewAngle(30.0)
            camera.SetRoll(-90.0)
            renderer.SetActiveCamera(camera)
            vtk_show(renderer, 600, 600)

            camera = renderer.GetActiveCamera()
            camera.SetPosition(301.0, 1045.0, 122.0)
            camera.SetFocalPoint(301.0, 245.5, 122.0)
            camera.SetViewAngle(30.0)
            camera.SetRoll(0.0)
            renderer.SetActiveCamera(camera)
            vtk_show(renderer, 600, 600)
            writer = vtk.vtkSTLWriter()
            writer.SetInputConnection(dmc.GetOutputPort())
            writer.SetFileTypeToBinary()
            writer.SetFileName(stlFilename + str(userid) + '.stl')
            writer.Write()
            shutil.move("F:\\Final year project\\3D Innovators production\\Innovators\\" +stlFilename + str(userid) + '.stl', pathStlfiles)
            downloadStlpath = '../dicom/dicom/stlFiles/' + directoryName + '/' + stlFilename + str(userid) + '.stl'
            messages.success(request, "Thanks for using, click specified link to download file")
            return render(request, 'downloader.html', {'stlPath': downloadStlpath})

        except:
            messages.error(request,"Please select the dicom files correctly and try again")
            return redirect(uploader)
    return render(request, 'uploader.html')


def services(request):
    return render(request, 'services.html')
