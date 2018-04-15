var p1_score = 0;
var p2_score = 0;
var p1_enable = true;
var p2_enable = true;
var wait = false;
var nameA = "";
var nameB = "";

newQuestion();

function post_answer(u, ans) {
    console.log(ans);
    $.ajax("/answermulti", {dataType:"json", method:"POST", data:{user: u, answer: ans}}).done(function (data) {
        console.log(data);
        if (data['correct'] === false ){
            if (u === 1){
                p1_enable = false;
                $('#button_p1').attr("class", "btn btn-danger");
            }
            else if(u === 2){
                p2_enable = false;
                $('#button_p2').attr("class", "btn btn-danger");
            }
            if (!p1_enable && !p2_enable){
                $('#button_p1').attr("class", "btn btn-danger");
                $('#button_p2').attr("class", "btn btn-danger");
                // alert("tudo mal");
                newQuestion();
            }
        }
        else if (data['correct'] === true){
            if (u === 1){
                p1_score++;
                $("#p1_score").html(p1_score);
                $('#button_p1').attr("class", "btn btn-success");
            }
            else if(u === 2){
                p2_score++;
                $("#p2_score").html(p2_score);
                $('#button_p2').attr("class", "btn btn-success");
            }
            if(ans === nameA)
                $('#cardA').css({'backgroundColor': 'LightGreen'});
            else
                $('#cardB').css({'backgroundColor': 'LightGreen'});
            if(p1_score >= 10) {
                $("#winner").html("Player 1 wins!");
                $('#popup').modal('show');
                window.removeEventListener("keypress", key_handle);
            }
            else if(p2_score >= 10) {
                $("#winner").html("Player 2 wins!");
                $('#popup').modal('show');
                window.removeEventListener("keypress", key_handle);
            }
            else {
                newQuestion();
            }
        }
        wait = false;

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
    if(code === 'a' && p1_enable && !wait){ //a
        wait = true;
        //p1
        //A
        post_answer(1, nameA);
    }
    else if (code === 's' && p1_enable && !wait){ //s
        wait = true;
        //p1
        //B
        post_answer(1, nameB);
    }
    else if(code === 'k' && p2_enable && !wait){ //k
        wait = true;
        //p2
        //A
        post_answer(2, nameA);
    }
    else if(code === 'l' && p2_enable && !wait){ //l
        wait = true;
        //p2
        //B
        post_answer(2, nameB);
    }
}

function newQuestion() {
    $.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
        console.log(data);
        nameA = data['A'].name;
        nameB = data['B'].name;
        var a_url = data['A'].image_url;
        var b_url = data['B'].image_url;
        $("#p1_score").html(p1_score);
        $("#p2_score").html(p2_score);
        $('#A').html(data['A'].name);
        $('#A').val(data['A'].name);
        $('#B').html(data['B'].name);
        $('#B').val(data['B'].name);
        $('#imgA').attr("src", a_url);
        $('#imgB').attr("src", b_url);
        $('#nomeA').html(nameA);
        $('#nomeB').html(nameB);
        p1_enable = true;
        p2_enable = true;
        $('#cardA').css({'backgroundColor': 'LightGoldenRodYellow'});
        $('#cardB').css({'backgroundColor': 'LightGoldenRodYellow'});
        $('#button_p1').attr("class", "btn btn-outline-primary");
        $('#button_p2').attr("class", "btn btn-outline-warning");
    }).fail(function () {
        console.log("erro");
    });
}
window.addEventListener("keydown", key_handle);