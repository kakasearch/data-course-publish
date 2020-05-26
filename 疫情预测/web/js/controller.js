function getTime() {
    var date = new Date();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    var second =date.getSeconds();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    if (second >= 1 && second <= 9) {
        second = "0" + second;
    }
    var currentDate = date.getFullYear() + "年" + month + "月" + strDate
            + " " + date.getHours() + ":" + date.getMinutes() + ":" + second;
    $("#tim").html(currentDate)
}
function get_c1_data() { $.ajax({ url: "c1.json", dataType: "json",success: function(data) { $(".num h1").eq(0).text(data.confirm);
            $(".num h1").eq(1).text(data.suspect);
            $(".num h1").eq(2).text(data.heal);
            $(".num h1").eq(3).text(data.dead);
            $(".txt h2").eq(0).text("累计确诊");
            $(".txt h2").eq(1).text("剩余疑似");
            $(".txt h2").eq(2).text("累计治愈");
            $(".txt h2").eq(3).text("累计死亡") } }) }


function get_l1_data() { $.ajax({ url: "l1.json", dataType: "json",success: function(data) { ec_left1_Option.xAxis[0].data = data.day;
            ec_left1_Option.series[0].data = data.confirm;
            ec_left1_Option.series[1].data = data.suspect;
            ec_left1_Option.series[2].data = data.heal;
            ec_left1_Option.series[3].data = data.dead;
            ec_left1.setOption(ec_left1_Option) } }) }

function get_l2_data() { $.ajax({ url: "l2.json", dataType: "json",success: function(data) { ec_left2_Option.xAxis[0].data = data.day;
            ec_left2_Option.series[0].data = data.confirm_add;
            ec_left2_Option.series[1].data = data.suspect_add;
            ec_left2_Option.series[2].data = data.heal_add;
            ec_left2_Option.series[3].data = data.dead_add;
            ec_left2.setOption(ec_left2_Option) }, error: function(xhr, type, errorThrown) {} }) }

function get_r1_data() { $.ajax({ url: "r1.json", dataType: "json",success: function(data) { ec_right1_option.xAxis.data = data.city;
            ec_right1_option.series[0].data = data.confirm;
            ec_right1.setOption(ec_right1_option) } }) }

function get_r2_data() { $.ajax({ url: "r2.json", dataType: "json",success: function(data) { ec_right2_option.series[0].data = data.kws;
            ec_right2.setOption(ec_right2_option) } }) }
get_c1_data();
get_l1_data();
get_l2_data();
get_r1_data();
get_r2_data();
setInterval(getTime, 1000);
window.addEventListener("resize", function() { ec_left1.resize();
    ec_left2.resize();
    ec_center.resize();
    ec_right1.resize();
    ec_right2.resize() });