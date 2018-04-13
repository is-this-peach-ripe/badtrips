
$.ajax("/newquestion").done(function (data) {
    console.log(data);
}).fail(function () {
    console.log("erro");
});