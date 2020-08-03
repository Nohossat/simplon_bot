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

        if (response.style.display == "block") {
            response.style.display = "none";
        } else {
            response.style.display = "block";
        }

        for (let element of document.getElementsByClassName('response_faq')) {
            if (response != element) {
                element.style.display = "none";
            }
        }

    })
}

// add click listener for the voir plus btn
let see_more_btns = document.getElementsByClassName('see-more-btn');

for (let see_more_btn of see_more_btns) {
    see_more_btn.addEventListener('click', function(e) {
        previous_sibling = e.target.previousElementSibling;
        next_sibling = e.target.nextElementSibling;
        previous_sibling.style.display = "none";
        next_sibling.style.display = "inline";
        e.target.style.display = "none";
    })
}

// scroll to the last bloc_question if exists

bloc_questions = document.getElementsByClassName('bloc_question')

console.log(bloc_questions.length)
if (bloc_questions.length > 0) {
    window.scrollTo(0,bloc_questions[bloc_questions.length - 1].getBoundingClientRect().top);
}