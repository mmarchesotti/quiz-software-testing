import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    assert len(question.choices) == 3

def test_remove_choice_by_id():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.remove_choice_by_id(c1.id)
    assert len(question.choices) == 1
    assert question.choices[0].id == c2.id

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_correct_choice():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=False)
    selected = question.select_choices([c1.id, c2.id])
    assert selected == [c1.id]

def test_select_with_invalid_choice_id():
    question = Question(title='q1')
    question.add_choice('a', is_correct=True)
    result = question.select_choices([999])
    assert result == []

def test_select_more_than_max_selections():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    with pytest.raises(Exception):
        question.select_choices([c1.id, c2.id])

def test_set_correct_choices_marks_them_correct():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c2.id])
    assert not c1.is_correct
    assert c2.is_correct

def test_choice_text_length_validation():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_generate_choice_ids_sequentially():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3

def test_invalid_choice_id_raises_error():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)
