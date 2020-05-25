function tag_follow_toggle(url, operation) {
	$.ajax({
		url : url,
		data : {
			operation :  operation,
		},
		dataType : 'json',
		success: function(data) {
			let btn = $('#follow-toggle-button');
			// console.log(data);
			if(data.status == 'followed') {
				btn.html('Following');
			}
			else if(data.status == 'unfollowed') {
				btn.html('Follow');
			}
		}
	});
}