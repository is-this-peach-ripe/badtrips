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
        $("#score").html(score);
        $('#A').html(data['A'].name);
        $('#A').val(data['A'].name);
        $('#B').html(data['B'].name);
        $('#B').val(data['B'].name);
    }).fail(function () {
        console.log("erro");
    });
}