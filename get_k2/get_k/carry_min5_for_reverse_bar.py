# -*- coding: utf-8 -*-

from app.models import model_list, Calendar

if __name__ == '__main__':
    cbj = model_list['tmp_kline_min5']
    cbj.remove_all()
    t = Calendar.today()
    kbj = model_list['kline_min5']
    # kbj.copyto(cbj, condition={'date': Calendar.calc(t, -1)['date']}) # 补数据
    kbj.copyto(cbj, condition={'date': t})
    print('done')
