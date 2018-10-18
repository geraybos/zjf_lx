# -*- coding: utf-8 -*-

from app.actions import f_zjh_ttm_a, f_zybk_ttm_a, f_zz_ttm_a
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer
def change_date(t):
    print(t.year*10000+t.month*100+t.day)
    return  t.year*10000+t.month*100+t.day
if __name__ == '__main__':
    t=Calendar.today()
    print('t',t)
    t2=Calendar.calc(t,-1)['date']
    print('t2', t2)
    sd = change_date(t2)
    ed = change_date(t)
    dql = analyzer('date >= {} and date <= {}'.format(sd, ed))
    for i in ['fund_zz_ttm', 'fund_zjh_ttm', 'fund_zybk_ttm']:
        model_list[i].remove(dql)
    f_zz_ttm_a(start_date=sd,end_date=ed)
    f_zjh_ttm_a(p_type='zjh',start_date=sd,end_date=ed)
    f_zybk_ttm_a(start_date=sd,end_date=ed)

