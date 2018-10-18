# day
import multiprocessing

import matplotlib.pyplot as plt
from Calf import ModelData, BaseModel
import numpy as np
import datetime as dt
import pandas as pd
stock_codes=['603999', '603998', '603996', '603993', '603991', '603990', '603989', '603988', '603987', '603986', '603985', '603980', '603979', '603978', '603977', '603976', '603970', '603969', '603966', '603963', '603960', '603959', '603958', '603955', '603939', '603938', '603937', '603936', '603933', '603929', '603928', '603926', '603922', '603920', '603919', '603918', '603917', '603916', '603912', '603909', '603908', '603906', '603903', '603901', '603900', '603899', '603898', '603897', '603896', '603895', '603890', '603889', '603888', '603887', '603886', '603885', '603883', '603882', '603881', '603879', '603878', '603877', '603876', '603871', '603869', '603868', '603866', '603861', '603860', '603859', '603858', '603856', '603855', '603848', '603843', '603839', '603833', '603829', '603828', '603826', '603823', '603822', '603819', '603818', '603817', '603816', '603813', '603811', '603809', '603808', '603806', '603803', '603801', '603800', '603799', '603798', '603797', '603789', '603788', '603787', '603779', '603778', '603777', '603776', '603773', '603768', '603767', '603766', '603758', '603757', '603738', '603737', '603733', '603730', '603729', '603728', '603727', '603726', '603725', '603722', '603721', '603718', '603717', '603716', '603713', '603712', '603711', '603709', '603708', '603707', '603706', '603703', '603701', '603699', '603698', '603696', '603693', '603690', '603689', '603688', '603686', '603685', '603683', '603680', '603679', '603678', '603677', '603676', '603669', '603668', '603667', '603666', '603665', '603663', '603661', '603660', '603659', '603658', '603657', '603656', '603655', '603650', '603648', '603639', '603638', '603637', '603633', '603630', '603628', '603626', '603619', '603618', '603617', '603616', '603615', '603612', '603611', '603609', '603608', '603607', '603606', '603605', '603603', '603602', '603601', '603600', '603599', '603598', '603596', '603595', '603589', '603588', '603587', '603586', '603585', '603580', '603579', '603578', '603577', '603569', '603568', '603567', '603566', '603559', '603558', '603557', '603556', '603555', '603538', '603536', '603535', '603533', '603528', '603527', '603520', '603519', '603518', '603517', '603516', '603515', '603508', '603507', '603506', '603505', '603500', '603499', '603496', '603488', '603486', '603477', '603466', '603458', '603456', '603444', '603429', '603421', '603416', '603399', '603398', '603396', '603393', '603389', '603388', '603387', '603385', '603383', '603380', '603378', '603377', '603369', '603368', '603367', '603366', '603365', '603363', '603360', '603359', '603358', '603357', '603356', '603355', '603348', '603345', '603339', '603338', '603337', '603336', '603335', '603333', '603331', '603330', '603329', '603328', '603326', '603323', '603322', '603321', '603320', '603319', '603318', '603316', '603315', '603313', '603311', '603309', '603308', '603306', '603305', '603303', '603301', '603300', '603299', '603298', '603289', '603288', '603286', '603283', '603278', '603277', '603269', '603268', '603266', '603260', '603259', '603258', '603239', '603238', '603233', '603232', '603229', '603228', '603227', '603226', '603225', '603223', '603222', '603218', '603214', '603208', '603203', '603200', '603199', '603198', '603197', '603196', '603189', '603188', '603186', '603183', '603181', '603180', '603179', '603178', '603177', '603169', '603168', '603167', '603166', '603165', '603161', '603160', '603159', '603158', '603157', '603156', '603139', '603138', '603136', '603133', '603131', '603129', '603128', '603127', '603126', '603123', '603118', '603117', '603116', '603113', '603111', '603110', '603108', '603106', '603105', '603103', '603101', '603100', '603099', '603098', '603096', '603090', '603089', '603088', '603086', '603085', '603083', '603081', '603080', '603079', '603078', '603077', '603076', '603069', '603067', '603066', '603063', '603059', '603058', '603056', '603055', '603050', '603045', '603043', '603042', '603041', '603040', '603039', '603038', '603037', '603036', '603035', '603033', '603032', '603031', '603030', '603029', '603028', '603027', '603026', '603025', '603023', '603022', '603021', '603020', '603019', '603018', '603017', '603015', '603013', '603012', '603011', '603010', '603009', '603008', '603007', '603006', '603005', '603003', '603002', '603001', '603000', '601999', '601998', '601997', '601996', '601992', '601991', '601990', '601989', '601988', '601985', '601969', '601968', '601966', '601965', '601958', '601952', '601949', '601939', '601933', '601929', '601928', '601919', '601918', '601908', '601901', '601900', '601899', '601898', '601890', '601888', '601886', '601882', '601881', '601880', '601878', '601877', '601872', '601869', '601866', '601858', '601857', '601838', '601828', '601818', '601811', '601808', '601801', '601800', '601799', '601798', '601789', '601788', '601777', '601766', '601718', '601717', '601700', '601699', '601689', '601688', '601678', '601677', '601669', '601668', '601666', '601636', '601633', '601628', '601619', '601618', '601616', '601611', '601608', '601607', '601606', '601601', '601600', '601599', '601595', '601588', '601579', '601567', '601566', '601558', '601555', '601519', '601518', '601515', '601500', '601398', '601388', '601377', '601375', '601369', '601368', '601366', '601360', '601339', '601336', '601333', '601330', '601328', '601326', '601318', '601311', '601288', '601258', '601238', '601233', '601231', '601229', '601228', '601226', '601225', '601222', '601218', '601216', '601212', '601211', '601208', '601200', '601199', '601198', '601186', '601179', '601177', '601169', '601168', '601166', '601163', '601158', '601155', '601139', '601138', '601137', '601128', '601127', '601126', '601117', '601116', '601113', '601111', '601108', '601107', '601106', '601101', '601100', '601099', '601098', '601088', '601086', '601069', '601066', '601058', '601038', '601028', '601021', '601020', '601019', '601018', '601016', '601015', '601012', '601011', '601010', '601009', '601008', '601007', '601006', '601005', '601003', '601002', '601001', '601000', '600999', '600998', '600997', '600996', '600995', '600993', '600992', '600990', '600988', '600987', '600986', '600985', '600984', '600983', '600982', '600981', '600980', '600979', '600978', '600977', '600976', '600975', '600973', '600971', '600970', '600969', '600967', '600966', '600965', '600963', '600962', '600961', '600960', '600959', '600958', '600939', '600936', '600933', '600929', '600926', '600919', '600917', '600909', '600908', '600903', '600901', '600900', '600898', '600897', '600896', '600895', '600894', '600893', '600892', '600891', '600890', '600889', '600888', '600887', '600886', '600885', '600884', '600883', '600882', '600881', '600880', '600879', '600877', '600876', '600875', '600874', '600873', '600872', '600871', '600870', '600869', '600868', '600867', '600866', '600865', '600864', '600863', '600862', '600861', '600860', '600859', '600858', '600857', '600856', '600855', '600854', '600853', '600851', '600847', '600846', '600845', '600843', '600841', '600839', '600838', '600837', '600836', '600835', '600834', '600833', '600831', '600830', '600829', '600828', '600827', '600826', '600825', '600824', '600823', '600822', '600821', '600820', '600819', '600818', '600817', '600816', '600815', '600814', '600812', '600810', '600809', '600808', '600807', '600805', '600804', '600803', '600802', '600801', '600798', '600797', '600795', '600794', '600793', '600792', '600791', '600790', '600789', '600787', '600785', '600784', '600783', '600782', '600781', '600780', '600779', '600778', '600777', '600776', '600775', '600774', '600773', '600771', '600770', '600769', '600767', '600765', '600763', '600761', '600760', '600758', '600757', '600756', '600755', '600754', '600753', '600750', '600749', '600748', '600747', '600746', '600744', '600743', '600742', '600741', '600740', '600739', '600738', '600737', '600736', '600735', '600734', '600732', '600731', '600730', '600729', '600728', '600727', '600726', '600725', '600723', '600722', '600721', '600720', '600719', '600718', '600717', '600716', '600715', '600714', '600713', '600712', '600711', '600710', '600708', '600707', '600706', '600705', '600704', '600703', '600702', '600699', '600698', '600697', '600696', '600695', '600694', '600693', '600692', '600691', '600690', '600689', '600688', '600686', '600685', '600684', '600683', '600682', '600681', '600679', '600677', '600676', '600675', '600674', '600673', '600671', '600668', '600667', '600666', '600665', '600664', '600663', '600662', '600661', '600660', '600658', '600657', '600655', '600654', '600653', '600652', '600651', '600650', '600649', '600648', '600647', '600645', '600644', '600643', '600642', '600640', '600639', '600638', '600637', '600636', '600635', '600634', '600633', '600630', '600629', '600628', '600626', '600624', '600623', '600622', '600621', '600620', '600619', '600618', '600617', '600616', '600615', '600614', '600613', '600612', '600611', '600610', '600609', '600608', '600606', '600605', '600604', '600603', '600602', '600601', '600600', '600599', '600598', '600597', '600596', '600595', '600594', '600593', '600592', '600590', '600589', '600588', '600587', '600586', '600585', '600584', '600583', '600582', '600581', '600580', '600579', '600578', '600577', '600576', '600575', '600573', '600572', '600571', '600570', '600569', '600568', '600567', '600566', '600565', '600563', '600562', '600561', '600560', '600559', '600558', '600557', '600556', '600555', '600552', '600551', '600550', '600549', '600548', '600547', '600546', '600545', '600543', '600540', '600539', '600538', '600537', '600536', '600535', '600533', '600532', '600531', '600530', '600529', '600528', '600527', '600526', '600525', '600523', '600522', '600521', '600520', '600519', '600518', '600517', '600516', '600513', '600512', '600511', '600510', '600509', '600508', '600507', '600505', '600503', '600502', '600501', '600500', '600499', '600498', '600497', '600496', '600495', '600493', '600491', '600489', '600488', '600487', '600486', '600483', '600482', '600481', '600480', '600479', '600478', '600477', '600476', '600475', '600470', '600469', '600468', '600467', '600466', '600463', '600462', '600461', '600460', '600459', '600458', '600456', '600455', '600452', '600449', '600448', '600446', '600444', '600439', '600438', '600436', '600435', '600433', '600429', '600428', '600426', '600425', '600422', '600420', '600419', '600418', '600416', '600415', '600410', '600409', '600408', '600406', '600405', '600403', '600400', '600398', '600397', '600396', '600395', '600393', '600392', '600391', '600390', '600389', '600388', '600387', '600386', '600385', '600383', '600382', '600381', '600380', '600379', '600378', '600377', '600376', '600375', '600373', '600372', '600371', '600370', '600369', '600368', '600367', '600366', '600365', '600363', '600362', '600361', '600360', '600359', '600358', '600356', '600355', '600354', '600353', '600352', '600351', '600350', '600348', '600346', '600345', '600343', '600340', '600339', '600338', '600337', '600336', '600333', '600332', '600331', '600330', '600329', '600328', '600327', '600326', '600325', '600323', '600322', '600321', '600320', '600319', '600317', '600316', '600315', '600313', '600312', '600311', '600310', '600309', '600308', '600307', '600306', '600305', '600303', '600302', '600300', '600299', '600298', '600297', '600295', '600292', '600291', '600290', '600289', '600288', '600287', '600285', '600284', '600283', '600282', '600281', '600280', '600279', '600278', '600277', '600276', '600275', '600273', '600272', '600271', '600270', '600269', '600268', '600267', '600266', '600262', '600261', '600260', '600259', '600258', '600257', '600256', '600255', '600252', '600251', '600250', '600249', '600248', '600247', '600246', '600243', '600242', '600241', '600240', '600239', '600238', '600237', '600236', '600235', '600234', '600233', '600231', '600230', '600229', '600228', '600227', '600225', '600223', '600222', '600221', '600220', '600219', '600218', '600216', '600215', '600213', '600212', '600211', '600210', '600209', '600208', '600207', '600206', '600203', '600202', '600201', '600200', '600199', '600198', '600197', '600196', '600195', '600193', '600192', '600191', '600190', '600189', '600188', '600187', '600186', '600185', '600184', '600183', '600182', '600180', '600179', '600178', '600177', '600176', '600173', '600172', '600171', '600170', '600169', '600168', '600167', '600166', '600165', '600163', '600162', '600161', '600160', '600159', '600158', '600156', '600155', '600153', '600152', '600151', '600150', '600149', '600148', '600143', '600141', '600139', '600138', '600137', '600136', '600135', '600133', '600132', '600131', '600130', '600129', '600128', '600127', '600126', '600125', '600123', '600121', '600120', '600119', '600118', '600117', '600116', '600115', '600114', '600113', '600112', '600111', '600110', '600109', '600108', '600107', '600106', '600105', '600104', '600103', '600101', '600100', '600099', '600098', '600097', '600096', '600095', '600094', '600093', '600091', '600090', '600089', '600088', '600085', '600084', '600083', '600082', '600081', '600080', '600079', '600078', '600077', '600076', '600075', '600074', '600073', '600072', '600071', '600070', '600069', '600068', '600067', '600066', '600064', '600063', '600062', '600061', '600060', '600059', '600058', '600057', '600056', '600055', '600054', '600053', '600052', '600051', '600050', '600048', '600039', '600038', '600037', '600036', '600035', '600033', '600031', '600030', '600029', '600028', '600027', '600026', '600025', '600023', '600021', '600020', '600019', '600018', '600017', '600016', '600015', '600012', '600011', '600010', '600009', '600008', '600007', '600006', '600004', '600000', '300750', '300747', '300746', '300745', '300743', '300742', '300741', '300739', '300738', '300737', '300736', '300735', '300733', '300732', '300731', '300730', '300729', '300727', '300726', '300725', '300723', '300722', '300721', '300720', '300719', '300718', '300717', '300716', '300715', '300713', '300712', '300711', '300710', '300709', '300708', '300707', '300706', '300705', '300703', '300702', '300701', '300700', '300699', '300698', '300697', '300696', '300695', '300693', '300692', '300691', '300690', '300689', '300688', '300687', '300686', '300685', '300684', '300683', '300682', '300681', '300680', '300679', '300678', '300677', '300676', '300675', '300673', '300672', '300671', '300669', '300668', '300667', '300666', '300665', '300664', '300663', '300662', '300661', '300660', '300659', '300658', '300657', '300656', '300655', '300654', '300653', '300652', '300651', '300650', '300649', '300648', '300647', '300645', '300644', '300643', '300642', '300641', '300640', '300639', '300638', '300637', '300636', '300635', '300634', '300633', '300632', '300631', '300630', '300629', '300628', '300627', '300626', '300625', '300624', '300623', '300622', '300621', '300620', '300619', '300618', '300617', '300616', '300615', '300613', '300612', '300611', '300610', '300609', '300608', '300607', '300606', '300605', '300604', '300602', '300601', '300600', '300599', '300598', '300597', '300596', '300595', '300593', '300592', '300591', '300590', '300589', '300588', '300587', '300586', '300585', '300584', '300583', '300582', '300581', '300580', '300579', '300578', '300577', '300576', '300575', '300573', '300572', '300571', '300570', '300569', '300568', '300567', '300566', '300565', '300563', '300562', '300561', '300560', '300559', '300558', '300557', '300556', '300555', '300554', '300553', '300552', '300551', '300550', '300549', '300548', '300547', '300546', '300545', '300543', '300542', '300541', '300540', '300539', '300538', '300537', '300536', '300535', '300534', '300533', '300532', '300531', '300530', '300529', '300528', '300527', '300526', '300525', '300523', '300522', '300521', '300519', '300518', '300517', '300516', '300515', '300514', '300513', '300512', '300511', '300509', '300508', '300507', '300506', '300505', '300504', '300503', '300502', '300501', '300500', '300499', '300498', '300497', '300496', '300495', '300494', '300493', '300492', '300491', '300490', '300489', '300488', '300487', '300486', '300485', '300484', '300483', '300482', '300481', '300480', '300479', '300478', '300477', '300476', '300475', '300474', '300473', '300472', '300471', '300470', '300469', '300468', '300467', '300466', '300465', '300464', '300463', '300462', '300461', '300460', '300459', '300458', '300457', '300456', '300455', '300454', '300453', '300452', '300451', '300450', '300449', '300448', '300447', '300446', '300445', '300444', '300443', '300442', '300441', '300440', '300439', '300438', '300437', '300436', '300435', '300434', '300433', '300432', '300431', '300430', '300429', '300428', '300427', '300426', '300425', '300424', '300423', '300422', '300421', '300420', '300419', '300418', '300417', '300416', '300415', '300414', '300413', '300412', '300411', '300410', '300409', '300408', '300407', '300406', '300405', '300404', '300403', '300402', '300401', '300400', '300399', '300398', '300397', '300396', '300395', '300394', '300393', '300392', '300391', '300390', '300389', '300388', '300387', '300386', '300385', '300384', '300383', '300382', '300381', '300380', '300379', '300378', '300377', '300376', '300375', '300374', '300373', '300371', '300370', '300369', '300368', '300367', '300366', '300365', '300364', '300363', '300360', '300359', '300358', '300357', '300356', '300355', '300354', '300353', '300352', '300351', '300350', '300349', '300348', '300347', '300346', '300345', '300344', '300342', '300341', '300340', '300339', '300338', '300337', '300336', '300335', '300334', '300333', '300332', '300331', '300330', '300329', '300328', '300327', '300326', '300325', '300323', '300322', '300321', '300320', '300319', '300318', '300317', '300316', '300315', '300314', '300313', '300312', '300311', '300310', '300309', '300308', '300307', '300306', '300305', '300304', '300303', '300301', '300300', '300299', '300298', '300297', '300296', '300295', '300294', '300293', '300292', '300291', '300290', '300289', '300288', '300287', '300286', '300285', '300284', '300283', '300282', '300281', '300280', '300279', '300278', '300277', '300276', '300275', '300274', '300273', '300272', '300271', '300270', '300269', '300268', '300267', '300266', '300265', '300264', '300263', '300262', '300261', '300260', '300259', '300258', '300257', '300256', '300255', '300254', '300253', '300252', '300251', '300250', '300249', '300248', '300247', '300246', '300245', '300244', '300242', '300241', '300240', '300239', '300238', '300237', '300236', '300235', '300234', '300233', '300232', '300231', '300230', '300229', '300228', '300227', '300226', '300225', '300224', '300223', '300222', '300221', '300220', '300219', '300218', '300217', '300216', '300215', '300214', '300213', '300212', '300211', '300210', '300209', '300208', '300207', '300206', '300205', '300204', '300203', '300202', '300201', '300200', '300199', '300198', '300196', '300195', '300194', '300193', '300192', '300191', '300190', '300189', '300188', '300185', '300184', '300183', '300182', '300181', '300180', '300179', '300178', '300177', '300176', '300175', '300174', '300173', '300172', '300171', '300170', '300169', '300168', '300167', '300166', '300165', '300164', '300163', '300162', '300161', '300160', '300159', '300158', '300157', '300156', '300155', '300154', '300153', '300152', '300151', '300150', '300149', '300148', '300147', '300146', '300145', '300144', '300143', '300142', '300141', '300140', '300139', '300138', '300137', '300136', '300135', '300134', '300133', '300132', '300130', '300129', '300128', '300127', '300126', '300125', '300124', '300123', '300122', '300121', '300120', '300119', '300117', '300116', '300115', '300114', '300113', '300112', '300110', '300109', '300107', '300106', '300105', '300104', '300103', '300102', '300101', '300100', '300099', '300098', '300097', '300096', '300095', '300094', '300093', '300092', '300091', '300090', '300089', '300088', '300087', '300086', '300085', '300084', '300083', '300082', '300081', '300080', '300079', '300078', '300077', '300076', '300075', '300074', '300073', '300072', '300071', '300070', '300069', '300068', '300067', '300066', '300065', '300064', '300063', '300062', '300061', '300059', '300058', '300057', '300056', '300055', '300054', '300053', '300052', '300051', '300050', '300049', '300048', '300047', '300046', '300045', '300044', '300043', '300042', '300041', '300040', '300039', '300038', '300037', '300036', '300035', '300034', '300033', '300032', '300031', '300030', '300029', '300028', '300027', '300026', '300025', '300024', '300023', '300022', '300021', '300020', '300019', '300018', '300017', '300016', '300015', '300014', '300013', '300012', '300011', '300010', '300009', '300008', '300007', '300006', '300005', '300004', '300003', '300002', '300001', '002932', '002931', '002930', '002929', '002928', '002927', '002926', '002925', '002923', '002922', '002921', '002920', '002919', '002918', '002917', '002916', '002915', '002913', '002912', '002911', '002910', '002909', '002908', '002907', '002906', '002905', '002903', '002902', '002901', '002900', '002899', '002898', '002897', '002896', '002895', '002893', '002892', '002891', '002890', '002889', '002888', '002887', '002886', '002885', '002884', '002883', '002882', '002881', '002880', '002879', '002878', '002877', '002875', '002873', '002872', '002871', '002870', '002869', '002868', '002867', '002866', '002865', '002864', '002863', '002862', '002861', '002860', '002859', '002858', '002857', '002855', '002853', '002852', '002851', '002850', '002849', '002848', '002847', '002846', '002845', '002843', '002842', '002841', '002840', '002839', '002838', '002837', '002836', '002835', '002833', '002832', '002831', '002830', '002829', '002828', '002827', '002826', '002825', '002824', '002823', '002822', '002821', '002820', '002818', '002817', '002816', '002815', '002813', '002812', '002811', '002810', '002809', '002808', '002807', '002806', '002805', '002803', '002802', '002801', '002800', '002799', '002798', '002797', '002796', '002795', '002793', '002792', '002791', '002790', '002789', '002788', '002787', '002786', '002785', '002783', '002782', '002781', '002780', '002779', '002778', '002777', '002776', '002775', '002774', '002773', '002772', '002771', '002770', '002769', '002768', '002767', '002766', '002765', '002763', '002762', '002761', '002760', '002759', '002758', '002757', '002756', '002755', '002753', '002752', '002751', '002750', '002749', '002748', '002747', '002746', '002745', '002743', '002742', '002741', '002740', '002738', '002737', '002736', '002735', '002734', '002733', '002732', '002731', '002730', '002729', '002728', '002727', '002726', '002725', '002724', '002722', '002721', '002718', '002717', '002715', '002714', '002713', '002712', '002711', '002709', '002708', '002707', '002706', '002705', '002703', '002702', '002701', '002700', '002699', '002698', '002697', '002696', '002695', '002694', '002693', '002692', '002691', '002690', '002688', '002687', '002686', '002685', '002684', '002683', '002682', '002681', '002680', '002679', '002678', '002677', '002676', '002675', '002673', '002672', '002671', '002670', '002669', '002667', '002666', '002664', '002663', '002662', '002661', '002660', '002659', '002658', '002657', '002655', '002654', '002653', '002652', '002651', '002649', '002648', '002647', '002646', '002645', '002644', '002643', '002642', '002641', '002640', '002639', '002638', '002637', '002636', '002635', '002634', '002633', '002632', '002631', '002629', '002628', '002627', '002626', '002625', '002624', '002623', '002622', '002621', '002620', '002619', '002618', '002616', '002615', '002614', '002613', '002612', '002611', '002609', '002608', '002607', '002606', '002605', '002604', '002603', '002601', '002600', '002599', '002598', '002597', '002596', '002595', '002594', '002593', '002592', '002591', '002590', '002589', '002588', '002587', '002586', '002585', '002584', '002583', '002582', '002581', '002580', '002579', '002578', '002577', '002576', '002575', '002574', '002572', '002571', '002570', '002568', '002567', '002566', '002565', '002564', '002563', '002562', '002561', '002560', '002559', '002557', '002556', '002555', '002554', '002553', '002552', '002551', '002550', '002549', '002548', '002547', '002546', '002545', '002544', '002543', '002542', '002541', '002540', '002539', '002538', '002537', '002536', '002535', '002534', '002533', '002532', '002531', '002530', '002529', '002528', '002527', '002526', '002524', '002523', '002522', '002521', '002520', '002519', '002518', '002517', '002516', '002515', '002514', '002513', '002511', '002510', '002509', '002508', '002507', '002506', '002505', '002504', '002503', '002501', '002500', '002499', '002498', '002497', '002496', '002495', '002494', '002493', '002492', '002491', '002490', '002489', '002488', '002487', '002486', '002484', '002483', '002482', '002481', '002480', '002479', '002478', '002476', '002475', '002474', '002472', '002471', '002470', '002469', '002468', '002467', '002466', '002465', '002463', '002462', '002461', '002460', '002458', '002457', '002456', '002455', '002454', '002453', '002452', '002451', '002449', '002448', '002447', '002446', '002444', '002443', '002442', '002441', '002440', '002439', '002438', '002435', '002434', '002433', '002432', '002430', '002429', '002428', '002427', '002426', '002425', '002424', '002423', '002422', '002421', '002420', '002419', '002418', '002417', '002416', '002415', '002414', '002413', '002412', '002410', '002409', '002407', '002406', '002405', '002404', '002403', '002402', '002401', '002400', '002399', '002398', '002397', '002396', '002395', '002394', '002393', '002392', '002391', '002390', '002389', '002388', '002387', '002386', '002385', '002384', '002383', '002382', '002381', '002380', '002379', '002378', '002377', '002376', '002375', '002374', '002373', '002372', '002371', '002370', '002368', '002367', '002366', '002365', '002364', '002363', '002362', '002361', '002360', '002358', '002357', '002356', '002355', '002354', '002353', '002352', '002351', '002350', '002349', '002348', '002347', '002346', '002345', '002344', '002343', '002342', '002341', '002340', '002339', '002338', '002337', '002336', '002335', '002334', '002333', '002332', '002331', '002330', '002329', '002328', '002327', '002326', '002325', '002324', '002322', '002321', '002320', '002318', '002317', '002316', '002315', '002314', '002313', '002312', '002311', '002309', '002308', '002307', '002306', '002305', '002304', '002303', '002302', '002301', '002300', '002299', '002298', '002297', '002296', '002295', '002294', '002293', '002292', '002291', '002290', '002289', '002288', '002287', '002286', '002285', '002284', '002283', '002282', '002281', '002280', '002279', '002278', '002277', '002276', '002275', '002274', '002273', '002272', '002271', '002270', '002269', '002268', '002267', '002266', '002265', '002264', '002262', '002261', '002260', '002259', '002258', '002256', '002255', '002254', '002253', '002251', '002250', '002249', '002248', '002247', '002246', '002245', '002244', '002243', '002242', '002241', '002240', '002238', '002237', '002236', '002235', '002234', '002233', '002232', '002231', '002230', '002229', '002228', '002227', '002225', '002224', '002223', '002222', '002221', '002220', '002219', '002218', '002217', '002216', '002215', '002214', '002213', '002212', '002211', '002209', '002208', '002207', '002206', '002205', '002204', '002203', '002202', '002201', '002200', '002199', '002198', '002197', '002196', '002195', '002194', '002193', '002192', '002191', '002190', '002189', '002188', '002187', '002186', '002185', '002184', '002183', '002182', '002181', '002180', '002179', '002178', '002177', '002176', '002175', '002174', '002173', '002172', '002170', '002169', '002168', '002167', '002166', '002165', '002164', '002163', '002162', '002161', '002160', '002159', '002158', '002157', '002156', '002155', '002154', '002153', '002152', '002151', '002150', '002149', '002148', '002146', '002145', '002144', '002143', '002142', '002141', '002140', '002139', '002138', '002137', '002136', '002135', '002134', '002133', '002132', '002131', '002130', '002129', '002128', '002127', '002126', '002125', '002124', '002123', '002122', '002121', '002120', '002119', '002118', '002117', '002116', '002115', '002114', '002112', '002111', '002110', '002109', '002108', '002107', '002106', '002105', '002104', '002103', '002101', '002100', '002099', '002097', '002096', '002095', '002094', '002093', '002092', '002091', '002090', '002089', '002088', '002087', '002085', '002084', '002083', '002082', '002081', '002080', '002079', '002078', '002077', '002076', '002074', '002073', '002072', '002071', '002069', '002068', '002067', '002066', '002065', '002064', '002063', '002062', '002061', '002060', '002058', '002057', '002056', '002055', '002054', '002053', '002052', '002050', '002049', '002048', '002047', '002046', '002045', '002044', '002043', '002042', '002041', '002040', '002039', '002038', '002037', '002036', '002035', '002034', '002033', '002032', '002031', '002030', '002029', '002028', '002027', '002026', '002025', '002024', '002023', '002022', '002021', '002020', '002019', '002018', '002017', '002016', '002015', '002014', '002013', '002012', '002010', '002009', '002008', '002007', '002006', '002005', '002004', '002003', '002002', '002001', '001979', '001965', '001896', '001696', '000999', '000998', '000997', '000996', '000995', '000993', '000990', '000989', '000988', '000987', '000985', '000983', '000982', '000981', '000980', '000979', '000978', '000977', '000976', '000975', '000973', '000971', '000970', '000969', '000968', '000967', '000966', '000965', '000963', '000962', '000961', '000960', '000959', '000958', '000957', '000955', '000953', '000952', '000951', '000949', '000948', '000939', '000938', '000937', '000936', '000935', '000933', '000932', '000931', '000930', '000929', '000928', '000927', '000926', '000925', '000923', '000922', '000921', '000920', '000919', '000918', '000917', '000915', '000913', '000911', '000910', '000909', '000908', '000906', '000905', '000903', '000902', '000901', '000900', '000899', '000898', '000897', '000895', '000893', '000892', '000890', '000889', '000888', '000887', '000886', '000885', '000883', '000882', '000881', '000880', '000878', '000877', '000876', '000875', '000869', '000868', '000863', '000862', '000861', '000860', '000859', '000858', '000856', '000852', '000851', '000850', '000848', '000839', '000838', '000837', '000836', '000835', '000833', '000831', '000830', '000829', '000828', '000826', '000823', '000822', '000821', '000820', '000819', '000818', '000816', '000815', '000813', '000812', '000811', '000810', '000809', '000807', '000806', '000803', '000802', '000801', '000800', '000799', '000798', '000797', '000796', '000795', '000793', '000792', '000791', '000790', '000789', '000788', '000786', '000785', '000783', '000782', '000780', '000778', '000777', '000776', '000768', '000767', '000766', '000762', '000761', '000760', '000759', '000758', '000757', '000756', '000755', '000753', '000752', '000751', '000750', '000739', '000738', '000737', '000736', '000735', '000733', '000732', '000731', '000729', '000728', '000727', '000726', '000725', '000723', '000722', '000721', '000720', '000719', '000718', '000717', '000716', '000715', '000713', '000712', '000710', '000709', '000708', '000707', '000705', '000703', '000702', '000701', '000700', '000698', '000697', '000692', '000691', '000690', '000688', '000687', '000686', '000685', '000683', '000682', '000681', '000680', '000679', '000678', '000677', '000676', '000673', '000672', '000671', '000670', '000669', '000668', '000667', '000665', '000663', '000662', '000661', '000659', '000657', '000656', '000655', '000652', '000651', '000650', '000639', '000638', '000637', '000636', '000635', '000633', '000632', '000631', '000630', '000628', '000627', '000626', '000625', '000623', '000622', '000620', '000619', '000617', '000616', '000615', '000613', '000612', '000610', '000609', '000608', '000607', '000606', '000605', '000601', '000600', '000599', '000598', '000597', '000596', '000595', '000593', '000592', '000591', '000590', '000589', '000587', '000586', '000585', '000584', '000582', '000581', '000576', '000573', '000572', '000571', '000570', '000568', '000567', '000566', '000565', '000564', '000563', '000561', '000560', '000559', '000558', '000557', '000555', '000554', '000553', '000552', '000551', '000550', '000548', '000547', '000546', '000544', '000543', '000541', '000539', '000538', '000537', '000536', '000534', '000533', '000532', '000531', '000530', '000529', '000528', '000525', '000524', '000523', '000521', '000520', '000519', '000518', '000517', '000516', '000514', '000513', '000510', '000509', '000507', '000506', '000505', '000504', '000503', '000502', '000501', '000498', '000488', '000430', '000429', '000428', '000425', '000423', '000422', '000421', '000420', '000419', '000418', '000417', '000416', '000415', '000413', '000411', '000410', '000409', '000408', '000407', '000404', '000403', '000402', '000401', '000400', '000338', '000333', '000301', '000166', '000159', '000158', '000157', '000156', '000155', '000153', '000151', '000150', '000100', '000099', '000096', '000090', '000089', '000088', '000078', '000070', '000069', '000068', '000066', '000065', '000063', '000062', '000061', '000060', '000059', '000058', '000056', '000055', '000050', '000049', '000046', '000045', '000043', '000042', '000040', '000039', '000037', '000036', '000035', '000034', '000032', '000031', '000030', '000028', '000027', '000026', '000025', '000023', '000022', '000021', '000020', '000019', '000018', '000017', '000016', '000014', '000012', '000011', '000010', '000009', '000007', '000006', '000005', '000004', '000002', '000001']
stock_codes=pd.DataFrame(dict(stock_code=stock_codes))
class Hot:
    def hot_day(self, date):
        data = ModelData.read_data(table_name='kline_day', field=['stock_code', 'close', 'open'], date=date)
        data = data.drop(['_id'], axis=1)
        data['profit'] = data.close / data.open - 1
        data['profit'] = data[abs(data.profit) < 0.11].profit
        data['pro'] = data.profit.map(lambda x: True if x > 0 else False)
        data = data.dropna()
        # data=data[0:56*56]

        arr = np.array(data.pro.tolist() + [0] * (64 * 64 - len(data))).reshape(64, 64)
        # ax = sns.heatmap(arr, vmin=-0.03, vmax=0.03,cbar=False)
        plt.matshow(arr, cmap='hot')
        plt.show()

    def hot_min(self, date, time, kline):
        data = ModelData.read_data(table_name=kline, field=['stock_code', 'close', 'open'], date=date, time=time)
        if len(data)<=0 and time==1130:
            data = ModelData.read_data(table_name=kline, field=['stock_code', 'close', 'open'], date=date, time=1300)


        data = data.drop(['_id'], axis=1)
        data['profit'] = data.close / data.open - 1
        data['profit'] = data[abs(data.profit) < 0.11].profit
        data['pro']=data.profit
        # data['pro'] = data.profit.map(lambda x: 1 if x > 0 else 0)
        data = data.dropna()
        data=pd.merge(stock_codes,data,on=['stock_code'])
        data=data.fillna(0)
        # print(data.stock_code.tolist())
        # data=data[0:56*56]
        arr = np.array(data.pro.tolist() + [0] * (64 * 64 - len(data))).reshape(64, 64)
        # ax = sns.heatmap(arr, vmin=-0.03, vmax=0.03,cbar=False)
        # plt.matshow(arr, cmap='hot')
        # plt.show()
        BaseModel('hot_min5_version4').insert_batch(dict(date=date, time=time, value=arr.tolist()))


def fun(data):
    for i, r in data.iterrows():
        try:
            print('date', r.date, 'time', r.time)
            Hot().hot_min(date=r.date, time=r.time, kline='kline_min5')
        except Exception as e:
            print(e)
# Hot().hot_day(date=dt.datetime(2018,8,1))


if __name__ == '__main__':

    data = ModelData.read_data(table_name='kline_min5', field=['date', 'time'], stock_code='000001',
                           date={'$gte': dt.datetime(2016, 1, 1),'$lte': dt.datetime(2018, 8, 6)})
    m=10
    # data=data[0:1]
    li = [data[i:i + m] for i in range(0, len(data), m)]
    pool=multiprocessing.Pool(processes=3)
    pool.map(fun,li)

