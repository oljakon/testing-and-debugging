Feature: Vacancy Catalog

  Scenario: User creates an application to a job
    Given registered user
    And job vacancy
    When user creates an application to a job
    Then returns code 201
