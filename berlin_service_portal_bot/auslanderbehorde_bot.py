import time
import bot

from bot import Bot


class AuslanderbehordeBot(Bot):
  def __init__(self):
    super().__init__("Ausländerbehörde Bot")

    # Pre-setup applicant information for service selection page
    self.config.get_int(
        "auslanderbehorde_bot",
        "number_of_applicants",
        "Number of applicants who need a residence title? (inluding foreign spouse and children)"
    )

    self.config.get_boolean(
        "auslanderbehorde_bot",
        "family_member_living",
        "Do the applicant live in Berlin with a family member? (e.g. wife, husband or child)"
    )

    # Pre-setup applicant information for details page
    self.config.get(
        "auslanderbehorde_bot",
        "first_name",
        "Applicant's first name?"
    )

    self.config.get(
        "auslanderbehorde_bot",
        "last_name",
        "Applicant's last name?"
    )

    self.config.get(
        "auslanderbehorde_bot",
        "date_of_birth",
        "Applicant's date of birth? (dd.mm.yyyy)"
    )

    self.config.get(
        "auslanderbehorde_bot",
        "email",
        "Applicant's e-mail?"
    )

    if self.config.get_boolean(
        "auslanderbehorde_bot",
        "has_residence_title",
        "Do you currently have a residence title? (e.g. a visa or a residence permit)"
    ):
      self.config.get(
          "auslanderbehorde_bot",
          "residence_title",
          "Applicant's number of residence title? (e.g. residence permit or EU Blue Card)"
      )

  def load_appointment_page(self):
    self.web_driver.page(
        "https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng?lang=en"
    )

    print("Loading appointment page")

  def check_terms_and_conditions(self):
    self.web_driver.click(
        "//input[@name='gelesen']"
    )

    print("Accepting terms and conditions")

  def click_next(self):
    self.web_driver.click(
        "//button[@name='applicationForm:managedForm:proceed']"
    )

    print("Clicking next")

  def select_citizenship(self):
    if self.config.has("auslanderbehorde_bot", "citizenship"):
      selection = self.config.get("auslanderbehorde_bot", "citizenship")
    else:
      options = self.web_driver.get_select_options_contents(
          "//select[@name='sel_staat']"
      )

      index = 0
      for option in options:
        print(f"({index}) {option}")
        index += 1

      selection = options[self.config.ask_int(
          "What's the applicant's citizenship? (index)"
      )]

      self.config.write("auslanderbehorde_bot", "citizenship", selection)

    self.web_driver.select_by_text("//select[@name='sel_staat']", selection)

    print(
        f"Selecting \"{selection}\" as the applicant's citizenship"
    )

  def select_number_of_applicants(self):
    number_of_applicants = self.config.get_int(
        "auslanderbehorde_bot",
        "number_of_applicants"
    )

    options = self.web_driver.get_select_options_contents(
        "//select[@name='personenAnzahl_normal']"
    )
    selection = options[number_of_applicants]

    self.web_driver.select_by_text(
        "//select[@name='personenAnzahl_normal']",
        selection
    )

    print(
        f"Selecting \"{selection}\" as the number of applicants"
    )

  def select_family_member_living(self):
    if self.config.get_boolean("auslanderbehorde_bot", "family_member_living"):
      selection = "yes"
    else:
      selection = "no"

    self.web_driver.select_by_text(
        "//select[@name='lebnBrMitFmly']",
        selection
    )

    print(
        f"Selecting \"{selection}\" as for applicant's living in Berlin with a family member"
    )

  def select_citizenship_of_family_member(self):
    if self.config.get_boolean("auslanderbehorde_bot", "family_member_living"):
      if self.config.has("auslanderbehorde_bot", "citizenship_of_family_member"):
        selection = self.config.get(
            "auslanderbehorde_bot", "citizenship_of_family_member")
      else:
        options = self.web_driver.get_select_options_contents(
            "//select[@name='fmlyMemNationality']"
        )

        index = 0
        for option in options:
          print(f"({index}) {option}")
          index += 1

        selection = options[self.config.ask_int(
            "What's the applicant's family member citizenship? (index)"
        )]

        self.config.write(
            "auslanderbehorde_bot",
            "citizenship_of_family_member",
            selection
        )

      self.web_driver.select_by_text(
          "//select[@name='fmlyMemNationality']", selection
      )

      print(
          f"Selecting \"{selection}\" as for applicant's family member citizenship"
      )
    else:
      print(
          f"Skipping selection for applicant's family member citizenship"
      )

  def select_service_level_1(self):
    if self.config.has("auslanderbehorde_bot", "service_level_1"):
      selection = self.config.get("auslanderbehorde_bot", "service_level_1")
    else:
      options = self.web_driver.get_contents(
          "//input[@name='level1']/following-sibling::label/p"
      )

      index = 0
      for option in options:
        print(f"({index}) {option}")
        index += 1

      selection = options[self.config.ask_int(
          "Select the service level 1 (index)"
      )]

      self.config.write("auslanderbehorde_bot", "service_level_1", selection)

    self.web_driver.click(
        f"//input[@name='level1']/following-sibling::label/p[contains(text(), '{selection}')]"
    )
    print(
        f"Clicking on \"{selection}\" as for the service selection level 1"
    )

  def select_service_level_2(self):
    if self.config.has("auslanderbehorde_bot", "service_level_2"):
      selection = self.config.get("auslanderbehorde_bot", "service_level_2")
    else:
      options = self.web_driver.get_contents(
          "//input[@name='level2']/following-sibling::label/p"
      )

      index = 0
      for option in options:
        print(f"({index}) {option}")
        index += 1

      selection = options[self.config.ask_int(
          "Select the service level 2 (index)"
      )]

      self.config.write("auslanderbehorde_bot", "service_level_2", selection)

    self.web_driver.click(
        f"//input[@name='level2']/following-sibling::label/p[contains(text(), '{selection}')]"
    )
    print(
        f"Clicking on \"{selection}\" as for the service selection level 2"
    )

  def select_service_level_3(self):
    service_level_2 = self.config.get(
        "auslanderbehorde_bot", "service_level_2")

    if self.config.has("auslanderbehorde_bot", "service_level_3"):
      selection = self.config.get("auslanderbehorde_bot", "service_level_3")
    else:
      options = self.web_driver.get_contents(
          f"//input[@name='level2']/following-sibling::label/p[contains(text(), '{service_level_2}')]/following::div[@class='level2-content'][1]//div[@class='level3']/label"
      )

      index = 0
      for option in options:
        print(f"({index}) {option}")
        index += 1

      selection = options[self.config.ask_int(
          "Select the service level 3 (index)"
      )]

      self.config.write("auslanderbehorde_bot", "service_level_3", selection)

    self.web_driver.click(
        f"//input[@name='level2']/following-sibling::label/p[contains(text(), '{service_level_2}')]/following::div[@class='level2-content'][1]//div[@class='level3']/label[contains(text(), '{selection}')]"
    )
    print(
        f"Clicking on \"{selection}\" as for the service selection level 3"
    )

  def wait_for_information_about_selected_service(self):
    self.web_driver.wait_visibility("//fieldset[@name='DIENSTLEISTUNGNAME']")
    print("Waiting for the selected service to be loaded")

  def has_appointment_selection(self):
    return self.web_driver.has_element("//legend[text()='Appointment selection']")

  def has_error_message(self):
    return self.web_driver.has_element("//*[@class='errorMessage']")

  def get_error_message(self): 
    return self.web_driver.get_content("//*[@class='errorMessage']")

  def check_available_appointments(self):
    count = 0
    not_found_count = 0

    while 1:
      time.sleep(self.refresh_interval)

      if self.has_appointment_selection():
        self._notify("Appointments available")
        break
      elif self.has_error_message():
        print(f"({count}) Error message: \"{self.get_error_message()}\"")
        count += 1
        not_found_count = 0
        time.sleep(3)
        self.click_next()
      else:
        not_found_count += 1
        if not_found_count > 3:
          raise Exception("Timeout for expected elements to be found")

  def search_calendar(self):
    self.month = self.__month_to_text(
        self.config.get_int("auslanderbehorde_bot", "month"))

    maximum_next_clicks = 3
    while maximum_next_clicks:
      self.web_driver.wait_visibility(
          "//div[contains(@class,'ui-datepicker-header')]//*[@class='ui-datepicker-month']")

      if self.web_driver.has_element(f"//div[contains(@class,'ui-datepicker-header')]//*[@class='ui-datepicker-month' and contains(text(), '{self.month}')]"):
        year = self.web_driver.get_content(
            "//div[contains(@class,'ui-datepicker-header')]//*[@class='ui-datepicker-year']")
        print(f"Calendar for \"{self.month} {year}\" found")
        return
      else:
        print(f"Searching for \"{self.month}\" calendar, clicking next")
        self.web_driver.click("//a[contains(@class, 'ui-datepicker-next')]")
        maximum_next_clicks -= 1
        time.sleep(5)
        continue

    raise Exception(f"Calendar \"{self.month}\" not found")

  def __month_to_text(self, month):
    return ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
            ][month - 1]

  def click_first_available_calendar_day_of_month(self):
    xpath = f"//div[div[*[@class='ui-datepicker-month'] = '{self.month}']]/following-sibling::table//a[contains(@class, 'ui-state-active')]"

    if self.web_driver.has_element(xpath):
      self.web_driver.click(xpath)
      day = self.web_driver.get_content(xpath)

      print(
          f"Clicking on the first available calendar date for \"{self.month}\", day \"{day}\""
      )
    else:
      raise Exception(f"No available date for \"{self.month}\" was found")

  def click_first_available_calendar_day(self):
    print("Enter function: click day")
    self.web_driver.click("//a[contains(@class, 'ui-state-active')]")

    day = self.web_driver.get_content(
        "//a[contains(@class, 'ui-state-active')]"
    )

    month = self.web_driver.get_content(
        "//a[contains(@class, 'ui-state-active')]/preceding::div[contains(@class, 'ui-datepicker-header')]//span[@class='ui-datepicker-month']"
    )

    print(
        f"Clicking on the first available calendar date, {day} of {month}"
    )

  def select_first_available_time(self):
    options = self.web_driver.get_select_options_contents(
        "//select[@name='dd_zeiten']")

    index = 0
    for option in options:
      print(f"({index}) {option}")
      index += 1

    self.web_driver.select_by_index("//select[@name='dd_zeiten']", len(options)-1)
    print(f"Clicking on the first available time, \"{options[len(options)-1]}\"")

  def fill_first_name(self):
    first_name = self.config.get("auslanderbehorde_bot", "first_name")
    self.web_driver.fill("//input[@name='antragsteller_vname']", first_name)
    print(f"Filling applicant's first name \"{first_name}\"")

  def fill_last_name(self):
    last_name = self.config.get("auslanderbehorde_bot", "last_name")
    self.web_driver.fill("//input[@name='antragsteller_nname']", last_name)
    print(f"Filling applicant's last name \"{last_name}\"")

  def fill_date_of_birth(self):
    date_of_birth = self.config.get("auslanderbehorde_bot", "date_of_birth")
    self.web_driver.fill(
        "//input[@name='antragsteller_gebDatum']", date_of_birth)
    print(f"Filling applicant's date of birth \"{date_of_birth}\"")

  def fill_email(self):
    email = self.config.get("auslanderbehorde_bot", "email")
    self.web_driver.fill("//input[@name='antragsteller_email']", email)
    print(f"Filling applicant's email \"{email}\"")

  def select_has_residence_title(self):
    if self.config.get_boolean("auslanderbehorde_bot", "has_residence_title"):
      selection = "yes"
    else:
      selection = "no"

    self.web_driver.select_by_text(
        "//select[@name='sel_aufenthaltserlaubnis']",
        selection
    )

    print(
        f"Selecting \"{selection}\" as for if applicant's has residence title"
    )

  def fill_residence_title(self):
    if self.config.get_boolean("auslanderbehorde_bot", "has_residence_title"):
      residence_title = self.config.get(
          "auslanderbehorde_bot", "residence_title")

      self.web_driver.fill(
          "//input[@name='antragsteller_nrAufenthaltserlaubnis']",
          residence_title
      )
      print(
          f"Filling \"{residence_title}\" as for applicant's residence title"
      )
    else:
      print("Skipping applicant's residence title")

  def wait_summary(self):
    print("Waiting for the appointment summary")
    self.web_driver.wait_visibility("//button[@id='summaryForm:proceed']")
    self._notify("Appointment summary")

  def click_book_appointment(self):
    # Appointment booking - Please check your data

    # After booking the appointment, you will receive an appointment confirmation with a summary of your data and all necessary information. Please make sure to bring complete documents. Otherwise we may not able to serve you.
    self.web_driver.click("//button[@id='summaryForm:proceed']")
    print("Clicking on \"Book appointment\"")

  def click_appointment_confirmation_as_pdf_file(self):
    # Thank you for booking your appointment

    # In your e-mail inbox you will find the appointment confirmation with all information about the required documents and fees.
    # However, we recommend that you save the appointment confirmation immediately and, if possible, print it out:

    xpath = "//div[@id='EN3']/a[@class='btnApplicationPdf']"

    # Appointment confirmation as PDF file
    print(
        f"Appointment confirmation PDF file link: {self.web_driver.get_attribute_content(xpath)}")
    self.web_driver.click(xpath)
    print("Clicking on \"Appointment confirmation as PDF file\"")


def main():
  def __load():
    auslanderbehorde_bot = AuslanderbehordeBot()

    # Information
    auslanderbehorde_bot.load_appointment_page()
    auslanderbehorde_bot.check_terms_and_conditions()
    auslanderbehorde_bot.click_next()

    # Service selection
    auslanderbehorde_bot.select_citizenship()
    auslanderbehorde_bot.select_number_of_applicants()
    auslanderbehorde_bot.select_family_member_living()
    auslanderbehorde_bot.select_citizenship_of_family_member()
    auslanderbehorde_bot.select_service_level_1()
    auslanderbehorde_bot.select_service_level_2()
    auslanderbehorde_bot.select_service_level_3()
    auslanderbehorde_bot.wait_for_information_about_selected_service()
    auslanderbehorde_bot.click_next()
    auslanderbehorde_bot.check_available_appointments()

    # Date selection
    # auslanderbehorde_bot.search_calendar()
    # auslanderbehorde_bot.click_first_available_calendar_day_of_month()
    auslanderbehorde_bot.click_first_available_calendar_day()
    auslanderbehorde_bot.select_first_available_time()
    auslanderbehorde_bot.click_next()

    # Details
    auslanderbehorde_bot.fill_first_name()
    auslanderbehorde_bot.fill_last_name()
    auslanderbehorde_bot.fill_date_of_birth()
    auslanderbehorde_bot.fill_email()
    auslanderbehorde_bot.select_has_residence_title()
    auslanderbehorde_bot.fill_residence_title()
    auslanderbehorde_bot.click_next()

    # Summary
    auslanderbehorde_bot.wait_summary()
    auslanderbehorde_bot.click_book_appointment()

    # Reservation
    auslanderbehorde_bot.click_appointment_confirmation_as_pdf_file()

  bot.loop(__load)


if __name__ == '__main__':
  main()
