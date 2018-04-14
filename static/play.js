var score = 0;

$.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
    console.log(data);
    $("#score").html(score);
    $('#A').html(data['A'].nome);
    $('#A').val(data['A'].nome);
    $('#B').html(data['B'].nome);
    $('#B').val(data['B'].nome);
}).fail(function () {
    console.log("erro");
});

function post_answer(bt) {
    console.log(bt);
    $.ajax("/answer", {dataType:"json", method:"POST", data:{answer: bt.value}}).done(function (data) {
        console.log(data);
        if (data['correct'] === false ){
            window.alert("gameover\nfinal score: " + score);
        }
        else {
            score++;
            $("#score").html(score);
        }
    });
}

function get_leaderboard() {
    $.ajax("/leaderboard", {datatype:"json", method:"POST"}).done(function (data) {
        console.log(data);
    })
}