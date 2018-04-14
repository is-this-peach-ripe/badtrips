var score = 0;

newQuestion();

function post_answer(bt) {
    console.log(bt);
    $.ajax("/answer", {dataType:"json", method:"POST", data:{answer: bt.value}}).done(function (data) {
        console.log(data);
        if (data['correct'] === false ){
            window.alert("gameover\nfinal score: " + score);
        }
        else {
            score++;
            newQuestion();
        }
    });
}

function get_leaderboard() {
    $.ajax("/leaderboard", {datatype:"json", method:"POST"}).done(function (data) {
        console.log(data);
    })
}

function newQuestion() {
    $.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
        console.log(data);
    var a_url = data['A'].image_url;
    var b_url = data['B'].image_url;
    $('#imgA').attr("src", a_url);
    $('#imgB').attr("src", b_url);
    $("#score").html(score);
    $('#nomeA').html(data['A'].name);
    $('#A').val(data['A'].name);
    $('#nomeB').html(data['B'].name);
    $('#B').val(data['B'].name);
    }).fail(function () {
        console.log("erro");
    });
}