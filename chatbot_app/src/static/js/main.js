// add click listener on topic buttons
let topics = document.getElementsByClassName('btn-topic');

for (let topic of topics) {
    topic.addEventListener('click', function(e){
        class_items = e.target.className.split(' ');
        question = document.querySelector(".topic_questions." + class_items[3]);

        for (let top of document.getElementsByClassName('topic_questions')) {
            top.style.display = "none";
        }

        question.style.display = "block";
    })
}

// add click listener for the questions per topic
let questions = document.getElementsByClassName('question_faq');

for (let question of questions) {
    question.addEventListener('click', function(e){
        class_items = e.target.className.split(' ');
        response = document.querySelector(".response_faq." + class_items[1] + "." + class_items[2]);

        for (let element of document.getElementsByClassName('response_faq')) {
            element.style.display = "none";
        }

        response.style.display = "block";
    })
}