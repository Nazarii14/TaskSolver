$(document).on('submit', '#number-form', async function(e) {
    e.preventDefault();
    var number = $('#number').val();
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    const errorMessage = document.getElementById("error-message");
    const taskNumberElement = document.getElementById('task-number');

    try {
        var data = await $.ajax({
            type: 'POST',
            url: '/task/add/',
            headers: {
              'X-CSRFToken': csrfToken,
              'Content-Type': 'application/json',
            },
            data: JSON.stringify({
              'number': number
            }),
            success: function(response) {
              if (response.status === "error") {
                errorMessage.innerHTML = response.message;
              } else {
                  errorMessage.innerHTML = "";
              }
              taskNumberElement.innerHTML = `Your tasks: (${response.count})\tYou can add ${response.number_of_tasks_left} more tasks.`;
            },
            error: function(xhr, status, error) {
              if (xhr.status === 400) {
                var response = JSON.parse(xhr.responseText);
                errorMessage.innerHTML = response.message;
              } else {
                  console.log('Error:', error);
              }
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
  });
