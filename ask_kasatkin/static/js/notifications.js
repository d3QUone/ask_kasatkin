var channel_id = $('div#channel_id').html();  // loads user_id from page

function comet (id, onmessage) {
	$.get('http://vksmm.info/listen', { cid: id }
	).done(function(data) {
			onmessage(data);
			comet(id, onmessage);
		}
	).fail(function(data) {
			comet(id, onmessage);
		}
	);
}

comet(channel_id, function(data) {
	console.log(data);
});
