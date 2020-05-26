		function getoptions(obj){
			options=[]
			for(var k = 0, pl = obj['date'].length; k<pl; k++ ){
				day=obj['date'][k]
				temp={
					backgroundColor: "",
			        title: {
			        	 text: '四川地区口罩短缺预测 '+day,
			        		x: "left"        },
			        	tooltip: {
			        		            trigger: 'item',
			        		            formatter: function(p) {
											
													  let str = p.name + '<br/>' + (p.value=='1'?'短缺':'充足')
													  return  str
													}
			        		        },
			        	toolbox: {
			        		            show: true,
			        		            orient: 'vertical',
			        		            left: 'right',
			        		            top: 'center',
			        		            feature: {
			        		                dataView: {readOnly: false},
			        		                restore: {},
			        		                saveAsImage: {}
			        		            }
			        		        },
			        	visualMap: {
			        		            min: 0,
			        		            max: 1,
			        		            //text: ['短缺', '充足'],
			        		            showLabel:true,  
			        		            realtime: false,
			        		            calculable: false,//true,
			        		            top: 420,
			        		            splitList: [{
 											    start: -0.5,
 											    end: 0.5,
 											    label:'充足'
 											}, {
 											    start: 0.5,
 											    end: 1.5,	
 											    label:'短缺'
 											},],
			        		            inRange: {
			        		                color:["#ffe8e8","#ff6f6f"],
			        		            }
			        		        },
				    series: [{
        name: "累计确诊人数",
        type: "map",
        mapType: "sc",
        roam: false,
        itemStyle: {
            normal: {
                borderColor: "rgba(0, 0, 0, 0.2)",
            },
            emphasis: {
                borderWidth: 0.5,
                borderColor: "#4b0082",
                areaColor: "#c7fffd",
            }
        },
        label: {
            normal: {
                show: true,
                fontSize: 8,
            },
            emphasis: {
                show: true,
                fontSize: 8,
            }
        },
        data: obj[day],
    }]
				}
				options.push(temp)
			}
			return options
		}
		////////////
		function dataFormatter(obj) {
		    for (var k = 0, pl = obj['date'].length; k<pl; k++ ) {
				day=obj['date'][k]
		        obj[day]=[];
		        for (var i = 0, l = obj['citys'].length; i < l; i++) {
					var pname=obj['citys'][i]
		            obj[day][i] = {
		                name: pname,
		                value:obj["data"][pname][k],
		            };
		        }
		    }
		    return obj;
			}
			/////////////////
		
		futuredata=''
		 $.ajax({
		             type: "GET",
		             url: "future.json",
		             dataType: "json",
		             success: function(data){
						 futuredata=data
						 console.log(data)
						 
						 futuredata= dataFormatter(futuredata)
						 
						 var myChart = echarts.init(document.getElementById("c2"), "dark")
						 myChart.showLoading();
						 $.get('map/四川.json', function (geoJson) {
						 
						     myChart.hideLoading();
						 
						     echarts.registerMap('sc', geoJson);
						 
						     myChart.setOption(option = {
						 		timeline: {
						 		    axisType: 'category',
						 		    // realtime: false,
						 		    // loop: false,
						 		    autoPlay: true,
						 		    // currentIndex: 2,
						 		    playInterval: 1000,
						 		    // controlStyle: {
						 		    //     position: 'left'
						 		    // },
						 		    data: futuredata['date'],
						 		    label: {
						 		        formatter : function(s) {
						 		            return (new Date(s)).getMonth()+1+"-"+(new Date(s)).getDate();
						 		        }
						 		    }
						 		},
						 	options: getoptions(futuredata),
						     });
						 });
					 },
					 })
		