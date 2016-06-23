/* Mark answer as chosen */
function mark(endpoint, eid) {
  $.post(endpoint,
    {
      id: eid, 
      csrfmiddlewaretoken: $.cookie('csrftoken')
    },
    update
  );
  function update(result){
    if (result != "None") {
      if (result == "True") {
        $("span.question__no__answer").html("Has answer!");
        $("span.question__no__answer").toggleClass("question__no__answer question__has__answer");

        $("span#" + eid + ".correct__button").html("Correct!");
      } else {
        $("span.question__has__answer").html("No answer");
        $("span.question__has__answer").toggleClass("question__has__answer question__no__answer");

        $("span#" + eid + ".correct__button").html("Press here to mark as true");
      }
    }
  }
}

$("span.correct__button").click(function(){
  mark("/mark_as_true/", $(this).attr('id'));
});
