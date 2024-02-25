import matplotlib.pyplot as plt

def plot_cost(file_list,all_data):
    dpi = 1000
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['savefig.dpi'] = dpi  # 图片像素
    plt.rcParams['figure.dpi'] = dpi  # 分辨率
    plt.rcParams["font.family"] = 'Times New Roman'
    color_list=[]
    for i in range(len(all_data)):
        color=input("请输入文件%s的颜色:"%(file_list[i]))
        color_list.append(color)
    max_len=0;
    for d in all_data:
        if max_len<len(d):
            max_len=len(d)
    x=[]
    for i in range(max_len):
        x.append(i)
    for i in range(len(all_data)):
        d=all_data[i]
        while(len(d)<max_len):
            d.append(float(0))
        plt.plot(x,d,color_list[i])
        # plt.plot(x, d, color_list[i])
    font2 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15,}
    plt.xlabel("epoch",fontdict=font2)
    plt.ylabel("loss",fontdict=font2)
    # plt.savefig("loss3000.png",dpi)
    plt.show()



if __name__ == "__main__":
    file_list=["D:/Workspaces/ECM/yhfexp/yhfexp/yhf/莫烦-Reinforcement-learning-with-tensorflow-master/Reinforcement-learning-with-tensorflow-master/contents/5_Deep_Q_Network/loss.txt"]                  #写入文件名，存入列表
    all_data = []
    for file in file_list:
        with open(file,'r') as f:
            data_list=f.read().split(",")
            data=[]
            for i in range(len(data_list)):
                d=data_list[i]
                if d=='':
                    continue
                # if d==0:
                #     continue
                if i<60000:
                    if i%100==0:
                        data.append(float(d))
            all_data.append(data)
    plot_cost(file_list,all_data)
