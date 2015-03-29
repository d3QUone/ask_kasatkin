//// QUESTIONS ///// {% url 'core:like_question' %}

$("span.question_like").click(function(){
  var pid = $(this).attr('id');
  $.post("/like_post/", 
    {
      pid: pid, 
      like: 1
    }, 
    update_rating
  );
  function update_rating(result){
    if (result != "None") {
      $("div#" + pid).html("Rating: " + result);
    }
  }
});

$("span.question_dislike").click(function(){
  var pid = $(this).attr('id');
  $.post("/like_post/", 
    {
      pid: pid, 
      like: -1
    }, 
    update_rating
  );
  function update_rating(result){
    if (result != "None") {
      $("div#" + pid).html("Rating: " + result);
    }
  }
});


///// ANSWERS ////// {% url 'core:like_answer' %}

$("span.ans_like").click(function(){
  var aid = $(this).attr('id');
  $.post("/like_answ/", 
    {
      aid: aid, 
      like: 1
    }, 
    update_rating
  );
  function update_rating(result){
    if (result != "None") {
      $("div#" + aid).html("Rating: " + result);
    }
  }
});

$("span.ans_dislike").click(function(){
  var aid = $(this).attr('id');
  $.post("/like_answ/", 
    {
      aid: aid, 
      like: -1
    }, 
    update_rating
  );
  function update_rating(result){
    if (result != "None") {
      $("div#" + aid).html("Rating: " + result);
    }
  }
});