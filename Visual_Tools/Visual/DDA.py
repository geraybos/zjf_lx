class DDA:
    @classmethod
    def draw_line(cls,point):
        x1=point[0][0]
        x2=point[1][0]
        y1=point[0][1]
        y2=point[1][1]
        dx=x2-x1
        dy=y2-y1
        step=max(dx,dy)
        xin=dx/step
        yin=dy/step
        x=x1
        y=y1
        x_list=list()
        y_list=list()
        for i in range(step+1):
            print(i)
            x_list.append(int(x+0.5))
            y_list.append(int(y))
            x=(x+xin)
            y=(y+yin)

        return x_list,y_list

