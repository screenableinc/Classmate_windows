import os
dire=os.listdir("C:\Windows\debug\WIA\[R.G. Catalyst] Devil May Cry 4\\")
inte = 0
for i in dire:
    try:
        os.rename("C:\Windows\debug\WIA\[R.G. Catalyst] Devil May Cry 4\\"+i,"C:\Windows\debug\WIA\[R.G. Catalyst] Devil May Cry 4\\"+str(inte)+".dty")
    except:
        continue
    inte=inte+1