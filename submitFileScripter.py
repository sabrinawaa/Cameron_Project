import os
import sys
import shutil
import numpy as np

def main(): 

    flavour = "workday"
    folder ="submit/scan_k1s/"
    os.makedirs(os.path.join(folder, "out"), exist_ok=True)
    os.makedirs(os.path.join(folder, "err"), exist_ok=True)
    os.makedirs(os.path.join(folder, "log"), exist_ok=True)
    FileName = "findk1s"
    with open(folder + FileName + ".submit", 'w') as ff:
            ff.write("executable = $(MYEXE)\n\n")
            ff.write("output = out/$(MYNAME)_$(ClusterId).$(ProcId).out\n")
            ff.write("error = err/$(MYNAME)_$(ClusterId).$(ProcId).err\n")
            ff.write("log = log/$(MYNAME)_$(ClusterId).$(ProcId).log\n\n")
            ff.write("transfer_input_files = $(MYINPUT)\n\n")
            # ff.write('+JobFlavour = "{}"\n\n'.format(flavour))


    py_filename = "/home/sabrinawang/TransferProj/find_ks.py"
    with open(folder + FileName + '.sh', 'w') as f:
        f.write("#!/bin/bash\n\n")
        f.write("source /home/sabrinawang/TransferProj/myenv/bin/activate\n\n")
        f.write("python3 " + py_filename+ " $1 $2\n")  #or else dynamnicaly change python file

    with open(folder + FileName + ".submit", 'a') as f:
        f.write("MYEXE= {}\n".format( "/home/sabrinawang/TransferProj/" + folder + FileName + ".sh \n"))
        f.write("MYINPUT = /home/sabrinawang/TransferProj/RF_track_4quad.py, {}\n\n".format(py_filename))
        ks = np.arange(-75,75,5)
        for k11 in ks:
            for k12 in ks:
                f.write(f"arguments = {k11} {k12}\n")
                f.write("queue\n\n")
        # f.write("MYEXE= {}\n".format(exeFileName))
        # f.write(f"MYNAME = k11={k11}_k12={k12}\n")
        
        # f.write("queue\n\n")       

if __name__ == "__main__": #execute code when file runs as script not imported as module
    main()
#%%
                        
#     for i in range(startPID, endPID, step):
#         exeFileName = "sq32_{}.sh".format(str(i))
#         mad_filename = "sq32_{}.madx".format(str(i))
#         py_filename = "sq32_{}.py".format(str(i))
#         with open(exeFileName, 'w') as f:
#             f.write("#!/bin/bash\n\n")
#             f.write("source TransferProject/myenv/bin/activate\n\n")
#             f.write("python3 {}\n".format(py_filename))
#             #fstring=literal string interpolation, interpolate values inside{}
            
#         shutil.copy("/Users/sabrinawang/Desktop/Cameron_Project/find_ks.py",py_filename)
#         with open(py_filename, 'r') as f:
#             content = f.read()
#             content = content.replace("k1_1 in ks","k1_1 in [{k11}]")
#             content = content.replace("k1_2 in ks","k1_2 in [{k12}]")
#         with open(py_filename, 'w') as f:     
#             f.write(content)
            
#         with open(oneSubmitFileName, 'a') as f:
#             f.write("MYEXE= {}\n".format(exeFileName))
#             f.write("MYNAME = {}\n".format("findk1s_"+str(i)))
#             f.write("MYINPUT = /afs/cern.ch/work/s/sawang/public/project/macro.madx, /afs/cern.ch/work/s/sawang/public/project/ft_q26.str, /afs/cern.ch/work/s/sawang/public/project/sps1.seq, {},  {}\n".format(mad_filename,py_filename))
#             f.write("queue\n\n")
        
#         os.chdir('/Users/sabrinawang/Desktop/Cameron_Project')

# if __name__ == "__main__": #execute code when file runs as script not imported as module
#     main()

# #%%

# def main():
#     k31 = [-0.9, -1.2, -1.5, -1.8,-2.1,-2.4] 
    
#     k32 = [-0.9, -1.2, -1.5, -1.8,-2.1,-2.4] 
#     folder = "./submit/1232Qx_248/"
#     flavour = "longlunch"
#     os.chdir(folder)
#     os.mkdir("out")
#     os.mkdir("err")
#     os.mkdir("log")
#     oct_name = "LOE.12002,LOEN.32002"
#     qx= 26.248

    
#     oneSubmitFileName = "track.sub"
#     with open(oneSubmitFileName, 'w') as ff:
#             ff.write("universe = vanilla\n")
#             ff.write("executable = $(MYEXE)\n\n")
#             ff.write("output = out/$(MYNAME)_$(ClusterId).$(ProcId).out\n")
#             ff.write("error = err/$(MYNAME)_$(ClusterId).$(ProcId).err\n")
#             ff.write("log = log/$(MYNAME)_$(ClusterId).$(ProcId).log\n\n")
#             ff.write("transfer_input_files = $(MYINPUT)\n\n")
#             ff.write('+AccountingGroup = "group_u_BE.ABP.normal"\n')
#             ff.write('+JobFlavour = "{}"\n\n'.format(flavour))
    
#     for idx in range(len(k31)):
#         exeFileName = "K3="+str(k31[idx])+'_'+str(k32[idx])+".sh"
#         mad_filename = "K3="+str(k31[idx])+'_'+str(k32[idx])+".madx"
#         py_filename = "K3="+str(k31[idx])+'_'+str(k32[idx])+".py"
        
#         with open(exeFileName, 'w') as f:
#             f.write("#!/bin/bash\n\n")
#             f.write("source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh\n")
#             f.write("source /afs/cern.ch/work/s/sawang/public/project/myenv/bin/activate\n\n")
#             f.write("python3 {}\n".format(py_filename))
#             #fstring=literal string interpolation, interpolate values inside{}
        
       

#         with open(py_filename, 'r') as f:
#             content = f.read()
#             content = content.replace("job=","job="+"'"+str(mad_filename)+"'")
#         with open(py_filename, 'w') as f:     
#             f.write(content)
            
#         with open(oneSubmitFileName, 'a') as f:
#             f.write("MYEXE= {}\n".format(exeFileName))
#             f.write("MYNAME = {}\n".format("JOB"+str(idx)))
#             f.write("MYINPUT = /afs/cern.ch/work/s/sawang/public/project/macro.madx, /afs/cern.ch/work/s/sawang/public/project/ft_q26.str, /afs/cern.ch/work/s/sawang/public/project/sps1.seq, {},  {}\n".format(mad_filename,py_filename))
#             f.write("queue\n\n")
#     os.chdir('/home/sawang/Desktop/Project/Sabrina-Project/')
#     # os.chdir("/Users/sabo4ever/Sabrina/EPFL/Project")
# if __name__ == "__main__": #execute code when file runs as script not imported as module
#     main()