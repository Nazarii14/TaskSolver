const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
const taskNumberElement = document.getElementById('task-number');
const deleteButtons = document.querySelectorAll('.delete-task');
const taskListContainer = document.getElementById('task-list-container');
const errorMessage = document.getElementById("error-message"); 

function deleteTask() {
    const taskId = $(this).data('task-id');
    console.log('Delete button clicked for task ID:', taskId);
    
    $.ajax({
        type: 'DELETE',
        url: `/task/delete/${taskId}`,
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        error: function(error) {
            console.error('Error:', error);
        },
    });
    checkTaskStatus();
}

$(document).on('click', '.delete-task', deleteTask);

function checkTaskStatus() {
    fetch('/task/check_task_status/', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const taskStatus = data.task_status;
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';
        tasksCount = data.count
        tasksLeft = data.number_of_tasks_left
        
        if (data.message == undefined) {
            data.message = "";
        }
        if (tasksCount == undefined) {
            tasksCount = 0;
        }

        if (tasksLeft == 0) {
            taskNumberElement.innerHTML = `Your tasks: (${tasksCount})\tYou can't add tasks anymore.`;
        }
        else {
            errorMessage.innerHTML = data.message
            taskNumberElement.innerHTML = `Your tasks: (${tasksCount})\tYou can add ${tasksLeft} more tasks.`;
        }

        if (taskStatus.length == 0) {
            const noTaskItem = document.createElement('li');
            noTaskItem.textContent = 'No task found';
            taskList.appendChild(noTaskItem);
        }
        else {
            for (const taskId in taskStatus) {
                const taskInfo = taskStatus[taskId];
                const taskItem = document.createElement('li');
                const isRunningText = taskInfo.is_finished ? 'Finished' : 'Running';

                taskItem.className = 'tasks';
                taskItem.id = `task-${taskId}`;
                taskItem.innerHTML = `
                    Num: ${taskInfo.number}
                    (${isRunningText})
                    Result: ${taskInfo.result}
                    <progress class="task-progress" value="${taskInfo.completion_percentage}" max="100"></progress>
                    ${taskInfo.completion_percentage}%
                    <button class="delete-task" data-task-id="${taskId}">Delete</button>
                `;
                taskList.appendChild(taskItem);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

setInterval(checkTaskStatus, 100);

window.addEventListener('load', checkTaskStatus);
window.addEventListener('DOMContentLoaded', checkTaskStatus);
