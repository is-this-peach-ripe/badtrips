var score = 0;
var valueA;
var valueB;
var gameOverFirst = '<div class=\"card border-danger mb-3 \" style=\"width: 18rem;\">\n' +
    '  <div class=\"card-body\">' +
    '<strong>Game over!</strong>' +
    '<br>You did well on the leaderboard! <i class=\"em em-memo\"></i> <br>';

var gameOverSecond = '</ul><a href="/"><button type=\"button\" class=\"btn btn-success\">Try Again! <i class=\"em em-wink\"></i></button></a>' +
    '</div></div>';
newQuestion();

function post_answer(bt) {
    console.log(bt);
    var value;
    if(bt === 'a') value = valueA;
    else value = valueB;
    $.ajax("/answer", {dataType:"json", method:"POST", data:{answer: value}}).done(function (data) {
        console.log(data);
        if (data['correct'] === false ){
            //window.alert("gameover\nfinal score: " + score);
            get_leaderboard();
        }
        else {
            score++;
            newQuestion();
        }
    });
}

function get_leaderboard() {
    $.ajax("/leaderboard", {datatype:"json", method:"POST"}).done(function (data) {
        var leaderboard = "<ul class=\"list-group\">";
        var li_s = "<li class=\"list-group-item d-flex justify-content-between align-items-center\">";
        var span_s = " <span class=\"badge badge-primary badge-pill\">";
        var end_li = "</span></li>";
        for (game of data){
            leaderboard = leaderboard+li_s+game[0]+span_s+game[1]+end_li;
        }

        var gameOver = gameOverFirst + leaderboard + gameOverSecond;
        $('#alert').html(gameOver);
        console.log(data);
    })
}

function newQuestion() {
    $.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
        console.log(data);
        var a_url = data['A'].image_url;
        var b_url = data['B'].image_url;
        valueA = data['A'].name;
        valueB = data['B'].name;
        $('#imgA').attr("src", a_url);
        $('#imgB').attr("src", b_url);
        $("#score").html(score);
        $('#nomeA').html(valueA);
        $('#A').val(valueA);
        $('#nomeB').html(valueB);
        $('#B').val(valueB);
    }).fail(function () {
        console.log("erro");
    });
}

