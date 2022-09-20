from patients import OurPatient, InputError
from pcrTest import PcrTest
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App


class MainWindow(Screen, FloatLayout):
    pass


class Reports(Screen):
    def dates_report(self):
        try:
            self.ids["'word_label'"].text = str(
                PcrTest.rep_by_dates(self.ids["'start_date'"].text, self.ids["'end_date'"].text))
            self.ids["'word_label'"].color = [0, 0, 0]

        except InputError as m:
            self.ids["'word_label'"].text = str(m)
            self.ids["'word_label'"].color = [1., 0, 0]

    def high_risk(self):
        try:
            self.ids["'word_label'"].text = str(PcrTest.high_risk_people_rep())
            self.ids["'word_label'"].color = [0, 0, 0]
        except InputError as m:
            self.ids["'word_label'"].text = str(m)
            self.ids["'word_label'"].color = [1., 0, 0]

    def positive_report(self):
        try:
            if self.ids["'name'"].text != '':
                self.ids["'word_label'"].text = str(PcrTest.positive_rep(self.ids["'name'"].text))
                self.ids["'word_label'"].color = [0, 0, 0]
            else:
                raise InputError("Please write name of patient")
        except InputError as m:
            self.ids["'word_label'"].text = str(m)
            self.ids["'word_label'"].color = [1., 0, 0]


class UpdatePcr(Screen):
    def update_pcr(self):
        try:
            PcrTest.update_test(self.ids["'in_pcr_id'"].text, self.ids["'result'"].text)
            self.ids["'message_user'"].text = 'The update was successful'
            self.ids["'message_user'"].color = [0.2, 1., 1.]
        except InputError as m:
            self.ids["'message_user'"].text = str(m)
            self.ids["'message_user'"].color = [1., 0, 0]


class DeletePcr(Screen):
    def del_pcr(self):
        try:
            PcrTest.delete_pcr(self.ids["'in_pcr_id'"].text)
            self.ids["'message_user'"].text = 'The delete was successful'
            self.ids["'message_user'"].color = [0.2, 1., 1.]
        except InputError as m:
            self.ids["'message_user'"].text = str(m)
            self.ids["'message_user'"].color = [1., 0, 0]

    def del_pcr_file(self):
        try:
            PcrTest.delete_pcr_test_file(self.ids["'in_file'"].text)
            self.ids["'message_user'"].text = 'The delete was successful'
            self.ids["'message_user'"].color = [0.2, 1., 1.]
        except IOError as m:
            self.ids["'message_user'"].text = str(m)
            self.ids["'message_user'"].color = [1., 0, 0]


class AddPcrTest(Screen):
    def add_pcr(self):
        try:
            pt = PcrTest(self.ids["'patient_id'"].text,self.ids["'pcr_id'"].text, self.ids["'result'"].text)
            PcrTest.add_pcr(self=pt)
            self.ids["'message_user'"].text = 'The addition was successful'
            self.ids["'message_user'"].color = [0.2, 1., 1.]
        except InputError as m:
            self.ids["'message_user'"].text = str(m)
            self.ids["'message_user'"].color = [1., 0, 0]


class AddPatientsByFile(Screen):
    def add_p_file(self):
        try:
            OurPatient.add_patient_from_file(self.ids["'file'"].text)
            self.ids["'message_user'"].text = 'The addition was successful'
            self.ids["'message_user'"].color = [0.2, 1., 1.]
        except IOError as m:
            self.ids["'message_user'"].text = str(m)
            self.ids["'message_user'"].color = [1., 0, 0]


class AddPatient(Screen):
    def add_p(self):
        try:
            pt = OurPatient(self.ids["'id_num'"].text, self.ids["'name'"].text, self.ids["'bitrhYear'"].text,
                            self.ids["'phone'"].text, self.ids["'email'"].text)
            OurPatient.add_patient(self=pt)
            self.ids["'message_user'"].text = 'The addition was successful'
            self.ids["'message_user'"].color = [0.2, 1., 1.]

        except InputError as m:
            self.ids["'message_user'"].text = str(m)
            self.ids["'message_user'"].color = [1., 0, 0]


class WindowManager(ScreenManager):
    pass


# the Base Class of our Kivy App
class MyApp(App):
    icon = 'images/logo2.png'
    title = 'Covid-19'

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        screen = Screen(name='MainWindow')
        sm.switch_to(screen, direction='right')


if __name__ == '__main__':
    app = MyApp()
    app.run()
    app.root_window.close()
