from patron import Patron


class Teacher(Patron):
    def __init__(self, name, teacher_id):
        super().__init__(name, teacher_id)
        self.students = {}  # dict to get the student name and his books , of specific teacher.

    """Function that return the students id numbers of specific teacher"""

    def get_the_students_of_a_teacher(self):
        print(f"Those are the students of the teacher number {self.patron_id}:\n {self.students.keys()}")
        return self.students.keys()
