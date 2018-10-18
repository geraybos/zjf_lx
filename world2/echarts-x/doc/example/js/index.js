$(function () {
    echart_1();
    echart_2();

    echart_3();
    echart_4();

    echart_map();
    echart_5();

    //echart_1河北货物收入
    function echart_1() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart_1'));
        option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c}万元"
            },
            legend: {
                x: 'center',
                y: '15%',
                data: [ 'Taiwan', 'U.S.A', 'Germany','Malaysia', 'Italy', 'Britain','Brazil','Turkey', 'France'],
                icon: 'circle',
                textStyle: {
                    color: '#fff',
                }
            },
            calculable: true,
            series: [{
                name: '',
                type: 'pie',
                //起始角度，支持范围[0, 360]
                startAngle: 0,
                //饼图的半径，数组的第一项是内半径，第二项是外半径
                radius: [41, 100.75],
                //支持设置成百分比，设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
                center: ['50%', '40%'],
                //是否展示成南丁格尔图，通过半径区分数据大小。可选择两种模式：
                // 'radius' 面积展现数据的百分比，半径展现数据的大小。
                //  'area' 所有扇区面积相同，仅通过半径展现数据大小
                roseType: 'area',
                //是否启用防止标签重叠策略，默认开启，圆环图这个例子中需要强制所有标签放在中心位置，可以将该值设为 false。
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: true,
                        formatter: '{c}'
                    },
                    emphasis: {
                        show: true
                    }
                },
                labelLine: {
                    normal: {
                        show: true,
                        length2: 1,
                    },
                    emphasis: {
                        show: true
                    }
                },
                data: [{
                        value: 101687*100,
                        name: 'Taiwan',
                        itemStyle: {
                            normal: {
                                color: '#f845f1'
                            }
                        }
                    },
                    {
                        value: 65776*100,
                        name: 'U.S.A',
                        itemStyle: {
                            normal: {
                                color: '#ad46f3'
                            }
                        }
                    },
                    {
                        value: 27259*100,
                        name: 'Germany',
                        itemStyle: {
                            normal: {
                                color: '#5045f6'
                            }
                        }
                    },
                    {
                        value: 25006*100,
                        name: 'Malaysia',
                        itemStyle: {
                            normal: {
                                color: '#4777f5'
                            }
                        }
                    },
                    {
                        value: 22526*100,
                        name: 'Italy',
                        itemStyle: {
                            normal: {
                                color: '#44aff0'
                            }
                        }
                    },
                    {
                        value: 22019*100,
                        name: 'Britain',
                        itemStyle: {
                            normal: {
                                color: '#45dbf7'
                            }
                        }
                    },
                    {
                        value: 21936*100,
                        name: 'Brazil',
                        itemStyle: {
                            normal: {
                                color: '#f6d54a'
                            }
                        }
                    },
                    {
                        value: 20688*100,
                        name: 'Turkey',
                        itemStyle: {
                            normal: {
                                color: '#f69846'
                            }
                        }
                    },
                    {
                        value: 17784*100,
                        name: 'France',
                        itemStyle: {
                            normal: {
                                color: '#ff4343'
                            }
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    {
                        value: 0,
                        name: "",
                        itemStyle: {
                            normal: {
                                color: 'transparent'
                            }
                        },
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    }
                ]
            }]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

    //echart_2河北省地图
    function echart_2() {
           // 基于准备好的dom，初始化echarts实例
           var myChart = echarts.init(document.getElementById('chart_2'));
           function showProvince() {
                   myChart.setOption(option = {
                       // backgroundColor: '#ffffff',
                       visualMap: {
                           show: false,
                           min: 0,
                           max: 45000,
                           left: 'left',
                           top: 'bottom',
                           text: ['高', '低'], // 文本，默认为数值文本
                           calculable: true,
                           inRange: {
                               color: ['red']
                           }
                       },
                       series: [{
                           type: 'map',
                           mapType: 'china',
                           roam: true,
                           label: {
                               normal: {
                                   show: false
                               },
                               emphasis: {
                                   textStyle: {
                                       color: '#fff'
                                   }
                               }
                           },
                           itemStyle: {
                               normal: {
                                   borderColor: '#389BB7',
                                   areaColor: '#fff',
                               },
                               emphasis: {
                                   areaColor: '#389BB7',
                                   borderWidth: 0
                               }
                           },
                           animation: false,
                           data: [
						      {name: '香港', value: 28397.812},
						      {name: '重庆', value: 28397.812},
							  {name: '上海', value: 19549.124},
							  {name: '北京', value: 19549.124},
							  {name: '广东', value: 19549.124},
							  {name: '澳门', value: 3150.143},
							  {name: 'Taiwan', value: 3150.143},
							]
                       }]
                   });
           }
   
           var currentIdx = 0;
           showProvince();
           // 使用刚指定的配置项和数据显示图表。
           window.addEventListener("resize", function () {
               myChart.resize();
           });
    }

    // echart_map中国地图
    function echart_map() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart_map'));

        var mapName = 'china'
        var data = []
        var toolTipData = [];

        /*获取地图数据*/
        myChart.showLoading();
        var mapFeatures = echarts.getMap(mapName).geoJson.features;
        myChart.hideLoading();
        var geoCoordMap = {
            '福州': [119.4543, 25.9222],
            '长春': [125.8154, 44.2584],
            '重庆': [107.7539, 30.1904],
            '西安': [109.1162, 34.2004],
            '成都': [103.9526, 30.7617],
            '常州': [119.4543, 31.5582],
            '北京': [116.4551, 40.2539],
            '北海': [109.314, 21.6211],
            '海口': [110.3893, 19.8516],
            '石家庄': [114.48, 38.03],
            '上海': [121.40, 31.73],
            '内蒙古': [106.82, 39.67]
        };

        var GZData = [
            [{
                name: '石家庄'
            }, {
                name: '福州',
                value: 95
            }],
            [{
                name: '石家庄'
            }, {
                name: '长春',
                value: 80
            }],
            [{
                name: '石家庄'
            }, {
                name: '重庆',
                value: 70
            }],
            [{
                name: '石家庄'
            }, {
                name: '西安',
                value: 60
            }],
            [{
                name: '石家庄'
            }, {
                name: '成都',
                value: 50
            }],
            [{
                name: '石家庄'
            }, {
                name: '常州',
                value: 40
            }],
            [{
                name: '石家庄'
            }, {
                name: '北京',
                value: 30
            }],
            [{
                name: '石家庄'
            }, {
                name: '北海',
                value: 20
            }],
            [{
                name: '石家庄'
            }, {
                name: '海口',
                value: 10
            }],
            [{
                name: '石家庄'
            }, {
                name: '上海',
                value: 80
            }],
            [{
                name: '石家庄'
            }, {
                name: '内蒙古',
                value: 80
            }]
        ];

        var convertData = function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var dataItem = data[i];
                var fromCoord = geoCoordMap[dataItem[0].name];
                var toCoord = geoCoordMap[dataItem[1].name];
                if (fromCoord && toCoord) {
                    res.push({
                        fromName: dataItem[0].name,
                        toName: dataItem[1].name,
                        coords: [fromCoord, toCoord]
                    });
                }
            }
            return res;
        };

        var color = ['#c5f80e'];
        var series = [];
        [
            ['石家庄', GZData]
        ].forEach(function (item, i) {
            series.push({
                name: item[0],
                type: 'lines',
                zlevel: 2,
                symbol: ['none', 'arrow'],
                symbolSize: 10,
                effect: {
                    show: true,
                    period: 6,
                    trailLength: 0,
                    symbol: 'arrow',
                    symbolSize: 5
                },
                lineStyle: {
                    normal: {
                        color: color[i],
                        width: 1,
                        opacity: 0.6,
                        curveness: 0.2
                    }
                },
                data: convertData(item[1])
            }, {
                name: item[0],
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 2,
                rippleEffect: {
                    brushType: 'stroke'
                },
                label: {
                    normal: {
                        show: true,
                        position: 'right',
                        formatter: '{b}'
                    }
                },
                symbolSize: function (val) {
                    return val[2] / 8;
                },
                itemStyle: {
                    normal: {
                        color: color[i]
                    }
                },
                data: item[1].map(function (dataItem) {
                    return {
                        name: dataItem[1].name,
                        value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value])
                    };
                })
            });
        });

        option = {
            tooltip: {
                trigger: 'item'
            },
            geo: {
                map: 'china',
                label: {
                    emphasis: {
                        show: false
                    }
                },
                roam: true,
                itemStyle: {
                    normal: {
                        borderColor: 'rgba(147, 235, 248, 1)',
                        borderWidth: 1,
                        areaColor: {
                            type: 'radial',
                            x: 0.5,
                            y: 0.5,
                            r: 0.8,
                            colorStops: [{
                                offset: 0,
                                color: 'rgba(175,238,238, 0)' // 0% 处的颜色
                            }, {
                                offset: 1,
                                color: 'rgba(47,79,79, .1)' // 100% 处的颜色
                            }],
                            globalCoord: false // 缺省为 false
                        },
                        shadowColor: 'rgba(128, 217, 248, 1)',
                        // shadowColor: 'rgba(255, 255, 255, 1)',
                        shadowOffsetX: -2,
                        shadowOffsetY: 2,
                        shadowBlur: 10
                    },
                    emphasis: {
                        areaColor: '#389BB7',
                        borderWidth: 0
                    }
                }
            },
            series: series
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });

    }

    //echart_3货物周转量
    function echart_3() {
        // 基于准备好的dom，初始化echarts实例
		var data=['Taiwan','U.S.A','Turkey','Italy','Malaysia','France'];
        var myChart = echarts.init(document.getElementById('chart_3'));
        myChart.clear();
        option = {
            title: {
                text: ''
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:data,
                textStyle:{
                    color: '#fff'
                },
                top: '8%'
            },
            grid: {
                top: '40%',
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            color: ['#FF4949','#FFA74D','#FFEA51','#4BF0FF','#44AFF0','#4E82FF','#584BFF','#BE4DFF','#F845F1'],
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: ['Mon','Tues','Wednes','Thurs','Fri'],
                splitLine: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
            },
            yAxis: {
                name: '',
                type: 'value',
                splitLine: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
            },
            series: [
                {
                    name:data[0],
                    type:'line',
                    data:[3961.88, 4233.63, 4183.14, 3633.01, 3704.47]
                },
                {
                    name:data[1],
                    type:'line',
                    data:[3374.76, 3364.76, 3274.76, 3371.82, 3259.87]
                },
                {
                    name:data[2],
                    type:'line',
                    data:[14.77, 15.17, 13.17, 14.56, 15.84]
                },
                {
                    name:data[3],
                    type:'line',
                    data:[686.17,847.26,895.22,865.28,886.72]
                },
                {
                    name:data[4],
                    type:'line',
                    data:[6133.47, 6577.89, 7019.56,6821.48,7294.59]
                },
                {
                    name:data[5],
                    type:'line',
                    data:[509.60, 862.54, 1481.77,1552.79,1333.62]
                }
            ]
        };
        myChart.setOption(option);
    }
    //河北高速公路
    function echart_4() {
        // 基于准备好的dom，初始化echarts实例
		var data=['丹麦', '挪威', '孟加拉国', '苏格兰'];
        var myChart = echarts.init(document.getElementById('chart_4'));

        option = {
    color: ['#003366', '#006699', '#4cabce', '#e5323e'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['丹麦', '挪威', '孟加拉国', '苏格兰'],
		 textStyle:{
                    color: '#fff'
                },
                top: '8%'
    },
    toolbox: {
        show: false,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            axisTick: {show: false},
            data: ['Mon', 'Tues', 'Wednes', 'Thurs', 'Fri'],
			axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
        }
    ],
    yAxis: [
        {
            type: 'value',
			 axisLine: {
                    lineStyle: {
                        color: '#fff'
                    }
                }
        }
    ],
    series: [
        {
            name: data[0],
            type: 'bar',
            barGap: 0,
            
            data: [320, 332, 301, 334, 390]
        },
        {
            name:  data[1],
            type: 'bar',
        
            data: [220, 182, 191, 234, 290]
        },
        {
            name:  data[2],
            type: 'bar',
           
            data: [150, 232, 201, 154, 190]
        },
        {
            name:  data[3],
            type: 'bar',
           
            data: [98, 77, 101, 99, 40]
        }
    ]
};
        
        myChart.setOption(option);

    }
    //河北省铁路
    function echart_5() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart_5'));
       //加载地图
           myChart.setOption({
               series: [{
                   type: 'map',
                   mapType: 'hebei'
               }]
           });

           var geoCoordMap = {
               '平山县': [114.1860500000,38.2599800000],
               '黄骅港站': [117.8486210772,38.2751643094],
               '南峪站': [113.943052,37.995488],
               '衡水站': [115.69794,37.74976],
               '涉县站': [113.674745,36.583286],
               '邯郸站': [114.482678,36.609077],
               '大名站': [115.108242,36.501907],
               '涿州站': [115.990812,39.48681],
               '保定站': [115.48644,38.869177],
               '石家庄': [114.489909,38.017389],
               '固安站': [116.330216,39.430955],
               '清河城站': [115.692921,37.070002],
               '青县站': [116.844816,38.583399],
               '吴桥站': [116.393252,37.633478],
               '张家口站': [114.895239,40.819243],
               '承德站': [117.962201,40.970432],
               '秦皇岛站': [119.591222,39.966179],
               '唐山站': [118.118024,39.817085],
           };

           var goData = [
               [{
                   name: '平山县'

               }, {
                   id: 1,
                   name: '黄骅港站',
                   value: 20
               }],
               [{
                   name: '南峪站'

               }, {
                   id: 1,
                   name: '衡水站',
                   value: 50
               }],
               [{
                   name: '涉县站'

               }, {
                   id: 1,
                   name: '邯郸站',
                   value: 60
               }],
               [{
                   name: '邯郸站'

               }, {
                   id: 1,
                   name: '大名站',
                   value: 20
               }],
               [{
                   name: '涉县站'

               }, {
                   id: 1,
                   name: '邯郸站',
                   value: 60
               }],
               [{
                   name: '涿州站'

               }, {
                   id: 1,
                   name: '保定站',
                   value: 90
               }],
               [{
                   name: '保定站'

               }, {
                   id: 1,
                   name: '石家庄',
                   value: 100
               }],
               [{
                   name: '石家庄'

               }, {
                   id: 1,
                   name: '邯郸站',
                   value: 60
               }],
               [{
                   name: '固安站'

               }, {
                   id: 1,
                   name: '衡水站',
                   value: 50
               }],
               [{
                   name: '衡水站'

               }, {
                   id: 1,
                   name: '清河城站',
                   value: 20
               }],
               [{
                   name: '青县站'

               }, {
                   id: 1,
                   name: '吴桥站',
                   value: 20
               }],
               [{
                   name: '张家口站'

               }, {
                   id: 1,
                   name: '承德站',
                   value: 90
               }],
               [{
                   name: '唐山站'

               }, {
                   id: 1,
                   name: '秦皇岛站',
                   value: 90
               }],
               [{
                   name: '张家口站'

               }, {
                   id: 1,
                   name: '唐山站',
                   value: 90
               }]
           ];
           //值控制圆点大小
           var backData = [
               [{
                   name: '黄骅港站'
               }, {
                   id: 2,
                   name: '平山县',
                   value: 20
               }],
               [{
                   name: '衡水站'
               }, {
                   id: 2,
                   name: '南峪站',
                   value: 20
               }],
               [{
                   name: '邯郸站'

               }, {
                   id: 1,
                   name: '涉县站',
                   value: 20
               }],
               [{
                   name: '大名站'

               }, {
                   id: 1,
                   name: '邯郸站',
                   value: 90
               }],
               [{
                   name: '保定站'

               }, {
                   id: 1,
                   name: '涿州站',
                   value: 20
               }],
               [{
                   name: '石家庄'

               }, {
                   id: 1,
                   name: '保定站',
                   value: 90
               }],
               [{
                   name: '邯郸站'

               }, {
                   id: 1,
                   name: '石家庄',
                   value: 100
               }],
               [{
                   name: '衡水站'

               }, {
                   id: 1,
                   name: '固安站',
                   value: 20
               }],
               [{
                   name: '清河城站'

               }, {
                   id: 1,
                   name: '衡水站',
                   value: 50
               }],
               [{
                   name: '吴桥站'

               }, {
                   id: 1,
                   name: '青县站',
                   value: 20
               }],
               [{
                   name: '承德站'

               }, {
                   id: 1,
                   name: '张家口站',
                   value: 90
               }],
               [{
                   name: '秦皇岛站'

               }, {
                   id: 1,
                   name: '唐山站',
                   value: 90
               }],
               [{
                   name: '唐山站'

               }, {
                   id: 1,
                   name: '张家口站',
                   value: 90
               }]
           ];

           var arcAngle = function(data) {
               var j, k;
               for (var i = 0; i < data.length; i++) {
                   var dataItem = data[i];
                   if (dataItem[1].id == 1) {
                       j = 0.2;
                       return j;
                   } else if (dataItem[1].id == 2) {
                       k = -0.2;
                       return k;
                   }
               }
           }

           var convertData = function(data) {
               var res = [];
               for (var i = 0; i < data.length; i++) {
                   var dataItem = data[i];
                   var fromCoord = geoCoordMap[dataItem[0].name];
                   var toCoord = geoCoordMap[dataItem[1].name];
                   if (dataItem[1].id == 1) {
                       if (fromCoord && toCoord) {
                           res.push([{
                               coord: fromCoord,
                           }, {
                               coord: toCoord,
                               value: dataItem[1].value //线条颜色
                           }]);
                       }
                   } else if (dataItem[1].id == 2) {
                       if (fromCoord && toCoord) {
                           res.push([{
                               coord: fromCoord,
                           }, {
                               coord: toCoord
                           }]);
                       }
                   }
               }
               return res;
           };

           var color = ['#fff', '#FF1493', '#00FF00'];
           var series = [];
           [
               ['1', goData],
               ['2', backData]
           ].forEach(function(item, i) {
               series.push({
                   name: item[0],
                   type: 'lines',
                   zlevel: 2,
                   symbol: ['arrow', 'arrow'],
                   //线特效配置
                   effect: {
                       show: true,
                       period: 6,
                       trailLength: 0.1,
                       symbol: 'arrow', //标记类型
                       symbolSize: 5
                   },
                   lineStyle: {
                       normal: {
                           width: 1,
                           opacity: 0.4,
                           curveness: arcAngle(item[1]), //弧线角度
                           color: '#fff'
                       }
                   },
                   data: convertData(item[1])
               }, {
                   type: 'effectScatter',
                   coordinateSystem: 'geo',
                   zlevel: 2,
                   //波纹效果
                   rippleEffect: {
                       period: 2,
                       brushType: 'stroke',
                       scale: 3
                   },
                   label: {
                       normal: {
                           show: true,
                           color: '#fff',
                           position: 'right',
                           formatter: '{b}'
                       }
                   },
                   //终点形象
                   symbol: 'circle',
                   //圆点大小
                   symbolSize: function(val) {
                       return val[2] / 8;
                   },
                   itemStyle: {
                       normal: {
                           show: true
                       }
                   },
                   data: item[1].map(function(dataItem) {
                       return {
                           name: dataItem[1].name,
                           value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value])
                       };
                   })

               });

           });

           option = {
               title: {
                   text: '',
                   subtext: '',
                   left: 'center',
                   textStyle: {
                       color: '#fff'
                   }
               },
               tooltip: {
                   trigger: 'item',
                   formatter: "{b}"
               },
               //线颜色及飞行轨道颜色
               visualMap: {
                   show: false,
                   min: 0,
                   max: 100,
                   color: ['#fff']
               },
               //地图相关设置
               geo: {
                   map: 'hebei',
                   //视角缩放比例
                   zoom: 1,
                   //显示文本样式
                   label: {
                       normal: {
                           show: false,
                           textStyle: {
                               color: '#fff'
                           }
                       },
                       emphasis: {
                           textStyle: {
                               color: '#fff'
                           }
                       }
                   },
                   //鼠标缩放和平移
                   roam: true,
                   itemStyle: {
                       normal: {
                           //          	color: '#ddd',
                           borderColor: 'rgba(147, 235, 248, 1)',
                           borderWidth: 1,
                           areaColor: {
                               type: 'radial',
                               x: 0.5,
                               y: 0.5,
                               r: 0.8,
                               colorStops: [{
                                   offset: 0,
                                   color: 'rgba(175,238,238, 0)' // 0% 处的颜色
                               }, {
                                   offset: 1,
                                   color: 'rgba(	47,79,79, .2)' // 100% 处的颜色
                               }],
                               globalCoord: false // 缺省为 false
                           },
                           shadowColor: 'rgba(128, 217, 248, 1)',
                           shadowOffsetX: -2,
                           shadowOffsetY: 2,
                           shadowBlur: 10
                       },
                       emphasis: {
                           areaColor: '#389BB7',
                           borderWidth: 0
                       }
                   }
               },
               series: series
           };
           myChart.setOption(option);
    }

    //点击跳转
    $('#chart_map').click(function(){
        window.location.href = './page/index.html';
    });
    $('.t_btn2').click(function(){
        window.location.href = "./page/index.html?id=2";
    });
    $('.t_btn3').click(function(){
        window.location.href = "./page/index.html?id=3";
    });
    $('.t_btn4').click(function(){
        window.location.href = "./page/index.html?id=4";
    });
    $('.t_btn5').click(function(){
        window.location.href = "./page/index.html?id=5";
    });
    $('.t_btn6').click(function(){
        window.location.href = "./page/index.html?id=6";
    });
    $('.t_btn7').click(function(){
        window.location.href = "./page/index.html?id=7";
    });
    $('.t_btn8').click(function(){
        window.location.href = "./page/index.html?id=8";
    });
    $('.t_btn9').click(function(){
        window.location.href = "./page/index.html?id=9";
    });
});
