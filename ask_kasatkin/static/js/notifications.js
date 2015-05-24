var $message = $("#message");
var channel_id = $("div#channel_id").html();  // opened question id
var ws = new WebSocket("ws://localhost:8888/ws/" + channel_id);

ws.onopen = function(){
  $message.attr("class", "label label-success");
  $message.text("open");
};
ws.onmessage = function(ev){
  $message.attr("class", 'label label-info');
  $message.hide();
  $message.fadeIn("slow");
  $message.text('recieved message');

  var json = JSON.parse(ev.data);
  var new_ans = '<a name="answer_' + json.id + '"></a><div class="row question__block fresh"><div class="col-xs-2 question__left"><img class="img-rounded question__avatar" src="/uploads/' + json.avatar + '"><div id="' + json.id + '" class="rating__info answer_rating">Rating: 0</div><div class="rating__like__block"><span id="' + json.id + '" class="like__button ans_like">+</span><span id="' + json.id + '" class="like__button ans_dislike">-</span></div></div><div class="col-xs-10 question__right"><p>' + json.text + '</p><div class="question__tags"><strong>Author:</strong>' + json.nickname + '</div></div></div>';
  $('div#fresh_answers').append(new_ans);
};
ws.onclose = function(ev){
  $message.attr("class", 'label label-important');
  $message.text('closed');
};
ws.onerror = function(ev){
  $message.attr("class", 'label label-warning');
  $message.text('error occurred');
};
