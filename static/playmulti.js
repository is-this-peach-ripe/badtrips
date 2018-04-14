var p1_score = 0;
var p2_score = 0;
var p1_enable = true;
var p2_enable = true;

$.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
    console.log(data);
    $("#p1_score").html(p1_score);
    $("#p2_score").html(p2_score);
    $('#A').html(data['A'].name);
    $('#A').val(data['A'].name);
    $('#B').html(data['B'].name);
    $('#B').val(data['B'].name);
    p1_enable = true;
    p2_enable = true;
}).fail(function () {
    console.log("erro");
});

function post_answer(u, ans) {
    console.log(ans);
    $.ajax("/answermulti", {dataType:"json", method:"POST", data:{user: u, answer: ans}}).done(function (data) {
        console.log(data);
        if (data['correct'] === false ){
            if (u === 1){
                p2_enable = true;
                p1_enable = false;
            }
            else if(u === 2){
                p1_enable = true;
                p2_enable = false;
            }
        }
        else {
            if (u === 1){
                p1_score++;
                $("#p1_score").html("Player 1: " + p1_score);
            }
            else if(u === 2){
                p2_score++;
                $("#p2_score").html("Player 2: " + p2_score);
            }
        }
    });
}

function get_leaderboard() {
    $.ajax("/leaderboard", {datatype:"json", method:"POST"}).done(function (data) {
        console.log(data);
    })
}

function key_handle(e) {
    var code = e.keyCode ? e.keyCode : e.which;
    console.log(code);
    if(code === 1 && p1_enable){
        p2_enable = false;
        //p1
        //A
        post_answer(1, $('#A').val());
    }
    else if (code === 2 && p1_enable){
        p2_enable = false;
        //p1
        //B
        post_answer(1, $('#B').val());
    }
    else if(code === 3 && p2_enable){
        p1_enable = false;
        //p2
        //A
        post_answer(2, $('#A').val());
    }
    else if(code === 4 && p2_enable){
        p1_enable = false;
        //p2
        //B
        post_answer(2, $('#B').val());
    }
}

window.addEventListener("keypress", key_handle);