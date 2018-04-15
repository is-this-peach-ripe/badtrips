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
            if(bt==='a')
                $('#cardA').css({'backgroundColor': 'IndianRed'});
            else
                $('#cardB').css({'backgroundColor': 'IndianRed'});
            //window.alert("gameover\nfinal score: " + score);
            get_leaderboard();
        }
        else {
            if(bt==='a') {
                $('#cardA').css({'backgroundColor': 'LightGreen'});
                if(data['review'] != null) {
                    $( "#nomeA" ).fadeIn( "slow", function() {
                        var stars = ""
                        var i;
                        for(i = 0; i < data['review']['rating']; i++) {
                            stars += "★";
                        }[]
                        $('#nomeA').css({'font-size': '2.5vh', 'font-style': 'italic'});
                        $('#buttonA').hide()
                        $('#nomeA').html(stars + "</br>\"" + data['review']['text'] + "\"</br>- " + data['review']['user']['name']); 
                    });
                }
            }
            else {
                $('#cardB').css({'backgroundColor': 'LightGreen'});
                if(data['review'] != null) {
                    $( "#nomeB" ).fadeIn( "slow", function() {
                        var stars = ""
                        var i;
                        for(i = 0; i < data['review']['rating']; i++) {
                            stars += "★";
                        }
                        $('#nomeB').css({'font-size': '2.5vh', 'font-style': 'italic'});
                        $('#buttonB').hide()
                        $('#nomeB').html(stars + "</br>" + data['review']['text'] + "</br>- " + data['review']['user']['name']); 
                    });
                }
            }
            score++;
            setTimeout(function(){
                newQuestion();
            }, 3000);
            

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
        $('#nomeA').css({'font-size': ""});
        $('#nomeB').css({'font-size': ""});
        $('#buttonA').show()
        $('#buttonB').show()
        $('#cardA').css({'backgroundColor': 'LightGoldenRodYellow'});
        $('#cardB').css({'backgroundColor': 'LightGoldenRodYellow'});

    }).fail(function () {
        console.log("erro");
    });
}

