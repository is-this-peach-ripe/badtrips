
$.ajax("/newquestion", {dataType:"json", method:"POST"}).done(function (data) {
    console.log(data);
}).fail(function () {
    console.log("erro");
});