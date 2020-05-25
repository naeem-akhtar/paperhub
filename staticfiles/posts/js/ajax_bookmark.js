toggleBookmark = function(url, post_id) {
	$.ajax({
		url : url,
		data : {
			'pk' : post_id
		},
		dataType : 'json',
		success: function(data) {
			// console.log(data);
			bookmark_icon = $('#bookmark-' + data.pk).find('i');
			if(data.bookmarked == 'true') {
				bookmark_icon.addClass('fa-bookmark').removeClass('fa-bookmark-o');
			}
			else {
				bookmark_icon.addClass('fa-bookmark-o').removeClass('fa-bookmark');
			}
		},
		fail: function(data){
    	console.log('Request failed :(');
    }
	});
}

$(".bookmark").click(function () {
	var post_id = $(this).attr('id').split('-')[1];
	toggleBookmark('/ajax/bookmark/', post_id);
});


