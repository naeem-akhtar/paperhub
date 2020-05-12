$("#id_username").change(function () {
	var username = $(this);
  console.log(username.val());

  if($('#username-taken')) {
  	$('#username-taken').remove();
  }

	$.ajax({
		url : '/ajax/validate_username/',
		data : {
			'username' : username.val()
		},
		dataType : 'json',
		success: function(data) {
			if(data.is_taken) {
				message = '<p id="username-taken"><strong style="color:red">' + data.error_message + '</strong></p>';
				username.after(message);
			}
		}
	});
});