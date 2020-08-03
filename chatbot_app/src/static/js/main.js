let topics = document.getElementsByClassName('btn-topic');

for (let topic of topics) {
    topic.addEventListener('click', function(e){
        class_items = e.target.className.split(' ');
        questions = document.getElementsByClassName("topic_questions " + class_items[3]);

        for (let top of document.getElementsByClassName('topic_questions')) {
            top.style.display = "none";
        }

        questions[0].style.display = "block";
    })
}

let responses = document.getElementsByClassName('topic_responses');

for (let resp of responses) {
    resp.addEventListener('click', function(e){
        console.log('test')
        e.target.style.display = "block";
    })
}