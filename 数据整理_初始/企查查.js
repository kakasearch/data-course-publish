/*
1.点击省份
2.点击城市
2+。上传数据
3×掉城市
4.差掉省份
5.下一个省份

*/
function info() {
    const arg = Array.from(arguments);
    arg.unshift(`color: white; background-color:#2274A5`);
    arg.unshift('%c qcc-spider:');
    console["info"].apply(console, arg);
}
function prov_click(num) {//省份点击，输入点击的谁

    let provs = document.querySelector("#provinceOld > div:nth-child(2)").getElementsByTagName("a")//每次刷新
    GM_setValue("遍历省份", provs[num].getAttribute("data-append"))
    info('点击省份', provs[num].getAttribute("data-append"))
    provs[num].click()
}
function city_click(num) {//city点击，输入点击的谁
    let citys = document.querySelector("#city_show").getElementsByTagName("a")
    changeHash_(citys[num], true, 1); zhugeTrack('查企业列表页地域筛选', { '筛选值': '城市' });
}
function getdata() {
    let provn = document.querySelector("#appendBox > span.m-l.label.btn-primary.provinceChoosen.appendSpan.clearSpan").innerTex
    let cityn = document.querySelector("#appendBox > span.m-l.label.btn-primary.cityChoosen.appendSpan.clearSpan").innerTex
    let code = /city:(\d+)/.exec(location.href)[1]
    let item_num = document.querySelector("#countOld > span").innerText

    let data = provn + "," + cityn + "," + code + "," + item_num + "\n"
    return data
}

if ((location.href.search('province') < 0) && confirm('开始吗？点击省份')) {
    let provs = document.querySelector("#provinceOld > div:nth-child(2)").getElementsByTagName("a")
    info('开始获取省份', provs)
    for (let num = 0; num < provs.length; num++) {//遍历省份
        provs = document.querySelector("#provinceOld > div:nth-child(2)").getElementsByTagName("a")
        prov_click(num);
        //wait load
        let int_prov = setInterval(function () {

            if (document.querySelector("#countOld")) {//已加载
                clearInterval(int_prov)
                let prov = document.querySelector("#appendBox > span.m-l.label.btn-primary.provinceChoosen.appendSpan.clearSpan")
                let citys = document.querySelector("#city_show").getElementsByTagName("a")
                for (let city_num = 0; city_num < citys.length; city_num++) {//遍历城市
                    city_click(city_num)
                    //wait load
                    let int_city = setInterval(function () {
                        if (document.querySelector("#countOld")) {//已加载
                            clearInterval(int_city)
                            let data = getdata()
                            info('准备上传', data)
                            debugger;
                            GM_xmlhttpRequest({
                                method: "GET",
                                url: "http://localhost:8000/qccspider?data=" + encodeURIComponent(data),
                                onload: function (response) {
                                    info('已上传', data)
                                    //clear city
                                    document.querySelector("#appendBox > span.m-l.label.btn-primary.cityChoosen.appendSpan.clearSpan").click()//关掉城市筛选
                                }
                            })
                        }
                    },5000)


                }
            }

        }, 3000)
        //clear prov
        document.querySelector("#appendBox > span.m-l.label.btn-primary.provinceChoosen.appendSpan.clearSpan").click()

    }

}