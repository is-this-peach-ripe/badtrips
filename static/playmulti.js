var p1_score = 0;
var p2_score = 0;
var p1_enable = true;
var p2_enable = true;

newQuestion();

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
            if (!p1_enable && !p2_enable){
                alert("tudo mal");
                newQuestion();
            }
        }
        else if (data['correct'] === true){
            if (u === 1){
                p1_score++;
                $("#p1_score").html("Player 1: " + p1_score);
            }
            else if(u === 2){
                p2_score++;
                $("#p2_score").html("Player 2: " + p2_score);
            }
            newQuestion();
        }
    });
}

function get_leaderboard() {
    $.ajax("/leaderboard", {datatype:"json", method:"POST"}).done(function (data) {
        console.log(data);
    })
}

function key_handle(e) {
    var code = e.key;
    console.log(e);
    if(code === 'a' && p1_enable){ //a
        p2_enable = false;
        //p1
        //A
        post_answer(1, $('#A').val());
    }
    else if (code === 's' && p1_enable){ //s
        p2_enable = false;
        //p1
        //B
        post_answer(1, $('#B').val());
    }
    else if(code === 'k' && p2_enable){ //k
        p1_enable = false;
        //p2
        //A
        post_answer(2, $('#A').val());
    }
    else if(code === 'l' && p2_enable){ //l
        p1_enable = false;
        //p2
        //B
        post_answer(2, $('#B').val());
    }
}

function newQuestion() {
    $.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
        console.log(data);
        $("#p1_score").html("Player 1: " + p1_score);
        $("#p2_score").html("Player 2: " + p2_score);
        $('#A').html(data['A'].name);
        $('#A').val(data['A'].name);
        $('#B').html(data['B'].name);
        $('#B').val(data['B'].name);
        p1_enable = true;
        p2_enable = true;
    }).fail(function () {
        console.log("erro");
    });
}
window.addEventListener("keypress", key_handle);